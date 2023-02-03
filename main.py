import numpy as np

from utilities.maze import Maze
from utilities.foundPath import FoundPath

if __name__ == "__main__":
    p = Maze(10,10,[[1,3],[1,5]],[[10,8]])
    print(p.startpoints)
    p.generate()
    p.printMaze()
    p.getMazeJson()
    p.getMazeImage()
