class breadth_first_search:
    def __init__(self, grid):
        self.grid = grid
        self.grid_height = len(self.grid)
        self.grid_width = len(self.grid[0])
        self.queue = []
        self.parent_cell = None
        self.end = self.get_end()
        self.moves_count = 0  # keeps truck of number of moves to complete algorithm
        # adds the starting cell to the queue
        self.add_to_queue(self.get_start())

    def get_start(self):
        for row in self.grid:
            for cell in row:
                if cell.is_start:
                    return cell

    def get_end(self):
        for row in self.grid:
            for cell in row:
                if cell.is_end:
                    return cell

    def add_to_queue(self, cell):
        """adds a cell to the end of the queue"""
        self.queue.append(cell)

    def remove_from_queue(self):
        """removes the first cell from the queue"""
        return self.queue.pop(0)

    def get_neighbors(self, cell):
        # down, left, right, up
        tests = ((-1, 0), (0, -1), (1, 0), (0, 1))
        neighbors = []
        for x, y in tests:
            if (
                0 <= cell.location[0] + x < self.grid_width
                and 0 <= cell.location[1] + y < self.grid_height
            ):
                if not self.grid[cell.location[1] + y][cell.location[0] + x].is_wall:
                    neighbors.append(
                        self.grid[cell.location[1] + y][cell.location[0] + x]
                    )
        return neighbors

    def perform_step(self):
        """looks at one square to solve the maze
        returns solution length if a solution is found
        returns 0 if no solution is possible,
        returns None if a step was made and no solution"""
        self.moves_count += 1

        # removes one cell from the queue and sets it up
        current_cell = self.remove_from_queue()
        current_cell.make_seen()

        # adding neighbors to queue
        for neighbor in self.get_neighbors(current_cell):
            if not neighbor.is_seen and neighbor not in self.queue:
                neighbor.parent = current_cell
                # adds neighbor to queue
                self.add_to_queue(neighbor)

        # checks if the cell is the end
        if current_cell.is_end:
            # keeps track of the length of solution
            solution_length = 0
            # marks all solution cells as solution
            while current_cell is not None:
                solution_length += 1
                current_cell.make_solution()
                current_cell = current_cell.parent

            return (
                solution_length - 1
            )  # starting and ending cell does not count as two moves, only one

        # if no solution is found
        if len(self.queue) == 0:
            return 0

    def get_move_count(self):
        return self.moves_count


class depth_first_search(breadth_first_search):
    def remove_from_queue(self):
        """removes the first cell from the queue"""
        return self.queue.pop(-1)


class greedy_best_first_search(breadth_first_search):
    def add_to_queue(self, cell):
        """adds cell to queue in the right location based on manhattan heuristic value"""
        # calculates cell's value based on manhattan distance
        cell.value = self.manhattan_heuristic_value(cell)

        # adds cell to its right location in queue based on ascending value
        for index in range(len(self.queue)):
            if self.queue[index].value > cell.value:
                self.queue.insert(index, cell)
                break
        else:
            self.queue.append(cell)

    def manhattan_heuristic_value(self, cell):
        return abs(self.end.location[0] - cell.location[0]) + abs(
            self.end.location[1] - cell.location[1]
        )


class a_star_search(greedy_best_first_search):
    def add_to_queue(self, cell):
        """adds cell to queue in the right location based on manhattan heuristic value"""
        # calculates parent step by subtracting the parent value by its manhattan value
        parent_steps = (
            (cell.parent.value - self.manhattan_heuristic_value(cell.parent))
            if cell.parent is not None
            else 0
        )
        # calculates cell value by manhattan value plus parent step plus one
        cell.value = self.manhattan_heuristic_value(cell) + parent_steps + 1

        # adds cell to its right location in queue based on ascending value
        for index in range(len(self.queue)):
            if self.queue[index].value > cell.value:
                self.queue.insert(index, cell)
                break
        else:
            self.queue.append(cell)
