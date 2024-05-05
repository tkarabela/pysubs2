import pytest
import pysubs2


def test_identifier_to_class() -> None:
    with pytest.raises(pysubs2.UnknownFormatIdentifierError) as exc_info:
        pysubs2.formats.get_format_class("unknown-format-identifier")
    assert exc_info.value.format_ == "unknown-format-identifier"


def test_ext_to_identifier() -> None:
    with pytest.raises(pysubs2.UnknownFileExtensionError) as exc_info:
        pysubs2.formats.get_format_identifier(".xyz")
    assert exc_info.value.ext == ".xyz"


def test_identifier_to_ext() -> None:
    with pytest.raises(pysubs2.UnknownFormatIdentifierError) as exc_info:
        pysubs2.formats.get_file_extension("unknown-format-identifier")
    assert exc_info.value.format_ == "unknown-format-identifier"


def test_format_detection_fail() -> None:
    with pytest.raises(pysubs2.FormatAutodetectionError) as exc_info:
        pysubs2.formats.autodetect_format("")
    assert not exc_info.value.formats
