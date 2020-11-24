import heapq
import collections
import pygame
import time
import random

"""
TODO: Implement more maze variations and solving algorithms.
TODO: Add graphical start and end with click.
"""

# Colours
WHITE = (255, 255, 255)
GREEN = (166, 243, 22)
BLUE = (95, 129, 157)
YELLOW = (243, 210, 22)
RED = (165, 66, 66)


class Maze(object):
    """
    create_grid -> Returns List of (x,y)
    FIX: Fork Cell are skeeped from final backpath. Reason beening
    they are poped from the stack at path direction change at some point and like
    that not part of the final stack
    """
    def __init__(self, i=20, j=20):
        self.i = i
        self.j = j
        self.width = 40
        self.wall = 1
        self.valid_moves = collections.defaultdict(list)
        self.grid = []

    def init_screen(self):
        window_width = self.width * self.i + self.wall
        window_height = self.width * self.j + self.wall
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Maze")

    def create_grid(self):
        """
        Draw the lines of the graphical grid.
        Save the top-left as x,y or the Cell in the grid list
        Carve the Maze
        """
        self.init_screen()
        w = self.width
        wall = self.wall
        for i in range(0, self.i):
            y = i * w
            for j in range(0, self.j):
                x = j * w
                # Top, Right, Bottom, Left
                pygame.draw.line(self.screen, WHITE, [x, y], [x + w, y], wall)
                pygame.draw.line(self.screen, WHITE, [x + w, y], [x + w, y + w], wall)
                pygame.draw.line(self.screen, WHITE, [x + w, y + w], [x, y + w], wall)
                pygame.draw.line(self.screen, WHITE, [x, y + w], [x, y], wall)
                self.grid.append((x, y))
        return self.grid

    def carve_out_maze(self):
        w = self.width
        grid = self.grid
        valid_moves = self.valid_moves

        visited = []
        stack = []

        # Init, add to Start and Visited
        (x, y) = start = grid[0]
        stack.append(start)
        visited.append(start)

        # Loop till stack is empty
        while len(stack):
            # Det. for the current cell which are not Visited in the Grid cells
            adj = []
            self.current_cell(x, y)
            if (x + w, y) not in visited and (x + w, y) in grid:
                adj.append("right")

            if (x - w, y) not in visited and (x - w, y) in grid:
                adj.append("left")

            if (x, y + w) not in visited and (x, y + w) in grid:
                adj.append("down")

            if (x, y - w) not in visited and (x, y - w) in grid:
                adj.append("up")

            if len(adj):
                # Select Random Cell
                cell_chosen = random.choice(adj)
                if cell_chosen == "right":
                    self.reg_valid((x, y), (x + w, y))
                    self.push_right(x, y)
                    visited.append((x + w, y))
                    stack.append((x + w, y))
                    x = x + w

                elif cell_chosen == "left":
                    self.reg_valid((x, y), (x - w, y))
                    self.push_left(x, y)
                    visited.append((x - w, y))
                    stack.append((x - w, y))
                    x = x - w

                elif cell_chosen == "down":
                    self.reg_valid((x, y), (x, y + w))
                    self.push_down(x, y)
                    visited.append((x, y + w))
                    stack.append((x, y + w))
                    y = y + w

                elif cell_chosen == "up":
                    self.reg_valid((x, y), (x, y - w))
                    self.push_up(x, y)
                    visited.append((x, y - w))
                    stack.append((x, y - w))
                    y = y - w
            else:
                # If there are no cells to move to go back
                (x, y) = stack.pop()
        return valid_moves

    def reg_valid(self, old, new):
        """
        Register as valid moves in both directions
        """
        self.valid_moves[old].append(new)
        self.valid_moves[new].append(old)

    def push_right(self, x, y):
        w, wall, x, y, = (self.width, self.wall, x + self.wall, y + self.wall,)
        pygame.draw.rect(surface=self.screen, color=BLUE, rect=(x, y, 2 * w - wall, w - wall))
        pygame.display.update()

    def push_left(self, x, y):
        w, wall, x, y, = (self.width, self.wall, x + self.wall, y + self.wall,)
        pygame.draw.rect(self.screen, BLUE, (x - w, y, 2 * w - wall, w - wall))
        pygame.display.update()

    def push_down(self, x, y):
        w, wall, x, y, = (self.width, self.wall, x + self.wall, y + self.wall,)
        pygame.draw.rect(self.screen, BLUE, (x, y, w - wall, 2 * w - wall))
        pygame.display.update()

    def push_up(self, x, y):
        w, wall, x, y, = (self.width, self.wall, x + self.wall, y + self.wall,)
        pygame.draw.rect(self.screen, BLUE, (x, y - w, w - wall, 2 * w - wall))
        pygame.display.update()

    def current_cell(self, x, y):
        w, wall, x, y, = (self.width, self.wall, x + self.wall, y + self.wall,)
        pygame.draw.rect(self.screen, GREEN, (x, y, w - wall, w - wall))
        pygame.display.update()
        time.sleep(0.03)
        pygame.draw.rect(self.screen, BLUE, (x, y, w - wall, w - wall))
        pygame.display.update()

    def solution_cell(self, x, y):
        w = self.width
        pygame.draw.rect(self.screen, YELLOW, ((x + w/2) - 3, (y + w/2) - 3, 6, 6))
        pygame.display.update()
        time.sleep(0.05)

    def tested_cell(self, x, y):
        w = self.width
        pygame.draw.rect(self.screen, RED, ((x + w/2) - 6, (y + w/2) - 6, 12, 12))
        pygame.display.update()
        time.sleep(0.05)

    def plot_path(self, path):
        for p in path:
            (x, y) = p
            self.solution_cell(x, y)

    def plot_tested(self, path):
        for p in path:
            (x, y) = p
            self.tested_cell(x, y)


class Cell(object):
    def __init__(self, x, y, valid_moves):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.reachable = valid_moves[(self.x, self.y)]

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def __gt__(self, other):
        if (self.x < other.x) and (self.y < other.y):
            return True
        elif (self.x > other.x) and (self.y < other.y):
            return True
        else:
            return False

    def __lt__(self, other):
        if (self.x < other.x) and (self.y > other.y):
            return True
        elif (self.x > other.x) and (self.y > other.y):
            return True
        else:
            return False


class AStar(object):
    """
    g: Cost from starting cell to x cell
    h: Linear distance from start cell to end cell
    valid_moves: defaultdict with valid moves from maze carve

    For heapq
    https://github.com/python/cpython/blob/3.8/Lib/heapq.py
    https://en.wikipedia.org/wiki/List_of_algorithms#Graph_algorithms
    """

    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = []
        self.cells = []

    def init_cells(self, grid, valid_moves, start):
        for cell in grid:
            (x, y) = cell
            self.cells.append(Cell(x, y, valid_moves))
        self.start = self.get_cell(start[0], start[1])
        # Last Right-Down Cell
        self.end = self.get_cell(grid[-1][0], grid[-1][1])

    def get_cell(self, x, y):
        """
        FIX: For very big matrices this is a bad search
        """
        for cell in self.cells:
            if (cell.x == x) and (cell.y == y):
                return cell

    def get_heuristic(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def get_closed(self):
        return [(cell.x, cell.y) for cell in self.closed]

    def update_cell(self, adj, cell):
        # Add a Constannt Cost for each child
        adj.g = cell.g + 10
        # Calculate the h independent of the parent
        adj.h = self.get_heuristic(adj)
        # Make relationship
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # Get the lowest f Cell
            f, cell = heapq.heappop(self.opened)
            # Register that we have visited this Cell
            self.closed.append(cell)
            # If its the Goal Cell get the path
            if cell is self.end:
                return self.get_path()
            # Get the coordinates of the reachable cells
            for c in cell.reachable:
                # Get the actual object
                ncell = self.get_cell(c[0], c[1])
                # If we haven't visisted this cell
                if ncell not in self.closed:
                    # If Multiple Paths
                    if (ncell.f, ncell) in self.opened:
                        if ncell.g > cell.g + 10:
                            self.update_cell(ncell, cell)
                    else:
                        # Lets update all the ncells in relation to the parent
                        self.update_cell(ncell, cell)
                        # and then add it to the heap
                        heapq.heappush(self.opened, (ncell.f, ncell))


maze = Maze()
grid = maze.create_grid()
valid_moves = maze.carve_out_maze()
astar = AStar()
astar.init_cells(grid, valid_moves, start=grid[10])
path = astar.process()
tested = astar.get_closed()
maze.plot_tested(tested)
maze.plot_path(path)

# plot_route_back(WIDTH-width-self.wall, HEIGHT-width-self.wall)
# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock = pygame.time.Clock()
    clock.tick(30)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
