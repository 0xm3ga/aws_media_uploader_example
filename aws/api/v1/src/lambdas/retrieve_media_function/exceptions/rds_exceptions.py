from base_exceptions import CustomException
from constants.error_messages import RDS_COMMUNICATION_ERROR_MSG


class RDSCommunicationError(CustomException):
    """Exception raised for errors in communication with RDS."""

    def __init__(self, error: str):
        super().__init__(error)
        self.message = RDS_COMMUNICATION_ERROR_MSG.format(error=error)