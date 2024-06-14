"""
API for fetching static instructions how to build configuration.
"""
from typing import Dict
from pathlib import Path
from ..files.json import read_json
from ..types import Setup, ConfigJson


def index(setup: Setup) -> Dict[str, ConfigJson]:
    """
    Collect and return complete static configuration information.
    """

    def remove_non_public(json: Path) -> ConfigJson:
        """
        Helper to drop non-public items unless setup says otherwise.
        """
        if setup["non_public"]:
            return json
        items = list(
            filter(lambda x: x["description"]["public"], json["items"]))
        return {
            "datamappings": json["datamappings"],
            "items": items,
            "view": json["view"] if "view" in json else {"groups": []}
        }

    configs = {}
    for path in setup["json_files"]:
        data = remove_non_public(read_json(path))
        configs[path.name] = data
    return configs
