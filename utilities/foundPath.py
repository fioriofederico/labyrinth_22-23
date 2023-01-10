from heapq import heappop, heappush

class FoundPath:

    __maze =  [
        [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    ]

    __start = (3, 0)
    __goal = (12, 8)
    def __int__(self, start, goal):
        self.__start = start
        self.__goal = goal
    pass
    """
    Convert the matrix in graph for found path
    """
    def maze2graph(self):
        height = len(self.__maze)
        width = len(self.__maze[0]) if height else 0
        graph = {(i, j): [] for j in range(width) for i in range(height) if not self.__maze[i][j]}
        for row, col in graph.keys():
            if row < height - 1 and not self.__maze[row + 1][col]:
                graph[(row, col)].append(("S ", (row + 1, col)))
                graph[(row + 1, col)].append(("N ", (row, col)))
            if col < width - 1 and not self.__maze[row][col + 1]:
                graph[(row, col)].append(("E ", (row, col + 1)))
                graph[(row, col + 1)].append(("W ", (row, col)))
        return graph



    """
    A* is a widely used pathfinding algorithm and an extension of Edsger Dijkstra's 1959 algorithm.
    A* uses a greedy search and finds a least-cost path from the given initial node to one goal node out of one or more possibilities.
    As A* traverses the graph, it follows a path of the lowest expected total cost or distance,
    keeping a sorted priority queue of alternate path segments along the way.
    It uses a heuristic cost function of node to determine the order in which the search visits nodes in the graph.
    For A* we take the first node which has the lowest sum path cost and expected remaining cost.
    But heuristics must be admissible, that is, it must not overestimate the distance to the goal.
    The time complexity of A* depends on the heuristic.
    
    For Python, we can use "heapq" module for priority queuing and add the cost part of each element.
    For a maze, one of the most simple heuristics can be "Manhattan distance".
    """

    def heuristic(self, cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    """
    Input: 
        Maze is all matrix with position wall and course
        Start Just with 2 parameter (row, column)
        Goal Just with 2 parameter (row, column)
        
    Output: 
        Movement wih North East South West
        And Cost for moviment
    """
    def find_path_astar(self):
        start = self.__start
        goal = self.__goal
        pr_queue = []
        heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
        visited = set()
        graph: dict = self.maze2graph()
        while pr_queue:
            _, cost, path, current = heappop(pr_queue)
            if current == goal:
                return path, cost
            if current in visited:
                continue
            visited.add(current)
            for direction, neighbour in graph[current]:
                heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + 1,
                                    path + direction, neighbour))
        return "NO WAY!"

