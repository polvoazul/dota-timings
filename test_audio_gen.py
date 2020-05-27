import audio_gen
import itertools

def test_structure():
    structure = audio_gen.make_structure()
    assert len(structure) == 28

    for type in audio_gen.TIMINGS.keys():
        assert type in (p.sound.type for p in structure)

    for p, k in itertools.combinations(structure, 2):
        assert not (k.begin <= p.begin and p.begin <= k.end)
        assert not (k.begin <= p.end and p.end <= k.end)
