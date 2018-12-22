import powergrid


def test_compute_power():
    assert powergrid.compute_power(122, 79, 57) == -5
    assert powergrid.compute_power(217, 196, 39) == 0
    assert powergrid.compute_power(101, 153, 71) == 4


def test_part_1():
    # The examples
    assert powergrid.part_1(serial=18) == (33, 45)
    assert powergrid.part_1(serial=42) == (21, 61)
    # The real puzzle
    assert powergrid.part_1(serial=1308) == (21, 41)


def test_part_2():
    # The examples
    assert powergrid.part_2(serial=18) == (90, 269, 16)
    assert powergrid.part_2(serial=42) == (232, 251, 12)
    # The real puzzle
    assert powergrid.part_2(serial=1308) == (227, 199, 19)
