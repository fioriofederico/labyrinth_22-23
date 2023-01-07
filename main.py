from utilities.maze import Maze

if __name__ == "__main__":
    p = Maze(30,30,[1,2])
    #p.readMazeJson("pippo.json")
    p.generate()
    #p.getMazeImage()
    #p.readMazeImage("maze.tiff")
    #p.readMazeJson('sample.json')
    #p.getMazeImage()
    p.getMazeImage()
    p.printMaze()

