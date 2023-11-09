import re
from typing import Dict, Any
import yaml
import ruamel.yaml  # works only for 'pip install ruamel.yaml<0.18.0'
from ruamel.yaml.scalarstring import LiteralScalarString


def print_dict(dictionary: dict):
    for key, val in dictionary.items():
        print(f"{key}: {val}")


def load_config(path: str = "./config/config.yaml") -> Dict[str, Dict[str, Any]]:
    yaml_file = open(path, "r")
    try:
        parsed_yaml = ruamel.yaml.safe_load(yaml_file)
    except Exception as e:
        print(f"Cannot parse file {path}.\n{e}")
        return dict()
    finally:
        yaml_file.close()
    return parsed_yaml


def write_config(path: str = "./config/config.yaml", config: Dict[str, Dict[str, Any]] = None) -> None:
    yaml_file = open(path, "w")
    yaml_string = ""
    for key, val in config.items():
        yaml_string += f"{key}:\n"
        for key_l2, val_2 in val.items():
            yaml_string += f"  {key_l2}: {val_2}\n"
        yaml_string += "\n"
    try:
        yaml_string = LiteralScalarString(yaml_string)
        yaml_output = ruamel.yaml.dump(yaml_string, Dumper=ruamel.yaml.RoundTripDumper, line_break=None)
        yaml_output = re.sub("\|-\n", "", yaml_output, count=1)
        yaml_output = re.sub("\|\+\n", "", yaml_output, count=1)
        yaml_output = re.sub("\|\n", "", yaml_output, count=1)
        yaml_output = re.sub("\.\.\.", "", yaml_output, count=1)
        yaml_string = re.sub("\n{3,}", "\n\n", yaml_string)
        yaml_file.write(yaml_output)
    except yaml.YAMLError as e:
        print(f"Error converting string to YAML: {e}")
    finally:
        yaml_file.close()
