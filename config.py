from dataclasses import dataclass

MINUTE, SECOND = 60_000, 1_000

@dataclass
class Timing:
    at: int
    offset: int

    @property
    def time(self): return self.at + self.offset

def every(interval, start=0, end=64*MINUTE, offset=-20*SECOND):
    assert interval + start + end > 1000, 'Forgot the unit? (*MINUTE, *SECOND)'
    return [Timing(t, offset) for t in range(start, end, interval)]

def at(time, offset=-20*SECOND):
    assert time == 0 or time*time > 1000, 'Forgot the unit? (*MINUTE, *SECOND)'
    return [Timing(time, offset)]

CONFIG = {
    'audio_folder': 'audios',
    'interval_between_conflicts':  2 * SECOND,
    # 'precursor_percent':           10,
    'default_offset':          20 * SECOND,
    'random_humanizer_factor':     0.8,  # 0 is full random, 1 never repeats sounds (unless not enough sounds)
}

TIMINGS = {
    'game_start'     : at(-30*SECOND, offset=0) + at(33*MINUTE, offset=0),
    'bounty_runes'   : every(5*MINUTE,       start=5*MINUTE),
    'mid_runes'      : every(2*MINUTE,       start=4*MINUTE,       end=12*MINUTE),
    'outpost_xp'     : every(10*MINUTE,      start=10*MINUTE,      offset=-40*SECOND),
    'tome'           : every(10*MINUTE,      start=10*MINUTE,      offset=+5*SECOND),
    'wards_respawn'  : every((135*2)*SECOND, start=135*2*SECOND,   offset=+5*SECOND),
    'neutral_items_1': at(7*MINUTE),
    'neutral_items_2': at(17*MINUTE),
    'neutral_items_3': at(27*MINUTE),
    'neutral_items_4': at(37*MINUTE),
    'neutral_items_5': at(60*MINUTE),
}
