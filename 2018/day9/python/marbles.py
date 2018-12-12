import itertools


class Node:
    """A single node in a linked list."""

    def __init__(self, value, back=None, forward=None):
        self.value = value
        self.back = back
        self.forward = forward

    def insert_after(self, node):
        temp = self.forward
        self.forward = node
        node.back = self
        node.forward = temp
        temp.back = node

    def insert_before(self, node):
        temp = self.back
        temp.forward = node
        node.back = temp
        node.forward = self
        self.back = node

    def pop(self):
        self.back.forward = self.forward
        self.forward.back = self.back
        return self

    @staticmethod
    def as_str(node, current=0):
        next_node = node
        msg = ''
        while 1:
            if next_node == current:
                msg = msg + "({})".format(next_node.value).ljust(4)
            else:
                msg = msg + "{}".format(next_node.value).ljust(4)
            next_node = next_node.forward
            if next_node == node:
                break
        return msg


def pool():
    i = 0
    while 1:
        yield Node(i)
        i = i + 1


def run_game_nodes(num_players, final_marble_value, noisy=False):
    marble_pool = pool()
    zero_marble = next(marble_pool)

    current_marble = zero_marble
    current_marble.forward = current_marble
    current_marble.back = current_marble

    scores = {}
    max_score = -1

    for player in itertools.cycle(range(num_players)):
        player = player + 1  # Players are 1-indexed
        new_marble = next(marble_pool)
        if (new_marble.value % 23 == 0) and (new_marble.value != 0):
            for _ in range(7):
                current_marble = current_marble.back
            popped = current_marble.pop()
            current_marble = popped.forward
            new_score = scores.get(player, 0) + (
                    popped.value +
                    new_marble.value)
            scores[player] = new_score
            if new_score > max_score:
                max_score = new_score
        else:
            current_marble.forward.insert_after(new_marble)
            current_marble = new_marble

        if noisy:
            msg = '[{}]  '.format(player) + Node.as_str(
                zero_marble, current_marble)
            print(msg)

        if new_marble.value == final_marble_value:
            break

    return scores, max_score


def part_1(num_players, final_marble_value, noisy=False):
    _, max_score = run_game_nodes(
        num_players,
        final_marble_value,
        noisy=noisy,)
    return max_score
