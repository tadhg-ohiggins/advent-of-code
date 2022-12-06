from toolz import sliding_window

TEST_ANSWERS = (7, 19)
PUZZLE_ANSWERS = (1582, 3588)


def find_end_of_start(data, size):
    def find_first_heterogenous(sequences):
        return "".join(next(s for s in sequences if len(set(s)) == size))

    start = find_first_heterogenous(sliding_window(size, data))
    return size + data.index(start)


preprocess = str.strip


def part_one(data):
    return find_end_of_start(data, 4)


def part_two(data):
    return find_end_of_start(data, 14)
