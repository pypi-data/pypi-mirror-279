import dateutil
from prompt_toolkit.validation import Validator
import typer
from typing_extensions import Annotated, Optional
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console
from inferless_cli.commands.deploy.deploy_prompt import deploy_prompt
from inferless_cli.utils.constants import DEFAULT_YAML_FILE_NAME, SPINNER_DESCRIPTION
from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import (
    check_import_source,
    decrypt_tokens,
    get_models,
    get_by_keys,
    is_inferless_yaml_present,
    key_bindings,
    log_exception,
    read_yaml,
)

from inferless_cli.utils.services import (
    activate_model,
    deactivate_model,
    delete_model,
    get_workspace_models,
    rebuild_model,
    get_model_code,
    get_model_details,
)
from inferless_cli.utils.validators import validate_models


app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = SPINNER_DESCRIPTION
no_models = "[red]No models found in your workspace[/red]"
model_id_string = "Model ID"


@app.command(
    "rebuild",
    help="rebuild a model. (If you have a inferless.yaml file in your current directory, you can use the --local or -l flag to redeploy the model locally.)",
)
def rebuild(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
    local: bool = typer.Option(False, "--local", "-l", help="Local rebuild"),
):
    try:
        is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)
        is_local_modified = False
        if (
            is_yaml_present
            and not local
            and check_import_source(DEFAULT_YAML_FILE_NAME) == "LOCAL"
        ):
            config = read_yaml(DEFAULT_YAML_FILE_NAME)
            if "import_source" in config and config["import_source"] == "LOCAL":
                temp_model_id = config.get("model_import_id")
                if temp_model_id:
                    local = typer.confirm(
                        f"Found {DEFAULT_YAML_FILE_NAME} file. do you want to redeploy? "
                    )
                    if local:
                        is_local_modified = True
        if local:
            config_file_name = DEFAULT_YAML_FILE_NAME
            if not is_local_modified:
                config_file_name = prompt(
                    "Enter the name of your config file: ",
                    default=DEFAULT_YAML_FILE_NAME,
                )
            if check_import_source(config_file_name) == "LOCAL":
                deploy_prompt(True, config_file_name)
            else:
                rich.print(
                    "[yellow]Warning:[/yellow] Only local models can be rebuilt locally using inferless.yaml, for [blue]GIT[/blue] based deployment don't use [blue]`--local`[/blue] or [blue]-l[/blue] flag"
                )
                rebuild_model_fun(model_id)
        else:
            rebuild_model_fun(model_id)
    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


def rebuild_model_fun(model_id):
    try:
        models = {}
        _, _, _, workspace_id, _ = decrypt_tokens()
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)

            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to rebuild: ",
                completer=get_models(models=models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(
                        choice, models=models["models"]["models"]
                    )
                ),
                validate_while_typing=False,
            )
            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        validate = typer.confirm("Are you sure you want to rebuild this model? ")
        if validate:
            model_name = None
            with Progress(
                SpinnerColumn(),
                TextColumn(desc),
                transient=True,
            ) as progress:
                task_id = progress.add_task(description=processing, total=None)
                model_name = get_by_keys(
                    models["models"]["models"],
                    model_id,
                    "id",
                    "name",
                )
                if model_name is None:
                    raise InferlessCLIError(
                        f"Model with id: [bold]{model_id}[/bold] not found"
                    )

                details = get_model_details(model_id)
                rebuild_model(details["models"]["model_import"])

                progress.remove_task(task_id)

            rich.print(f"Rebuilding model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "list",
    help="List all models.",
)
def list_models():
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        table = Table(
            title="Model List",
            box=rich.box.ROUNDED,
            title_style="bold Black underline on white",
        )
        table.add_column("ID", style="yellow")
        table.add_column(
            "Name",
        )
        table.add_column("Created At")
        table.add_column("Updated At")
        table.add_column("Is Serverless")
        table.add_column("Status")

        for model in models["models"]["models"]:
            created_at = "-"
            updated_at = "-"
            try:
                created_at = dateutil.parser.isoparse(model["created_at"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except Exception as e:
                log_exception(e)
            try:
                updated_at = dateutil.parser.isoparse(model["updated_at"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except Exception as e:
                log_exception(e)

            table.add_row(
                model["id"],
                model["name"],
                created_at,
                updated_at,
                "Yes" if model["is_serverless"] else "No",
                model["status"],
            )

        total_models = models["models"]["total_models"]
        total_models_deployed = models["models"]["total_models_deployed"]

        console = Console()
        console.print(table)
        console.print("\n")
        # Display total models and total models deployed
        console.print(f"Total Models: [bold]{total_models}[/bold]\n")
        console.print(f"Total Models Deployed: [bold]{total_models_deployed}[/bold]\n")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "deactivate",
    help="deactivate a model. ",
)
def deactivate(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)

            models = get_workspace_models(
                workspace_id=workspace_id, workspace_filter="ACTIVE"
            )

            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(
                "[red]No Active models found in your workspace[/red]"
            )

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to deactivate: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        validate = typer.confirm("Are you sure you want to deactivate this model? ")
        if validate:
            model_name = None
            with Progress(
                SpinnerColumn(),
                TextColumn(desc),
                transient=True,
            ) as progress:
                task_id = progress.add_task(description=processing, total=None)
                model_name = get_by_keys(
                    models["models"]["models"],
                    model_id,
                    "id",
                    "name",
                )
                if model_name is None:
                    raise InferlessCLIError(
                        f"Model with id: [bold]{model_id}[/bold] not found"
                    )

                deactivate_model(model_id)
                progress.remove_task(task_id)

            rich.print(f"Deactivating model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "activate",
    help="activate a model. ",
)
def activate(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(
                workspace_id=workspace_id, workspace_filter="INACTIVE"
            )
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(
                "[red]No Deactivated models found in your workspace[/red]"
            )

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to activate: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            model_name = get_by_keys(
                models["models"]["models"],
                model_id,
                "id",
                "name",
            )
            if model_name is None:
                raise InferlessCLIError(
                    f"Model with id: [bold]{model_id}[/bold] not found"
                )

            activate_model(model_id)

            progress.remove_task(task_id)

            rich.print(f"Activating model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "delete",
    help="delete a model.",
)
def delete(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to delete: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        validate = typer.confirm("Are you sure you want to delete this model? ")
        if validate:
            model_name = None
            with Progress(
                SpinnerColumn(),
                TextColumn(desc),
                transient=True,
            ) as progress:
                task_id = progress.add_task(description=processing, total=None)
                model_name = get_by_keys(
                    models["models"]["models"],
                    model_id,
                    "id",
                    "name",
                )
                if model_name is None:
                    raise InferlessCLIError(
                        f"Model with id: [bold]{model_id}[/bold] not found"
                    )
                delete_model(model_id)
                progress.remove_task(task_id)
            rich.print(f"Deleted model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command("info", help="Get model details.")
def info(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to get details for: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        model_name = None
        data = None
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)

            model_name = get_by_keys(
                data=models["models"]["models"],
                value=model_id,
                key1="id",
                key2="name",
            )
            if model_name is None:
                raise InferlessCLIError(
                    f"Model with id: [bold]{model_id}[/bold] not found"
                )

            data = get_model_code(model_id)

            progress.remove_task(task_id)

        if data is not None:
            rich.print("[bold]Details:[/bold]")
            rich.print(f"[green]Name:[/green] {model_name}")
            rich.print(f"[green]ID:[/green] {model_id}")
            rich.print(f"[green]URL:[/green] {data['location']}\n")

    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)
