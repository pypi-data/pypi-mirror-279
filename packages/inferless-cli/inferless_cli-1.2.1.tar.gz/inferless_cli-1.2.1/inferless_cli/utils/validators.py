from prompt_toolkit.validation import ValidationError


def validate_workspaces(choice, options):
    valid_choices = [item["name"] for item in options]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    return choice


def validate_volumes(choice, volumes):
    valid_choices = [item["name"] for item in volumes]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    return choice


def validate_models(choice, models):
    valid_choices = [item["name"] for item in models]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    return choice
