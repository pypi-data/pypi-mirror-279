import rich
from inferless_cli.utils.helpers import (
    create_yaml,
    yaml,
)


def update_config_file(path, volume):
    with open(path, "r") as yaml_file:
        config = yaml.load(yaml_file)
        config["configuration"]["custom_volume_name"] = volume["name"]
        config["configuration"]["custom_volume_id"] = volume["id"]
        create_yaml(config, path)
        rich.print(f"[green]{path} file updated successfully[/green]")
