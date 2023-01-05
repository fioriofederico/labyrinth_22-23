from utilities.maze import Maze

if __name__ == "__main__":
    p = Maze(30,30,[1,5],[30,28])
    #p.generate()
    #p.getMazeImage()
    #p.readMazeImage("maze.tiff")
    p.readMazeJson('sample.json')
    p.getMazeImage()
    p.printMaze()

