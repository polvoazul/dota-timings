MINUTE, SECOND = 60_000, 1_000

def every(mins, start=0, end=64):
    return list(range(start*MINUTE, end*MINUTE, int(mins*MINUTE)))

def at(mins, exact=False):
    return [mins*MINUTE + (CONFIG['precursor_absolute'] if exact else 0)]

CONFIG = {
    'interval_between_conflicts':  2 * SECOND,
    # 'precursor_percent':           10,
    'precursor_absolute':          20 * SECOND,
    'random_humanizer_factor':     0.8,  # 0 is full random, 1 never repeats sounds (unless not enough sounds)
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
