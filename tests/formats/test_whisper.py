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
