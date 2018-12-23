import plants


def test_state_text_to_int():
    assert plants.state_text_to_int("....#") == 1
    assert plants.state_text_to_int("#...#") == 17
    assert plants.state_text_to_int(".....") == 0


def test_parse_instructions():
    assert plants.parse_instructions([
        '..... => #',
        '#.... => #',
        '..#.. => #',
        '.##.. => #',
        '....# => .',
        '..#.# => .',
    ]) == set([0, 4, 12, 16])


def test_parse_initial_state():
    assert plants.parse_initial_state('#..#.#') == set([0, 3, 5])


def test_load_initial_state_and_instructions_from_file():
    initial_state, instructions = (
        plants.load_initial_state_and_instructions_from_file(
            "../test_data.txt"))
    assert initial_state == set([0, 3, 5, 8, 9, 16, 17, 18, 22, 23, 24])
    assert instructions == set(
        [3, 4, 8, 10, 11, 12, 15, 21, 23, 26, 27, 28, 29, 30])


def test_next_state():
    initial_state, instructions = (
        plants.load_initial_state_and_instructions_from_file(
            "../test_data.txt"))
    next_state = plants.get_next_state(initial_state, instructions)
    assert next_state == set([idx for idx, char in enumerate(
        "#...#....#.....#..#..#..#...........")
        if char == "#"])


def test_part_1():
    assert plants.part_1("../data.txt", 20) == 2140


def test_part_2():
    assert plants.part_2() == 1900000000384
