from . import graph

def load_graphs():
    lines = graph.load_text_lines_from_file('../test_data.txt')
    children, parents = graph.text_lines_to_graphs(lines)
    return children, parents

def test_children():
    children, _ = load_graphs()

    assert children == {
            'A': set(['C']),
            'F': set(['C']),
            'C': set(),
            'D': set(['A']),
            'B': set(['A']),
            'E': set(['B', 'D', 'F']),}

def test_parents():
    _, parents = load_graphs()

    assert parents == {
            'A': set(['B', 'D']),
            'B': set(['E']),
            'C': set(['A', 'F']),
            'D': set(['E']),
            'E': set(),
            'F': set(['E']),}


def test_nodes_for_resolvability():
    children, _ = load_graphs()

    # Only one node resolvable, because no parents
    assert graph.check_nodes_for_resolvability(
        children.keys(),
        children,
        set(),) == set(['C'])

    # Some of the checked nodes have fully resolved parents
    assert graph.check_nodes_for_resolvability(
        set(['A', 'F', 'D', 'B']),
        children,
        set(['C']),) == set(['A', 'F'])

    # Do not repeat nodes
    assert graph.check_nodes_for_resolvability(
        set(['C']),
        children,
        set(['C']),) == set()

    assert graph.check_nodes_for_resolvability(
        set(['A', 'F', 'B']),
        children,
        set(['C', 'A']),) == set(['F', 'B'])

    # None of the checked nodes have fully resolved parents
    assert graph.check_nodes_for_resolvability(
        set(['A', 'F', 'D', 'B']),
        children,
        set(),) == set()


def test_full_run():
    assert graph.part_1("../test_data.txt") == 'CABDFE'
