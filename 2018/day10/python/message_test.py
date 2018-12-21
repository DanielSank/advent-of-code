import message


def test_parse_text_line():
    parsed = message.load_file('../test_data.txt')
    assert parsed[0] == (9, 1, 0, 2)
    assert parsed[1] == (7, 0, -1, 0)
    assert parsed[2] == (3, -2, -1, 1)
    assert parsed[3] == (6, 10, -2, -1)
    assert parsed[12] == (10, -3, -1, 1)
