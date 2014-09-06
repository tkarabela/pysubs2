from nose.tools import assert_raises
import pysubs2

def test_identifier_to_class():
    with assert_raises(pysubs2.UnknownFormatIdentifierError):
        pysubs2.formats.get_format_class("unknown-format-identifier")

def test_ext_to_identifier():
    with assert_raises(pysubs2.UnknownFileExtensionError):
        pysubs2.formats.get_format_identifier(".xyz")

def test_identifier_to_ext():
    with assert_raises(pysubs2.UnknownFormatIdentifierError):
        pysubs2.formats.get_file_extension("unknown-format-identifier")

def test_format_detection_fail():
    with assert_raises(pysubs2.FormatAutodetectionError):
        pysubs2.formats.autodetect_format("")
