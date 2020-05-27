import audio_gen

def test_structure():
    structure = audio_gen.make_structure()
    assert len(structure) == 29

    for type in audio_gen.TIMINGS.keys():
        assert type in (p.sound.type for p in structure)
