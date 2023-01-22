import numpy as np

from utilities.maze import Maze
from utilities.foundPath import FoundPath

if __name__ == "__main__":
    p = Maze(20, 20, [[1, 3], [1, 8]], [20, 4], [[2, 2, 16], [2, 3, 32], [4, 3, 48]])
    p.generate()
    start = [(x[0], x[1]) for x in p.startpoints]
    goal = tuple(p.endpoint)
    maze = p.getMaze()
    maze = np.where(np.array(maze) == 'w', 0, 1)
    bread_crumbs = [((x[0], x[1]), x[2]) for x in p.getBreadcrumbs()]
    maze = p.getMatixWithBreadcrumbs(maze, bread_crumbs)
    maze = maze.tolist()
    foundPath = FoundPath(maze, start, goal)
    path = foundPath.find_multi_path_astar_return_visited()
    json = foundPath.getPathRetunrJson()
    foundPath.write_json_file(json, './output/', 'output')
