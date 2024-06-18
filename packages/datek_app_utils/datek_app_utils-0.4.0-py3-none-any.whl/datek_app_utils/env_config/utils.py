from datek_app_utils.env_config.base import ConfigMeta, Variable
from datek_app_utils.env_config.errors import (
    ConfigAttributeError,
    ConfigAttributeErrorType,
    ValidationError,
)


def validate_config(class_: ConfigMeta):
    errors = []

    for item in class_:
        try:
            _validate_attribute(item)
        except ConfigAttributeError as error:
            errors.append(error)

    if errors:
        raise ValidationError(errors)


def _validate_attribute(item: Variable):
    try:
        value = item.value
    except ValueError:
        raise ConfigAttributeError(
            error_type=ConfigAttributeErrorType.INVALID_VALUE,
            attribute_name=item.name,
            required_type=item.type,
        )

    if item.default_value is ... and value is None:
        raise ConfigAttributeError(
            error_type=ConfigAttributeErrorType.NOT_SET,
            attribute_name=item.name,
            required_type=item.type,
        )
