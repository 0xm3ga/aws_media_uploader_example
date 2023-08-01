from base_exceptions import CustomException
from constants import error_messages as em


class RDSCommunicationError(CustomException):
    """Exception raised for errors in communication with RDS."""

    def __init__(self, error: str):
        super().__init__(error)
        self.message = em.RDS_COMMUNICATION_ERROR_MSG.format(error=error)
