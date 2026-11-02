"""Sudoku solver using backtracking."""

from time import perf_counter


def allowed(cell_grid, row_slot, col_slot, trial_digit):
    box_top, box_left = (row_slot // 3) * 3, (col_slot // 3) * 3
    return (trial_digit not in cell_grid[row_slot]
            and all(cell_grid[line][col_slot] != trial_digit
                    for line in range(9))
            and all(cell_grid[line][slot] != trial_digit
                    for line in range(box_top, box_top + 3)
                    for slot in range(box_left, box_left + 3)))


def solve(clue_grid):
    """Solve a copy of the puzzle; reject malformed or conflicting clues."""
    if len(clue_grid) != 9 or any(len(line) != 9 for line in clue_grid):
        raise ValueError("Enter nine rows of nine integers.")
    if any(type(clue) is not int or not 0 <= clue <= 9
           for line in clue_grid for clue in line):
        raise ValueError("Use integers 0-9; 0 means blank.")
    cell_grid = [line[:] for line in clue_grid]
    for row_slot in range(9):
        for col_slot in range(9):
            clue_digit = cell_grid[row_slot][col_slot]
            if clue_digit:
                cell_grid[row_slot][col_slot] = 0
                if not allowed(cell_grid, row_slot, col_slot, clue_digit):
                    raise ValueError("Duplicate clue in a row, column or box.")
                cell_grid[row_slot][col_slot] = clue_digit

    def fill_blank():
        for row_slot in range(9):
            for col_slot in range(9):
                if cell_grid[row_slot][col_slot] == 0:
                    for trial_digit in range(1, 10):
                        if allowed(cell_grid, row_slot, col_slot, trial_digit):
                            cell_grid[row_slot][col_slot] = trial_digit
                            if fill_blank():
                                return True
                            cell_grid[row_slot][col_slot] = 0
                    return False
        return True

    return cell_grid if fill_blank() else None


def main():
    print("Enter nine rows; use 0 for blanks:")
    try:
        clue_grid = [list(map(int, input(f"Row {line + 1}: ").split()))
                     for line in range(9)]
        sudoku_clock = perf_counter()
        sudoku_answer = solve(clue_grid)
        sudoku_seconds = perf_counter() - sudoku_clock
    except (ValueError, EOFError) as error:
        print(f"Invalid input: {error}")
        return
    if sudoku_answer is None:
        print("No solution.")
    else:
        print("Solution:")
        for solved_line in sudoku_answer:
            print(" ".join(map(str, solved_line)))
    print(f"Execution time: {sudoku_seconds:.6f} seconds")


if __name__ == "__main__":
    main()
