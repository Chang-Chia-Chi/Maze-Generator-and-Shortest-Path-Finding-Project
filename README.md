# Maze-Generator-and-Shortest-Path-Finding Project
![image](https://github.com/Chang-Chia-Chi/Maze-Generator-and-Shortest-Path-Finding-Project/blob/master/pic/maze.gif) 
![image](https://github.com/Chang-Chia-Chi/Maze-Generator-and-Shortest-Path-Finding-Project/blob/master/pic/q_learning.gif)
  
This project uses `Python` along with `pygame` package, to visualize complex **maze generation** and multiple **shortest-path finding algorithms**.
## Algorithms
|Algorithm              |Purpose            
| ------------------------------|-----------
|Randomized Prim's Algorithm    |Maze generation
|Dijkstra's Algorithm           |Shortest-Path-Finding
|Breadth First Search Algorithm |Shortest-Path-Finding
|A* Search Algorithm            |Shortest-Path-Finding
|Q-Learing + Depth First Search Algorithm|Shortest-Path-Finding
## Setup
-   Clone the repository:
`https://github.com/Chang-Chia-Chi/Maze-Generator-and-Shortest-Path-Finding-Project.git`  
-   Run `pip3 install -r requirements.txt` to install `pygame` package required.  
-   Change direction to `/Shortest_Path`  
-   Run `python runner.py` to start the game.

## How to Play
![image](https://github.com/Chang-Chia-Chi/Maze-Generator-and-Shortest-Path-Finding-Project/blob/master/pic/board.jpg)
![image](https://github.com/Chang-Chia-Chi/Maze-Generator-and-Shortest-Path-Finding-Project/blob/master/pic/cell_color.jpg)
### Mouse event
|Left Click |
|-----------|
| **Drawing** walls on board|
| **Erasing** walls on board|
| **Button click**|
  
|Right Click|Note
|-----------|-----
|**Set** `start & target` cell|Create `start` first then `target`
|**Remove** `start & target` cell|Must remove `target` first then `start`

### Board button
|Button|Purpose|Note
| -----------|-------|----
|**Search Start**|Start Shortest-Path-Finding using specified algorithms|If any of `start`, `target` cell and `algorithm` <br>has not been chosen, search will not start.
|**Draw Wall**|Drawing walls manually|Will not overwrite `start` and `target` cells.
|**Erase Wall**|Deleting walls manually|
|**Maze**|Generating Maze|Choose `start` cell only and `no wall exist`.<br>Recommend to `reset` board first.
|**Reset**|Reset and initailize board|

### Algorithm button
|Button|Algorithm
|------|---------
|**D**|Dijkstra
|**B**|Breadth First Search
|**A**|A* Search
|**Q**|Q-Learning with Depth First Search
