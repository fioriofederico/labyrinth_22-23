from utilities.maze import Maze

if __name__ == "__main__":
    p = Maze(8,8,[[1,3],[4,1]])
    p.generate()
    p.getMazeImage()

