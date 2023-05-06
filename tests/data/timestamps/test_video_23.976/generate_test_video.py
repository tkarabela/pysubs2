from textwrap import dedent
from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta
from fractions import Fraction
import pysubs2
import subprocess
import os

# create an image
out = Image.new("RGB", (1280, 720), (255, 255, 255))

# get a font
fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", 32)

fps = Fraction(23_976, 1000)

os.makedirs("./img", exist_ok=True)

with open("test_video.srt", "w") as fp:
    for frame in range(500):
        canvas = out.copy()
        # get a drawing context
        d = ImageDraw.Draw(canvas)

        ms1 = round(1000 * frame * (1/fps))
        us1 = round(1000_000 * frame * (1/fps))
        ms1_next = round(1000 * (frame+1) * (1 / fps))
        t1 = timedelta(microseconds=us1)
        text = dedent(f"""\
        Frame {frame:04}
        T = {ms1:06} ms ({t1}) @ {float(fps):.3f} fps
        """).strip()
        # draw multiline text
        d.multiline_text((10, 10), text, font=fnt, fill=(0, 0, 0))

        canvas.save(f"img/test_video_{frame:04}.png")

        print(frame+1, file=fp)
        print(pysubs2.formats.SubripFormat.ms_to_timestamp(ms1), "-->", pysubs2.formats.SubripFormat.ms_to_timestamp(ms1_next), file=fp)
        print(text, file=fp)
        print(file=fp)


subprocess.check_call(["ffmpeg", "-y", "-r", f"{float(fps):.4f}", "-i", "img/test_video_%04d.png", "-pix_fmt", "yuv420p", "test_video.mkv"])
subprocess.check_call(["mkvextract", "test_video.mkv", "timestamps_v2", "0:ts-track0.txt"])

# subs = pysubs2.load("test_video.srt")
# subs.save("test_video.ass")
#
# subprocess.check_call(["ffmpeg", "-y", "-i", "test_video.mkv", "-vf", "subtitles=test_video.ass", "test_video_with_ass.mkv"])
# subprocess.check_call(["ffmpeg", "-y", "-i", "test_video.mkv", "-vf", "subtitles=test_video.srt", "test_video_with_srt.mkv"])
