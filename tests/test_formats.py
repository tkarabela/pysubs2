import pytest
import pysubs2


def test_identifier_to_class():
    with pytest.raises(pysubs2.UnknownFormatIdentifierError) as exc_info:
        pysubs2.formats.get_format_class("unknown-format-identifier")
    assert exc_info.value.format_ == "unknown-format-identifier"


def test_ext_to_identifier():
    with pytest.raises(pysubs2.UnknownFileExtensionError) as exc_info:
        pysubs2.formats.get_format_identifier(".xyz")
    assert exc_info.value.ext == ".xyz"


def test_identifier_to_ext():
    with pytest.raises(pysubs2.UnknownFormatIdentifierError) as exc_info:
        pysubs2.formats.get_file_extension("unknown-format-identifier")
    assert exc_info.value.format_ == "unknown-format-identifier"


def test_format_detection_fail():
    with pytest.raises(pysubs2.FormatAutodetectionError) as exc_info:
        pysubs2.formats.autodetect_format("")
    assert not exc_info.value.formats
