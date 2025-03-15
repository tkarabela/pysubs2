"""
test of SubStation [Fonts] handling

"""

from pysubs2 import SSAFile
import os.path as op


FONT_SUBS_AEGISUB_PATH = op.join(op.dirname(__file__), "data/subtitle_with_attached_fonts_aegisub.ass")
FONT_SUBS_PYSUBS_PATH = op.join(op.dirname(__file__), "data/subtitle_with_attached_fonts_pysubs2_ref.ass")
FONT_SUBS_NO_EVENTS_PATH = op.join(op.dirname(__file__), "data/subtitle_with_attached_fonts_no_events.ass")
IMAGE_SUBS_AEGISUB_PATH = op.join(op.dirname(__file__), "data/subtitle_with_attached_images_aegisub.ass")
IMAGE_SUBS_PYSUBS_PATH = op.join(op.dirname(__file__), "data/subtitle_with_attached_images_pysubs2_ref.ass")

def test_font_passthrough_from_aegisub() -> None:
    subs_aegisub = SSAFile.load(FONT_SUBS_AEGISUB_PATH)
    subs_pysubs2_ref = SSAFile.load(FONT_SUBS_PYSUBS_PATH)
    assert subs_aegisub.equals(subs_pysubs2_ref)  # sanity check for input

    # convert Aegisub, make sure we get the same output as reference
    subs_pysubs2_text = subs_aegisub.to_string("ass")

    with open(FONT_SUBS_PYSUBS_PATH) as fp:
        subs_pysubs2_text_ref = fp.read()

    assert subs_pysubs2_text.strip() == subs_pysubs2_text_ref.strip()

    # check again after loading
    subs_pysubs2 = SSAFile.from_string(subs_pysubs2_text)
    assert subs_pysubs2_ref.equals(subs_pysubs2)


def test_file_ending_with_font_section() -> None:
    subs = SSAFile.load(FONT_SUBS_NO_EVENTS_PATH)
    subs_ref = SSAFile.load(FONT_SUBS_PYSUBS_PATH)
    assert set(subs.fonts_opaque.keys()) == set(subs_ref.fonts_opaque.keys())


def test_image_passthrough_from_aegisub() -> None:
    subs_aegisub = SSAFile.load(IMAGE_SUBS_AEGISUB_PATH)
    subs_pysubs2_ref = SSAFile.load(IMAGE_SUBS_PYSUBS_PATH)
    assert subs_aegisub.equals(subs_pysubs2_ref)  # sanity check for input

    # convert Aegisub, make sure we get the same output as reference
    subs_pysubs2_text = subs_aegisub.to_string("ass")

    with open(IMAGE_SUBS_PYSUBS_PATH) as fp:
        subs_pysubs2_text_ref = fp.read()

    assert subs_pysubs2_text.strip() == subs_pysubs2_text_ref.strip()

    # check again after loading
    subs_pysubs2 = SSAFile.from_string(subs_pysubs2_text)
    assert subs_pysubs2_ref.equals(subs_pysubs2)

# the following tests would be useful if we supported fonts in a non-opaque way

# GARAMOND_REGULAR_PATH = op.join(op.dirname(__file__), "data/EBGaramond08-Regular.ttf")
# GARAMOND_ITALIC_PATH = op.join(op.dirname(__file__), "data/EBGaramond08-Italic.ttf")
#
#
# def test_synthetic_empty_font():
#     fonts = {"empty.ttf": b""}
#
#     subs = SSAFile()
#     subs.events.append(SSAEvent(text="test subtitle"))
#     subs.fonts.update(fonts)
#
#     s = subs.to_string("ass")
#     subs_loaded = SSAFile.from_string(s)
#
#     assert subs.equals(subs_loaded)
#     assert subs_loaded.fonts == fonts
#
#
# def test_synthetic_single_font():
#     fonts = {"simple.ttf": b"This is a simple binary file" + bytes(range(256))}
#
#     subs = SSAFile()
#     subs.events.append(SSAEvent(text="test subtitle"))
#     subs.fonts.update(fonts)
#
#     s = subs.to_string("ass")
#     subs_loaded = SSAFile.from_string(s)
#
#     assert subs.equals(subs_loaded)
#     assert subs_loaded.fonts == fonts
#
#
# def test_synthetic_multiple_fonts():
#
#
#     fonts = {
#         "first.ttf": b"This is a simple binary file" + bytes(range(256)),
#         "second.ttf": b"Another binary file"
#     }
#
#     subs = SSAFile()
#     subs.events.append(SSAEvent(text="test subtitle"))
#     subs.fonts.update(fonts)
#
#     s = subs.to_string("ass")
#     subs_loaded = SSAFile.from_string(s)
#
#     assert subs.equals(subs_loaded)
#     assert subs_loaded.fonts == fonts
#
#
# def test_real_multiple_fonts():
#     with open(GARAMOND_REGULAR_PATH, "rb") as fp:
#         garamond_regular_data = fp.read()
#     with open(GARAMOND_ITALIC_PATH, "rb") as fp:
#         garamond_italic_data = fp.read()
#
#     fonts = {
#         op.basename(GARAMOND_REGULAR_PATH): garamond_regular_data,
#         op.basename(GARAMOND_ITALIC_PATH): garamond_italic_data
#     }
#
#     subs = SSAFile()
#     subs.events.append(SSAEvent(text="test subtitle"))
#     subs.fonts.update(fonts)
#
#     s = subs.to_string("ass")
#     subs_loaded = SSAFile.from_string(s)
#
#     assert subs.equals(subs_loaded)
#     assert subs_loaded.fonts == fonts
