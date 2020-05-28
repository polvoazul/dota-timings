#!/usr/bin/env python3

import pydub.exceptions
from pydub import AudioSegment
from pydub.effects import normalize
from pprint import pprint
import glob
import random
from dataclasses import dataclass
from itertools import zip_longest
from collections import Counter
from loguru import logger
import sys, os
from config import MINUTE, SECOND, CONFIG, TIMINGS

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{elapsed}</green> <level>{message}</level>")
log = logger.info

def main(seed=None):
    seed = seed or random.randint(100, 999)
    structure = make_structure()
    log('Structure ready, will write:')
    pprint(Counter(p.sound.type for p in structure))
    log('compiling...\n')
    audio = compile(structure)
    filename = f'out-{seed}.ogg'
    log(f'exporting {filename}')
    audio.export(f'audios/_other/out/{filename}', 'ogg')

    import shutil
    log(f'Updating public.ogg - {os.path.getsize("audios/_other/out/" + filename) // (1024):,}KB')
    shutil.copy(f'audios/_other/out/{filename}', 'audios/_other/out/public.ogg')
    log('Done')

    # breakpoint()

def compile(structure):
    output = []
    cursor = -1 * MINUTE
    for play in structure:
        output.append(AudioSegment.silent(play.begin - cursor)) 
        print(f'added {(play.begin - cursor) // 1000} seconds of silence')
        output.append(play.sound.audio)
        print(play)
        cursor = play.end
    def binary_join(a_list): # sequential append is slow on pydub, this binary join is 3x faster
        if len(a_list) == 0: return AudioSegment.empty()
        if len(a_list) == 1: return a_list[0]
        half = len(a_list)//2
        return binary_join(a_list[:half]) + binary_join(a_list[half:])
    return binary_join(output)
    # def sequential_join(a_list):
    #     return functools.reduce(lambda x, y: x+y, a_list)
    # return sequential_join(output)

def make_structure(seed=None):
    random.seed(seed)
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
class SoundType:
    TYPES = {}

    @classmethod
    def get_type(self, type_name):
        type = self.TYPES.get(type_name) or SoundType(type_name)
        self.TYPES[type_name] = type
        return type

    name: str

    def __init__(self, name):
        self.name = name
        self.files = []

    def shuffle_a_file(self):
        if random.random() > CONFIG['random_humanizer_factor'] or not self.files:
            self.files = glob.glob(f'audios/{self.name}/*') or ['audios/placeholder.ogg']
        file = random.choice(self.files)
        self.files.remove(file)
        return file

@dataclass
class Sound:
    file: str
    type: str

    def __init__(self, type):
        self.type = type
        self.file = SoundType.get_type(type).shuffle_a_file()
        try:
            self.audio = AudioSegment.from_file(self.file, self.file.split('.')[-1])
        except pydub.exceptions.CouldntDecodeError:
            print(f'ERROR: FILE {self.file} not supported')
            raise
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
            sign =  1 if s >= 0 else -1
            addon = 0 if s >= 0 else 1
            return f'{ (s//60)+addon :02.0f}:{ (sign*s)%60 :02.0f} - {ms}'
        return f'Play(sound={self.sound!r}, times: {time(self.begin)} => {time(self.end)}'

if __name__ == '__main__':
    main()
