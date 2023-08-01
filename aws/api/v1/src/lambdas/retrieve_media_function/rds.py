import logging
from typing import Dict

from botocore.exceptions import BotoCoreError
from constants.error_messages import INVALID_RDS_RESPONSE_MSG, RDS_COMMUNICATION_ERROR_MSG
from exceptions import MissingRequiredRDSVariablesError, RDSCommunicationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_rds_data(filename: str) -> Dict[str, str]:
    """Fetch RDS data given a filename."""
    try:
        # TODO: replace with actual logic
        return {
            "username": "b5784a47-cb06-4712-9889-c5e68c960233",
            "content_type": "images",
        }
    except BotoCoreError as e:
        error_message = str(e)
        logger.error(RDS_COMMUNICATION_ERROR_MSG.format(error=error_message))
        raise RDSCommunicationError(str(e))
    except Exception as e:
        error_message = str(e)
        logger.error(RDS_COMMUNICATION_ERROR_MSG.format(error=error_message))
        raise RDSCommunicationError(str(e))


def fetch_media_info_from_rds(filename: str) -> tuple:
    """Fetch media information from the RDS."""
    try:
        rds_data = get_rds_data(filename)
    except Exception as e:
        error_message = str(e)
        logger.error(RDS_COMMUNICATION_ERROR_MSG.format(error=error_message))
        raise RDSCommunicationError(error_message)

    required_fields = ["username", "content_type"]
    missing_data = [field for field in required_fields if field not in rds_data]

    if missing_data:
        error_message = ", ".join(missing_data)
        logger.error(INVALID_RDS_RESPONSE_MSG.format(missing_data=error_message))
        raise MissingRequiredRDSVariablesError(error_message)

    return rds_data["username"], rds_data["content_type"]
