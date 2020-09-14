import sys
from Maze import *
from show import *
from Algorithm import *

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)

RectButtonFont = pygame.font.Font("OpenSans-Regular.ttf", 16)
CirButtonFont = pygame.font.Font("OpenSans-Regular.ttf", 40)

colors = {
    "black": (0, 0, 0), # background
    "white": (255, 255, 255), # route
    "blue": (0, 0, 255), # start
    "red": (255, 0, 0), # target
    "gray": (128, 128, 135), # wall
    "green": (0, 255, 127), # explored
    "purple": (204, 204, 255), # Q_learning training
    "p_yellow": (255, 255, 0), # shortest paht
    "yellow": (255, 227, 132), # button color change when click
    "frontier": (255, 192, 203) # frontier for maze generation
}

# board and algorithm parameter
TRAIN = 10
PADDING = 32
RADIUS = 40
board_height = height-4*PADDING
board_width = width-4*PADDING
v_cells = 30
h_cells = 30
cell_size = int(min(board_height/(v_cells), 
                    board_width/(h_cells)))
board_origin = (PADDING, PADDING)

start_button = RectButton(
                        left=PADDING, top=height-2*PADDING,
                        width=3*PADDING, height=1.5*PADDING,
                        text="Search Start", textcolor=colors["black"],
                        rectcolor=colors["white"],screen=screen,font=RectButtonFont)

draw_button = RectButton(
                        left=4.5*PADDING, top=height-2*PADDING,
                        width=3*PADDING, height=1.5*PADDING,
                        text="Draw Wall", textcolor=colors["black"],
                        rectcolor=colors["white"],screen=screen,font=RectButtonFont)

erase_button = RectButton(
                        left=8*PADDING, top=height-2*PADDING,
                        width=3*PADDING, height=1.5*PADDING,
                        text="Erase Wall", textcolor=colors["black"],
                        rectcolor=colors["white"],screen=screen,font=RectButtonFont)

maze_button = RectButton(
                        left=11.5*PADDING, top=height-2*PADDING,
                        width=3*PADDING, height=1.5*PADDING,
                        text="Maze", textcolor=colors["black"],
                        rectcolor=colors["white"],screen=screen,font=RectButtonFont)

reset_button = RectButton(
                        left=15*PADDING, top=height-2*PADDING,
                        width=3*PADDING, height=1.5*PADDING,
                        text="Reset", textcolor=colors["black"],
                        rectcolor=colors["white"],screen=screen,font=RectButtonFont)

dijkstra_button = CirButton(
                            center=(17*PADDING+10,3*PADDING), radius=RADIUS, text="D",
                            textcolor=colors["black"], circolor=colors["white"],
                            screen=screen, font=CirButtonFont)

bfs_button = CirButton(
                        center=(17*PADDING+10,6*PADDING), radius=RADIUS, text="B",
                        textcolor=colors["black"], circolor=colors["white"],
                        screen=screen, font=CirButtonFont)

asearch_button = CirButton(
                            center=(17*PADDING+10,9*PADDING), radius=RADIUS, text="A",
                            textcolor=colors["black"], circolor=colors["white"],
                            screen=screen, font=CirButtonFont)

qlearning_button = CirButton(
                            center=(17*PADDING+10,12*PADDING), radius=RADIUS, text="Q",
                            textcolor=colors["black"], circolor=colors["white"],
                            screen=screen, font=CirButtonFont)

SEARCH = False
DRAW = False
ERASE = False
RESET = False
ALGO = None
board = Board(v_cells, h_cells, board_origin[0], board_origin[1], cell_size, screen, colors)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(colors["black"])

    if not SEARCH:
        # draw borad and store cells (pygame rect object) for drawing and erasing wall
        cells = board.draw_board()
        
        # call game board buttons
        start_button()
        draw_button()
        erase_button()
        maze_button()
        reset_button()

        # call algorithm buttons
        dijkstra_button()
        bfs_button()
        asearch_button()
        qlearning_button()
        
        # if Reset button is pressed, change color back to white and set flag to False
        if RESET == True:
            time.sleep(0.05)
            reset_button.color_change(colors["white"])
            reset_button()
            RESET = False

        # mouse event
        left, _, right = pygame.mouse.get_pressed()

        # if left clicked, get mouse position and take corresponding action
        if left == 1:
            mouse = pygame.mouse.get_pos()

            # Board modified selections
            # button for start search
            if start_button.rect.collidepoint(mouse):
                if SEARCH == False:
                    SEARCH = True
                    DRAW = False
                    ERASE = False
                    
                    draw_button.color_change(colors["white"])
                    erase_button.color_change(colors["white"])
                    start_button.color_change(colors["yellow"])
                    
                    start_button()
                    draw_button()
                    erase_button()
                    time.sleep(0.1)
            # button for drawing wall
            elif draw_button.rect.collidepoint(mouse):
                if DRAW == False:
                    DRAW = True
                    ERASE = False
                    draw_button.color_change(colors["yellow"])
                    erase_button.color_change(colors["white"])
                else:
                    DRAW = False
                    draw_button.color_change(colors["white"])   

                time.sleep(0.1)                
            # button for erasing wall
            elif erase_button.rect.collidepoint(mouse):
                if ERASE == False:
                    ERASE = True
                    DRAW = False
                    erase_button.color_change(colors["yellow"])
                    draw_button.color_change(colors["white"])
                else:
                    ERASE = False
                    erase_button.color_change(colors["white"])    

                time.sleep(0.1)
            # button for reset board
            elif reset_button.rect.collidepoint(mouse):
                DRAW = False
                ERASE = False
                RESET = True
                
                draw_button.color_change(colors["white"])
                erase_button.color_change(colors["white"])
                reset_button.color_change(colors["yellow"])
                reset_button()
                
                board.reset()
                time.sleep(0.1)   
            # button for automated generate maze
            elif maze_button.rect.collidepoint(mouse):
                if board.wall:
                    print("Please Reset the Board")
                    time.sleep(0.1)   
                    continue

                if not board.start:
                    print("Please Select Start")
                    time.sleep(0.1)   
                    continue
                elif board.target:
                    print("Please Do Not Set Target")
                    time.sleep(0.1)   
                    continue
                
                DRAW = False
                ERASE = False
                draw_button.color_change(colors["white"])
                erase_button.color_change(colors["white"])
                maze_button.color_change(colors["yellow"])
                maze_button()

                maze_creator = Maze(board)
                maze_creator.initialize()
                maze_creator.generate()

                maze_button.color_change(colors["white"])
                maze_button()
                time.sleep(0.1)

            # Algorithm selections
            # button for dijkstra
            if dijkstra_button.distance(mouse) < RADIUS:
                ALGO = "Dijkstra"

                dijkstra_button.color_change(colors["yellow"])
                bfs_button.color_change(colors["white"])
                asearch_button.color_change(colors["white"])
                qlearning_button.color_change(colors["white"])
                time.sleep(0.1)   

            # button for BFS
            elif bfs_button.distance(mouse) < RADIUS:
                ALGO = "BFS"

                bfs_button.color_change(colors["yellow"])
                dijkstra_button.color_change(colors["white"])
                asearch_button.color_change(colors["white"])
                qlearning_button.color_change(colors["white"])
                time.sleep(0.1)   

            # button for A_search
            elif asearch_button.distance(mouse) < RADIUS:
                ALGO = "A_search"

                asearch_button.color_change(colors["yellow"])
                dijkstra_button.color_change(colors["white"])
                bfs_button.color_change(colors["white"])
                qlearning_button.color_change(colors["white"])
                time.sleep(0.1)

            # button for Q_learning
            elif qlearning_button.distance(mouse) < RADIUS:
                ALGO = "Q_learning"

                qlearning_button.color_change(colors["yellow"])
                dijkstra_button.color_change(colors["white"])
                bfs_button.color_change(colors["white"])
                asearch_button.color_change(colors["white"])
                time.sleep(0.1)

            # drawing or erasing wall by checking corresponding flag and position of mouse
            else:
                for i in range(v_cells):
                    for j in range(h_cells):
                        cell = cells[i][j]
                        if (i,j) != board.start or (i,j) != board.target:
                            if DRAW and cell.collidepoint(mouse):
                                board.wall.add((i,j))
                            elif ERASE and cell.collidepoint(mouse) and (i,j) in board.wall:
                                board.wall.remove((i,j))

        # right clicked, defining start and target point
        elif right == 1:
            mouse = pygame.mouse.get_pos()

            for i in range(v_cells):
                for j in range(h_cells):
                    cell = cells[i][j]
                    if cell.collidepoint(mouse):
                        # if it's not wall and start has not been created, create start
                        if (i,j) not in board.wall and board.start is None:
                            board.start = (i,j)
                        # if it's not wall and start, and target has not been created, create target
                        elif (i,j) not in board.wall and (i,j) != board.start and board.target is None:
                            board.target = (i,j)
                        # if it's start and target has not been created, chancel start
                        elif (i,j) == board.start and board.target is None:
                            board.start = None
                        # if it's target, chancel target
                        elif (i,j) == board.target:
                            board.target = None
            time.sleep(0.1)

        pygame.display.flip()

    # search start
    else:
        # if start or target have not been specified, game will not start
        if board.start is None or board.target is None:
            print("Please choose position of start and target")
            SEARCH = False
            start_button.color_change(colors["white"])
            continue  

        # elif algorithm is not selected, game will not start
        elif ALGO is None:
            print("Please select algorithm")
            SEARCH = False
            start_button.color_change(colors["white"])
            continue

        if board.visited or board.path:
            board.clear_visited()

        # run chosen algorithm
        if ALGO == "Dijkstra":
            algorithm = Dijkstra(board)
            algorithm.initialize()
            algorithm.solver()
        
        elif ALGO == "BFS":
            algorithm = BFS(board)
            algorithm.initialize()
            algorithm.solver()           
        
        elif ALGO == "A_search":
            algorithm = A_search(board)
            algorithm.initialize()
            algorithm.solver()

        elif ALGO == "Q_learning":
            algorithm = Q_Learning(board)
            algorithm.solver(TRAIN)

        # if find shortest path, draw the path. if not, show "No Solution Found"
        if algorithm.find == True:
            algorithm.output()
        else:
            print("No Solution Found!")

        # set SEARCH flag to False to restart the game
        SEARCH = False
        start_button.color_change(colors["white"])