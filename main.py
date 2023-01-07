from utilities.maze import Maze

if __name__ == "__main__":
    p = Maze(4,4)
    #p.generate()
    #p.getMazeJson()
    p.readMazeJson("maze.json")
    p.getMazeImage()


