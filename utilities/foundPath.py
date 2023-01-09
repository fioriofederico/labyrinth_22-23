def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}
    for row, col in graph.keys():
        if row < height - 1 and not maze[row + 1][col]:
            graph[(row, col)].append(("S ", (row + 1, col)))
            graph[(row + 1, col)].append(("N ", (row, col)))
        if col < width - 1 and not maze[row][col + 1]:
            graph[(row, col)].append(("E ", (row, col + 1)))
            graph[(row, col + 1)].append(("W ", (row, col)))
    return graph

from heapq import heappop, heappush
from collections import deque


def find_path_dfs(maze):
    #start, goal = (1, 0), (len(maze) - 2, len(maze[0]) - 2)
    start, goal = (0, 0), (11, 1)
    stack = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)
    while stack:
        path, current = stack.pop()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            stack.append((path + direction, neighbour))
    return "NO WAY!"

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

def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def find_path_astar(maze, start, goal):
    start = start
    goal = goal
    pr_queue = []
    heappush(pr_queue, (0 + heuristic(start, goal), 0, "", start))
    visited = set()
    graph = maze2graph(maze)
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + heuristic(neighbour, goal), cost + 1,
                                path + direction, neighbour))
    return "NO WAY!"


MAZE = [
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

MAZETwo = [
    [0, 0, 0, 1, 1, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0]
]

MAZETree = [
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]
print(find_path_astar(MAZE, (3, 0), (12, 8)))
print(find_path_astar(MAZETwo, (1, 2), (3, 5)))
print(find_path_astar(MAZETree, (1, 3), (3, 11)))
