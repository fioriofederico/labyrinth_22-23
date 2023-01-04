from utilities.maze import Maze

if __name__ == "__main__":
    p = Maze(15,15)
    p.generate()
    p.getMazeImage()
    print(p.startpoint)
    print(p.endpoint)
