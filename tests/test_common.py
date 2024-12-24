from pysubs2 import Color
from pysubs2.common import etree_register_namespace_override
import pytest
import xml.etree.ElementTree as ET


def test_color_argument_validation() -> None:
    Color(r=0, g=0, b=0)  # does not raise

    with pytest.raises(ValueError):
        Color(r=0, g=0, b=256)

    with pytest.raises(ValueError):
        Color(r=0, g=0, b=-1)


def test_etree_register_namespace_override() -> None:
    test_xml_elem = ET.Element("{http://my-namespace}test")
    assert ET.tostring(test_xml_elem) == b'<ns0:test xmlns:ns0="http://my-namespace" />'

    with etree_register_namespace_override():
        ET.register_namespace("", "http://my-namespace")
        assert ET.tostring(test_xml_elem) == b'<test xmlns="http://my-namespace" />'

    assert ET.tostring(test_xml_elem) == b'<ns0:test xmlns:ns0="http://my-namespace" />'
