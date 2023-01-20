import numpy as np

from utilities.maze import Maze
from utilities.foundPath import FoundPath

if __name__ == "__main__":
    p = Maze(10, 10, [[1, 3]], [10, 4], [[2, 2, 2], [2, 3, 200], [4, 3, 128]])
    p.generate()
    p.getMazeImage()
    start = [(x[0], x[1]) for x in p.startpoints]
    goal = tuple(p.endpoint)
    maze = p.getMaze()
    maze = np.where(np.array(maze) == 'w', 0, 1)
    maze = (np.array2string(maze, separator=", "))
    print(maze)
    print(start)
    print(goal)
    foundPath = FoundPath(maze, start, goal)
    path = foundPath.find_path_astar()
    print(path)
