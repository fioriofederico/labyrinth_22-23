from typing import List, Tuple
from heapq import heappop, heappush


def deikstra(maze: List[List[int]], start: List[Tuple[int, int]], goal: Tuple[int, int]):
    ROW, COL = len(maze), len(maze[0])
    directions = ["E", "W", "N", "S"]

    def is_valid(x, y):
        return 0 <= x < ROW and 0 <= y < COL and maze[x][y] != 0

    def heuristic(current, goal):
        x1, y1 = current
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def bfs(start):
        pr_queue = []
        heappush(pr_queue, (0 + heuristic(start, goal), 0, "", "", start))
        visited = set()
        paths = []
        while len(paths) < 3 and pr_queue:
            _, cost, path, path_cords, current = heappop(pr_queue)
            if current == goal:
                paths.append((start, goal, path, cost))
            if current in visited:
                continue
            visited.add(current)
            x, y = current
            for direction in directions:
                if direction == "E":
                    if is_valid(x, y + 1):
                        heappush(pr_queue, (cost + maze[x][y + 1] + heuristic((x, y + 1), goal), cost + maze[x][y + 1],
                                            path + direction, path_cords + str((x, y + 1)), (x, y + 1)))
                if direction == "W":
                    if is_valid(x, y - 1):
                        heappush(pr_queue, (cost + maze[x][y - 1] + heuristic((x, y - 1), goal), cost + maze[x][y - 1],
                                            path + direction, path_cords + str((x, y - 1)), (x, y - 1)))
                if direction == "N":
                    if is_valid(x - 1, y):
                        heappush(pr_queue, (cost + maze[x - 1][y] + heuristic((x - 1, y), goal), cost + maze[x - 1][y],
                                            path + direction, path_cords + str((x - 1, y)), (x - 1, y)))
                if direction == "S":
                    if is_valid(x + 1, y):
                        heappush(pr_queue, (cost + maze[x + 1][y] + heuristic((x + 1, y), goal), cost + maze[x + 1][y],
                                            path + direction, path_cords + str((x + 1, y)), (x + 1, y)))
        return paths or ["NO WAY!"]

    paths = []
    for s in start:
        path = bfs(s)
        if path == ["NO WAY!"]:
            paths.append(path)
        else:
            paths.extend(path)
    return paths

maze = [[1, 0, 1, 1, 1, 1],
        [4, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [0, 0, 1, 1, 4, 1],
        [1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1]]

start = [(0, 0), (2, 2), (4, 4)]
goal = (5, 5)

print(deikstra(maze, start, goal))
