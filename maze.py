import pygame
import time
import random
from queue import PriorityQueue

# (X,X)--------(X+W,Y)
#   |            |
#   |            |
#   |            |
#   |            |
#   |            |
# (X,Y+W)------(X+W,Y+W)

# Vars
start = 0
end = 0
width = 40
N = 6  # Number of Cells
WALL = 1

# Pygame window
WIDTH = width * N
HEIGHT = width * N
FPS = 30

# Colours
WHITE = (255, 255, 255)
GREEN = (166, 243, 22)
BLUE = (95, 129, 157)
YELLOW = (243, 210, 22)

# Init Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

# Lists used as Stacks
grid = []
visited = []
stack = []
solution = {}


# Build Grid
def create_grid(x, y, w):
    for i in range(0, N):
        y = i * w
        for j in range(0, N):
            x = j * width
            # Top
            pygame.draw.line(screen, WHITE, [x, y], [x + width, y])
            # Right
            pygame.draw.line(screen, WHITE, [x + width, y], [x + width, y + width])
            # Bottom
            pygame.draw.line(screen, WHITE, [x + width, y + width], [x, y + width])
            # Left
            pygame.draw.line(screen, WHITE, [x, y + width], [x, y])
            # Add Top/Left Coordinates as Representation of grid to grid[]
            grid.append((x, y))


# From the PyGame: draw.rect in Rect variation (left, top, width, height)
def push_right(x, y):
    x, y, = (
        x + WALL,
        y + WALL,
    )
    pygame.draw.rect(screen, BLUE, (x, y, 2 * width - WALL, width - WALL), 0)
    pygame.display.update()


def push_left(x, y):
    x, y, = (
        x + WALL,
        y + WALL,
    )
    pygame.draw.rect(screen, BLUE, (x - width, y, 2 * width - WALL, width - WALL), 0)
    pygame.display.update()


def push_down(x, y):
    x, y, = (
        x + WALL,
        y + WALL,
    )
    pygame.draw.rect(screen, BLUE, (x, y, width - WALL, 2 * width - WALL), 0)
    pygame.display.update()


def push_up(x, y):
    x, y, = (
        x + WALL,
        y + WALL,
    )
    pygame.draw.rect(screen, BLUE, (x, y - width, width - WALL, 2 * width - WALL), 0)
    pygame.display.update()


def single_cell(x, y):
    x, y, = (
        x + WALL,
        y + WALL,
    )
    pygame.draw.rect(screen, GREEN, (x, y, width - 2 * WALL, width - 2 * WALL), 0)
    pygame.display.update()


def backtracking_cell(x, y):
    x, y, = (
        x + WALL,
        y + WALL,
    )
    pygame.draw.rect(screen, BLUE, (x, y, width - 2 * WALL, width - 2 * WALL), 0)
    pygame.display.update()


def solution_cell(x, y):
    pygame.draw.rect(screen, YELLOW, ((x + width/2), (y + width/2), 5, 5), 0)
    pygame.display.update()


def carve_out_maze(x, y):
    # Init, add to Start and Visited
    stack.append((x, y))
    visited.append((x, y))
    # Show Init Position
    single_cell(x, y)

    # Loop till stack is empty
    while len(stack) > 0:
        time.sleep(0.03)

        # Det. for the current cell which are the posible next cell to moves too
        cell = []
        if (x + width, y) not in visited and (x + width, y) in grid:
            cell.append("right")

        if (x - width, y) not in visited and (x - width, y) in grid:
            cell.append("left")

        if (x, y + width) not in visited and (x, y + width) in grid:
            cell.append("down")

        if (x, y - width) not in visited and (x, y - width) in grid:
            cell.append("up")

        # If there are possible cells to move too choose one randomly
        if len(cell) > 0:
            # Select Random Cell
            cell_chosen = random.choice(cell)

            if cell_chosen == "right":
                # Move Grafically
                push_right(x, y)
                solution[(x + width, y)] = (x, y)
                #  Make New Current
                x = x + width
                # Add to Visit and Stack
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - width, y)] = x, y
                x = x - width
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x, y + width)] = x, y
                y = y + width
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x, y - width)] = x, y
                y = y - width
                visited.append((x, y))
                stack.append((x, y))
        else:
            # If there are no cells to move too go back on the stack
            (x, y) = stack.pop()
            # Move Graficlly by whiching colors
            single_cell(x, y)
            time.sleep(0.03)
            backtracking_cell(x, y)


def plot_route_back(x, y):
    # Position to the Corner
    x, y = x - width, y - width
    # Graphical move
    solution_cell(x, y)

    # Move till cell position = start position
    while (x, y) != (0, 0):
        # Dictionary of paths works as a sort of chained list
        x, y = solution[x, y]
        solution_cell(x, y)
        time.sleep(0.3)


create_grid(start, end, width)
carve_out_maze(start, end)
plot_route_back(WIDTH, HEIGHT)


class State(object):
    """
    Steps:
    1) Generate a list of all possible next Steps toward goal from current position
    2) Store Children in PriorityQueue based on distance to goal, closest first
    3) Select closest child and Repeat until goal reached or no more Children
    """

    def __init__(self, value, parent, start=0, goal=0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0

        if parent:
            self.start = parent.start
            self.goal = parent.goal
            self.path = parent.path[:]
            self.path.append(value)
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def GetDistance(self):
        pass

    def CreateChildren(self):
        pass


class State_String(State):
    def __init__(self, value, parent, start=0, goal=0):

        super(State_String, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()

    def GetDistance(self):

        if self.value == self.goal:
            return 0
        dist = 0
        for i in range(len(self.goal)):
            letter = self.goal[i]
            try:
                dist += abs(i - self.value.index(letter))
            except Exception:
                dist += abs(i - self.value.find(letter))
        return dist

    def CreateChildren(self):
        if not self.children:
            for i in range(len(self.goal) - 1):
                val = self.value
                val = val[:i] + val[i + 1] + val[i] + val[i + 2:]
                child = State_String(val, self)
                self.children.append(child)


class AStar_Solver:
    def __init__(self, start, goal):
        self.path = []
        self.visitedQueue = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def Solve(self):
        startState = State_String(self.start, 0, self.start, self.goal)

        count = 0
        self.priorityQueue.put((0, count, startState))

        while not self.path and self.priorityQueue.qsize():
            closestChild = self.priorityQueue.get()[2]
            closestChild.CreateChildren()
            self.visitedQueue.append(closestChild.value)

            for child in closestChild.children:
                if child.value not in self.visitedQueue:
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

        return self.path

    # a = AStar_Solver(start1, goal1)
    # a.Solve()

    # for i in range(len(a.path)):
    #     print("{0}) {1}".format(i, a.path[i]))


# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
