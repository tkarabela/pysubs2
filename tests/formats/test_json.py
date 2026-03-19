import pytest
from typing import Any

from pysubs2 import SSAFile, SSAEvent, SSAStyle, Color
from pysubs2.exceptions import FormatAutodetectionError


def test_write_read() -> None:
    subs = SSAFile()
    e1 = SSAEvent(text="Hello, world!")
    e2 = SSAEvent(text="The other subtitle.\\NWith two lines.", style="custom style")
    s1 = SSAStyle(italic=True, primarycolor=Color(r=255, g=0, b=0, a=0))

    subs.append(e1)
    subs.append(e2)
    subs.styles["custom style"] = s1

    json_text = subs.to_string("json")

    subs2 = SSAFile.from_string(json_text, "json")
    subs3 = SSAFile.from_string(json_text)

    assert subs2.equals(subs)
    assert subs3.equals(subs)


def test_read_unsupported_json_issue_85(tmp_path: Any) -> None:
    path = tmp_path / "test.atpj"
    with path.open("w") as fp:
        print("""{"some data": [1,2,3]}""", file=fp)

    with pytest.raises(FormatAutodetectionError):
        SSAFile.load(path)
