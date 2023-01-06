from utilities.maze import Maze

if __name__ == "__main__":
    p = Maze(4,4,[1,1])
    #p.generate()
    #p.getMazeImage()
    #p.readMazeImage("maze.tiff")
    #p.readMazeJson('sample.json')
    p.getMazeImage()
    p.printMaze()

