from heapq import heappop, heappush

class FoundPath:
    __maze = [
        [0, 1, 1, 1, 1, 1, 2, 0, 1, 1, 1, 1],
        [0, 0, 0, 2, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 2, 1, 1, 1, 4, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 13, 0, 1, 14, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 4, 0, 1],
        [1, 0, 0, 0, 1, 16, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 3, 0, 0, 5, 0, 6, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 4, 0, 0, 0, 1],
        [1, 0, 8, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 15, 0, 1, 2, 0, 0, 1],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 12],
        [0, 0, 1, 1, 1, 1, 10, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 11, 0, 0, 1, 1, 16],
        [0, 0, 12, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 14, 1, 1, 15, 0, 0, 1, 1, 1],
    ]
    #Nota fondamentale il primo valore rappresenta la riga il secondo la colonna essendo un array si conta sempre a partite da 0
    __start = [(0, 1), (0, 6), (15, 3)]
    __goal = (9, 7)
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
        graph = {(i, j): [] for j in range(width) for i in range(height) if self.__maze[i][j]}
        for row, col in graph.keys():
            if row < height - 1 and self.__maze[row + 1][col]:
                graph[(row, col)].append(("S", (row + 1, col), self.__maze[row][col]))
                graph[(row + 1, col)].append(("N", (row, col), self.__maze[row][col]))
            if col < width - 1 and self.__maze[row][col + 1]:
                graph[(row, col)].append(("E", (row, col + 1), self.__maze[row][col]))
                graph[(row, col + 1)].append(("W", (row, col), self.__maze[row][col]))
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
        startInput = self.__start
        goal = self.__goal
        print(len(startInput))
        for i in range(len(startInput)):
            print(i)
            start = startInput[i]
            print(start)
            print(goal)
            pr_queue = []
            costSum = 0
            heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
            visited = set()
            graph: dict = self.maze2graph()
            while pr_queue:
                _, cost, path, current = heappop(pr_queue)
                if current == goal:
                    print(path, cost)
                if current in visited:
                    continue
                visited.add(current)
                for direction, neighbour, real_cost in graph[current]:
                    heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + 1 + real_cost,
                                        path + direction, neighbour))
            print("NO WAY!")

