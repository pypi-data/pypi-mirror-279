"""
Configuration item definitions.
"""
import struct
from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional
from .types import Setup
from .error import NimuException
from functools import reduce
from operator import mul

PACKMETHOD = {
    'enum1': 'b',
    'enum2': 'h',
    'enum4': 'i',
    'u32': 'I',
    'u16': 'H',
    'u8': 'B',
    'real': 'f'
}


def listify(value):
    if isinstance(value, list):
        return value
    return [value]


# flatten a list of lists to a single list, lst might be a scalar, a list or a list of lists
def flatten(lst):
    if isinstance(lst, list):
        return [a for i in lst for a in flatten(i)]
    return [lst]


def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    if len(shape) == 0:
        return lst[0]
    n = reduce(mul, shape[1:])
    return [reshape(lst[i*n:(i+1)*n], shape[1:]) for i in range(len(lst)//n)]


# a function for validating that input value is of expected shape and all values are numeric.
# if shape is an empty list, then the value is expected to be a scalar.
def validate_shape(value, shape, validtypes):
    if len(shape) == 0:
        if not isinstance(value, validtypes):
            raise NimuException(f"Expected scalar value, got {value}.")
    else:
        if not isinstance(value, list):
            raise NimuException(f"Expected list, got {value}.")
        if len(value) != shape[0]:
            raise NimuException(f"Expected list of length {shape[0]}, got {value}.")
        for v in value:
            validate_shape(v, shape[1:], validtypes)


# change the datatype recursively to a different type
def change_datatype(value, shape, newtype):
    if len(shape) == 0:
        return newtype(value)
    return [change_datatype(v, shape[1:], newtype) for v in value]


@dataclass
class DataMapping:
    name: str
    type: str
    cname: str
    options: Dict[str, int] = field(default_factory=dict)

    def _hexstring2int(self, value):
        if isinstance(value, str) and value.startswith('0x'):
            return int(value, 16)
        return value

    def map2device(self, values: List[Any]) -> List[Any]:
        """
        Map values to the device values.
        """
        if self.options:
            values = [self._hexstring2int(self.options[v]) for v in values]
        return values

    def map2value(self, values: List[Any]) -> List[Any]:
        """
        Map values to the UI values.
        """
        if self.options:
            inv_options = {self._hexstring2int(v): k for k, v in self.options.items()}
            values = [inv_options[v] for v in values]
        return values


@dataclass
class ItemDescription:
    id: int
    group: List[str]
    name: str
    nameUI: str
    description: str
    public: bool = False


@dataclass
class ItemData:
    type: str
    constant: bool = False
    defaultValue: Any = None
    dimension: List[int] = field(default_factory=list)
    constraints: Any = None

    def __post_init__(self):
        validtypesmap = {'u32': (int), 'u16': (int), 'u8': (int), 'real': (int, float)}
        if self.type in validtypesmap:
            validate_shape(self.defaultValue, self.dimension, validtypesmap[self.type])

        convmap = {'u32': int, 'u16': int, 'u8': int, 'real': float}
        if self.type in convmap:
            self.defaultValue = change_datatype(self.defaultValue, self.dimension, convmap[self.type])

        if len(self.dimension) > 2:
            raise NimuException(f"Dimension must be a list of length 0, 1 or 2, got {self.dimension}.")
        if any(d <= 0 for d in self.dimension):
            raise NimuException(f"Dimension must be positive, got {self.dimension}.")


@dataclass
class Item:
    description: ItemDescription
    data: ItemData
    mapping: Optional[DataMapping] = None

    @property
    def id(self):
        return self.description.id

    @property
    def name(self):
        return '.'.join(self.description.group) + '.' + self.description.name

    @property
    def type(self):
        if self.mapping:
            if self.mapping.type != 'scalar':
                return self.mapping.type
        return self.data.type

    @property
    def elem_size(self):
        sizemap = {
            'u32': 4,
            'u16': 2,
            'u8': 1,
            'real': 4,
            'enum1': 1,
            'enum2': 2,
            'enum4': 4
        }
        if self.type in sizemap:
            return sizemap[self.type]
        raise NimuException(f"Cannot determine length in bytes for type '{self.type}' in {self} (Not implemented).")

    def __len__(self):
        """
        How many data bytes value takes.
        """
        nelems = reduce(lambda x1, x2: x1*x2, self.data.dimension, 1)
        return self.elem_size * nelems


def device2value(setup: Setup, item: Item, bytes: List[int]):
    """
    Convert device bytes to value.
    """
    if len(list(filter(lambda v: v is None, bytes))) > 0:
        setup["logger"].warning(f"Incomplete value received for {item.name}.")
        return None

    t = item.type

    if t in PACKMETHOD:
        n = len(bytes) // item.elem_size
        raw_flat = list(struct.unpack(f'<{n}{PACKMETHOD[t]}', bytearray(bytes)))
        converted_flat = item.mapping.map2value(raw_flat)
        converted = reshape(converted_flat, item.data.dimension)
        return converted

    raise NimuException(f"Cannot determine value for type '{t}' in {item} (Not implemented).")


def value2device(setup: Setup, item: Item, value: Any):
    """
    Convert a configuration value to the list of device bytes.
    """
    t = item.type
    value = item.mapping.map2device(listify(value))

    if t in PACKMETHOD:
        flattenval = flatten(value)
        n = len(flattenval)
        packed = struct.pack(f'<{n}{PACKMETHOD[t]}', *flattenval)
        return packed

    raise NimuException(f"Cannot convert value {value} of type '{t}' in {item} (Not implemented).")


def to_values(setup: Setup, items: Dict[int, Item], resp: Dict[int, List[int]]) -> Dict[int, Any]:
    """
    Parse all values from device byte arrays and construct mapping from item IDs to values.
    """
    ret = dict()
    for item_id in resp:
        if resp[item_id] is None:
            continue
        value = device2value(setup, items[item_id], resp[item_id])
        if value is not None:
            ret[item_id] = value
    return ret


def from_values(setup: Setup, items: Dict[int, Item], config: Dict[str, Any]) -> Dict[int, List[int]]:
    """
    Convert item values to array of bytes.
    """
    ret = dict()
    for item_id in config:
        value = value2device(setup, items[int(item_id)], config[item_id])
        if value is not None:
            ret[item_id] = value
    return ret
