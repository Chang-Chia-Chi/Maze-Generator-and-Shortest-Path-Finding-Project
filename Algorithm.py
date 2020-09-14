import time
import heapq
import pygame
import random
from env import *
from Queue import *
from collections import defaultdict
from abc import ABCMeta, abstractmethod

INF = float('inf')
DELAY = 0.01
DISTANCE = 1

class Search(metaclass=ABCMeta):
    """
    class for search algorithms
    """
    @abstractmethod
    def solver(self):
        """
        Solver to find shortest path between start and target node
        """
        pass
    
    @abstractmethod
    def initialize(self):
        """
        Create information required for solver
        """
        pass

    def output(self):
        # get cells first in case path to be drawn directly
        cells = self.board.draw_board()   

        # derive shortest path starting from target node and reverse it
        node = self.target_node
        while node.parent is not None:
            self.board.path.append(node.state)
            node = node.parent
        self.board.path.reverse()

        # draw shortest path step by step
        color = self.board.colors["p_yellow"]                     
        for i, j in self.board.path:
            time.sleep(1.5*DELAY)
            rect = cells[i][j]
            pygame.draw.rect(self.board.screen, color, rect)
            pygame.display.flip()

class Dijkstra(Search):
    """
    Dijkstra Algorithm
    """
    def __init__(self, board:Board):
        self.board = board
        self.find = False

    def initialize(self):
        """
        Create following information for solver:
        1. adjacent list
        2. node_dict: key is coordinate of node; value is node
        3. distance dict to store distance between nodes and start_node
        """
        self.node_dict = {}
        self.distance = {}

        # create nodes
        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                # if (i,j) is wall, do not create Node
                if (i,j) in self.board.wall:
                    continue

                pos = (i,j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node

                self.node_dict[pos] = node
                self.distance[node] = INF

        self.distance[self.start_node] = 0

        # add neighbor_nodes to adjacent list with action and distance
        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            # get possible neighbor positions of node
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                # get neighbor_node from node_dict
                neighbor_node = self.node_dict[(row, col)]
                # update adj_list
                self.adj_list[node][neighbor_node] = [action, DISTANCE]

    def relax(self, node:Node, neighbor: Node):
        """
        Function to update distance dict for each node, and push node into heap by distance
        """
        if self.distance[neighbor] > self.distance[node] + self.adj_list[node][neighbor][1]:

            # update distance
            self.distance[neighbor] = self.distance[node] + self.adj_list[node][neighbor][1]

            # update parent and action take
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]
            
            # push neighbor into heap
            self.entry_count += 1
            heapq.heappush(self.heap, (self.distance[neighbor], self.entry_count, neighbor))

    def solver(self):
        """
        Dijkstra algorithm
        """
        # When pusing node into heap and there exists equal distance values, 
        # then heap will arrange those nodes in order of entry time.
        self.heap = []
        self.entry_count = 1
        heapq.heappush(self.heap, (self.distance[self.start_node], self.entry_count, self.start_node))

        while self.heap and self.find == False:
            time.sleep(DELAY)
            # Extract_Min
            (_, _, node) = heapq.heappop(self.heap)
            
            # If find target node, set self.find == True
            if node.state == self.target_node.state:
                self.find = True

            # Mark node as visited
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)
            # if there is no outgoing edge, continue while loop
            if not self.adj_list[node]:
                continue

            # if there exists outgoing edges, iteration through all edges
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.relax(node, neighbor)
            pygame.display.flip()

class A_search(Search):
    """
    A* Search algorithm
    """
    def __init__(self, board:Board):
        self.board = board
        self.find = False

    def initialize(self):
        """
        Create following information for solver:
        1. adjacent list
        2. node_dict: key is coordinate of node; value is node
        3. g_scores dictionary
        4. h_scores dictionary
        """
        self.node_dict = {}
        self.g_scores = {}
        self.h_scores = {}

        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                if (i,j) in self.board.wall:
                    continue

                pos = (i,j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node
                
                self.node_dict[pos] = node
                self.g_scores[node] = INF
                self.h_scores[node] = 0

        self.g_scores[self.start_node] = 0

        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                neighbor_node = self.node_dict[(row, col)]
                self.adj_list[node][neighbor_node] = [action, DISTANCE]

    def relax(self, node:Node, neighbor: Node):
        """
        Function to update g_scores dict for each node, and push node into heap by g_scores+h_scores

        node: selected visited node --> Node
        neighbor: neighboring nodes haven't been visited --> Node
        """
        if self.g_scores[neighbor] > self.g_scores[node] + self.adj_list[node][neighbor][1]:

            # update distance
            self.g_scores[neighbor] = self.g_scores[node] + self.adj_list[node][neighbor][1]

            # update parent and action take
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]

            # push neighbor into heap
            self.entry_count += 1
            self.h_scores[neighbor] = A_search.manhattan(neighbor, self.target_node)
            heapq.heappush(self.heap, (self.g_scores[neighbor]+self.h_scores[neighbor], self.entry_count,neighbor))

    @staticmethod
    def manhattan(node_1:Node, node_2:Node)->int:
        """
        Compute manhattan distance between two nodes

        node_1: first node to be computed --> Node
        node_2: second node to be computed --> Node
        """
        start_x, start_y = node_1.state
        target_x, target_y = node_2.state
        return abs(start_x-target_x) + abs(start_y-target_y)
    
    def solver(self):
        """
        A* Search algorithm
        """
        # When pusing node into heap and there exists equal distance values, 
        # then heap will arrange those nodes in order of entry time.
        self.heap = []
        self.entry_count = 1
        h_score_s2t = A_search.manhattan(self.start_node, self.target_node) # h_score from start to target
        heapq.heappush(self.heap, (h_score_s2t, self.entry_count, self.start_node))

        while self.heap and not self.find:
            time.sleep(DELAY)
            # Extract_Min
            _, _, node = heapq.heappop(self.heap)

            # If find target node, set self.find == True
            if node.state == self.target_node.state:
                self.find = True

            # Mark node as visited
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            # if there is no outgoing edge, continue while loop
            if not self.adj_list[node]:
                continue

            # if there exists outgoing edges, iteration through all edges
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.relax(node, neighbor)

            pygame.display.flip()

class BFS(Search):
    """
    Breathe First Search algorithm
    """
    def __init__(self, board:Board):
        self.board = board
        self.find = False
    
    def initialize(self):
        """
        Create following information for solver:
        node_dict: key is coordinate of node; value is node
        """
        self.node_dict = {}
        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                if (i,j) in self.board.wall:
                    continue

                pos = (i,j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node
                
                self.node_dict[pos] = node

    def solver(self):
        """
        BFS algorithm
        """
        self.queue = Queue()
        self.queue.add(self.start_node)
        self.queue.frontier.add(self.start_node.state)

        while not self.queue.empty() and not self.find:
            
            time.sleep(DELAY)
            node = self.queue.remove()
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                # if find target node, stop loop
                if (row, col) == self.target_node.state:
                    self.target_node.parent = node
                    self.target_node.action = action
                    self.find = True
                    break
                
                # if node is not visited and not in frontier, add node to queue
                if (row, col) not in self.queue.frontier and \
                   self.node_dict[(row, col)] not in self.board.visited:

                    neighbor = self.node_dict[(row, col)]
                    neighbor.parent = node
                    neighbor.action = action
                    self.queue.add(neighbor)
                    self.queue.frontier.add((row, col))

            pygame.display.flip()

class Q_Learning(Search):
    """
    Q-Learning Algorithm: Q(s,a) <-- Q(s,a) + alpha*((reward+best_future_reward) - Q(s,a))
    
    alpha: learning rate, within range 0.0~1.0
    epsilon: parameter for epsilon-greedy algorithm, within 0.0~1.0.
             if epsilon equals to 0.0, it'll be equivalent to 
             best greedy algorithm.
    """
    def __init__(self, board:Board, alpha=0.5, epsilon=0.1):
        self.board = board
        self.find = False

        if alpha < 0.0 or alpha > 1.0:
            raise ValueError("Learning rate should be within 0.0 ~ 1.0")
        else:
            self.alpha = alpha
        if epsilon < 0.0 or epsilon > 1.0:
            raise ValueError("Learning rate should be within 0.0 ~ 1.0")
        else:
            self.epsilon = epsilon
    
    def initialize(self):
        """
        Create following information for solver:
        node_dict: key is coordinate of node; value is node
        """
        self.node_dict = {}
        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                # if (i,j) in self.board.wall:
                #     continue
                pos = (i,j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node
                
                self.node_dict[pos] = node
        
        self.q_values = defaultdict(dict)
        for pos in self.node_dict:
            neighbors = self.board.neighbors(pos, wall_included=True)
            for _, neighbor in neighbors:
                self.q_values[pos][neighbor] = 0

    def update_q_value(self, state:tuple, next_state:tuple, reward:int):
        """
        update q_values based on formula below:
        Q(s, a) = Q(s, a) + alpha * (current_reward + best_future_reward - Q(s,a))
        
        state: position of node -> tuple
        next_state: next position node after move -> tuple
        reward: current_reward -> int
        """
        old_q = self.q_values[state][next_state]
        new_est = reward + self.best_reward(next_state)
        new_q = old_q + self.alpha*(new_est - old_q)
        self.q_values[state][next_state] = new_q

    def best_reward(self, state:tuple)->float:
        """
        return best_future_reward from a state.

        state: position of node -> tuple
        """
        next_states = self.board.neighbors(state, wall_included=True)
        best = 0
        
        for _, next_state in next_states:
            best = max(best, self.q_values[state][next_state])

        return best

    def choose_action(self, state:tuple, available_actions:list, epsilon=True)->tuple:
        """
        return best action from a state

        state: position of node -> tuple
        available_actions: a list of all possible move -> list
        epsilon: if epsilon is True, epsilon greedy algorithm will be used.
                 else it'll return action with highest q_value.
        """
        t = int(time.time())
        random.seed(t)

        q_values = []
        for action in available_actions:
            q_value = self.q_values[state][action]
            q_values.append((q_value, action))

        q_values = sorted(q_values, key=lambda x:x[0], reverse=True)
        if not epsilon:
            return q_values[0][1]
        
        else:
            best_q = q_values[0]
            chosen = random.choices([best_q, q_values], weights=[1-self.epsilon, self.epsilon])
            if chosen != best_q:
                chosen = random.choice(q_values)
            return chosen[1]

    def solver(self, n):
        """
        Train AI to find shortest path using Q_Learning and DFS, do not allow AI to go back.
        """
        print('Training Start')
        search = self.initialize()

        self.board.draw_board(return_cells=False)
        pygame.display.flip()

        for i in range(n):
            stop = False
            last_state = None
            cur_state = None
            self.trail_path = [self.start_node.state]
            self.board.visited.add(self.start_node)
            while not stop and self.trail_path:
                # get current_state from last element of trail_path
                cur_state = self.trail_path[-1]

                # get all possible next_states have not been visited
                neighbors = self.board.neighbors(cur_state, wall_included=True)
                available_actions = [
                    neighbor 
                    for _, neighbor in neighbors
                    if self.node_dict[neighbor] not in self.board.visited
                ]

                # if every possible next_state has been visited and not find target, 
                # update q_value with -100 reward for last_state -> cur_state
                # and pop cur_state from trail_path. (It means the path is dead end)
                if len(available_actions) == 0 and len(self.board.visited) >= 3:
                    if self.trail_path[-1] == self.start_node.state:
                        self.trail_path.pop()
                    
                    else:
                        last_state = self.trail_path[-2]
                        self.update_q_value(
                            state=last_state,
                            next_state=cur_state,
                            reward=-100
                        )
                        self.trail_path.pop()
                    continue

                next_state = self.choose_action(cur_state, available_actions)
                # if next_state is wall, add to visited and update q_value with -10 reward
                if next_state in self.board.wall:
                    self.board.visited.add(self.node_dict[next_state])

                    self.update_q_value(
                        state=cur_state,
                        next_state=next_state,
                        reward=-10
                    )
                    continue
                    
                # if find target_node, update q_value with 100 reward
                elif next_state == self.target_node.state:
                    self.node_dict[next_state].parent = self.node_dict[cur_state]

                    self.update_q_value(
                        state=cur_state,
                        next_state=next_state,
                        reward=100
                    )
                    stop=True
                    self.find = True

                # normal path adding, update q_value with 0 reward
                else:
                    self.board.visited.add(self.node_dict[next_state])
                    self.trail_path.append(next_state)
                    self.node_dict[next_state].parent = self.node_dict[cur_state]

                    self.update_q_value(
                        state=cur_state,
                        next_state=next_state,
                        reward=0
                    )

                # draw condition of training
                cells = self.board.draw_board()   
                color = self.board.colors["purple"]                     
                for i, j in self.trail_path:
                    if (i, j) == self.board.start:
                        continue
                    rect = cells[i][j]
                    pygame.draw.rect(self.board.screen, color, rect)
                pygame.display.flip()
                
            if stop:
                self.board.clear_visited()
            
            if not self.trail_path:
                break

        # reset board.visited and board.path to ensure not effect output function
        self.board.clear_visited()
        print('Finish Training')

    def output(self):
        """
        Solve shortest path after training
        """
        # start from start node
        node = self.start_node
        visited = {node.state}
        self.board.path.append(node.state)
        # while node is not target, keep path adding
        count = 0
        while node != self.target_node:
            time.sleep(DELAY)
            self.board.draw_board(return_cells=False)

            neighbors = self.board.neighbors(node.state)
            available_actions = [
                neighbor 
                for _, neighbor in neighbors
                if neighbor not in visited
            ]
            best_action = self.choose_action(node.state, available_actions, epsilon=False)

            # get next node and append to board.path
            new_node = self.node_dict[best_action]    
            new_node.parent = node
            visited.add(new_node.state)
            if new_node.state in self.board.path:
                print("Train Fail")
                break

            self.board.path.append(new_node.state)
            node = new_node
            count += 1
            pygame.display.flip()
        
        if node == self.target_node:
            print('Total Step is {}'.format(count+1))