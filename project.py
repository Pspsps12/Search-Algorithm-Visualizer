import algorithms
from cell import Cell
import pygame
import sys


FPS = 120  # The program will look at _ cells per second

# Creating window size
WINDOW_SIZE_X = 1000  # px
WINDOWS_SIZE_Y = 700  # px
BACKGROUND_COLOR = (200, 200, 200)
# border
BORDER_WIDTH = 20  # px

# Initializes pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOWS_SIZE_Y))
clock = pygame.time.Clock()

# Creating a grid
GRID_SIZE_X = 30
GRID_SIZE_Y = 30
grid = [
    [Cell(column, row) for column in range(GRID_SIZE_X)] for row in range(GRID_SIZE_Y)
]
GRID_CELL_DIMENSIONS = (WINDOWS_SIZE_Y - (2 * BORDER_WIDTH)) / GRID_SIZE_Y
GRID_ORIGIN = (
    WINDOW_SIZE_X - BORDER_WIDTH - GRID_SIZE_X * GRID_CELL_DIMENSIONS,
    BORDER_WIDTH,
)

# Creates default start and end positions
grid[0][len(grid[0]) - 1].make_end()
grid[len(grid) - 1][0].make_start()

# initializes font
font = pygame.font.SysFont("Ariel", 30)
# creating algorithms buttons
algorithms_buttons = {
    "breadth_first_search": {
        "text": font.render("breath first search", True, (0, 0, 0)),
        "location": (BORDER_WIDTH, 100 + BORDER_WIDTH),  # (x,y)
        "width": 250,
        "height": 40,
        "color": (150, 150, 150),
        "algorithm": algorithms.breadth_first_search,
    },
    "depth_first_search": {
        "text": font.render("depth first search", True, (0, 0, 0)),
        "location": (BORDER_WIDTH, 200 + BORDER_WIDTH),  # (x,y)
        "width": 250,
        "height": 40,
        "color": (150, 150, 150),
        "algorithm": algorithms.depth_first_search,
    },
    "greedy_best_first_search": {
        "text": font.render("greedy best first search", True, (0, 0, 0)),
        "location": (BORDER_WIDTH, 300 + BORDER_WIDTH),  # (x,y)
        "width": 250,
        "height": 40,
        "color": (150, 150, 150),
        "algorithm": algorithms.greedy_best_first_search,
    },
    "a_star_search": {
        "text": font.render("a star search", True, (0, 0, 0)),
        "location": (BORDER_WIDTH, 400 + BORDER_WIDTH),  # (x,y)
        "width": 250,
        "height": 40,
        "color": (150, 150, 150),
        "algorithm": algorithms.a_star_search,
    },
}


def main():
    # General variables
    mouse_down = False
    mouse_location_cell_is_wall = None
    working_algorithm = None
    algorithm_move_every___number_of_frames = 1
    frame_counter = 0
    grid_needs_reset = False
    solution_length = None
    moves_count = 0

    while True:
        # draws window
        draw_window(moves_count, solution_length)
        clock.tick(FPS)
        if working_algorithm is None:
            for event in pygame.event.get():
                # checks if window is closed
                if event.type == pygame.QUIT:
                    sys.exit()

                # checks if mouse is not pressed
                if event.type == pygame.MOUSEBUTTONUP:
                    # resets cell type
                    mouse_location_cell_is_wall = None
                    # reset mouse
                    mouse_down = False

                # checks if mouse is held down
                if mouse_down and event.type == pygame.MOUSEMOTION:
                    # does the grid needs a reset after the algorithm ran
                    if grid_needs_reset:
                        reset_grid(grid)
                        grid_needs_reset = False

                    # checks which cell the mouse is on
                    cell = is_on_square(*pygame.mouse.get_pos())
                    # If mouse is on a cell
                    if cell is not None:
                        # if a cell type isn't already saved
                        if mouse_location_cell_is_wall is None:
                            # saves the cell type
                            mouse_location_cell_is_wall = cell.is_wall

                        # change a cell to the first clicked cell type (saved cell)
                        change_cell_to_wall_or_to_empty(
                            cell, mouse_location_cell_is_wall
                        )

                # checks if mouse is pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # does the grid needs a reset after the algorithm ran
                    if grid_needs_reset:
                        reset_grid(grid)
                        grid_needs_reset = False

                    mouse_down = True
                    # checks which cell the mouse is on
                    cell = is_on_square(*pygame.mouse.get_pos())
                    # If mouse is on a cell
                    if cell is not None:
                        # saves first cell type
                        mouse_location_cell_is_wall = cell.is_wall
                        # change a cell to the first clicked cell type (saved cell)
                        change_cell_to_wall_or_to_empty(
                            cell, mouse_location_cell_is_wall
                        )

                    else:
                        # checks if a button is pressed
                        working_algorithm = is_on_algorithm_button(
                            *pygame.mouse.get_pos()
                        )

                        # if an algorithm is chosen, initialize it
                        if working_algorithm is not None:
                            working_algorithm = working_algorithm(grid)

                            # resets mouse
                            mouse_down = False

        # if working algorithm is not None
        else:
            if frame_counter > algorithm_move_every___number_of_frames:
                frame_counter = 0

                # gets algorithm's move count
                moves_count = working_algorithm.get_move_count()

                # performs a move and checks if the algorithm stopped
                if (solution_length := working_algorithm.perform_step()) is not None:

                    grid_needs_reset = True
                    working_algorithm = None

                    # resets the input back to normal
                    pygame.event.get()

            frame_counter += 1
    pygame.quit()  # quit pygame after closing window


def is_on_square(x, y):
    x -= GRID_ORIGIN[0]
    y -= GRID_ORIGIN[1]

    # checks if mouse in on any of the squares
    if not (0 < x < GRID_SIZE_X * GRID_CELL_DIMENSIONS) or not (
        0 < y < GRID_SIZE_Y * GRID_CELL_DIMENSIONS
    ):
        return None

    # returns the cell in (x, y) location
    return grid[int(y // GRID_CELL_DIMENSIONS)][int(x // GRID_CELL_DIMENSIONS)]


def is_on_algorithm_button(x, y):
    """checks if the x, y location is on an algorithm button,
    if so, it hides all of the buttons and returns the button algorithm"""
    # loops over all buttons
    for b in algorithms_buttons.values():
        # checks if the location is on an algorithm button
        if (
            b["location"][0] < x < (b["location"][0] + b["width"])
            and b["location"][1] < y < b["location"][1] + b["height"]
        ):
            # returns the algorithm
            return b["algorithm"]


def change_cell_to_wall_or_to_empty(cell, is_wall):
    if not cell.is_start and not cell.is_end:
        if is_wall:
            cell.make_empty()
        else:
            cell.make_wall()


def draw_window(moves_count, solution_length):
    """Draws the maze to the screen"""
    # draws background
    screen.fill(BACKGROUND_COLOR)

    # draws grid
    for row_index in range(len(grid)):
        for column_index in range(len(grid[0])):
            y = GRID_ORIGIN[1] + row_index * GRID_CELL_DIMENSIONS
            x = GRID_ORIGIN[0] + column_index * GRID_CELL_DIMENSIONS
            # creates a rectangle for the cell
            rect = pygame.Rect(x, y, GRID_CELL_DIMENSIONS, GRID_CELL_DIMENSIONS)
            # places the rectangle on the screen
            pygame.draw.rect(screen, grid[row_index][column_index].current_color, rect)

    # draws buttons
    for b in algorithms_buttons.values():
        # draws button
        pygame.draw.rect(
            screen,
            b["color"],
            pygame.Rect(b["location"][0], b["location"][1], b["width"], b["height"]),
        )
        # draws text
        screen.blit(b["text"], (b["location"][0] + 10, b["location"][1] + 10))

    # displays solution length

    screen.blit(
        font.render("moves count: " + str(moves_count), True, (0, 0, 0)),
        (BORDER_WIDTH, WINDOWS_SIZE_Y - BORDER_WIDTH - 60),
    )
    screen.blit(
        font.render("solution length: " + str(solution_length), True, (0, 0, 0)),
        (BORDER_WIDTH, WINDOWS_SIZE_Y - BORDER_WIDTH - 10),
    )

    # updates screen
    pygame.display.update()


def reset_grid(grid):
    """resets cells to their value prior to algorithm running"""
    for row in grid:
        for cell in row:
            if cell.is_start:
                cell.__init__(*cell.location)
                cell.make_start()
            elif cell.is_end:
                cell.__init__(*cell.location)
                cell.make_end()
            elif cell.is_wall:
                cell.__init__(*cell.location)
                cell.make_wall()
            else:
                cell.__init__(*cell.location)


if __name__ == "__main__":
    main()
