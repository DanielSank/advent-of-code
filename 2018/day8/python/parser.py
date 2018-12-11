def load_file_as_list_of_numbers(filename):
    with open(filename) as f:
        text = f.read()
    text = text[:-1]  # Remove trailing newline
    return [int(x) for x in text.split(' ')]


def parse_node_for_part_1(data, idx):
    subnodes = data[idx]
    metadatas = data[idx + 1]
    idx = idx + 2

    metadata_sum = 0
    for _ in range(subnodes):
        idx, subnode_sum = parse_node_for_part_1(data, idx)
        metadata_sum = metadata_sum + subnode_sum

    for _ in range(metadatas):
        metadata_sum = metadata_sum + data[idx]
        idx = idx + 1

    return idx, metadata_sum


def part_1(filename):
    return parse_node_for_part_1(
        load_file_as_list_of_numbers(filename),
        0,)


def node_value(data, idx):
    """Return the node's value and the next index to look at."""
    num_subnodes = data[idx]
    num_metadatas = data[idx + 1]
    idx = idx + 2

    if num_subnodes == 0:
        value = sum(data[idx + incr] for incr in range(num_metadatas))
        return idx + num_metadatas, value

    subnode_values = []
    for _ in range(num_subnodes):
        idx, value = node_value(data, idx)
        subnode_values.append(value)

    value = sum(
        subnode_values[snidx - 1]
        for snidx in data[idx:idx+num_metadatas]
        if (snidx <= len(subnode_values) and
            snidx >= 1))

    return idx + num_metadatas, value


def part_2(filename):
    numbers = load_file_as_list_of_numbers(filename)
    return node_value(numbers, 0)
