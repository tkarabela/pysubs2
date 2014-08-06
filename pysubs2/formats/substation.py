import re

from ..ssastyle import SSAStyle

OVERRIDE_SEQUENCE = re.compile(r"{[^}]*}")

def parse_tags(text, style=SSAStyle(), styles={}):
    """
    Split text into fragments with computed SSAStyles.
    
    Returns list of tuples (fragment, style), where fragment is a part of text
    between two brace-delimited override sequences, and style is the computed
    styling of the fragment, ie. the original style modified by all override
    sequences before the fragment.
    
    Newline and non-breakable space overrides are left as-is.
    
    Supported override tags:
    
    - i, b, u, s
    - r (with or without style name)
    
    """
    
    fragments = OVERRIDE_SEQUENCE.split(text)
    if len(fragments) == 1:
        return [(text, style)]
    
    def apply_overrides(all_overrides):
        s = style.copy()
        for tag in re.findall(r"\\[ibus][10]|\\r[a-zA-Z_0-9 ]*", all_overrides):
            if tag == r"\r":
                s = style.copy() # reset to original line style
            elif tag.startswith(r"\r"):
                name = tag[2:]
                if name in styles:
                    s = styles[name].copy() # reset to named style
            else:
                if "i" in tag: s.italic = "1" in tag
                elif "b" in tag: s.bold = "1" in tag
                elif "u" in tag: s.underline = "1" in tag
                elif "s" in tag: s.strikeout = "1" in tag
        return s
    
    overrides = OVERRIDE_SEQUENCE.findall(text)
    overrides_prefix_sum = ["".join(overrides[:i]) for i in range(len(overrides) + 1)]
    computed_styles = map(apply_overrides, overrides_prefix_sum)
    return list(zip(fragments, computed_styles))

# XXX: SSA/ASS implementation
