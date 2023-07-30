class UnsupportedImageFormatError(Exception):
    """Raised when an image format is not supported."""

    pass


class S3AccessError(Exception):
    """Raised when there's an error accessing or manipulating data in S3."""

    pass


class ValidationError(Exception):
    """Raised when a value fails a validation check."""

    @staticmethod
    def check_value(value, allowed_values, parameter):
        """Check if a value is in a list of allowed values."""
        if value not in allowed_values:
            raise ValidationError(f"{parameter} must be one of {allowed_values}")

    @staticmethod
    def check_subset(values, allowed_values, parameter):
        """Check if a set of values is a subset of a set of allowed values."""
        if not set(value for value in values).issubset(allowed_values):
            raise ValidationError(f"{parameter} must be a subset of {allowed_values}")

    @staticmethod
    def check_required_fields(fields: dict, required: list):
        """Check if a dictionary contains all required fields."""
        missing = [field for field in required if not fields.get(field)]
        if missing:
            raise ValidationError(f"{', '.join(missing)} are required in the event")

    @staticmethod
    def check_non_empty_list(value, field_name):
        """Check if a list is not empty."""
        if not value:
            raise ValidationError(f"{field_name} list cannot be empty")


class EnvironmentVariableNotFound(Exception):
    """Raised when an expected environment variable is not found."""

    ENV_ERROR_MSG = "Environment variable '{}' not set"

    def __init__(self, variable):
        super().__init__(self.ENV_ERROR_MSG.format(variable))
