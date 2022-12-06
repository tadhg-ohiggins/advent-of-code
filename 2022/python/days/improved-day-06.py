from toolz import sliding_window

TEST_ANSWERS = (7, 19)
PUZZLE_ANSWERS = (1582, 3588)


def find_first_unique(sequences):
    return "".join(next(s for s in sequences if len(set(s)) == len(s)))


def preprocess(data):
    return data.strip()


def part_one(data):
    windows = sliding_window(4, data)
    return 4 + data.index(find_first_unique(windows))


def part_two(data):
    windows = sliding_window(14, data)
    return 14 + data.index(find_first_unique(windows))
