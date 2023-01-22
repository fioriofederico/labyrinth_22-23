import numpy as np

from utilities.maze import Maze
from utilities.foundPath import FoundPath

if __name__ == "__main__":
    p = Maze()
    p.readMazeImage("./indata/30-20_marked.tiff")
    p.printMaze()
