import logging
from typing import Any, Dict, Optional, Type

from shared import exceptions as ex
from shared.constants.error_messages import ValidationErrorMessages


class EventValidator:
    def __init__(self, event: Dict[str, Any]):
        self._event = event
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

    def _get_from_dict(self, dictionary: Dict[str, Any], key: str, optional: bool = False):
        try:
            return dictionary[key]
        except KeyError:
            if optional:
                return None
            else:
                self.logger.error(ValidationErrorMessages.MISSING_PARAMETER.format(parameter=key))
                raise ex.MissingParameterError(parameter=key)

    def _validate_type(self, value: Any, name: str, expected_type: Optional[Type] = None):
        if value is None or expected_type is None:
            return

        if not isinstance(value, expected_type):
            self.logger.error(
                ValidationErrorMessages.INVALID_TYPE.format(
                    parameter=name,
                    actual=type(value).__name__,
                    expected=expected_type.__name__,
                )
            )
            raise ex.InvalidTypeError(
                parameter=name,
                actual=type(value).__name__,
                expected=expected_type.__name__,
            )

    def _validate_value(self, value: Any, name: str, allowed_values=None):
        if allowed_values is None or value is None:
            return

        if value not in allowed_values:
            self.logger.error(
                ValidationErrorMessages.PARAMETER_NOT_IN_SET.format(
                    parameter=name,
                    value=value,
                    allowed_values=allowed_values,
                )
            )
            raise ex.InvalidValueError(parameter=name, value=value, allowed_values=allowed_values)

    def _get_and_validate(
        self,
        dictionary: Dict[str, Any],
        name: str,
        optional: bool = False,
        expected_type: Optional[Type] = None,
        allowed_values=None,
    ):
        value = self._get_from_dict(dictionary, name, optional)
        self._validate_type(value, name, expected_type)
        self._validate_value(value, name, allowed_values)
        return value

    def get_query_string_parameter(
        self,
        name: str,
        optional: bool = False,
        expected_type: Optional[Type] = None,
        allowed_values=None,
    ) -> Any:
        return self._get_and_validate(
            dictionary=self._event.get("queryStringParameters", {}),
            name=name,
            optional=optional,
            expected_type=expected_type,
            allowed_values=allowed_values,
        )

    def get_path_parameter(
        self,
        name: str,
        optional: bool = False,
        expected_type: Optional[Type] = None,
        allowed_values=None,
    ) -> Any:
        return self._get_and_validate(
            dictionary=self._event.get("pathParameters", {}),
            name=name,
            optional=optional,
            expected_type=expected_type,
            allowed_values=allowed_values,
        )

    def get_authorizer_parameter(self, name: str, optional: bool = False) -> Any:
        value = self._get_from_dict(
            dictionary=self._event.get("requestContext", {})
            .get("authorizer", {})
            .get("claims", {}),
            key=f"cognito:{name}",
            optional=optional,
        )

        if value is None and optional is False:
            self.logger.error(ValidationErrorMessages.UNAUTHORIZED)
            raise ex.UnauthorizedError(ValidationErrorMessages.UNAUTHORIZED)

        return value
