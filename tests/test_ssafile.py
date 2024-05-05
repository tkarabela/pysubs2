import pytest

from pysubs2 import SSAFile, SSAStyle, SSAEvent, make_time


def test_repr_default() -> None:
    subs = SSAFile()
    ref = "<SSAFile with 0 events and 1 styles>"
    assert repr(subs) == ref


def test_repr_simple() -> None:
    subs = SSAFile()
    subs.append(SSAEvent(start=make_time(m=5), end=make_time(m=6)))
    subs.append(SSAEvent(start=make_time(m=125), end=make_time(m=126)))
    subs.append(SSAEvent(start=make_time(m=15), end=make_time(m=16)))
    subs.styles["style1"] = SSAStyle()
    subs.styles["style2"] = SSAStyle()
    ref = "<SSAFile with 3 events and 3 styles, last timestamp 2:06:00>"
    assert repr(subs) == ref


def test_shift() -> None:
    #TODO: write more tests
    subs = SSAFile()

    with pytest.raises(ValueError):
        subs.shift(frames=5)

    with pytest.raises(ValueError):
        subs.shift(fps=23.976)

    with pytest.raises(ValueError):
        subs.shift(frames=5, fps=-1)


def test_import_styles() -> None:
    red1 = SSAStyle()
    red2 = SSAStyle()
    green = SSAStyle()
    subs1 = SSAFile()
    subs2 = SSAFile()

    def prepare() -> None:
        subs1.styles = {}
        subs2.styles = {}
        subs1.styles["green"] = green
        subs1.styles["red"] = red1
        subs2.styles["red"] = red2

    prepare()
    subs2.import_styles(subs1)
    assert subs2.styles["green"] is green
    assert subs2.styles["red"] is red1

    prepare()
    subs2.import_styles(subs1, overwrite=False)
    assert subs2.styles["green"] is green
    assert subs2.styles["red"] is red2

    with pytest.raises(TypeError):
        subs2.import_styles({})  # type: ignore[arg-type]


def test_rename_style() -> None:
    subs = SSAFile()
    red = SSAStyle()
    green = SSAStyle()

    def prepare() -> None:
        subs.events = [SSAEvent(style="red"), SSAEvent(style="unrelated")]
        subs.styles = dict(red=red, green=green)

    prepare()
    subs.rename_style("red", "blue")
    assert "red" not in subs.styles
    assert subs.styles["blue"] is red
    assert subs[0].style == "blue"
    assert subs[1].style == "unrelated"

    prepare()
    with pytest.raises(ValueError):
        # cannot delete style via move
        subs.rename_style("red", "green")

    prepare()
    with pytest.raises(ValueError):
        subs.rename_style("red", "illegal,name")
    with pytest.raises(ValueError):
        subs.rename_style("red", "illegal\nname")
    with pytest.raises(KeyError):
        subs.rename_style("nonexistent-style", "blue")


def test_transform_framerate() -> None:
    subs = SSAFile()
    subs.append(SSAEvent(start=0, end=10))
    subs.append(SSAEvent(start=1000, end=1010))

    with pytest.raises(ValueError):
        subs.transform_framerate(1, 0)
    with pytest.raises(ValueError):
        subs.transform_framerate(1, -1)
    with pytest.raises(ValueError):
        subs.transform_framerate(0, 1)
    with pytest.raises(ValueError):
        subs.transform_framerate(-1, 1)

    subs.transform_framerate(10, 20)
    assert subs[0] == SSAEvent(start=0, end=5)
    assert subs[1] == SSAEvent(start=500, end=505)


def test_insertion_of_wrong_type() -> None:
    subs = SSAFile()
    subs.append(SSAEvent())

    with pytest.raises(TypeError):
        subs.append(42)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        subs.insert(42)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        subs[0] = 42  # type: ignore[call-overload]


def test_slice_api() -> None:
    subs = SSAFile()
    subs[:] = [
        SSAEvent(text="A"),
        SSAEvent(text="B"),
        SSAEvent(text="C")
    ]
    assert subs[0].text == "A"
    assert subs[-1].text == "C"

    bc = subs[1:]
    assert len(bc) == 2
    assert bc[0].text == "B"
    assert bc[1].text == "C"

    del subs[1:]
    assert len(subs) == 1
    assert subs[0].text == "A"

    subs[:] = (SSAEvent(text=c) for c in "XYZ")
    assert len(subs) == 3
    assert subs[0].text == "X"
    assert subs[1].text == "Y"
    assert subs[2].text == "Z"
