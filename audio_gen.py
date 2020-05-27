#!/usr/bin/env python3

from pydub import AudioSegment
from pprint import pprint
import glob
import random
from dataclasses import dataclass
from itertools import zip_longest

random.seed(42)

MINUTE, SECOND = 60_000, 1_000


def main():
    structure = make_structure()
    pprint(structure)
    return
    audio = compile(structure)
    canvas = AudioSegment.silent(MINUTE * 65)
    canvas = canvas.overlay(sound, position)
    canvas

def make_structure():
    structure = []
    for sound, times in TIMINGS.items():
        sound = Sound(sound)
        structure += [Play(sound, end=time) for time in times]
    structure = sorted(structure, key=lambda play: play.end)

    for play, last_play in zip_longest(structure, [None] + structure):
        play.end -= CONFIG['precursor_absolute']
        if last_play and last_play.begin <= play.end <= last_play.end:
            play.end = last_play.begin - CONFIG['interval_between_conflicts']

    return structure

@dataclass
class Sound:
    file: str
    type: str

    def __init__(self, type):
        files = glob.glob(f'audio/{type}/*')
        self.type = type
        self.file = random.choice(files) if files else 'audios/placeholder.ogg'
        self.audio = AudioSegment.from_file(self.file, self.file.split('.')[1])

@dataclass
class Play:
    sound: Sound
    end: float

    @property
    def begin(s): return s.end - (len(s.sound.audio) / MINUTE)

def every(mins, start=0, end=70):
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

main()
