from random import random, randint
from colorama import Fore
from PIL import Image
import numpy as np
import os
import json
import jsonschema
from typing import List, Literal

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

  >>> m = Maze(4,4,[[0,0]])
  Traceback (most recent call last):
  ValueError: Start point [x,y] invalid, x must be greater than 0 and less than 5; provided: 0

  >>> m = Maze(4,4,[[3,0]])
  Traceback (most recent call last):
  ValueError: Start point [x,y] invalid, y must be greater than 0 and less than 5; provided: 0

  >>> m = Maze(4,4,[[1,1]])
  Traceback (most recent call last):
  ValueError: Start point cant be in a edge; provided: 1-1

  >>> m = Maze(4,4,[[1,4]])
  Traceback (most recent call last):
  ValueError: Start point cant be in a edge; provided: 1-4

  >>> m = Maze(4,4,endpoints=[[4,2]])

  >>> m = Maze(4,4,endpoints=[[4,1]])
  Traceback (most recent call last):
  ValueError: End point cant be in a edge; provided: 4-1

  >>> m = Maze(4,4,endpoints=[[4,4]])
  Traceback (most recent call last):
  ValueError: End point cant be in a edge; provided: 4-4

  >>> m = Maze(4,4,[[2,1]])

  >>> m = Maze(4,4,[[2,1]],[[4,2]],[[]])
  Traceback (most recent call last):
  ValueError: Invalid breadcrumb declaration, provided []

  >>> m = Maze(4,4,[[2,1]],[[4,2]],[[2,2,96],[2,3,96],[3,3,96],[3,2,128]])

  >>> m = Maze(4,4,[[2,1]],[[4,2]],[[2,2,96],[4,3,96],[3,3,128]])
  Traceback (most recent call last):
  ValueError: Invalid breadcrumb: out of maze bounds, provided [4, 3, 96]

  >>> m = Maze(4,4,[[2,1]],[[4,2]],[[2,2,96],[1,3,96],[3,3,128]])
  Traceback (most recent call last):
  ValueError: Invalid breadcrumb: out of maze bounds, provided [1, 3, 96]

  >>> m = Maze(4,4,[[2,1]],[[4,2]],[[2,2,96],[3,1,96],[3,3,128]])
  Traceback (most recent call last):
  ValueError: Invalid breadcrumb: out of maze bounds, provided [3, 1, 96]

  >>> m = Maze(4,4,[[2,1]],[[4,2]],[[2,2,96],[3,4,96],[3,3,128]])
  Traceback (most recent call last):
  ValueError: Invalid breadcrumb: out of maze bounds, provided [3, 4, 96]

  >>> m = Maze(4,4,[[2,1]],[[4,2]],[[2,2, 128],[4,4,128],[3,3,96]])
  Traceback (most recent call last):
  ValueError: Invalid breadcrumb: out of maze bounds, provided [4, 4, 128]

  >>> m = Maze(4,4,[[4,2]])

  >>> m = Maze(4,4,[[3,4]])

  >>> m = Maze(4,4,[[2,2]])
  Traceback (most recent call last):
  ValueError: Start point [x,y] invalid; provided: [2, 2]

  >>> m = Maze()
  >>> m.readMazeImage("tests/testcase/maze.tiff")
  array([['w', 'sp', 'w', 'w'],
         ['w', 'c', 'c', 'w'],
         ['w', 'w', 'bc', 'w'],
         ['w', 'w', 'ep', 'w']], dtype='<U2')

  >>> m.readMazeJson("tests/testcase/maze.json")
  array([['w', 'sp', 'w', 'w'],
         ['w', 'c', 'c', 'w'],
         ['w', 'w', 'bc', 'w'],
         ['w', 'w', 'ep', 'w']], dtype='<U2')

  >>> m.readMazeJson("tests/testcase/maze_1.json")
  Traceback (most recent call last):
  Exception: 'larghezza' is a required property

  >>> m.readMazeJson("tests/testcase/maze_2.json")
  Traceback (most recent call last):
  Exception: [] is too short

  >>> m.readMazeJson("tests/testcase/maze_3.json")
  Traceback (most recent call last):
  KeyError: 'iniziali'

  >>> m.readMazeJson("tests/testcase/maze_4.json")
  Traceback (most recent call last):
  Exception: 'lunghezza' is a required property

  >>> m.readMazeJson("tests/testcase/maze_4.json")
  Traceback (most recent call last):
  Exception: 'lunghezza' is a required property

  >>> m.readMazeJson("tests/testcase/maze_5.json")
  Traceback (most recent call last):
  json.decoder.JSONDecodeError: Expecting ',' delimiter: line 4 column 5 (char 43)

  >>> m.readMazeJson("tests/testcase/maze_6.json")
  Traceback (most recent call last):
  ValueError: Invalid wall: [3, 0]

  >>> m.readMazeJson("tests/testcase/maze_7.json")
  Traceback (most recent call last):
  ValueError: Invalid wall: [0, 3]

  >>> m.readMazeJson("tests/testcase/maze_8.json")
  array([['w', 'c', 'w', 'w'],
         ['w', 'c', 'c', 'c'],
         ['w', 'w', 'bc', 'c'],
         ['w', 'sp', 'ep', 'c']], dtype='<U2')
  
  >>> m.readMazeJson("tests/testcase/maze_9.json")
  array([['w', 'c', 'w', 'w'],
         ['w', 'bc', 'bc', 'c'],
         ['w', 'bc', 'bc', 'c'],
         ['w', 'sp', 'ep', 'c']], dtype='<U2')
  '''
  __maze = []
  __walls = []
  __breadcrumbs = []
  startpoints = []
  endpoints = []
  __mazeSchema = {
    "type": "object",
    "required": [ "larghezza", "altezza", "pareti"],
    "properties": {
      "larghezza": {
        "type": "number",
        "minimum" : 4
      },
      "altezza": {
        "type": "number",
        "minimum" : 4
      },
      "pareti": {
        "type" : "array",
        "items": {
          "type" : "object",
          "required": [ "orientamento", "posizione", "lunghezza" ],
          "properties" : {
            "orientamento": { 
              "type":"string",
            },
            "posizione": {
              "type":"array",
              "items": { 
                "type": "number",
                "minimum": 0
              }
            },
            "lunghezza": { 
              "type": "number",
              "minimum": 1
            }
          }
        }
      },
      "iniziali": {
        "type":"array",
        "items": {
          "type":"array",
          "items":{"type": "number"},
          "minItems": 2
        },
        "minItems": 1,
      },
      "finale":  {
        "type":"array",
        "items": {
          "type":"array",
          "items":{"type": "number"},
          "minItems": 2
        },
        "minItems": 1,
      },
      "costi":  {
        "type":"array",
        "items": { 
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 3,
          "maxItems": 3
        }
      }
    }
  }

  def __init__(self, height:int=4, width:int=4, startpoints:List[List[int]]=[], endpoints:List[List[int]]=[], breadcrumbs:List[List[int]]=[]):
    '''Initialize a Maze object. 

    Parameters:
    - height (int): First dimension of the maze, should be greater than 3
    - width (int): Second dimension of the maze, should be greater than 3
    - startpoint ([int,int]): The ingress of the maze, should along the corner of the maze.
    - endpoints ([int, int]): The exit point of the maze, should be along the corner of the maze.
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

    # Clean maze
    self.resetMaze()

    if len(startpoints) > 0:
      for startpoint in startpoints:
        # Check start point and endpoints
        if (height > 0 and width > 0 and len(startpoint)==2):
          self.__checkPoint(startpoint,'S',height,width)
      
      for startpoint in startpoints:
        #Set start point if valid   
        self.startpoints.append([startpoint[0]-1,startpoint[1]-1])
      
    if len(endpoints) > 0:
      for endpoint in endpoints:
        # Check start point and endpoints
        if (height > 0 and width > 0 and len(endpoint)==2):
          self.__checkPoint(endpoint,'E',height,width)
      
      for endpoint in endpoints:
        #Set start point if valid   
        self.endpoints.append([endpoint[0]-1,endpoint[1]-1])
  
    # Checks breadcrumbs
    if (len(breadcrumbs)>0):
      # Checks breadcrumbs
      for bc in breadcrumbs:
        self.__checkBreadCrumbPoint(bc,height,width)
      
      # Set breadcrumb if they are valid
      for bc in breadcrumbs:
        self.__breadcrumbs.append([bc[0]-1,bc[1]-1,bc[2]])
    else:
      # Set a void list
      self.__breadcrumbs = []

  def resetMaze(self):
    self.__maze = []
    self.__walls = []
    self._breadcrumbs = []
    self.startpoints = []
    self.endpoints = []

  def __checkBreadCrumbPoint(self, bc: List[int], height: int, width: int) -> None :
    '''Check if a breadcrumb point is inside the maze bounds.
    Raise ValueError if the breadcrumb is not inside the maze bounds.
    
    Parameters:
    - breadcrumbs([int, int]):  The positions of the breadcrumb
    - height(int): The height of the maze
    - width(int): The width of the maze

    Returns:
    Nothing
    '''

    if (len(bc)==3):
      if not ((bc[0]>1 and bc[0]<height)and(bc[1]>1 and bc[1]<width)):
        raise ValueError(f"Invalid breadcrumb: out of maze bounds, provided {bc}")
    else:
      raise ValueError(f"Invalid breadcrumb declaration, provided {bc}")

  def __checkPoint(self, point: List[int], point_type: Literal["S","E"],height:int,width:int) -> None:
    '''Verify that a point is along the maze corner.
    Raise ValueError if a point is not along maze corners.

    Parameters:
    - point ([int,int]): A point in the maze.
    - point_type (Literal['S','E']): Indicate if the point is a Startpoint or an Endpoint
    - height(int): The height of the maze
    - width(int): The width of the maze

    Returns:
    Nothing
    '''
    if (point[0]<1 or point[0]>(width)):
      raise ValueError(f"{'Start' if point_type=='S' else 'End'} point [x,y] invalid, x must be greater than 0 and less than {width+1}; provided: {point[0]}")
    elif (point[1]<1 or point[1]>(width)):
      raise ValueError(f"{'Start' if point_type=='S' else 'End'} point [x,y] invalid, y must be greater than 0 and less than {width+1}; provided: {point[1]}")
    elif (point[0]==1 and (point[1]==1 or point[1]==width)):
      raise ValueError(f"{'Start' if point_type=='S' else 'End'} point cant be in a edge; provided: {point[0]}-{point[1]}")
    elif (point[0]==height and (point[1]==1 or point[1]==width)):
      raise ValueError(f"{'Start' if point_type=='S' else 'End'} point cant be in a edge; provided: {point[0]}-{point[1]}")
    elif((point[0]==1 or point[0]==height) and point[1]>0 and point[1]<width+1 and point_type!="E"):
      pass
    elif ((point[1]==1 or point[1]==width) and point[0]>0 and point[0]<height+1 and point_type!="E" ):
      pass
    elif (point_type=="E"):
      pass
    else:
      raise ValueError(f"{'Start' if point_type=='S' else 'End'} point [x,y] invalid; provided: {point}")


  def getMazeJson(self) -> None:
    '''
    Create a json description of the maze if a maze was created or setted.
    It raises a generic Exception if the maze obj doesnt have a maze loaded or generated.
    '''

    if not(bool(self.__maze)):
      raise Exception("Maze not initialized.")

    maze_obj = {
      "larghezza" : 0,
      "altezza" : 0,
      "pareti" : [],
      "iniziali" : [],
      "finale": [],
      "costi": [] 
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
    maze_obj['iniziali'] = [[a,b] for a, b in self.startpoints]
    maze_obj['finale'] = [[a,b] for a, b in self.endpoints]
    maze_obj["costi"] = [[int(a),int(b),int(c)] for a, b, c in self.__breadcrumbs]

    with open("maze.json", "w") as outfile:
      json.dump(maze_obj, outfile)
      outfile.close()

  def __validateJson(self,json:dict) -> None:
    '''
    Validate the raeded json based on schema definitions.

    Parameters:
    - json(dict): The json to validate

    Returns:
    Nothing
    '''

    # Check schema consistency
    try:
      jsonschema.validate(json,schema=self.__mazeSchema)
    except Exception as e:
      raise Exception(e.message)

    for i in json["iniziali"]:
      # Shifted by one cause its not an user input
      self.__checkPoint([i[0]+1,i[1]+1],'S',json["altezza"],json["larghezza"])
    
    # Shifted by one cause its not an user input
    for i in json["finale"]:
      self.__checkPoint([i[0]+1,i[1]+1],'E',json["altezza"],json["larghezza"])

    # Check walls consistency
    for wall in json["pareti"]:
      if wall["orientamento"] == "H":
        if wall["posizione"][1]+wall["lunghezza"]>json["larghezza"]:
          raise ValueError(f"Invalid wall: {wall['posizione']}")
      elif wall["orientamento"] == "V":
        if wall["posizione"][0]+wall["lunghezza"]>json["altezza"]:
          raise ValueError(f"Invalid wall: {wall['posizione']}")
      elif wall["orientamento"] == "":
          raise ValueError(f"Invalid wall: {wall['posizione']}")
    
    # Checks breadcrumbs
    if (len(json["costi"])>0):
      for bc in json["costi"]:
        #Plus + 1 cause when read from json we start count from 0
        self.__checkBreadCrumbPoint([bc[0]+1,bc[1]+1,bc[2]],json["altezza"],json["larghezza"])


  def readMazeJson(self,path:str) -> None: 
    '''
    Read a json description of a maze with the following structure and populate the maze object.
    e.g
    {
      "larghezza": 41,
      "altezza": 21,
      "pareti": 
      [
        {
          "orientamento": "H",
          "posizione": 
          [
            0,
            0
          ],
          "lunghezza": 19
        },
        ...
      ],
      "iniziali":
      [
        [0, 3] [...]
      ],
      "finale":
      [
        20, 12
      ],
      "costi":
      [
        [1, 1, 10], [...]
      ]
    }
    
    This method raise a OSError if the provided path doesnt exist.

    Parameters:
    - path (str): The path to the specified json maze description

    Returns:
    Nothing
    '''

    # Check if the path and the file exist
    if not(bool(os.path.exists(path))):
      raise OSError(2,"The provided file doesnt exitst.",path)

    # Open the file
    with open(path) as json_file:
      data = json.load(json_file)
      self.__validateJson(data)

    # Clean maze
    self.resetMaze()
    
    # Set maze attribute
    self.__height = data['altezza']
    self.__width = data['larghezza']

    if data["iniziali"] != []:
      self.startpoints=data["iniziali"]

    if data["finale"] != []:
      self.endpoints = data["finale"]

    if data["costi"] != []:
      self.__breadcrumbs = data["costi"]

    self.__maze = [["c" for j in range(self.__width)] for i in range(self.__height)]

    # Build walls 
    for wall in data["pareti"]:
      if wall["orientamento"] == "H":
        for i in range(0,wall["lunghezza"]):
          self.__maze[wall["posizione"][0]][wall["posizione"][1]+i] = "w"
      else:
        for i in range(0,wall["lunghezza"]):
          self.__maze[wall["posizione"][0]+i][wall["posizione"][1]] = "w"

    if self.startpoints != []:
      for startpoint in self.startpoints:
        self.__maze[startpoint[0]][startpoint[1]] = "sp"
    
    if self.endpoints != []:
      for endpoints in self.endpoints:
        self.__maze[endpoints[0]][endpoints[1]] = "ep"

    if self.__breadcrumbs != []:
      for bc in self.__breadcrumbs:
        self.__maze[bc[0]][bc[1]] = "bc"

  def getMaze(self) -> np.ndarray:
    '''
    Return a NumPy array description of the maze.

    e.g
    [[w, c, w, w],
     [w, c, c, w],
     [w, w, c, w],
     [w, w, c, w]]
    
    Return:
    maze(np.ndarray): The numpy array rappresentation of the Maze
    '''
    return np.asarray(self.__maze)
  
  def printMaze(self) -> None:
    '''
    Print via console stdout the maze array description.

    Return:
    Nothing
    '''

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
  
  def getMazeImage(self) -> None:
    '''
    Generate a tiff image rapresent the current maze obj, the generated file will be named 'maze.tiff'
    It raises a generic Exception if the maze obj doesnt have a maze loaded or generated.

    Return:
    Nothing
    '''

    # Check if a maze was loaded or generated
    if not(bool(self.__maze)):
      raise Exception("Maze not initialized.")

    # Create a numpy array that represent the maze
    a = np.zeros((self.__height,self.__width,3), dtype=np.int8)

    # Value the fields
    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'c'):
          a[i,j]=[255,255,255]
        elif (self.__maze[i][j] == 'bc'):
          # Search the breadcrumb
          for bc in self.__breadcrumbs:
            if (bc[0] == i and bc[1] == j):
              # Set the breadcrumb color
              for bc in self.__breadcrumbs:
                if bc[0]==i and bc[1]==j:
                  color = bc[2]
                  break
              a[i,j]=[color,color,color]
        elif(self.__maze[i][j] == 'u'):
          a[i,j]=[124,252,0]
        elif(self.__maze[i][j] == 'sp'):
          a[i,j]=[0,255,0]
        elif(self.__maze[i][j] == 'ep'):
          a[i,j]=[255,0,0]
        else:
          a[i,j]=[0,0,0]
    
    # Save the tiff in the current main folder
    im = Image.fromarray(a,mode="RGB")
    im.save("./maze.tiff")

  def resizeMazeImg(self,path="maze.tiff") -> None:
    '''
    Resize maze img. Create a large version of the maze tiff.
    This method raise a OSError if the provided path doesnt exist.
    Return:
    Nothing
    '''

    a = self.readMazeImage(path)

    (height, width) = a.shape

    new_height = height*3
    new_width = width*3

    # Create a numpy array that represent the maze
    a = np.zeros((new_height,new_width,3), dtype=np.int8)

    # Value the fields
    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'c'):
          #Sopra
          a[i*3,j*3+1]=[255,255,255]
          #Sotto
          a[i*3+2,j*3+1]=[255,255,255]

          # Dx
          a[i*3+1,j*3+2]=[255,255,255]
          # Sx
          a[i*3+1,j*3]=[255,255,255]

          # SD
          a[i*3,j*3+2]=[255,255,255]
          # SS
          a[i*3,j*3]=[255,255,255]

          # GD
          a[i*3+2,j*3+2]=[255,255,255]
          # GS
          a[i*3+2,j*3]=[255,255,255]

          # Al centro
          a[i*3+1,j*3+1]=[255,255,255]
        elif (self.__maze[i][j] == 'bc'):
          # Search the breadcrumb
          for bc in self.__breadcrumbs:
            if (bc[0] == i and bc[1] == j):
              # Set the breadcrumb color
              #Sopra
              a[i*3,j*3+1]=[bc[2],bc[2],bc[2]]
              #Sotto
              a[i*3+2,j*3+1]=[bc[2],bc[2],bc[2]]

              # Dx
              a[i*3+1,j*3+2]=[bc[2],bc[2],bc[2]]
              # Sx
              a[i*3+1,j*3]=[bc[2],bc[2],bc[2]]

              # SD
              a[i*3,j*3+2]=[bc[2],bc[2],bc[2]]
              # SS
              a[i*3,j*3]=[bc[2],bc[2],bc[2]]

              # GD
              a[i*3+2,j*3+2]=[bc[2],bc[2],bc[2]]
              # GS
              a[i*3+2,j*3]=[bc[2],bc[2],bc[2]]

              a[i*3+1,j*3+1]=[bc[2],bc[2],bc[2]]
        elif(self.__maze[i][j] == 'u'):
          #Sopra
          a[i*3,j*3+1]=[124,252,0]
          #Sotto
          a[i*3+2,j*3+1]=[124,252,0]

          # Dx
          a[i*3+1,j*3+2]=[124,252,0]
          # Sx
          a[i*3+1,j*3]=[124,252,0]

          # SD
          a[i*3,j*3+2]=[124,252,0]
          # SS
          a[i*3,j*3]=[124,252,0]

          # GD
          a[i*3+2,j*3+2]=[124,252,0]
          # GS
          a[i*3+2,j*3]=[124,252,0]

          a[i*3+1,j*3+1]=[124,252,0]
        elif(self.__maze[i][j] == 'sp'):
          #Sopra
          a[i*3,j*3+1]=[0,255,0]
          #Sotto
          a[i*3+2,j*3+1]=[0,255,0]

          # Dx
          a[i*3+1,j*3+2]=[0,255,0]
          # Sx
          a[i*3+1,j*3]=[0,255,0]

          # SD
          a[i*3,j*3+2]=[0,255,0]
          # SS
          a[i*3,j*3]=[0,255,0]

          # GD
          a[i*3+2,j*3+2]=[0,255,0]
          # GS
          a[i*3+2,j*3]=[0,255,0]

          a[i*3+1,j*3+1]=[0,255,0]
        elif(self.__maze[i][j] == 'ep'):
          #Sopra
          a[i*3,j*3+1]=[255,0,0]
          #Sotto
          a[i*3+2,j*3+1]=[255,0,0]

          # Dx
          a[i*3+1,j*3+2]=[255,0,0]
          # Sx
          a[i*3+1,j*3]=[255,0,0]

          # SD
          a[i*3,j*3+2]=[255,0,0]
          # SS
          a[i*3,j*3]=[255,0,0]

          # GD
          a[i*3+2,j*3+2]=[255,0,0]
          # GS
          a[i*3+2,j*3]=[255,0,0]

          a[i*3+1,j*3+1]=[255,0,0]
        else:
          #Sopra
          a[i*3,j*3+1]=[0,0,0]
          #Sotto
          a[i*3+2,j*3+1]=[0,0,0]

          # Dx
          a[i*3+1,j*3+2]=[0,0,0]
          # Sx
          a[i*3+1,j*3]=[0,0,0]

          # SD
          a[i*3,j*3+2]=[0,0,0]
          # SS
          a[i*3,j*3]=[0,0,0]

          # GD
          a[i*3+2,j*3+2]=[0,0,0]
          # GS
          a[i*3+2,j*3]=[0,0,0]

          a[i*3+1,j*3+1]=[0,0,0]

    # creating image object of
    # above array
    # Save the tiff in the current main folder
    im = Image.fromarray(a,mode="RGB")
    im.save("./large_maze.tiff")


  def readMazeImage(self,path: str) -> None:
    '''
    Read maze img and create a maze obj rappresentation.
    This method raise a OSError if the provided path doesnt exist.
    
    Parameters:
    - path (str): The path to the specified maze img.

    Return:
    Nothing
    '''

    # Check if the path and the file exist
    if not(bool(os.path.exists(path))):
      raise OSError(2,"The provided file doesnt exitst.",path)
    
    im = Image.open(path)
    a = np.asarray(im)

    (height, width, rgb_dim) = a.shape

    # Clean maze
    self.resetMaze()

    self.__height = height
    self.__width = width
    self.__maze = [[None for j in range(width)] for i in range(height)]

    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (a[i,j]==[255,255,255]).all():
          self.__maze[i][j] = 'c'
        elif (a[i,j]==[0,0,0]).all():
          self.__maze[i][j] = 'w'
        elif (a[i,j] == [255,0,0]).all():
          self.endpoints.append([i,j])
          self.__maze[i][j] = 'ep'
        elif (a[i,j] == [0,255,0]).all():
          self.startpoints.append([i,j])
          self.__maze[i][j] = 'sp'
        else:
          self.__breadcrumbs.append([i,j,a[i,j][0]])
          self.__maze[i][j] = 'bc'

  def __surroundingCells(self, rand_wall: list) -> int:
    '''
    Find number of surrounding cells.

    Parameters:
    - rand_wall ([int, int]): The position of the wall.

    Returns:
    s_cells (int): n. of surrainding cells
    '''

    # Number of surrounding cells
    s_cells = 0
    
    #Check up
    if (self.__maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
      s_cells += 1
    #Check down
    if (self.__maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
      s_cells += 1
    #Check left
    if (self.__maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
      s_cells +=1
    #Check right
    if (self.__maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
      s_cells += 1
      
    return s_cells

  def __markUpperAsWall(self,rand_wall) -> None:
    '''
    Mark Upper cell as Wall Border

    Parameters:
    - rand_wall ([int, int]): The position of the wall.

    Return:
    Nothing
    '''

    # Check if it is the upper bound
    if (rand_wall[0] != 0):
      # If the upper block is not a cell already mark it as wall border
      if (self.__maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
        self.__maze[rand_wall[0]-1][rand_wall[1]] = 'w'
      
      # Add the block to the list of walls if is not present
      if ([rand_wall[0]-1, rand_wall[1]] not in self.__walls):
        self.__walls.append([rand_wall[0]-1, rand_wall[1]])

  def __markLeftAsWall(self,rand_wall) -> None:
    '''
    Mark Left cell as Wall Border

    Return:
    Nothing
    '''

    # Check if it is the left bound
    if (rand_wall[1] != 0):
      # If the left block is not a cell already mark it as wall border
      if (self.__maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
        self.__maze[rand_wall[0]][rand_wall[1]-1] = 'w'

      # Add the block to the list of walls if is not present
      if ([rand_wall[0], rand_wall[1]-1] not in self.__walls):
        self.__walls.append([rand_wall[0], rand_wall[1]-1])

  def __markRightAsWall(self,rand_wall) -> None:
    '''
    Mark Right cell as Wall Border

    Return:
    Nothing
    '''

    # Check if it is the right bound
    if (rand_wall[1] != self.__width-1):
      # If the right block is not a cell already mark it as wall border
      if (self.__maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
        self.__maze[rand_wall[0]][rand_wall[1]+1] = 'w'

      # Add the block to the list of walls if is not present
      if ([rand_wall[0], rand_wall[1]+1] not in self.__walls):
        self.__walls.append([rand_wall[0], rand_wall[1]+1])

  def __markBottomAsWall(self,rand_wall) -> None:
    '''
    Mark Bottom cell as Wall Border

    Return:
    Nothing
    '''

    # Check if it is the lower bound
    if (rand_wall[0] != self.__height-1):
      # If the lower block is not a cell already mark it as wall border
      if (self.__maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
        self.__maze[rand_wall[0]+1][rand_wall[1]] = 'w'

      # Add the block to the list of walls if is not present
      if ([rand_wall[0]+1, rand_wall[1]] not in self.__walls):
        self.__walls.append([rand_wall[0]+1, rand_wall[1]])
  
  def __deleteWall(self, rand_wall) -> None:
    '''
    Delete the wall from walls border list.

    Return:
    Nothing
    '''

    for wall in self.__walls:
      if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        self.__walls.remove(wall)

  def generate(self) -> None:
    '''
    Generate a random maze of specified dimensions.

    Return:
    Nothing
    '''

    # Clean maze
    self.resetMaze()

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

    if len(self.startpoints)>2:
      if len(self.startpoints[0])==2:
        if (self.startpoints[0][0]==0):
          starting_height=self.startpoints[0][0]+1
        elif self.startpoints[0][0]==(self.__height-1):
          starting_height=self.startpoints[0][0]-1
        else:       
          starting_height=self.startpoints[0][0]

        if (self.startpoints[0][1]==0):
          starting_width=self.startpoints[0][1]+1
        elif (self.startpoints[0][1]==self.__width-1):
          starting_width=self.startpoints[0][0]-1
        else:       
          starting_width=self.startpoints[0][1]

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
      
      self.__deleteWall(rand_wall)
      
    # Mark the remaining unvisited cells as walls
    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'u'):
          self.__maze[i][j] = 'w'

    # Set entrance
    if len(self.startpoints)>0:
      for startpoint in self.startpoints:
        if len(startpoint)==2:
          self.__maze[startpoint[0]][startpoint[1]] = 'sp'
          if startpoint[0]==0:
            self.__maze[startpoint[0]+1][startpoint[1]] = 'c'
          elif startpoint[0]==self.__height-1:
            self.__maze[startpoint[0]-1][startpoint[1]] = 'c'
          elif startpoint[1]==0:
            self.__maze[startpoint[0]][startpoint[1]+1] = 'c'
          elif startpoint[1]==self.__width-1:
            self.__maze[startpoint[0]][startpoint[1]-1] = 'c'
    else:
      for i in range(0, self.__width):
        if (self.__maze[1][i] == 'c'):
          self.__maze[0][i] = 'sp'
          self.startpoints.append([0,i])
          break

    # Set exit
    if len(self.endpoints)==2:
      self.__maze[self.endpoints[0]][self.endpoints[1]] = 'ep'
      if self.endpoints[0]==0:
        self.__maze[self.endpoints[0]+1][self.endpoints[1]] = 'c'
      elif self.endpoints[0]==self.__height-1:
        self.__maze[self.endpoints[0]-1][self.endpoints[1]] = 'c'
      elif self.endpoints[1]==0:
        self.__maze[self.endpoints[0]][self.endpoints[1]+1] = 'c'
      elif self.endpoints[1]==self.__width-1:
        self.__maze[self.endpoints[0]][self.endpoints[1]-1] = 'c' 
    else:
      for i in range(self.__width-1, 0, -1):
        if (self.__maze[self.__height-2][i] == 'c'):
          self.__maze[self.__height-1][i] = 'ep'
          self.endpoints.append([self.__height-1,i])
          break

    if len(self.__breadcrumbs) > 0:
      for bc in self.__breadcrumbs:
        self.__maze[bc[0]][bc[1]] = "bc"


  def getBreadcrumbs(self) -> List:
    '''
    Return breadcrumbs list.

    Returns:
    breadcrumbs(list): The list of posix of breadcrumbs and their values
    '''
    return self.__breadcrumbs

  def getMatrixWithBreadcrumbs(self, matrix, coordinates_value_list):
    '''
    '''
    for coord, value in coordinates_value_list:
      x, y, val = coord[0], coord[1], value
      matrix[x][y] = val
    return matrix

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    