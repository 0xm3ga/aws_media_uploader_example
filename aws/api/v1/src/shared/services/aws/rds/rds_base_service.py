import logging
from typing import Dict, Tuple

from botocore.exceptions import BotoCoreError
from shared.constants.logging_messages import RdsMessages
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
            logger.info(RdsMessages.Info.FETCH_RDS_DATA_SUCCESS.format(filename=filename))
            return data
        except BotoCoreError as e:
            error_message = RdsMessages.Error.RDS_COMMUNICATION_ERROR.format(error=str(e))
            logger.error(error_message)
            raise RDSCommunicationError(error_message) from None
        except Exception as e:
            error_message = RdsMessages.Error.UNEXPECTED_ERROR.format(error=str(e))
            logger.error(error_message)
            raise RDSCommunicationError(error_message) from None

    @staticmethod
    def fetch_media_info_from_rds(filename: str) -> Tuple[str, str]:
        """Fetch media information from the RDS."""
        rds_data = RdsBaseService.get_rds_data(filename)

        required_fields = ["username", "content_type"]
        missing_data = [field for field in required_fields if field not in rds_data]

        if missing_data:
            error_message = RdsMessages.Error.INVALID_RDS_RESPONSE.format(
                missing_data=", ".join(missing_data)
            )
            logger.error(error_message)
            raise MissingRequiredRDSVariablesError(error_message)

        logger.info(RdsMessages.Info.FETCH_MEDIA_INFO_SUCCESS.format(filename=filename))
        return rds_data["username"], rds_data["content_type"]
