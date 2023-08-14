from unittest.mock import patch

import pytest
from botocore.exceptions import BotoCoreError

from aws.api.v1.src.shared.services.aws.rds.rds_base_service import (
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

# ===================== TESTS: RdsBaseService =====================


def test_get_rds_data_success():
    """Test successfully fetching RDS data given a filename."""
    data = RdsBaseService.get_rds_data(VALID_FILENAME)
    assert data == RDS_MOCK_DATA


@patch(
    "aws.api.v1.src.shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
    side_effect=BotoCoreError(),
)
def test_get_rds_data_boto_error(mock_get_rds_data):
    """Test BotoCoreError when fetching RDS data."""
    with pytest.raises(BotoCoreError):
        RdsBaseService.get_rds_data(VALID_FILENAME)


@patch(
    "aws.api.v1.src.shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
    side_effect=Exception(),
)
def test_get_rds_data_unexpected_error(mock_get_rds_data):
    """Test unexpected error when fetching RDS data."""
    with pytest.raises(Exception):
        RdsBaseService.get_rds_data(VALID_FILENAME)


def test_fetch_media_info_from_rds_success():
    """Test successfully fetching media info from RDS."""
    username, content_type = RdsBaseService.fetch_media_info_from_rds(VALID_FILENAME)
    assert username == RDS_MOCK_DATA["username"]
    assert content_type == RDS_MOCK_DATA["content_type"]


@patch(
    "aws.api.v1.src.shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
    return_value=MISSING_CONTENT_TYPE_DATA,
)
def test_fetch_media_info_from_rds_missing_content_type(mock_get_rds_data):
    """Test missing content_type when fetching media info from RDS."""
    with pytest.raises(
        MissingRequiredRDSVariablesError,
        match=RdsMessages.Error.INVALID_RDS_RESPONSE.format(missing_data="content_type"),
    ):
        RdsBaseService.fetch_media_info_from_rds(VALID_FILENAME)


@patch(
    "aws.api.v1.src.shared.services.aws.rds.rds_base_service.RdsBaseService.get_rds_data",
    return_value=MISSING_USERNAME_DATA,
)
def test_fetch_media_info_from_rds_missing_username(mock_get_rds_data):
    """Test missing username when fetching media info from RDS."""
    with pytest.raises(
        MissingRequiredRDSVariablesError,
        match=RdsMessages.Error.INVALID_RDS_RESPONSE.format(missing_data="username"),
    ):
        RdsBaseService.fetch_media_info_from_rds(VALID_FILENAME)
