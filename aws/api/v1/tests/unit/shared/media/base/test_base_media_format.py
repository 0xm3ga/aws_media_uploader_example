import pytest

from aws.api.v1.src.shared.media.base import BaseMediaFormats, Extension, FeatureErrorMessages

# ===================== TESTS: __init__ and _validate_formats =====================


def test_initialize_base_media_formats_not_implemented():
    """Test initialization raises error when FORMATS not defined."""
    with pytest.raises(
        NotImplementedError,
        match=FeatureErrorMessages.FEATURE_NOT_IMPLEMENTED.format(feature_name="FORMATS"),
    ):
        BaseMediaFormats()


# Test for a subclass of BaseMediaFormats when FORMATS is defined
def test_initialize_sub_media_formats_implemented():
    """Test initialization doesn't raise error when FORMATS is defined in a subclass."""

    # Define a subclass with FORMATS implemented
    class SubMediaFormats(BaseMediaFormats):
        formats = {Extension.AVI: "format_name"}  # Replace with a valid extension and format

    # Shouldn't raise an error
    SubMediaFormats()


# Test for a subclass of BaseMediaFormats when FORMATS is defined for _validate_formats
def test_validate_formats_implemented():
    """Test _validate_formats doesn't raise error when FORMATS is defined in a subclass."""

    # Define a subclass with FORMATS implemented
    class SubMediaFormats(BaseMediaFormats):
        formats = {Extension.AVI: "format_name"}  # Replace with a valid extension and format

    sub_formats = SubMediaFormats()
    # This shouldn't raise an error
    sub_formats._validate_formats()
