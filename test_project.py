import project
from project import is_on_square, change_cell_to_wall_or_to_empty, reset_grid


def main():
    test_is_on_square()
    test_change_cell_to_wall_or_to_empty()
    test_reset_grid()


def test_is_on_square():
    # if location is on first square, return first square
    assert (
        is_on_square(
            project.GRID_ORIGIN[0] + project.GRID_CELL_DIMENSIONS / 2,
            project.GRID_ORIGIN[1] + project.GRID_CELL_DIMENSIONS / 2,
        )
        == project.grid[0][0]
    )

    # if location is on last square, return last square
    assert (
        is_on_square(
            project.GRID_ORIGIN[0]
            + project.GRID_SIZE_X * project.GRID_CELL_DIMENSIONS
            - project.GRID_CELL_DIMENSIONS / 2,
            project.GRID_ORIGIN[1]
            + project.GRID_SIZE_Y * project.GRID_CELL_DIMENSIONS
            - project.GRID_CELL_DIMENSIONS / 2,
        )
        == project.grid[-1][-1]
    )


def test_change_cell_to_wall_or_to_empty():
    # create an empty cell
    cell = project.Cell(0, 0)

    # make sure that the cell is empty
    assert not cell.is_wall

    # convert cell to wall
    change_cell_to_wall_or_to_empty(cell, cell.is_wall)

    # checks if hte cell was changed to wall
    assert cell.is_wall

    # change cell back to empty
    change_cell_to_wall_or_to_empty(cell, cell.is_wall)

    # checks of the cell was changed to a wall
    assert not cell.is_wall


def test_reset_grid():
    # creates a 3x3 test grid
    grid = []
    for y in range(3):
        grid.append([])
        for x in range(3):
            grid[y].append(project.Cell(x, y))

    # sets first cell as start
    grid[0][0].make_start()

    # sets last grid as end
    grid[-1][-1].make_end()

    # makes some cells walls:
    # first row, last cell
    grid[0][-1].make_wall()
    # middle row, middle cell
    grid[1][1].make_wall()

    # make a cells seen
    grid[1][0].make_seen()

    # makes a cell solution
    grid[2][0].make_solution()

    # calls reset grid function
    reset_grid(grid)

    # checks that the start is still a start
    assert grid[0][0].is_start

    # checks that the last cell is still an end cell
    assert grid[-1][-1].is_end

    # checks that all wall cells are still walls
    # first row, last cell
    assert grid[0][-1].is_wall
    # middle row, middle cell
    assert grid[1][1].is_wall

    # checks that en empty cells remains empty
    assert not grid[0][1].is_wall

    # checks that a seen cell is now empty
    assert not grid[1][0].is_wall

    # checks that a solution cell is not empty
    assert not grid[2][0].is_wall


if __name__ == "__main__":
    main()
