from unittest.mock import patch

import pytest
from botocore.exceptions import BotoCoreError

from shared.services.aws.rds.rds_base_service import (
    MissingRequiredRDSVariablesError,
    RdsBaseService,
    RdsMessages,
)

# ===================== CONSTANTS =====================
VALID_FILENAME = "mock-uuid"

RDS_MOCK_DATA = {
    "username": "b5784a47-cb06-4712-9889-c5e68c960233",
    "content_type": "images",
}

MISSING_CONTENT_TYPE_DATA = {
    "username": "b5784a47-cb06-4712-9889-c5e68c960233",
}

MISSING_USERNAME_DATA = {
    "content_type": "images",
}


class TestRdsBaseService:
    def test_get_rds_data_success(self):
        """Test successfully fetching RDS data given a filename."""
        data = RdsBaseService.get_rds_data(VALID_FILENAME)
        assert data == RDS_MOCK_DATA

    @patch(
        "shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
        side_effect=BotoCoreError(),
    )
    def test_get_rds_data_boto_error(self, mock_get_rds_data):
        """Test BotoCoreError when fetching RDS data."""
        with pytest.raises(BotoCoreError):
            RdsBaseService.get_rds_data(VALID_FILENAME)

    @patch(
        "shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
        side_effect=Exception(),
    )
    def test_get_rds_data_unexpected_error(self, mock_get_rds_data):
        """Test unexpected error when fetching RDS data."""
        with pytest.raises(Exception):
            RdsBaseService.get_rds_data(VALID_FILENAME)

    def test_fetch_media_info_from_rds_success(self):
        """Test successfully fetching media info from RDS."""
        username, content_type = RdsBaseService.fetch_media_info_from_rds(VALID_FILENAME)
        assert username == RDS_MOCK_DATA["username"]
        assert content_type == RDS_MOCK_DATA["content_type"]

    @patch(
        "shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
        return_value=MISSING_CONTENT_TYPE_DATA,
    )
    def test_fetch_media_info_from_rds_missing_content_type(self, mock_get_rds_data):
        """Test missing content_type when fetching media info from RDS."""
        with pytest.raises(
            MissingRequiredRDSVariablesError,
            match=RdsMessages.Error.MISSING_VARIABLES_IN_RESPONSE.format(error="content_type"),
        ):
            RdsBaseService.fetch_media_info_from_rds(VALID_FILENAME)

    @patch(
        "shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
        return_value=MISSING_USERNAME_DATA,
    )
    def test_fetch_media_info_from_rds_missing_username(self, mock_get_rds_data):
        """Test missing username when fetching media info from RDS."""
        with pytest.raises(
            MissingRequiredRDSVariablesError,
            match=RdsMessages.Error.MISSING_VARIABLES_IN_RESPONSE.format(error="username"),
        ):
            RdsBaseService.fetch_media_info_from_rds(VALID_FILENAME)
