import pysubs2


SAMI_INPUT1 = """\
<SAMI>
<Head>
   <Title>President John F. Kennedy Speech</Title>
   <SAMIParam>
      Copyright {(C)Copyright 1997, Microsoft Corporation}
      Media {JF Kennedy.wav}
      Metrics {time:ms; duration: 73000;}
      Spec {MSFT:1.0;}
   </SAMIParam>

   <STYLE TYPE="text/css"><!--
      P {margin-left: 29pt; margin-right: 29pt; font-size: 12pt; 
      text-align: left; font-family: tahoma, arial, sans-serif; 
      font-weight: normal; color: white; background-color: black;}

      TABLE {Width: "248pt" ;}

      .ENUSCC {Name: "English Captions"; lang: en-US-CC;}

#Source {margin-bottom: -15pt; background-color: silver; 
         color: black; vertical-align: normal; font-size: 12pt; 
         font-family: tahoma, arial, sans-serif; 
         font-weight: normal;}

#Youth {color: greenyellow; font-size: 18pt;}

#BigPrint-1 {color: yellow; font-size: 24pt;}-->
   </Style>
</Head>

<Body>
   <SYNC Start=0>
      <P Class=ENUSCC ID=Source>Pres. John F. Kennedy   
   <SYNC Start=10>
      <P Class=ENUSCC>Let the word go forth, 
         from this time and place to friend and foe 
         alike that the torch
   <SYNC Start=8800>
      <P Class=ENUSCC>has been passed to a new generation of Americans, 
         born in this century, tempered by war,
   <SYNC Start=19500>
      <P Class=ENUSCC>disciplined by a hard and bitter peace, 
         proud of our ancient heritage, and unwilling to witness
   <SYNC Start=28000>
      <P Class=ENUSCC>or permit the slow undoing of those human rights
          to which this nation has always
   <SYNC Start=38000>
      <P Class=ENUSCC>been committed and to which we are 
         committed today at home and around the world.
   <SYNC Start=46000>
      <P Class=ENUSCC>Let every nation know, 
         whether it wishes us well or ill, 
         that we shall pay any price, bear any burden,
   <SYNC Start=61000>
      <P Class=ENUSCC>meet any hardship, support any friend, 
         oppose any foe, to ensure the survival and
         success of liberty.
   <SYNC Start=73000>
      <P Class=ENUSCC ID=Source>End of:
      <P Class=ENUSCC>President John F. Kennedy Speech
</Body>
</SAMI>
"""

SAMI_INPUT2 = """\
<SAMI>
<Head>
   <Title>President John F. Kennedy Speech</Title>
   <SAMIParam>
      Copyright {(C)Copyright 1997, Microsoft Corporation}
      Media {JF Kennedy.wav}
      Metrics {time:ms; duration: 73000;}
      Spec {MSFT:1.0;}
   </SAMIParam>

   <STYLE TYPE="text/css"><!--
      P {margin-left: 29pt; margin-right: 29pt; font-size: 12pt; 
      text-align: left; font-family: tahoma, arial, sans-serif; 
      font-weight: normal; color: white; background-color: black;}

      TABLE {Width: "248pt" ;}

      .ENUSCC {Name: "English Captions"; lang: en-US-CC;}

#Source {margin-bottom: -15pt; background-color: silver; 
         color: black; vertical-align: normal; font-size: 12pt; 
         font-family: tahoma, arial, sans-serif; 
         font-weight: normal;}

#Youth {color: greenyellow; font-size: 18pt;}

#BigPrint-1 {color: yellow; font-size: 24pt;}-->
   </Style>
</Head>

<Body>
   <SYNC Start=0>
      <P Class=ENUSCC>Test of <B>bold <I>italic <U>underline <S>strikethrough</S></U></I></B>
</Body>
</SAMI>
"""

SAMI_OUTPUT1 = r"""
1
00:00:00,000 --> 00:00:00,010
Pres. John F. Kennedy

2
00:00:00,010 --> 00:00:06,272
Let the word go forth,
from this time and place to friend and foe
alike that the torch

3
00:00:08,800 --> 00:00:15,196
has been passed to a new generation of Americans,
born in this century, tempered by war,

4
00:00:19,500 --> 00:00:26,365
disciplined by a hard and bitter peace,
proud of our ancient heritage, and unwilling to witness

5
00:00:28,000 --> 00:00:33,860
or permit the slow undoing of those human rights
to which this nation has always

6
00:00:38,000 --> 00:00:43,860
been committed and to which we are
committed today at home and around the world.

7
00:00:46,000 --> 00:00:53,334
Let every nation know,
whether it wishes us well or ill,
that we shall pay any price, bear any burden,

8
00:01:01,000 --> 00:01:08,267
meet any hardship, support any friend,
oppose any foe, to ensure the survival and
success of liberty.

9
00:01:13,000 --> 00:01:16,180
End of:
President John F. Kennedy Speech
"""


def test_sami_simple():
    subs = pysubs2.SSAFile.from_string(SAMI_INPUT1)
    assert subs.to_string("srt").strip() == SAMI_OUTPUT1.strip()


def test_sami_basic_tags():
    subs = pysubs2.SSAFile.from_string(SAMI_INPUT2)
    assert len(subs) == 1
    assert subs[0].text == r"Test of {\b1}bold {\i1}italic {\u1}underline {\s1}strikethrough{\s0}{\u0}{\i0}{\b0}"
