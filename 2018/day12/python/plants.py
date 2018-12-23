import re

import numpy as np

INSTRUCTION_RE = re.compile(r'(.*) => (.)')
CHARACTERS = {'.': 0, '#': 1}


def load_initial_state_and_instructions_from_file(filename):
    with open(filename) as f:
        lines = f.read().split('\n')[:-1]
    instructions = parse_instructions(lines[2:])
    initial_state = parse_initial_state(lines[0].split(': ')[1])
    return initial_state, instructions


def parse_initial_state(text):
    return set([idx for idx, char in enumerate(text) if char == '#'])


def parse_instructions(instructions_lines: str) -> set:
    instructions = set()
    for line in instructions_lines:
        state_text, result_text = INSTRUCTION_RE.match(line).groups()
        state = state_text_to_int(state_text)
        result = CHARACTERS[result_text]
        if result == 1:
            instructions.add(state)
    return instructions


def state_text_to_int(text):
    result = 0
    for b, char in enumerate(text[::-1]):
        if char == '#':
            result += 1 << b
    return result


def get_next_state(
        state_input: set,
        instructions: set,):
    """Get the next state, given an input state and instruction set.

    Args:
        state: Pots with plants in them.
        instructions: Maps five-plant arrangement to 1 for plant, 0 for no
            plant.
    """
    state_output = set()
    pot_min = min(state_input)
    pot_max = max(state_input)
    for pot in range(pot_min - 2, pot_max + 3):
        val = sum(
            1 << b for b, neighbor in enumerate(range(pot + 2, pot - 3, -1))
            if neighbor in state_input)
        if val in instructions:
            state_output.add(pot)
    return state_output


def part_1(filename="../data.txt", steps=20):
    state, instructions = load_initial_state_and_instructions_from_file(
        filename)
    for _ in range(steps):
        state = get_next_state(state, instructions)
    return sum(state)


def part_2():
    """Return the answer to part 2.

    We were unable to get get_next_state performant enough to generate the
    correct answer at 50 billion steps. However, by inspecting the result for
    500, 5,000, 50,000, and 500,000 steps, we noticed a pattern: the result
    was always
        19 0..0 384
    where the number of zeros is equal to the number of steps divided by
    500.
    """
    return 1900000000384
