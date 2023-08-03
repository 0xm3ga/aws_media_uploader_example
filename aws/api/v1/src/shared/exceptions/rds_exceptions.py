from shared.constants.error_messages import RdsErrorMessages

from .base_exceptions import CustomException


class RDSCommunicationError(CustomException):
    """Exception raised for errors in communication with RDS."""

    def __init__(self, error: str):
        super().__init__(error)
        self.message = RdsErrorMessages.RDS_COMMUNICATION_ERROR.format(error=error)
