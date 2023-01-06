from random import random, randint
from colorama import Fore
from PIL import Image
import numpy as np
import json

class Maze:
  '''
  Maze Object, It's defined by:
  - Height (int): First dimension of the maze
  - Width (int): Second dimension of the maze
  - Startpoint ([int,int]): The ingress of the maze
  - Endpoint ([int, int]): The exit point of the maze
  - Breadcrumbs([[int, int],[...],[...]]):  The positions of breadcrumbs

  >>> m = Maze()

  >>> m = Maze(1,0)
  Traceback (most recent call last):
  ValueError: Value provided for height is invalid, should be greater than 3: 1

  >>> m = Maze(1,1)
  Traceback (most recent call last):
  ValueError: Value provided for height is invalid, should be greater than 3: 1

  >>> m = Maze(1,2)
  Traceback (most recent call last):
  ValueError: Value provided for height is invalid, should be greater than 3: 1

  >>> m = Maze(1,3)
  Traceback (most recent call last):
  ValueError: Value provided for height is invalid, should be greater than 3: 1

  >>> m = Maze(1,4)
  Traceback (most recent call last):
  ValueError: Value provided for height is invalid, should be greater than 3: 1

  >>> m = Maze(2,1)
  Traceback (most recent call last):
  ValueError: Value provided for height is invalid, should be greater than 3: 2

  >>> m = Maze(3,1)
  Traceback (most recent call last):
  ValueError: Value provided for height is invalid, should be greater than 3: 3

  >>> m = Maze(4,1)
  Traceback (most recent call last):
  ValueError: Value provided for width is invalid, should be greater than 3: 1

  >>> m = Maze(4,1)
  Traceback (most recent call last):
  ValueError: Value provided for width is invalid, should be greater than 3: 1

  >>> m = Maze(4,3)
  Traceback (most recent call last):
  ValueError: Value provided for width is invalid, should be greater than 3: 3

  >>> m = Maze(4,4)

  >>> m = Maze(4,4,[0,0])
  Traceback (most recent call last):
  ValueError: Start point [x,y] invalid, x must be eq. to 1; provided: 0

  >>> m = Maze(4,4,[3,0])
  Traceback (most recent call last):
  ValueError: Start point [x,y] invalid, x must be eq. to 1; provided: 3

  >>> m = Maze(4,4,[1,1])
  Traceback (most recent call last):
  ValueError: Start point cant be in a edge; provided: 1-1

  >>> m = Maze(4,4,[1,4])
  Traceback (most recent call last):
  ValueError: Start point cant be in a edge; provided: 1-4

  >>> m = Maze(4,4,endpoint=[4,2])

  >>> m = Maze(4,4,endpoint=[4,1])
  Traceback (most recent call last):
  ValueError: End point cant be in a edge; provided: 4-1

  >>> m = Maze(4,4,endpoint=[4,4])
  Traceback (most recent call last):
  ValueError: End point cant be in a edge; provided: 4-4

  '''
  __maze = []
  __walls = []
  __breadcrumbs = []
  startpoint = []
  endpoint = []

  def __init__(self, height=0, width=0, startpoint=[], endpoint=[], breadcrumbs=[[]]):
    '''Initialize a Maze object. 

    Parameters:
    - height (int): First dimension of the maze, should be greater than 3
    - width (int): Second dimension of the maze, should be greater than 3
    - startpoint ([int,int]): The ingress of the maze, should be on the top of the maze.
    - endpoint ([int, int]): The exit point of the maze, should be on the bottom of the maze.
    - breadcrumbs([[int, int],[...],[...]]):  The positions of breadcrumbs

    Returns:
    maze (Maze): A new maze object with params setted
    '''

    if (height != 0 and height > 3):
      self.__height = height
    elif (height == 0):
      self.__height = 0
    else:
      raise ValueError(f"Value provided for height is invalid, should be greater than 3: {height}")


    if (width != 0 and width > 3):
      self.__width = width
    elif (width == 0):
      self.__width = 0
    else:
      raise ValueError(f"Value provided for width is invalid, should be greater than 3: {width}")


    if (height > 0 and len(startpoint)==2):
      if (startpoint[0]!=1):
        raise ValueError(f"Start point [x,y] invalid, x must be eq. to 1; provided: {startpoint[0]}")
      elif (startpoint[1]<1 or startpoint[1]>(width)):
        raise ValueError(f"Start point [x,y] invalid, y must be greater than 0 and less than {width+1}; provided: {startpoint[1]}")
      elif (startpoint[0]==1 and (startpoint[1]==1 or startpoint[1]==width)):
        raise ValueError(f"Start point cant be in a edge; provided: {startpoint[0]}-{startpoint[1]}")
      else:
        self.startpoint = [None for i in range(2)]
        self.startpoint[0]=(startpoint[0]-1)
        self.startpoint[1]=(startpoint[1]-1)
    elif (height == 0 and len(startpoint)==2):
      raise ValueError(f"Start point cant be expressed when height eq. 0 or not expressed")
    
    if (width > 0 and len(endpoint)==2):
      if (endpoint[0]!=height):
        raise ValueError(f"End point [x,y] invalid, x must be eq. to {height}; provided: {endpoint[0]}")
      elif (endpoint[1]<1 or endpoint[1]>width):
        raise ValueError(f"End point [x,y] invalid, y must be greater than 0 and less than {width+1}; provided: {endpoint[1]}")
      elif (endpoint[0]==height and (endpoint[1]==width or endpoint[1]==1)):
        raise ValueError(f"End point cant be in a edge; provided: {endpoint[0]}-{endpoint[1]}")
      else:
          self.endpoint = [None for i in range(2)]
          self.endpoint[0]=(endpoint[0]-1)
          self.endpoint[1]=(endpoint[1]-1)
    elif (width == 0 and len(endpoint)==2):
      raise ValueError(f"End point cant be expressed when height eq. 0 or not expressed")
  
  def getMazeJson(self):
    '''
    Create a json description of the maze.
    '''
    if not(bool(self.__maze)):
      return

    maze_obj = {
      "larghezza" : 0,
      "altezza" : 0,
      "pareti" : []
    }

    wall = {
      "orientamento": "",
      "posizione": [],
      "lunghezza": 0
    }

    i = 0
    j = 0

    walls_list = []
    
    while i < self.__height:
      while j < self.__width:
        if (j+1 != self.__width):
          if (self.__maze[i][j] == 'w' and self.__maze[i][j+1] == 'w'):
            wall["orientamento"] = "H"
            wall["posizione"] = [i,j] 
            wall_length = 0
            while (j < self.__width and self.__maze[i][j] == 'w'):
              wall_length+=1
              j+=1

            wall["lunghezza"] = wall_length
            walls_list.append(wall.copy())
          else:
            j+=1
        else:
          j+=1 

      j=0
      i+=1

    i = 0
    j = 0

    while i < self.__width:
      while j < self.__height: 
        if (j+1 != self.__height):
          if (self.__maze[j][i] == 'w' and self.__maze[j+1][i] == 'w'):
            wall["orientamento"] = "v"
            wall["posizione"] = [j,i] 
            wall_length = 0
            while (j < self.__height and self.__maze[j][i] == 'w'):
              wall_length+=1
              j+=1

            wall["lunghezza"] = wall_length
            walls_list.append(wall.copy())
          else:
            j+=1
        else:
          j+=1 

      j=0
      i+=1

    maze_obj['altezza'] = self.__height
    maze_obj['larghezza'] = self.__width
    maze_obj['pareti'] = walls_list

    with open("maze.json", "w") as outfile:
      json.dump(maze_obj, outfile)

  def readMazeJson(self,path:str):
    with open(path) as json_file:
      data = json.load(json_file)
      print(data)
    
    self.__height = data['altezza']
    self.__width = data['larghezza']
    self.__maze = [["c" for j in range(self.__height)] for i in range(self.__width)]

    for wall in data["pareti"]:
      if wall["orientamento"] == "H":
        for i in range(0,wall["lunghezza"]):
          self.__maze[wall["posizione"][0]][wall["posizione"][1]+i] = "w"
      else:
        for i in range(0,wall["lunghezza"]):
          self.__maze[wall["posizione"][0]+i][wall["posizione"][1]] = "w"



  def getMaze(self) -> np.ndarray:
    return np.asarray(self.__maze)
  
  def printMaze(self):
    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'u'):
          print(Fore.WHITE + str(self.__maze[i][j]), end=" ")
        elif (self.__maze[i][j] == 'c'):
          print(Fore.GREEN + str(self.__maze[i][j]), end=" ")
        elif (self.__maze[i][j] == 'bc'):
          print(Fore.YELLOW + str(self.__maze[i][j]), end=" ")
        else:
          print(Fore.RED + str(self.__maze[i][j]), end=" ")
        
      print('\n')
  
  def getMazeImage(self):

    a = np.zeros((self.__height,self.__width,3), dtype=np.int8)

    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'c'):
          a[i,j]=[255,255,255]
        elif (self.__maze[i][j] == 'bc'):
          a[i,j]=[255,140,0]
        elif(self.__maze[i][j] == 'u'):
          a[i,j]=[124,252,0]
        else:
          a[i,j]=[0,0,0]
          
    im = Image.fromarray(a,mode="RGB")
    im.save("./maze.tiff")

  def resizeMazeImg(self,path: str):
    im = Image.open(path)
    base_width = 1400
    width_percent = (base_width / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(width_percent)))
    im = im.resize((base_width, hsize), Image.ANTIALIAS)
    im.save("./maze.tiff")


  def readMazeImage(self,path: str):
    
    im = Image.open(path)
    a = np.asarray(im)

    (height, width, rgb_dim) = a.shape

    self.__height = height
    self.__width = width
    self.__maze = [[None for j in range(width)] for i in range(height)]

    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (a[i,j]==[255,255,255]).all():
          self.__maze[i][j] = 'c'
        elif (a[i,j]==[0,0,0]).all():
          self.__maze[i][j] = 'w'
        else:
          self.__breadcrumbs.append([i,j])
          self.__maze[i][j] = 'bc'

    return self.getMaze()

  # Find number of surrounding cells
  def __surroundingCells(self, rand_wall):
    s_cells = 0
    if (self.__maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
      s_cells += 1
    if (self.__maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
      s_cells += 1
    if (self.__maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
      s_cells +=1
    if (self.__maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
      s_cells += 1
      
    return s_cells

  def __markUpperAsWall(self,rand_wall):
    if (rand_wall[0] != 0):
      if (self.__maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
        self.__maze[rand_wall[0]-1][rand_wall[1]] = 'wb'
      if ([rand_wall[0]-1, rand_wall[1]] not in self.__walls):
        self.__walls.append([rand_wall[0]-1, rand_wall[1]])

  def __markLeftAsWall(self,rand_wall):
    if (rand_wall[1] != 0):
      if (self.__maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
        self.__maze[rand_wall[0]][rand_wall[1]-1] = 'wb'
      if ([rand_wall[0], rand_wall[1]-1] not in self.__walls):
        self.__walls.append([rand_wall[0], rand_wall[1]-1])

  def __markRightAsWall(self,rand_wall):
    if (rand_wall[1] != self.__width-1):
      if (self.__maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
        self.__maze[rand_wall[0]][rand_wall[1]+1] = 'wb'
      if ([rand_wall[0], rand_wall[1]+1] not in self.__walls):
        self.__walls.append([rand_wall[0], rand_wall[1]+1])

  def __markBottomAsWall(self,rand_wall):
    if (rand_wall[0] != self.__height-1):
      if (self.__maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
        self.__maze[rand_wall[0]+1][rand_wall[1]] = 'wb'
      if ([rand_wall[0]+1, rand_wall[1]] not in self.__walls):
        self.__walls.append([rand_wall[0]+1, rand_wall[1]])
  
  def __deleteWall(self, rand_wall):
    for wall in self.__walls:
      if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        self.__walls.remove(wall)

  def generate(self):
    # Denote all cells as unvisited
    # Create an empty list of list (matrix) with height x width dimension
    for i in range(0, self.__height):
      line = []
      for j in range(0, self.__width):
        line.append('u')
      self.__maze.append(line)

    # Randomize starting point and set it a cell
    # Generate a random point inside the list of list (matrix)
    # The starting point must not be in the corner of the matrix
    # so range over 1 to width-2 and 1 to height-2

    if len(self.startpoint)==2:

      if (self.startpoint[0]==0):
        starting_height=self.startpoint[0]+1
      elif self.startpoint[0]==(self.__height-1):
        starting_height=self.startpoint[0]-1
      else:       
        starting_height=self.startpoint[0]

      if (self.startpoint[1]==0):
        starting_width=self.startpoint[1]+1
      elif (self.startpoint[1]==self.__width-1):
        starting_width=self.startpoint[0]-1
      else:       
        starting_width=self.startpoint[1]

    else:
      starting_height = randint(1,(self.__height-2))
      starting_width = randint(1,(self.__width-2))

    # Mark it as cell and add surrounding walls to the list
    self.__maze[starting_height][starting_width] = 'c'
    self.__walls.append([starting_height - 1, starting_width])
    self.__walls.append([starting_height, starting_width - 1])
    self.__walls.append([starting_height, starting_width + 1])
    self.__walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    self.__maze[starting_height-1][starting_width] = 'w'
    self.__maze[starting_height][starting_width - 1] = 'w'
    self.__maze[starting_height][starting_width + 1] = 'w'
    self.__maze[starting_height + 1][starting_width] = 'w'

    while (self.__walls):
      # Pick a random wall
      rand_wall = self.__walls[int(random()*len(self.__walls))-1]

      # Check if it is a left wall
      if (rand_wall[1] != 0):
        # If on the left there is an Untrucked and on the right there is a Cell
        # U W C
        if (self.__maze[rand_wall[0]][rand_wall[1]-1] == 'u' and self.__maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
          # Find the number of surrounding cells
          s_cells = self.__surroundingCells(rand_wall)

          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            self.__markUpperAsWall(rand_wall)
            self.__markBottomAsWall(rand_wall)
            self.__markLeftAsWall(rand_wall)
        
          # Delete wall
          self.__deleteWall(rand_wall)
          continue

      # Check if it is an upper wall
      if (rand_wall[0] != 0):
        # U
        # W
        # C
        if (self.__maze[rand_wall[0]-1][rand_wall[1]] == 'u' and self.__maze[rand_wall[0]+1][rand_wall[1]] == 'c'):

          s_cells = self.__surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            self.__markUpperAsWall(rand_wall)
            self.__markLeftAsWall(rand_wall)
            self.__markRightAsWall(rand_wall)

          # Delete wall
          self.__deleteWall(rand_wall)
          continue

      # Check the bottom wall
      if (rand_wall[0] != self.__height-1):
        # C
        # W
        # U
        if (self.__maze[rand_wall[0]+1][rand_wall[1]] == 'u' and self.__maze[rand_wall[0]-1][rand_wall[1]] == 'c'):

          s_cells = self.__surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            self.__markBottomAsWall(rand_wall)
            self.__markLeftAsWall(rand_wall)
            self.__markRightAsWall(rand_wall)

          # Delete wall
          self.__deleteWall(rand_wall)
          continue

      # Check the right wall
      if (rand_wall[1] != self.__width-1):
        # C W U
        if (self.__maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.__maze[rand_wall[0]][rand_wall[1]-1] == 'c'):

          s_cells = self.__surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'
            # Mark the new walls
            self.__markRightAsWall(rand_wall)
            self.__markBottomAsWall(rand_wall)
            self.__markUpperAsWall(rand_wall)

          # Delete wall
          self.__deleteWall(rand_wall)
          continue
      
      # if (self.__surroundingWalls(rand_wall)>3):
      #   self.__deleteWall(rand_wall)
      
      self.__deleteWall(rand_wall)
      
    # Mark the remaining unvisited cells as walls
    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'u'):
          self.__maze[i][j] = 'w'

    # Set entrance
    if len(self.startpoint)==2:
      self.__maze[self.startpoint[0]][self.startpoint[1]] = 'c'
    else:
      for i in range(0, self.__width):
        if (self.__maze[1][i] == 'c'):
          self.__maze[0][i] = 'c'
          break

    # Set exit
    if len(self.endpoint)==2:
      self.__maze[self.endpoint[0]][self.endpoint[1]] = 'c'
      self.__maze[self.endpoint[0]-1][self.endpoint[1]] = 'c' 
    else:
      for i in range(self.__width-1, 0, -1):
        if (self.__maze[self.__height-2][i] == 'c'):
          self.__maze[self.__height-1][i] = 'c'
          break


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    