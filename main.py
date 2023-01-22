import numpy as np

from utilities.maze import Maze
from utilities.foundPath import FoundPath

if __name__ == "__main__":
    p = Maze(20,30)
    p.generate()
    p.printMaze()
    p.getMazeJson()
    p.generate()
    p.getMazeImage()
    p.readMazeJson("maze.json")
    p.generate()
    p.getMazeImage()
