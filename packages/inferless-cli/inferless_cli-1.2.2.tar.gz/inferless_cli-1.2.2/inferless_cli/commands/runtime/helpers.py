import rich
from inferless_cli.utils.helpers import (
    create_yaml,
    yaml,
)


def update_config_file(path, runtime):
    with open(path, "r") as yaml_file:
        config = yaml.load(yaml_file)
        config["configuration"]["custom_runtime_id"] = runtime["id"]
        config["configuration"]["custom_runtime_version"] = str(
            runtime["current_version"]
        )
        create_yaml(config, path)
        rich.print(f"[green]{path} file updated successfully[/green]")
