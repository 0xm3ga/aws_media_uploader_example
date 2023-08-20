import logging
from typing import Any, Dict, Optional, Type

from shared.constants.logging_messages import ValidationMessages
from shared.exceptions import (
    InvalidParamTypeError,
    InvalidParamValueError,
    MissingAuthorizerError,
    MissingParameterError,
)


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
                self.logger.error(ValidationMessages.Error.MISSING_PARAM.format(param=key))
                raise MissingParameterError(param=key)

    def _validate_type(self, value: Any, name: str, expected_type: Optional[Type] = None):
        if value is None or expected_type is None:
            return

        if not isinstance(value, expected_type):
            print(
                f"Value: {value}, Type: {type(value)}, Expected Type: {expected_type}"
            )  # Add this line
            self.logger.error(
                ValidationMessages.Error.INVALID_PARAM_TYPE.format(
                    param=name,
                    actual=type(value).__name__,
                    allowed=expected_type.__name__,
                )
            )
            raise InvalidParamTypeError(
                param=name,
                actual=type(value),
                allowed=[expected_type],
            )

    def _validate_value(self, value: Any, name: str, allowed_values=None):
        if allowed_values is None or value is None:
            return

        if value not in allowed_values:
            self.logger.error(
                ValidationMessages.Error.INVALID_PARAM_VALUE.format(
                    param=name,
                    actual=value,
                    allowed=allowed_values,
                )
            )
            raise InvalidParamValueError(
                param=name,
                actual=value,
                allowed=allowed_values,
            )

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

        self.logger.info(ValidationMessages.Info.VALIDATION_SUCCESSFUL.format(parameter=name))
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
        try:
            value = self._get_from_dict(
                dictionary=self._event.get("requestContext", {})
                .get("authorizer", {})
                .get("claims", {}),
                key=f"cognito:{name}",
                optional=optional,
            )
        except MissingParameterError:
            MissingAuthorizerError.log_error
            raise MissingAuthorizerError

        self.logger.info(ValidationMessages.Info.AUTHORIZE_SUCCESSFUL.format(parameter=name))
        return value
