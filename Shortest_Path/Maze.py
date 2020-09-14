import time
import random
from env import *

DELAY = 0.01

class Maze:
    def __init__(self, board:Board):
        self.board = board

    def initialize(self):
        """
        Create following information for solver:
        1.board.wall: set all cells as wall except for start and target
        2.passages: set start and target as passages to record maze path
        3.board.frontiers: add frontiers of start and target to board.frontiers
        """
        # set every cell to be wall first
        self.board.wall = {
            (i, j) for i in range(self.board.v_cells)
                   for j in range(self.board.h_cells)
        }

        # put start and target into frontier
        self.passages = {self.board.start}

        # delete start and target from wall
        self.board.wall = self.board.wall.difference(self.passages)

        # initailize frontier
        self.board.frontiers = self.get_frontiers(self.board.start)
                               
    def get_frontiers(self, state:tuple)->set:
        """
        return frontiers of a state. A frontier cell is wall
        with distance 2 (in straight) of given state.

        state: position of node --> tuple
        """
        x, y = state
        frontiers = {(x-2,y), (x+2,y), (x,y-2), (x, y+2)}
        temp_frontiers = frontiers.copy()
        for row, col in temp_frontiers:
            if (row < 0 or row >= self.board.v_cells) or (col < 0 or col >= self.board.h_cells) or \
               (row, col) in self.passages or (row, col) not in self.board.wall:
               frontiers.remove((row, col))

        return frontiers
    
    def frontier_neighbor(self, frontier:tuple)->tuple:
        """
        randomly pick a cell which is in distance 2 to cells in passages from chosen frontier
        
        frontier: position of frontier --> tuple
        """
        t = int(time.time())
        random.seed(t)

        x, y = frontier
        neighbors = {(x-2,y), (x+2,y), (x,y-2), (x, y+2)}

        temp_neighbors = neighbors.copy()
        for cell in temp_neighbors:
            if cell not in self.passages:
                neighbors.remove(cell)

        neighbor = random.choice(list(neighbors))
        return neighbor
    
    def connect_cell(self, cell_1:tuple, cell_2:tuple):
        """
        Connecting cells by changing wall cell between 
        passages and chosen frontier_neighbor to be part of maze.

        cell_1: first cell to be connected --> tuple
        cell_2: second cell to be connected --> tuple
        """
        x1, y1 = cell_1
        x2, y2 = cell_2

        x_diff = x1 - x2
        y_diff = y1 - y2

        if x_diff != 0 and y_diff == 0:
            x_conn = (x1+x2) // 2
            y_conn = y1

        elif y_diff != 0 and x_diff == 0:
            y_conn = (y1+y2) // 2
            x_conn = x1
        
        if (x_conn, y_conn) in self.board.wall:
            self.passages.add((x_conn, y_conn))
            self.board.wall.remove((x_conn, y_conn))

    def generate(self):
        """
        main function to generate maze using randomized Prim's algorithm
        """
        if not self.board.frontiers:
            raise ValueError("use initialze function first")

        while self.board.frontiers:
            t = int(time.time())
            random.seed(t)
            time.sleep(DELAY)
            self.board.draw_board(return_cells=False)
            
            # randomly select a cell in frontier as part of maze
            frontier = random.choice(list(self.board.frontiers))
            self.passages.add(frontier)

            # randomly select a frontier neighbor and connect path
            neighbor = self.frontier_neighbor(frontier)
            self.connect_cell(frontier, neighbor)
            
            # add new frontiers, which are computed by chosen frontier, to board.frontier
            next_frontiers = self.get_frontiers(frontier)
            self.board.frontiers = self.board.frontiers | next_frontiers
            
            # delete cell from frontier and board.wall
            self.board.frontiers.remove(frontier)
            self.board.wall.remove(frontier)

            pygame.display.flip()