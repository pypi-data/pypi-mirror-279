import os
import tempfile
import time
import rich
import typer
from prompt_toolkit import prompt
from inferless_cli.commands.deploy.constants import FAILED_TO_CREATE_MODEL_MESSAGE
from inferless_cli.commands.init.helpers import get_region_id
from inferless_cli.commands.volume.volume_prompt import find_volume_by_id
from inferless_cli.utils.constants import (
    DEFAULT_YAML_FILE_NAME,
    GIT,
    GITHUB,
    SPINNER_DESCRIPTION,
)
from inferless_cli.utils.exceptions import ConfigurationError, InferlessCLIError
from rich.progress import Progress, SpinnerColumn, TextColumn
from inferless_cli.utils.helpers import (
    create_zip_file,
    decrypt_tokens,
    get_current_mode,
    is_inferless_yaml_present,
    log_exception,
    read_yaml,
)
from inferless_cli.utils.inferless_config_handler import InferlessConfigHandler
from inferless_cli.utils.services import (
    create_presigned_io_upload_url,
    get_model_import_details,
    get_templates_list,
    get_workspace_regions,
    get_workspaces_list,
    import_model,
    set_env_variables,
    start_import_model,
    update_model_configuration,
    upload_file,
    upload_io,
    validate_github_url_permissions,
    validate_import_model,
)


def deploy_prompt(redeploy, config_file_name=None):
    rich.print("\nWelcome to the Inferless Model Deployment! \n")

    try:
        config = InferlessConfigHandler()
        if not config_file_name:
            config_file_name = prompt(
                "Enter the name of your config file: ", default=DEFAULT_YAML_FILE_NAME
            )
        yaml_data = config_initilizer(config_file_name)
        config.set_loaded_config(yaml_data)

        check_serverless_access(config)
        check_for_old_deployment(config, config_file_name, redeploy)
        handle_model_import(config, redeploy)
        handle_input_output_upload(config)
        model_validator(config)
        handle_model_configuration(config)
        update_model_secrets(config)
        handle_model_import_complete(config, config_file_name, redeploy)

    except ConfigurationError as error:
        rich.print(f"\n[red]Error (inferless.yaml): [/red] {error}")
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


def config_initilizer(config_file_name):
    is_yaml_present = is_inferless_yaml_present(config_file_name)

    if not is_yaml_present:
        raise ConfigurationError("Config file not found")

    yaml_data = read_yaml(config_file_name)
    if not yaml_data:
        raise ConfigurationError("Config Data not found")

    return yaml_data


def check_serverless_access(config):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()
        if config.get_value("configuration.is_serverless"):
            with Progress(
                SpinnerColumn(),
                TextColumn(SPINNER_DESCRIPTION),
                transient=True,
            ) as progress:
                progress.add_task(
                    description="Checking Permissons. Please wait...", total=None
                )
                workspaces = get_workspaces_list()
            allow_serverless = False
            for workspace in workspaces:
                if workspace["id"] == workspace_id:
                    allow_serverless = workspace["allow_serverless"]
                    break
            if not allow_serverless:
                email_address = "nilesh@inferless.com"
                rich.print(
                    f"[red]Serverless is not enabled for your account [yellow](beta feature)[/yellow][/red] \nplease contact [blue]{email_address}[/blue]",
                )
                raise InferlessCLIError("Serverless is not enabled for your account")
    except Exception as e:
        raise Exception(f"Error at check_serverless_access - {e}")


def check_for_old_deployment(config, config_file_name, redeploy):

    if config.get_value("model_import_id"):
        if config.get_value("import_source") == GIT:
            rich.print(
                "if you want to redeploy the model please use this command [blue]`inferless model rebuild`[/blue]\n"
            )
            raise InferlessCLIError(
                f"[red]model_import_id already exists in {config_file_name}.[/red] \nremove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]\n"
            )

        is_failed = False
        old_response = get_model_import_details(config.get_value("model_import_id"))
        if old_response and old_response.get("model_import").get("status") == "FAILURE":
            is_failed = True

        if not is_failed and not redeploy:

            rich.print(
                "if you want to redeploy the model please use this command [blue]`inferless model rebuild -l`[/blue]\n"
            )
            raise InferlessCLIError(
                f"[red]model_import_id already exists in {config_file_name}.[/red] \nremove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]\n"
            )

        if config.get_value("name") != old_response.get("model_import").get("name"):

            raise InferlessCLIError(
                f"[red]name mismatch.[/red] Remove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]"
            )

    if redeploy and not config.get_value("model_import_id"):
        raise InferlessCLIError(
            f"[red]model_import_id not found in {config_file_name}[/red]. To deploy run command [blue]`inferless deploy`[/blue]"
        )


def handle_model_import(config, redeploy):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:

        task_id = progress.add_task(description="Getting warmed up...", total=None)
        if config.get_value("import_source") == GIT:
            rich.print(
                "Deploying from git (make sure you have pushed your code to git)"
            )
            progress.update(task_id, description="Creating model...")
            details = handle_git_deployment(config)
        elif config.get_value("import_source") == "LOCAL":
            title = "Redeploying" if redeploy else "Deploying"
            description = (
                f"{title} from local directory (make sure you have saved your code)"
            )
            rich.print(description)
            progress.update(task_id, description=f"{title} model...")
            details = handle_local_deployment(config, redeploy, progress, task_id)
        else:
            details = None

        if details is None or not details.get("model_import").get("id"):
            raise InferlessCLIError(FAILED_TO_CREATE_MODEL_MESSAGE)

        config.update_config("model_import_id", details.get("model_import").get("id"))
        rich.print("[green]Model initilized...![/green]")
        progress.remove_task(task_id)
        return details


def handle_git_deployment(config):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()

    rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")

    payload = {
        "name": config.get_value("name"),
        "details": {
            "is_auto_build": False,
            "webhook_url": "",
            "github_url": config.get_value("model_url"),
            "runtime": "PYTORCH",
        },
        "import_source": GIT,
        "source_framework_type": config.get_value("source_framework_type"),
        "provider": GITHUB,
        "workspace": workspace_id,
    }
    details = import_model(payload)
    return details


def handle_local_deployment(config, redeploy, progress, task_id):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()
    rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")

    payload = {
        "name": config.get_value("name"),
        "details": {
            "is_auto_build": False,
            "webhook_url": "",
            "upload_type": "local",
            "is_cli_deploy": True,
            "runtime": "PYTORCH",
        },
        "import_source": "FILE",
        "source_framework_type": config.get_value("source_framework_type"),
        "source_location": "LOCAL_FILE",
        "workspace": workspace_id,
    }
    if redeploy:
        payload["id"] = config.get_value("model_import_id")
    details = import_model(payload)

    if not details.get("model_import").get("id"):
        raise InferlessCLIError(FAILED_TO_CREATE_MODEL_MESSAGE)

    progress.update(task_id, description="Uploading model to secure location...")

    payload["id"] = details.get("model_import").get("id")
    details = upload_model(payload)

    return details


def upload_model(payload):

    with tempfile.TemporaryDirectory() as temp_dir:
        directory_to_snapshot = os.getcwd()  # Current working directory

        model_id = payload.get("id")
        zip_filename = os.path.join(
            temp_dir, f"{os.path.basename(directory_to_snapshot)}.zip"
        )
        create_zip_file(zip_filename, directory_to_snapshot)
        s3_key = (
            f"cli_zip_files/{model_id}/{os.path.basename(directory_to_snapshot)}.zip"
        )
        file_size = os.path.getsize(zip_filename)
        with open(zip_filename, "rb") as zip_file:

            model_url = upload_file(zip_file, s3_key, file_size, upload_type="ZIP")

            payload["details"]["model_url"] = model_url
            payload["id"] = model_id

        details = import_model(payload)
        if not details.get("model_import").get("id"):
            raise InferlessCLIError(FAILED_TO_CREATE_MODEL_MESSAGE)
        return details


def handle_input_output_upload(config):

    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Uploading input_schema.py / input.json and output.json",
            total=None,
        )
        model_id = config.get_value("model_import_id")
        io_schema = False

        if config.get_value("io_schema"):
            io_schema = config.get_value("io_schema")

        if not io_schema:

            input_file_name = f"{model_id}/input.json"
            output_file_name = f"{model_id}/output.json"
            input_payload = {
                "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                "file_name": input_file_name,
            }
            output_payload = {
                "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                "file_name": output_file_name,
            }
            create_presigned_io_upload_url(
                input_payload, config.get_value("optional.input_file_name")
            )
            create_presigned_io_upload_url(
                output_payload, config.get_value("optional.output_file_name")
            )
            S3_BUCKET_NAME = "infer-data"
            if get_current_mode() == "DEV":
                S3_BUCKET_NAME = "infer-data-dev"
            s3_input_url = f"s3://{S3_BUCKET_NAME}/{input_file_name}"
            s3_output_url = f"s3://{S3_BUCKET_NAME}/{output_file_name}"
            _ = upload_io(
                {
                    "id": model_id,
                    "input_json": {"s3_infer_data_url": s3_input_url},
                    "output_json": {"s3_infer_data_url": s3_output_url},
                }
            )


def model_validator(config):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Validating the model...",
            total=None,
        )
        model_id = config.get_value("model_import_id")
        if not model_id:
            raise InferlessCLIError("Model id is not available. Please try again.")

        if config.get_value("import_source") == GIT:
            validate_github_url_permissions(url=config.get_value("model_url"))
        start_import_model({"id": model_id})
        status, res = poll_model_status(model_id)

        if status == "FAILURE":
            error_msg = res["model_import"]["import_error"]["message"]
            rich.print(f"[red]{error_msg}[/red]")
            raise InferlessCLIError(error_msg)
        rich.print("[green]Model Validated...![/green]")


def poll_model_status(id):
    start_time = time.time()
    while True:

        response = get_model_import_details(id)

        status = response.get("model_import", {}).get("status")

        if status in ["FILE_STRUCTURE_VALIDATED", "SUCCESS", "FAILURE"]:
            return status, response

        if status in ["FILE_STRUCTURE_VALIDATION_FAILED", "IMPORT_FAILED"]:
            raise InferlessCLIError(f"Status was {status}, response was: {response}")

        elapsed_time = time.time() - start_time
        if elapsed_time >= 5 * 60:
            raise InferlessCLIError("Structure validation timed out after 5 minutes")

        time.sleep(5)


def handle_model_configuration(config):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        _, _, _, workspace_id, _ = decrypt_tokens()
        progress.add_task(
            description="Updating model configuration...",
            total=None,
        )
        region_value = "AZURE"

        if config.get_value("configuration.region"):
            regions = get_workspace_regions({"workspace_id": workspace_id})
            region_value = get_region_id(
                config.get_value("configuration.region"), regions
            )
            if region_value is None:
                region_value = "AZURE"

        config_payload = {
            "id": config.get_value("model_import_id"),
            "configuration": {
                "region": region_value,
                "runtime": "PYTORCH",
                "cpu": float(config.get_value("configuration.vcpu")),
                "inference_time": config.get_value("configuration.inference_time"),
                "is_auto_build": False,
                "is_dedicated": config.get_value("configuration.is_dedicated"),
                "machine_type": config.get_value("configuration.gpu_type"),
                "is_serverless": config.get_value("configuration.is_serverless"),
                "max_replica": config.get_value("configuration.max_replica"),
                "min_replica": config.get_value("configuration.min_replica"),
                "memory": float(config.get_value("configuration.ram")),
                "scale_down_delay": config.get_value("configuration.scale_down_delay"),
            },
        }

        if config.get_value("configuration.custom_volume_id") and config.get_value(
            "configuration.custom_volume_name"
        ):
            volume_data = find_volume_by_id(
                workspace_id, config.get_value("configuration.custom_volume_id")
            )
            if not volume_data or volume_data.get("region") != region_value:
                raise InferlessCLIError(
                    "Volume id not found. Please check the volume id and try again."
                )

            config_payload["configuration"]["custom_volume_config"] = config.get_value(
                "configuration.custom_volume_id"
            )
            config_payload["configuration"]["custom_volume_name"] = config.get_value(
                "configuration.custom_volume_name"
            )

        if config.get_value("configuration.custom_runtime_id"):
            runtimes = get_templates_list(workspace_id)

            runtime_id = config.get_value("configuration.custom_runtime_id")
            runtime = None

            for rt in runtimes:

                if rt["id"] == runtime_id and rt["region"] == region_value:
                    runtime = rt
                    break

            if runtime is None:
                raise InferlessCLIError(
                    "Runtime id not found. Please check the runtime id and try again."
                )

            config_payload["configuration"]["custom_docker_template"] = runtime_id
            config_payload["configuration"]["custom_docker_config"] = ""
            if config.get_value("configuration.custom_runtime_version"):
                config_payload["configuration"]["custom_docker_version"] = int(
                    config.get_value("configuration.custom_runtime_version")
                )

        update_model_configuration(config_payload)
        rich.print("[green]Model Configuration Updated...![/green]")


def update_model_secrets(config):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:

        if config.get_value("env") or config.get_value("secrets"):
            progress.add_task(
                description="Setting environment variables...",
                total=None,
            )
            env_payload = {
                "model_import_id": config.get_value("model_import_id"),
                "variables": config.get_value("env") or {},
                "credential_ids": config.get_value("secrets") or [],
                "patch": False,
            }
            set_env_variables(env_payload)
            rich.print("[green]Model Environment/Secrets Updated...![/green]")


def handle_model_import_complete(config, config_file_name, redeploy):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        model_id = config.get_value("model_import_id")
        progress.add_task(
            description="Finalizing model import...",
            total=None,
        )

        validate_import_model({"id": model_id})
        description = "Model import started, here is your model_import_id: "
        if redeploy:
            description = "Redeploying the model, here is your model_import_id: "
        config.save_config(config_file_name)

        rich.print(f"\n{description} [blue]{model_id}[/blue] \n")
        message = (
            "You can check the logs by running this command:\n\n"
            f"[blue]inferless log -i {model_id}[/blue]"
        )
        rich.print(message)
