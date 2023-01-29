import numpy as np
import json

from utilities.maze import Maze
from utilities.foundPath import FoundPath
import funzioni.funzioni_finali
import time


if __name__ == "__main__":
    p = Maze()
    p.readMazeJson("./indata/labirinto2_marked.json")
    start = [(x[0], x[1]) for x in p.startpoints]
    if len(p.endpoints) == 1:
        endpoint = p.endpoints[0]
    else:
        endpoint = p.endpoints
    goal = tuple(endpoint)
    maze = p.getMaze()
    maze = np.where(np.array(maze) == 'w', 0, 1)
    bread_crumbs = [((x[0], x[1]), x[2]) for x in p.getBreadcrumbs()]
    maze = p.getMatixWithBreadcrumbs(maze, bread_crumbs)
    maze = maze.tolist()
    foundPath = FoundPath(maze, start, goal)
    path = foundPath.find_multi_path_astar_return_visited()
    json = foundPath.getPathRetunrJson()
    foundPath.write_json_file(json, './output/', 'output')

