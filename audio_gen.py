#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.effects import normalize
from pprint import pprint
import glob
import random
from dataclasses import dataclass
from itertools import zip_longest
from collections import Counter


MINUTE, SECOND = 60_000, 1_000


def main(seed=None):
    seed = seed or random.randint(100, 999)
    random.seed(seed)
    structure = make_structure()
    print('Structure ready, will write:')
    pprint(Counter(p.sound.type for p in structure))
    print('\ncompiling...\n')
    audio = compile(structure)
    filename = f'out-{seed}.ogg'
    print(f'exporting {filename}')
    audio.export(f'out/{filename}', 'ogg')
    # breakpoint()

def compile(structure):
    output = AudioSegment.empty()
    output = []
    cursor = -1 * MINUTE
    for play in structure:
        output = output.append(AudioSegment.silent(play.begin - cursor), crossfade=0)
        print(f'added {(play.begin - cursor) // 1000} seconds of silence')
        output = output.append(play.sound.audio, crossfade=3)
        print(play)
        cursor = play.end
    return output

def make_structure():
    structure = []
    for sound, times in TIMINGS.items():
        structure += [Play(Sound(sound), end=time) for time in times]
    structure = sorted(structure, key=lambda play: play.end)

    from collections import defaultdict
    conflicts = defaultdict(list)
    for play in structure:
        play.end -= CONFIG['precursor_absolute']
        conflicts[play.end].append(play)
    for conflict in conflicts.values():
        last_begin = None
        for i in conflict:
            if last_begin is not None:
                i.end = last_begin - CONFIG['interval_between_conflicts'] # play this before
            last_begin = i.begin

    return sorted(structure, key=lambda play: play.end)

@dataclass
class Sound:
    file: str
    type: str

    def __init__(self, type):
        files = glob.glob(f'audios/{type}/*')
        self.type = type
        self.file = random.choice(files) if files else 'audios/placeholder.ogg'
        self.audio = AudioSegment.from_file(self.file, self.file.split('.')[1])
        self.audio = normalize(self.audio)

@dataclass
class Play:
    sound: Sound
    end: int # ms

    @property
    def begin(s): return s.end - len(s.sound.audio)

    def __repr__(self):
        def time(ms):
            s = ms // 1000
            sign = 1 if s >= 0 else -1
            addon = 1 if s < 0 else 0
            return f'{ (s//60)+addon :02.0f}:{ (sign*s)%60 :02.0f} - {ms}'
        return f'Play(sound={self.sound!r}, times: {time(self.begin)} => {time(self.end)}'

def every(mins, start=0, end=64):
    return list(range(start*MINUTE, end*MINUTE, int(mins*MINUTE)))

def at(mins, exact=False):
    return [mins*MINUTE + (CONFIG['precursor_absolute'] if exact else 0)]

CONFIG = {
    'interval_between_conflicts': 2 * SECOND,
    'precursor_percent': 10,
    'precursor_absolute': 20 * SECOND
}

TIMINGS = {
    'bounty_runes' : every(5, start=5),
    'game_start' : at(0, exact=True) + at(33, exact=True),
    'mid_runes' : every(2, start=4, end=12),
    'outpost_xp' : every(10, start=10),
    'wards_respawn' : every(270 / 60),
    'tome' : every(10),
    'neutral_items_1': at(7),
    'neutral_items_2': at(17),
    'neutral_items_3': at(27),
    'neutral_items_4': at(37),
    'neutral_items_5': at(60),
}

if __name__ == '__main__':
    main()
