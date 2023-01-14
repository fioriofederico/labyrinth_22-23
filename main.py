from utilities.maze import Maze
from utilities.foundPath import FoundPath

if __name__ == "__main__":
    p = Maze(30,30,[[1,10],[30,4],[15,30]],[15,1],[[22,10,96], [10,10,200], [15,23,128]])
    p.generate()
    p.getMazeImage()
    print(p.startpoints)
    print(p.endpoint)

