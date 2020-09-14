import pygame

class Node:
    """
    create node object to store node coordinate and its parent

    state: position standing --> tuple
    action: action take to move --> str
    parent: parent of node --> Node
    """
    def __init__(self, state:tuple, action:str, parent=None):
        self.state = state
        self.parent = parent
        self.action = action
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state
        else:
            return False
        
    def __repr__(self):
        if self.parent is None:
            fmt = "Node {} and no Parent".format(self.state)
        else:
            fmt = "Node {} with Parent {}".format(self.state, self.parent.state)
        return fmt
    
    def __hash__(self):
        return hash(self.state)


class Board:
    """
    create board object to present agent states

    v_cells: number of vertical cells --> int
    h_cells: number of horizontal cells --> int
    origin_x: origin x position of screen --> int
    origin_y: origin y position of screen --> int
    cell_size: size per cell --> int
    screen: pygame object "pygame.display.set_mode()" --> pygame
    colors: color dictionary --> dict
    """
    def __init__(self, v_cells:int, h_cells:int, origin_x:int, origin_y:int, 
                 cell_size:int, screen:int, colors:dict):
        self.v_cells = v_cells
        self.h_cells = h_cells
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.cell_size = cell_size
        self.screen = screen
        self.colors = colors
        self.wall = set()
        self.visited = set()
        self.frontiers = set()
        self.path = list()
        self.start = None
        self.target = None
    
    def draw_board(self, return_cells=True)->bool:
        cells = []
        for i in range(self.v_cells):
            row = []
            for j in range(self.h_cells):
                rect = pygame.Rect(self.origin_x + i*self.cell_size,
                                   self.origin_y + j*self.cell_size,
                                   self.cell_size, self.cell_size)
                color = self.colors["white"]
                if (i, j) == self.start:
                    color = self.colors["blue"]
                elif (i, j) == self.target:
                    color = self.colors["red"]
                elif (i, j) in self.frontiers:
                    color = self.colors["frontier"]
                elif (i, j) in self.wall:
                    color = self.colors["gray"]
                elif (i, j) in self.path:
                    color = self.colors["p_yellow"]
                else:
                    for node in self.visited:
                        if (i, j) == node.state:
                            color = self.colors["green"]
                pygame.draw.rect(self.screen, color, rect)
                row.append(rect)
            cells.append(row)

        if return_cells:
            return cells

    def neighbors(self, state:tuple, wall_included=False)->list:
        """
        Return possible action could be taken

        state: position of node --> tuple
        wall_included: whether walls are included in neighbors
        """
        row, col = state
        actions = {
            "UP": (row-1, col),
            "DOWN": (row+1, col),
            "LEFT": (row, col-1),
            "RIGHT": (row, col+1)
        }
        res = []
        for action, (r, c) in actions.items():
            if not wall_included:
                if 0 <= r < self.v_cells and 0 <= c < self.h_cells and \
                    (r, c) not in self.wall:
                    res.append([action, (r, c)])
            else:
                if 0 <= r < self.v_cells and 0 <= c < self.h_cells:
                    res.append([action, (r, c)])
        
        return res if len(res) != 0 else None
    
    def reset(self):
        self.wall = set()
        self.visited = set()
        self.path = list()
        self.start = None
        self.target = None
    
    def clear_visited(self):
        self.visited = set()
        self.path = list()