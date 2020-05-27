#!/usr/bin/env python3

from pydub import AudioSegment
from pprint import pprint
import glob
import random
from dataclasses import dataclass
from itertools import zip_longest


MINUTE, SECOND = 60_000, 1_000


def main(seed=None):
    seed = seed or random.randint(100, 999)
    random.seed(seed)
    structure = make_structure()
    pprint(structure)
    print('\ncompiling...\n')
    audio = compile(structure)
    filename = f'out-{seed}.mp3'
    print(f'exporting {filename}')
    audio.export(f'out/{filename}', 'mp3')
    breakpoint()

def compile(structure):
    output = AudioSegment.empty()
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

    # TODO: rewrite conflict solving to resolve
    from collections import defaultdict
    conflict = defaultdict(list)
    for play in structure:
        play.end -= CONFIG['precursor_absolute']
        conflict[play.end].append(play)

    def solve_conflict(substructure):
        last_begin = None
        for i in substructure:
            if last_begin is not None:
                i.end = last_begin - CONFIG['interval_between_conflicts'] # play this before
            last_begin = i.begin

    for s in conflict.values():
        solve_conflict(s)

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
    return list(range(start*MINUTE, end*MINUTE, mins*MINUTE))

def at(mins, exact=False):
    return [mins*MINUTE + (CONFIG['precursor_absolute'] if exact else 0)]

CONFIG = {
    'interval_between_conflicts': 2 * SECOND,
    'precursor_percent': 10,
    'precursor_absolute': 20 * SECOND
}

TIMINGS = {
    'bounty_runes' : every(5, start=5),
    'game_start' : at(0, exact=True),
    'mid_runes' : every(2, start=4, end=12),
    'outpost_xp' : every(10, start=10),
    # 'wards_respawn' : 
    # 'tome' : 
    'neutral_items_1': at(7),
    'neutral_items_2': at(17),
    'neutral_items_3': at(27),
    'neutral_items_4': at(37),
    'neutral_items_5': at(60),
}

if __name__ == '__main__':
    main()
