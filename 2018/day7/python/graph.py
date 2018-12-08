import re


RE = re.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin.")


def load_text_lines_from_file(filename):
    with open(filename) as f:
        lines = f.read().split('\n')
    if lines[-1] == '':
        lines = lines[0:-1]
    return lines


def text_lines_to_graphs(lines):
    """Produce two dependency graphs from a set of text lines.

    Returns:
        dict: Maps children to parents.
        dict: Maps parents to children.
    """
    graph_children = {}
    graph_parents = {}

    for line in lines:
        parent, child = RE.match(line).groups()

        parents = graph_children.setdefault(child, set())
        parents.add(parent)
        graph_children[child] = parents

        children = graph_parents.setdefault(parent, set())
        children.add(child)
        graph_parents[parent] = children


    nodes = set(graph_children.keys())
    nodes.update(set(graph_parents.keys()))

    for node in nodes:
        if node not in graph_children:
            graph_children[node] = set()
        if node not in graph_parents:
            graph_parents[node] = set()

    return graph_children, graph_parents


def check_nodes_for_resolvability(nodes, graph, resolved_nodes):
    """Return nodes with no parents and which weren't alerady resolved"""
    return set([child for child in nodes
        if not set([parent for parent in graph[child]
            if parent not in resolved_nodes])
        and child not in resolved_nodes])


def part_1(filename):
    graph_children, graph_parents = text_lines_to_graphs(
        load_text_lines_from_file(filename))

    resolved = set([])
    answer = []

    nodes_to_check = check_nodes_for_resolvability(
        graph_children.keys(),
        graph_children,
        resolved,)

    while len(resolved) < len(graph_children):
        # Find the next alphabetical resolvable node,
        node_to_resolve = sorted(list(check_nodes_for_resolvability(
            nodes_to_check,
            graph_children,
            resolved,)))[0]
        # mark it resolved,
        resolved.add(node_to_resolve)
        # add it to the answer,
        answer.append(node_to_resolve)
        # and add its children to the set of nodes to check next.
        nodes_to_check.update(graph_parents[node_to_resolve])
    return ''.join(answer)


class Work:
    def __init__(self, node, start_time, overhead):
        self.node = node
        self.time_start = start_time
        self.overhead = overhead

    @property
    def time_required(self):
        return ord(self.node) - 64 + self.overhead

    def done(self, time):
        """Return node if done, otherwise None."""
        elapsed = time - self.time_start
        if elapsed == self.time_required:
            return self.node
        elif elapsed > self.time_required:
            raise RuntimeError("Unreachable")

    def __hash__(self):
        return ord(self.node)

    def __eq__(self, other):
        return (self.node == other.node and
                self.time_start == other.time_start and
                self.overhead == other.overhead)

    def __str__(self):
        return "Node: {}, Time start: {}".format(self.node, self.time_start)

    def __repr__(self):
        return str(self)


def part_2(filename, max_workers=5, overhead=60):
    graph_children, graph_parents = text_lines_to_graphs(
        load_text_lines_from_file(filename))

    resolved = set()

    nodes_to_check = check_nodes_for_resolvability(
        graph_children.keys(),
        graph_children,
        resolved,)
    workers = set()
    time = 0

    while len(resolved) < len(graph_children):
        for worker in frozenset(workers):
            maybe_node = worker.done(time)
            if maybe_node:
                resolved.add(maybe_node)
                workers.remove(worker)
                for child in graph_parents[maybe_node]:
                    if all(parent in resolved for parent in graph_children[child]):
                        nodes_to_check.add(child)

        nodes_to_work_on = sorted(list(nodes_to_check))
        while len(workers) < max_workers and len(nodes_to_work_on):
            node = nodes_to_work_on.pop(0)
            workers.add(Work(
                node,
                time,
                overhead,))
            nodes_to_check.remove(node)
        time = time + 1

    return time - 1
