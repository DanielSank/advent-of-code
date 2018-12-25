## README

Test data files `test_data_part_1.txt` and `test_data_part_2.txt` are taken directly from the puzzle.
The file `test_data_part_2a.txt` is a modification of `test_data_part_2.txt` where we test for two things that are missing from the test provided by the puzzle:

1. Three-body collisions.
2. We make sure the case of `>--<` is properly handled as a collision after two steps. If all carts were moved simultaneously before checking for collision, we would not detect a collision here, because we'd get
    ```
    >--<
    -><-
    -<>-
    <-->
    ```
