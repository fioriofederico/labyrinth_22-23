from utilities.maze import Maze
from utilities.foundPath import FoundPath
import numpy as np

if __name__ == "__main__":
    p = Maze(30,30,[[1,10],[30,4],[15,30]],[15,1],[[22,10,96], [10,10,200], [15,23,128]])
    p.generate()
    p.getMazeImage()
    p.startpoints
    p.endpoint
    maze = p.getMaze()
    #print(maze)
    #print(len(maze))
    startPoint = []
    endPoint = ''
    mioMaze = np.zeros((len(maze),len(maze)), dtype=int)
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] == 'w':
                mioMaze[i][j] = 0
            elif maze[i][j] == 'sp':
                mioMaze[i][j] = 1
                #startPoint.append(str('('+i+','+j+')'))
            elif maze[i][j] == 'c':
                mioMaze[i][j] = 1
            elif maze[i][j] == 'bc':
                mioMaze[i][j] == 10
    print(mioMaze)