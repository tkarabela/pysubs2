import pysubs2


TRANSCRIBE_RESULT = {
    'text': ' And so my fellow Americans ask not what your country can do for you, ask what you can do for your country.',
    'segments': [{'id': 0, 'seek': 0, 'start': 0.0, 'end': 7.6000000000000005,
                  'text': ' And so my fellow Americans ask not what your country can do for you,',
                  'tokens': [50364, 400, 370, 452, 7177, 6280, 1029, 406, 437, 428, 1941, 393, 360, 337, 291, 11, 50744,
                             50744, 1029, 437, 291, 393, 360, 337, 428, 1941, 13, 50894], 'temperature': 0.0,
                  'avg_logprob': -0.39726984089818496, 'compression_ratio': 1.3417721518987342,
                  'no_speech_prob': 0.09207311272621155},
                 {'id': 1, 'seek': 760, 'start': 7.6, 'end': 36.6, 'text': ' ask what you can do for your country.',
                  'tokens': [50364, 1029, 437, 291, 393, 360, 337, 428, 1941, 13, 51814], 'temperature': 0.0,
                  'avg_logprob': -0.4266586701075236, 'compression_ratio': 0.8809523809523809,
                  'no_speech_prob': 0.0026147987227886915}], 'language': 'en'}


WHISPER_JAX_INPUT = r"""
[01:14.500 -> 01:15.500]  Okay.
[01:15.500 -> 01:17.500]  You know you can't smoke weed and drive, right?
[01:17.500 -> 01:19.500]  That's a DWI, man.
[01:19.500 -> 01:20.500]  Really?
[01:20.500 -> 01:21.500]  Yeah.
[01:22.500 -> 01:25.000]  And the reason I'm saying that is I can smell it, right?
[01:25.000 -> 01:29.000]  And I don't know if it's literally all over you.
[01:29.000 -> 01:32.000]  Or what's all that all over your shirt and your pants?
[01:32.000 -> 01:34.000]  Yeah, I know what I should say.
[01:34.000 -> 01:36.000]  It's like it's all over you, man.
[01:36.000 -> 01:38.000]  Hey, come on, dude.
[01:38.000 -> 01:40.000]  Yeah.
[01:40.000 -> 01:44.000]  So, if you drink and drive, it's a DWI, right?
[01:44.000 -> 01:47.880]  If you smoke weed and drive drive it's the DWI. They're both legal
"""

WHISPER_JAX_OUTPUT_SRT = r"""
1
00:01:14,500 --> 00:01:15,500
Okay.

2
00:01:15,500 --> 00:01:17,500
You know you can't smoke weed and drive, right?

3
00:01:17,500 --> 00:01:19,500
That's a DWI, man.

4
00:01:19,500 --> 00:01:20,500
Really?

5
00:01:20,500 --> 00:01:21,500
Yeah.

6
00:01:22,500 --> 00:01:25,000
And the reason I'm saying that is I can smell it, right?

7
00:01:25,000 --> 00:01:29,000
And I don't know if it's literally all over you.

8
00:01:29,000 --> 00:01:32,000
Or what's all that all over your shirt and your pants?

9
00:01:32,000 --> 00:01:34,000
Yeah, I know what I should say.

10
00:01:34,000 --> 00:01:36,000
It's like it's all over you, man.

11
00:01:36,000 --> 00:01:38,000
Hey, come on, dude.

12
00:01:38,000 --> 00:01:40,000
Yeah.

13
00:01:40,000 --> 00:01:44,000
So, if you drink and drive, it's a DWI, right?

14
00:01:44,000 --> 00:01:47,880
If you smoke weed and drive drive it's the DWI. They're both legal
"""


def test_read_whisper_transcript_dict() -> None:
    subs = pysubs2.load_from_whisper(TRANSCRIBE_RESULT)

    e1, e2 = subs
    assert e1.start == 0
    assert e1.end == 7600
    assert e1.text == "And so my fellow Americans ask not what your country can do for you,"
    assert e2.start == 7600
    assert e2.end == 36600
    assert e2.text == "ask what you can do for your country."


def test_read_whisper_segments_list() -> None:
    subs = pysubs2.load_from_whisper(TRANSCRIBE_RESULT["segments"])  # type: ignore[arg-type]

    e1, e2 = subs
    assert e1.start == 0
    assert e1.end == 7600
    assert e1.text == "And so my fellow Americans ask not what your country can do for you,"
    assert e2.start == 7600
    assert e2.end == 36600
    assert e2.text == "ask what you can do for your country."


def test_parse_whisper_jax() -> None:
    subs = pysubs2.SSAFile.from_string(WHISPER_JAX_INPUT)
    assert subs.to_string("srt").strip() == WHISPER_JAX_OUTPUT_SRT.strip()
