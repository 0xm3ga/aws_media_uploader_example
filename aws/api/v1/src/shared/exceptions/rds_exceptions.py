from shared.constants.logging_messages import RdsMessages

from .base_exceptions import CustomException


class RDSCommunicationError(CustomException):
    """Exception raised for errors in communication with RDS."""

    def __init__(self, error: str):
        super().__init__(error)
        self.message = RdsMessages.Error.RDS_COMMUNICATION_ERROR.format(error=error)
