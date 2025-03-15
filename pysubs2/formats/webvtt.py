import json
import re
from typing import Any, Dict, List, Optional, Sequence, TextIO, Tuple, Union

from .base import FormatBase
from .subrip import SubripFormat
from .substation import parse_tags
from ..ssaevent import SSAEvent
from ..ssafile import SSAFile
from ..ssastyle import SSAStyle
from ..time import make_time

NestedDict = Dict[str, Union[str, List[Any], Dict[str, Any]]]
TIMESTAMP = re.compile(r"(\d{2,}:)?(\d{2}):(\d{2})\.(\d{3})")
CUE_SETTING = re.compile(
    r"vertical:\w+|line:-?\d+%?|position:\d+%(?:,\w+-\w+)?|size:\d+%|align:\w+|region:\w+")
NRS_BLOCK = re.compile(r"NOTE|REGION|STYLE")


def is_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


def get_info_before_first_timestamp(fp: TextIO) -> Dict[str, str]:
    info = {}
    for line in fp:
        if TIMESTAMP.match(line):
            break
        elif m := re.match(r"WEBVTT\s+(.+)\s*", line):
            info["header_text"] = m.group(1).strip()
        elif m := re.match(r"X-TIMESTAMP-MAP=(.+)\s*", line):
            info["x_timestamp_map"] = m.group(1).strip()
    fp.seek(0)
    return info


def format_vtt_info_key(s: str, reverse: bool = False) -> str:
    # Reverse conversion: convert ASS script info tag format to variable name
    if reverse:
        if s.startswith('VTT'):
            s = s[3:]
        parts = re.findall(r'[A-Z][^A-Z]*', s)
        result = '_'.join(part.lower() for part in parts)
    # Forward conversion: convert variable name to ASS script info tag format
    else:
        parts = s.split('_')
        capitalized_parts = [part.capitalize() for part in parts]
        result = 'VTT' + ''.join(capitalized_parts)
    return result


def disguise_block(fp: TextIO) -> None:
    """Disguise NOTE, REGION, STYLE, as cue to record their relative positions to fit reordering."""
    lines: List[str] = []
    # Record the start index of each NOTE, and the nearest time after it
    blocks_index0type: List[Tuple[int, str, Tuple[str, ...]]] = []
    # Record the time of each disguised block
    blocks_time: List[List[str]] = []

    timestamp_to_ms = WebVTTFormat.timestamp_to_ms
    ms_to_timestamp = WebVTTFormat.ms_to_timestamp

    last_time: Tuple[int, str, Tuple[str, ...]] = (0, "", ("",))
    for i, line in enumerate(fp):
        lines.append(line)
        if NRS_BLOCK.match(line):
            blocks_index0type.append((i, "isnrs", ("",)))
        elif (m := TIMESTAMP.match(line)) and blocks_index0type:
            if blocks_index0type[-1][1] == "isnrs":
                blocks_index0type.append((i, "istime", m.groups()))
            last_time = (i, "istime", m.groups())

    if not blocks_index0type:
        fp.seek(0)
        return

    if blocks_index0type[-1][1] == "isnrs":
        blocks_index0type.insert(-1, last_time)

    start_time: int = 0
    end_time: int = 0
    blocks_index0type.reverse()
    for b in blocks_index0type:
        if b[1] == "istime":
            end_time = timestamp_to_ms(b[2])
            start_time = end_time - 10
            blocks_time.append([ms_to_timestamp(end_time), ""])
        elif b[1] == "isnrs" and start_time and end_time:
            blocks_time.append([ms_to_timestamp(
                start_time), ms_to_timestamp(end_time)])
        else:
            blocks_time.append(["", ""])

    blocks_index0type.reverse()
    blocks_time.reverse()
    for bi, bt in zip(blocks_index0type, blocks_time):
        if bi[1] == "istime":
            start_time = timestamp_to_ms(bi[2]) + 10
            end_time = start_time + 10
        if bi[1] == "isnrs" and bt[0] == "":
            bt[:] = [ms_to_timestamp(
                start_time), ms_to_timestamp(end_time)]

    for bi, bt in zip(blocks_index0type, blocks_time):
        if bi[1] == "isnrs":
            lines[bi[0]] = f"isnrs\n{bt[0]} --> {bt[1]}\n{lines[bi[0]]}"

    fp.seek(0)
    fp.writelines(lines)
    fp.truncate()
    fp.seek(0)


class WebVTTFormat(FormatBase):
    """Web Video Text Tracks (WebVTT) subtitle format implementation"""

    @staticmethod
    def ms_to_timestamp(ms: int) -> str:
        result = SubripFormat.ms_to_timestamp(ms)
        return result.replace(",", ".")

    @staticmethod
    def timestamp_to_ms(groups: Sequence[str]) -> int:
        _h, _m, _s, _ms = groups
        if not _h:
            h = 0
        else:
            h = int(_h.strip(":"))
        m, s, ms = map(int, (_m, _s, _ms))
        return make_time(h=h, m=m, s=s, ms=ms)

    @classmethod
    def guess_format(cls, text: str) -> Optional[str]:
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if text.lstrip().startswith("WEBVTT"):
            return "vtt"
        else:
            return None

    @classmethod
    def from_file(cls, subs: "SSAFile", fp: TextIO, format_: str, keep_html_tags: bool = False,
                  keep_unknown_html_tags: bool = False, **kwargs: Any) -> None:
        """
        See :meth:`pysubs2.formats.FormatBase.from_file()`

        Supported tags:

          - ``<i>``
          - ``<u>``
          - ``<b>``

        Keyword args:
            keep_html_tags: If True, all HTML tags will be kept as-is instead of being
                converted to SubStation tags (eg. you will get ``<i>example</i>`` instead of ``{\\i1}example{\\i0}``).
                Setting this to True overrides the ``keep_unknown_html_tags`` option.
            keep_unknown_html_tags: If True, supported HTML tags will be converted
                to SubStation tags and any other HTML tags will be kept as-is
                (eg. you would get ``<blink>example {\\i1}text{\\i0}</blink>``).
                If False, these other HTML tags will be stripped from output
                (in the previous example, you would get only ``example {\\i1}text{\\i0}``)
        """
        timestamps: List[Tuple[int, int]] = []  # (start, end)
        # contains lists of lines following each cue timing
        following_lines: List[List[str]] = []
        # contains cue settings with each cue timing
        cues_about: List[NestedDict] = []

        info = get_info_before_first_timestamp(fp)
        disguise_block(fp)

        last_line = ""
        for line in fp:
            stamps = TIMESTAMP.findall(line)
            if len(stamps) == 2:  # timestamp line
                start, end = map(cls.timestamp_to_ms, stamps)
                timestamps.append((start, end))
                temp_cue_about: NestedDict = {}
                if setting := CUE_SETTING.findall(line):
                    temp_cue_about["setting"] = dict([s.split(":") for s in setting])
                if id_ := last_line.strip():
                    temp_cue_about["identifier"] = id_
                if temp_cue_about:
                    cues_about.append(temp_cue_about)
                else:
                    cues_about.append({})
                following_lines.append([])
            else:
                if timestamps:
                    following_lines[-1].append(line)
            last_line = line

        def prepare_text(lines: List[str], is_final_block: bool = False) -> str:
            # The final block does not need to process
            if is_final_block:
                pass
            # In general, the last element of follow lines in a vtt file is the identifier of the next cue or a blank line, remove it.
            elif len(lines) > 2 or (len(lines) == 2 and not lines[-1].strip()):
                lines = lines[:-1]
            # If the cue payload is empty and the next cue has no identifier, follow lines has only one element and it is a blank line.
            elif len(lines) == 1 and not lines[0].strip():
                return ""

            # Handle the general case.
            s = "".join(lines).strip()
            # When rewriting the vtt file, set keep_html_tags to True, otherwise the specified styles of i, u, b will be lost. For example, <i.myclass>text</i>.
            if not keep_html_tags:
                s = re.sub(r"< *i.*?>", r"{\\i1}", s)
                s = re.sub(r"< */ *i *>", r"{\\i0}", s)
                s = re.sub(r"< *u.*?>", r"{\\u1}", s)
                s = re.sub(r"< */ *u *>", r"{\\u0}", s)
                s = re.sub(r"< *b.*?>", r"{\\b1}", s)
                s = re.sub(r"< */ *b *>", r"{\\b0}", s)
            if not (keep_html_tags or keep_unknown_html_tags):
                # strip other HTML tags
                s = re.sub(r"< */? *[a-zA-Z][^>]*>", "", s)
            s = re.sub(r"\n", r"\\N", s)  # convert newlines
            return s

        blocks_count = len(timestamps)
        for i, ((start, end), lines, c_about) in enumerate(zip(timestamps, following_lines, cues_about)):
            if i == blocks_count - 1:
                is_final_block = True
            else:
                is_final_block = False
            e = SSAEvent(start=start, end=end, text=prepare_text(
                lines, is_final_block), vtt_cue_about=c_about)
            if NRS_BLOCK.match(e.text):
                e.is_comment = True
            subs.append(e)
        cls._write_info_to_subs(subs, info)

    @classmethod
    def to_file(cls, subs: "SSAFile", fp: TextIO, format_: str, apply_styles: bool = True,
                cue_with_identifier: bool = False, reorder_cues_by_time: bool = True,
                blank_lines_between_blocks: int = 2, override_identifiers_with_numbers: bool = False,
                **kwargs: Any) -> None:
        """
        See :meth:`pysubs2.formats.FormatBase.to_file()`

        Italic, underline and bold styling is supported.

        Keyword args:
            apply_styles: If False, do not write any styling (ignore line style
                and override tags).
            cue_with_identifier: The identifier is a name that identifies the cue.
                If True, currently, the identifier contains only a number, just like srt.
            reorder_cues_by_time: If True, reorder cues by start time.
            blank_lines_between_blocks: Number of blank lines between blocks.
            override_identifiers_with_numbers: If True, override the original identifiers with sequential numbers.
        """

        def prepare_text(text: str, style: SSAStyle, is_comment: bool) -> str:
            text = text.replace(r"\h", " ")
            text = text.replace(r"\n", "\n")
            text = text.replace(r"\N", "\n")

            body = []
            # Exclude cue text that is metadata text in JSON format
            if not is_comment and not is_json(text):
                for fragment, sty in parse_tags(text, style, subs.styles):
                    if apply_styles:
                        if sty.italic:
                            fragment = f"<i>{fragment}</i>"
                        if sty.underline:
                            fragment = f"<u>{fragment}</u>"
                        if sty.bold:
                            fragment = f"<b>{fragment}</b>"
                    body.append(fragment)
            else:
                body.append(text)

            return re.sub("\n+", "\n", "".join(body).strip())

        info = cls._read_info_from_subs(subs)
        print("WEBVTT", file=fp, end="")
        if header_text := info.get("header_text"):
            print(f" {header_text}", file=fp, end="")
        if x_timestamp_map := info.get("x_timestamp_map"):
            print("", file=fp)
            print(f"X-TIMESTAMP-MAP={x_timestamp_map}", file=fp, end="")

        sepreator = "\n\n"
        if blank_lines_between_blocks >= 1:
            sepreator = "\n" * blank_lines_between_blocks + "\n"
        print("", file=fp, end=sepreator)

        lines = cls._get_lines(subs, reorder_cues_by_time)
        has_identifier = any(line.vtt_cue_about.get("identifier") for line in lines)
        lineno = 0
        for line in lines:
            start = cls.ms_to_timestamp(line.start)
            end = cls.ms_to_timestamp(line.end)
            text = prepare_text(line.text, subs.styles.get(
                line.style, SSAStyle.DEFAULT_STYLE), line.is_comment)

            if cue_with_identifier and not line.is_comment:
                if override_identifiers_with_numbers or not has_identifier:
                    lineno += 1
                    print(lineno, file=fp)
                elif identifier := line.vtt_cue_about.get("identifier"):
                    print(identifier, file=fp)
            if temp_setting := line.vtt_cue_about.get("setting"):
                if isinstance(temp_setting, dict):
                    setting = " ".join(
                        [f"{k}:{v}" for k, v in temp_setting.items()])
                    print(start, "-->", end, setting, file=fp)
            else:
                if not line.is_comment:
                    print(start, "-->", end, file=fp)

            # Ensure there is only one blank line at the end
            if "@last line" in line.name:
                line.name = line.name.replace("@last line", "")
                sepreator = "\n\n"
            print(text, end=sepreator, file=fp)

    @classmethod
    def _get_lines(cls, subs: "SSAFile", sort_by_time: bool = True) -> List[SSAEvent]:
        lines = subs.events
        lines[-1].name += "@last line"
        if sort_by_time:
            lines.sort(key=lambda e: e.start)
        return lines

    @classmethod
    def _write_info_to_subs(cls, subs: "SSAFile", info: Dict[str, str]) -> None:
        for k, v in info.items():
            k_str = format_vtt_info_key(k)
            subs.info[k_str] = v

    @classmethod
    def _read_info_from_subs(cls, subs: "SSAFile") -> Dict[str, str]:
        info: Dict[str, str] = {}
        for k_str, v in subs.info.items():
            if re.match(r'VTT', k_str):
                k = format_vtt_info_key(k_str, reverse=True)
                info[k] = v
        return info
