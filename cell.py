class Cell:
    def __init__(self, *location, steps=0):
        # Initializes colors
        self.empty_color = "gray"
        self.wall_color = "black"
        self.seen_color = "cyan"
        self.solution_color = "orange"
        self.start_color = "lightGreen"
        self.end_color = "darkGreen"
        self.current_color = self.empty_color
        self.location = location
        self.parent = None
        self.value = None  # for greedy best first search and A*
        self.steps = steps  # steps it took to get to the cell for A* search
        # Initializes variables
        self.is_end = False
        self.is_start = False
        self.is_wall = False  # true if wall, false if empty
        self.is_seen = False

    def make_wall(self):
        """converts cell to a wall cell"""
        self.current_color = self.wall_color
        self.is_wall = True
        self.is_start = False
        self.is_end = False

    def make_empty(self):
        """converts cell to an empty cell"""
        self.current_color = self.empty_color
        self.is_wall = False
        self.is_start = False
        self.is_end = False

    def make_seen(self):
        """converts cell to a seen cell"""
        self.current_color = self.seen_color
        self.is_seen = True

    def make_start(self):
        """converts cell to a start cell"""
        self.current_color = self.start_color
        self.is_start = True
        self.is_end = False
        self.is_wall = False

    def make_end(self):
        """converts cell to an end cell"""
        self.current_color = self.end_color
        self.is_end = True
        self.is_start = False
        self.is_wall = False

    def make_solution(self):
        """converts cell to a solution cell"""
        self.current_color = self.solution_color
