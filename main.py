from utilities.maze import Maze
from utilities.foundPath import FoundPath

if __name__ == "__main__":
    p = Maze(15,15)
    p.generate()
    p.getMazeImage()
    print(p.startpoint)
    print(p.endpoint)

    path = FoundPath()
    print(path.find_path_astar())