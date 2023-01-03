from utilities.maze import Maze

if __name__ == "__main__":
    p = Maze(7,10,[1,1],[1,1])
    p.readMazeImage("indata/30-20_marked.tiff")
    p.getMazeImage()
    p.printMaze()
