from pysubs2 import SSAFile, SSAEvent, SSAStyle, Color

def test_write_read():
    subs = SSAFile()
    e1 = SSAEvent(text="Hello, world!")
    e2 = SSAEvent(text="The other subtitle.\\NWith two lines.", style="custom style")
    s1 = SSAStyle(italic=True, primarycolor=Color(r=255, g=0, b=0, a=0))

    subs.append(e1)
    subs.append(e2)
    subs.styles["custom style"] = s1

    json_text = subs.to_string("json")

    subs2 = SSAFile.from_string(json_text, "json")

    assert subs2.equals(subs)
