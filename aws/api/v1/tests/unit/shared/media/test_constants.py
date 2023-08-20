from shared.media.constants import AspectRatioData, DimensionData


# ===================== TESTS: AspectRatioData =====================
def test_aspect_ratio_str_representation():
    """
    Test the string representation of the AspectRatioData class.
    """
    ar = AspectRatioData(4, 5)
    assert str(ar) == "4:5"


def test_aspect_ratio_as_tuple():
    """
    Test the tuple representation of the AspectRatioData class.
    """
    ar = AspectRatioData(4, 5)
    assert ar.as_tuple() == (4, 5)


# ===================== TESTS: DimensionData =====================
def test_dimension_str_representation():
    """
    Test the string representation of the DimensionData class.
    """
    dimension = DimensionData(1080, 1350)
    assert str(dimension) == "1080:1350"


def test_dimension_as_tuple():
    """
    Test the tuple representation of the DimensionData class.
    """
    dimension = DimensionData(1080, 1350)
    assert dimension.as_tuple() == (1080, 1350)
