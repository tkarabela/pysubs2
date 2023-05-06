"""
pysubs2.time tests

"""

from fractions import Fraction 
import pytest

from pysubs2.time import *


# helper functions
cs2ms = lambda cs: 10 * cs
s2ms  = lambda s:  1000 * s
m2ms  = lambda m:  60 * 1000 * m
h2ms  = lambda h:  60 * 60 * 1000 * h


def test_timestamp():
    # proper SSA
    assert TIMESTAMP.match("1:23:45.67").groups() == ("1", "23", "45", "67")
    
    # proper SRT
    assert TIMESTAMP.match("10:23:45,678").groups() == ("10", "23", "45", "678")
    
    # malformed SRT
    assert TIMESTAMP.match("10:23:45.678").groups() == ("10", "23", "45", "678")
    assert TIMESTAMP.match("10:23:45,67").groups() == ("10", "23", "45", "67")
    assert TIMESTAMP.match("10:23:45.67").groups() == ("10", "23", "45", "67")
    assert TIMESTAMP.match("1:23:45,678").groups() == ("1", "23", "45", "678")
    assert TIMESTAMP.match("1:23:45.678").groups() == ("1", "23", "45", "678")
    assert TIMESTAMP.match("99:99:99,999").groups() == ("99", "99", "99", "999")
    assert TIMESTAMP.match("1:23:45,6789").groups() == ("1", "23", "45", "678") # at most 3 frac digits matched

    # malformed ASS (see pull request #54)
    assert TIMESTAMP.match("1:23:4.67") .groups() == ("1", "23", "4", "67")
    assert TIMESTAMP.match("1:2:45.67") .groups() == ("1", "2", "45", "67")
    assert TIMESTAMP.match("1:2:3.4").groups() == ("1", "2", "3", "4")

    # rejected stamps
    assert TIMESTAMP.match("-1:23:45.67") is None
    assert TIMESTAMP.match("12:45:67") is None
    assert TIMESTAMP.match("100:23:45,678") is None
    assert TIMESTAMP.match("1:23:45,") is None
    assert TIMESTAMP.match("1:23:45.") is None
    assert TIMESTAMP.match("1::45.67") is None
    assert TIMESTAMP.match(":12:45.67") is None


def test_timestamp_short():
    # proper TMP
    assert TIMESTAMP_SHORT.match("01:23:45").groups() == ("01", "23", "45")

    # malformed SRT
    assert TIMESTAMP_SHORT.match("10:23:45.678").groups() == ("10", "23", "45")
    assert TIMESTAMP_SHORT.match("10:23:45,").groups() == ("10", "23", "45")

    # rejected stamps
    assert TIMESTAMP_SHORT.match("-1:23:45") is None
    assert TIMESTAMP_SHORT.match("100:23:45") is None
    assert TIMESTAMP_SHORT.match("1:23:4") is None
    assert TIMESTAMP_SHORT.match("1:2:45") is None
    assert TIMESTAMP_SHORT.match("1::45") is None
    assert TIMESTAMP_SHORT.match(":12:45") is None


def test_timestamp_to_ms():
    # proper SSA
    assert timestamp_to_ms(TIMESTAMP.match("1:23:45.67").groups()) == \
        h2ms(1) + m2ms(23) + s2ms(45) + cs2ms(67)
    
    # proper SRT
    assert timestamp_to_ms(TIMESTAMP.match("10:23:45,678").groups()) == \
        h2ms(10) + m2ms(23) + s2ms(45) + 678
    
    # malformed SRT
    assert timestamp_to_ms(TIMESTAMP.match("99:99:99,999").groups()) == \
        h2ms(99) + m2ms(99) + s2ms(99) + 999

    assert timestamp_to_ms(TIMESTAMP.match("1:23:45,6789").groups()) == \
        h2ms(1) + m2ms(23) + s2ms(45) + 678

    # proper TMP
    assert timestamp_to_ms(TIMESTAMP_SHORT.match("10:23:45").groups()) == \
           h2ms(10) + m2ms(23) + s2ms(45)


def test_times_to_ms():
    # basic tests
    assert times_to_ms() == 0
    assert times_to_ms(h=5) == h2ms(5)
    assert times_to_ms(m=5) == m2ms(5)
    assert times_to_ms(s=5) == s2ms(5)
    assert times_to_ms(ms=5) == 5
    assert times_to_ms(h=5, m=5, s=5, ms=5) == h2ms(5) + m2ms(5) + s2ms(5) + 5
    
    # rounding
    assert times_to_ms(s=0.5) == 500
    assert isinstance(times_to_ms(s=0.5), int)
    assert times_to_ms(s=Fraction("1/2")) == 500
    assert isinstance(times_to_ms(s=Fraction("1/2")), int)
    
    # negative input
    assert times_to_ms(h=-1, m=60) == 0
    assert times_to_ms(h=-5, m=5, s=-5, ms=5) == h2ms(-5) + m2ms(5) + s2ms(-5) + 5
    
    # inverse of ms_to_times()
    assert times_to_ms(*ms_to_times(0)) == 0
    assert times_to_ms(*ms_to_times(1)) == 1
    assert times_to_ms(*ms_to_times(123456)) == 123456


def test_ms_to_times():
    # basic tests
    assert ms_to_times(0) == (0, 0, 0, 0)
    assert isinstance(ms_to_times(0), Times)
    assert ms_to_times(s2ms(5)) == (0, 0, 5, 0)
    assert ms_to_times(m2ms(5)) == (0, 5, 0, 0)
    assert ms_to_times(h2ms(5)) == (5, 0, 0, 0)
    assert ms_to_times(h2ms(5) + m2ms(5) + s2ms(5) + 5) == (5, 5, 5, 5)
    
    assert ms_to_times(h2ms(1) + m2ms(2) + s2ms(3) + 4).h == 1
    assert ms_to_times(h2ms(1) + m2ms(2) + s2ms(3) + 4).m == 2
    assert ms_to_times(h2ms(1) + m2ms(2) + s2ms(3) + 4).s == 3
    assert ms_to_times(h2ms(1) + m2ms(2) + s2ms(3) + 4).ms == 4
    
    # rounding
    assert ms_to_times(3.5) == (0, 0, 0, 4)
    assert isinstance(ms_to_times(3.5)[-1], int)
    assert ms_to_times(Fraction("7/2")) == (0, 0, 0, 4)
    assert isinstance(ms_to_times(Fraction("7/2"))[-1], int)
    
    # inverse of ms_to_times()
    assert ms_to_times(times_to_ms(ms=1)) == (0, 0, 0, 1)
    assert ms_to_times(times_to_ms(s=1)) == (0, 0, 1, 0)
    assert ms_to_times(times_to_ms(m=1)) == (0, 1, 0, 0)
    assert ms_to_times(times_to_ms(h=1)) == (1, 0, 0, 0)
    assert ms_to_times(times_to_ms(h=1,m=2,s=3,ms=4)) == (1, 2, 3, 4)


def test_frames_to_ms():
    # basic tests
    assert frames_to_ms(0, 25, TimeType.EXACT) == 0
    assert isinstance(frames_to_ms(0, 25, TimeType.EXACT), int)
    assert frames_to_ms(100, 25, TimeType.EXACT) == 4000
    assert frames_to_ms(1, 23.976, TimeType.EXACT) == 42
    assert isinstance(frames_to_ms(1, 23.976, TimeType.EXACT), int)
   
    # Negative frame handling
    with pytest.raises(ValueError):
        frames_to_ms(-1, 23.976, TimeType.EXACT)

    # framerate handling
    with pytest.raises(ValueError):
        frames_to_ms(frames=1, fps=0.0, time_type=TimeType.EXACT)
    with pytest.raises(ValueError):
        frames_to_ms(frames=1, fps=-25.0, time_type=TimeType.EXACT)
    with pytest.raises(TypeError):
        frames_to_ms(frames=1, fps="pal", time_type=TimeType.EXACT)  # keyword aliases from PySubs 0.1 are no longer supported

def test_ms_to_frames():
    # basic tests
    assert ms_to_frames(0, 25, TimeType.EXACT) == 0
    assert isinstance(ms_to_frames(0, 25, TimeType.EXACT), int)
    assert ms_to_frames(4000, 25, TimeType.EXACT) == 100
    assert ms_to_frames(42, 23.976, TimeType.EXACT) == 1
    assert isinstance(ms_to_frames(42, 23.976, TimeType.EXACT), int)
    
    # Negative ms handling
    with pytest.raises(ValueError):
        ms_to_frames(-42, 23.976, TimeType.EXACT)

    # framerate handling
    with pytest.raises(ValueError):
        ms_to_frames(1, fps=0.0, time_type=TimeType.EXACT)
    with pytest.raises(ValueError):
        ms_to_frames(1, fps=-25.0, time_type=TimeType.EXACT)
    with pytest.raises(TypeError):
        ms_to_frames(1, fps="pal", time_type=TimeType.EXACT)  # keyword aliases from PySubs 0.1 are no longer supported

def test_ms_to_str():
    assert ms_to_str(0) == "0:00:00"
    assert ms_to_str(0, fractions=True) == "0:00:00.000"
    assert ms_to_str(1) == "0:00:00"
    assert ms_to_str(1, fractions=True) == "0:00:00.001"
    assert ms_to_str(-1) == "-0:00:00" # TODO: negative zero... wart?
    assert ms_to_str(-1, fractions=True) == "-0:00:00.001"
    assert ms_to_str(h2ms(1) + m2ms(2) + s2ms(3) + 999) == "1:02:03"
    assert ms_to_str(h2ms(1) + m2ms(2) + s2ms(3) + 999, fractions=True) == "1:02:03.999"
    assert ms_to_str(-h2ms(1)) == "-1:00:00"
    assert ms_to_str(-h2ms(1), fractions=True) == "-1:00:00.000"
    assert ms_to_str(h2ms(1000)) == "1000:00:00"
