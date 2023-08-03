import logging
from typing import Dict, Tuple

from botocore.exceptions import BotoCoreError
from shared.constants.error_messages import RdsErrorMessages
from shared.constants.log_messages import RdsLogMessages
from shared.exceptions import MissingRequiredRDSVariablesError, RDSCommunicationError

logger = logging.getLogger(__name__)


class RdsBaseService:
    @staticmethod
    def get_rds_data(filename: str) -> Dict[str, str]:
        """Fetch RDS data given a filename."""
        try:
            # TODO: replace with actual logic
            data = {
                "username": "b5784a47-cb06-4712-9889-c5e68c960233",
                "content_type": "images",
            }
            logger.info(RdsLogMessages.FETCH_RDS_DATA_SUCCESS.format(filename=filename))
            return data
        except BotoCoreError as e:
            error_message = RdsErrorMessages.RDS_COMMUNICATION_ERROR.format(error=str(e))
            logger.error(error_message)
            raise RDSCommunicationError(error_message) from None
        except Exception as e:
            error_message = RdsErrorMessages.UNEXPECTED_ERROR.format(error=str(e))
            logger.error(error_message)
            raise RDSCommunicationError(error_message) from None

    @staticmethod
    def fetch_media_info_from_rds(filename: str) -> Tuple[str, str]:
        """Fetch media information from the RDS."""
        rds_data = RdsBaseService.get_rds_data(filename)

        required_fields = ["username", "content_type"]
        missing_data = [field for field in required_fields if field not in rds_data]

        if missing_data:
            error_message = RdsErrorMessages.INVALID_RDS_RESPONSE.format(
                missing_data=", ".join(missing_data)
            )
            logger.error(error_message)
            raise MissingRequiredRDSVariablesError(error_message)

        logger.info(RdsLogMessages.FETCH_MEDIA_INFO_SUCCESS.format(filename=filename))
        return rds_data["username"], rds_data["content_type"]
