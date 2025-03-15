import pytest
import os.path as op
from pysubs2 import SSAFile, SSAEvent, SSAStyle, Color, FormatAutodetectionError
import tempfile


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


def test_read_unsupported_json_issue_85() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = op.join(temp_dir, "test.atpj")
        with open(path, "w") as fp:
            print("""{"some data": [1,2,3]}""", file=fp)

        with pytest.raises(FormatAutodetectionError):
            SSAFile.load(path)
