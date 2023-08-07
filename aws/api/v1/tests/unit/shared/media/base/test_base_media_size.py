import pytest

from aws.api.v1.src.shared.media.base import BaseMediaSizes, FeatureErrorMessages

# ===================== TESTS: _validate_dimensions =====================


def test_validate_dimensions_not_implemented():
    """Test _validate_dimensions raises error when DIMENSIONS not defined."""
    with pytest.raises(
        NotImplementedError,
        match=FeatureErrorMessages.FEATURE_NOT_IMPLEMENTED.format(feature_name="DIMENSIONS"),
    ):
        BaseMediaSizes._validate_dimensions()


class SubMediaSizes(BaseMediaSizes):
    DIMENSIONS = {"some_aspect_ratio": {"some_size": "some_dimension_data"}}  # type: ignore


def test_validate_dimensions_implemented():
    """Test _validate_dimensions doesn't raise error when DIMENSIONS is defined in a subclass."""
    SubMediaSizes._validate_dimensions()
