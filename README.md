# Labyrinth

Final examination of the course of Programmazione, accademic year 2022/2023.

This project was developed by (Alphabetical order):

- Calandra Vincenzo Maria
- Fiorio Federico
- Papa Eleonora

under the supervision of Professor Iannello Giulio.

## How to install the environment?
First of all you must have conda as python package manager, you can find it [here](https://docs.conda.io/en/latest/miniconda.html).
After you have installed and configured it, you have to run the following command.

```console
foo@bar:~$ conda env create -f env.yml
```

After that you can activate your conda env.

```console
foo@bar:~$ conda activate maze
```

## How it works
Go to the principal folder and launch the code main.py. In the terminal you will have 3 options, choose the one you prefer:
1. Create Maze
    - For example:
    - Enter your choice: 1
    - Insert the height of the maze: 10
    - Insert the width of the maze: 10
    - Insert the start point as a list: 10 2
    - Do you want to add another start point? (yes/no): no 
    - Insert the goal point as a list: 8 4
    - Do you want to add breadcrumps? (0/1): 1
    - Insert the breadcrump (x y weight): 2 2 1
    - Do you want to add another breadcrump? (0/1): 1
    - Insert the breadcrump (x y weight): 4 3 5
    - Do you want to add another breadcrump? (0/1): 1
    - Insert the breadcrump (x y weight): 3 5 2
    - Do you want to add another breadcrump? (0/1): 0
    - Il percorso migliore è:
    - [(1, 8), (2, 8), (2, 7), (3, 7)]
2. Upload image 
    - For example:
    - Enter your choice: 2
    - Enter the path of the image on tiff: ./img_input/30-20_marked.tiff
3. Upload JSON
    - For example:
    - Enter your choice: 3
    - Enter the path of the json file: ./indata/20-10_marked.json

<b>Note</b>, consider the three implementation methods before you run your code.
* If you choose to create the maze, remember to stay in the borders when assigning variables
* If you choose to create a maze from an image make sure to insert the image in the "img_input" folder because the program will draw the maze on the last inserted image

# Example of a json file for a maze
```json
{
   "larghezza": 41,
   "altezza": 21,
   "pareti": [
      {
         "orientamento": "H",
         "posizione": [
            0,
            0
         ],
         "lunghezza": 19
      },
      {
         "orientamento": "H",
         "posizione": [
            0,
            20
         ],
         "lunghezza": 21
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            0
         ],
         "lunghezza": 20
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            14
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            18
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            20
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            26
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            30
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            34
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            36
         ],
         "lunghezza": 8
      },
      {
         "orientamento": "V",
         "posizione": [
            1,
            40
         ],
         "lunghezza": 20
      },
      {
         "orientamento": "H",
         "posizione": [
            2,
            2
         ],
         "lunghezza": 5
      },
      {
         "orientamento": "H",
         "posizione": [
            2,
            8
         ],
         "lunghezza": 7
      },
      {
         "orientamento": "V",
         "posizione": [
            2,
            16
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            2,
            22
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            2,
            27
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            2,
            31
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            2,
            38
         ],
         "lunghezza": 11
      },
      {
         "orientamento": "V",
         "posizione": [
            3,
            2
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            3,
            6
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            3,
            8
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            3,
            22
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            4,
            4
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            4,
            9
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            4,
            14
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            4,
            17
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "H",
         "posizione": [
            4,
            24
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            4,
            28
         ],
         "lunghezza": 7
      },
      {
         "orientamento": "V",
         "posizione": [
            5,
            28
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "V",
         "posizione": [
            5,
            30
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            6,
            3
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            6,
            7
         ],
         "lunghezza": 12
      },
      {
         "orientamento": "H",
         "posizione": [
            6,
            22
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "V",
         "posizione": [
            6,
            32
         ],
         "lunghezza": 5
      },
      {
         "orientamento": "V",
         "posizione": [
            7,
            4
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            7,
            22
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            7,
            24
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "H",
         "posizione": [
            8,
            1
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            8,
            5
         ],
         "lunghezza": 8
      },
      {
         "orientamento": "H",
         "posizione": [
            8,
            14
         ],
         "lunghezza": 9
      },
      {
         "orientamento": "H",
         "posizione": [
            8,
            26
         ],
         "lunghezza": 7
      },
      {
         "orientamento": "H",
         "posizione": [
            8,
            34
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "V",
         "posizione": [
            9,
            8
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            9,
            12
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            9,
            14
         ],
         "lunghezza": 10
      },
      {
         "orientamento": "H",
         "posizione": [
            10,
            2
         ],
         "lunghezza": 5
      },
      {
         "orientamento": "V",
         "posizione": [
            10,
            10
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            10,
            16
         ],
         "lunghezza": 9
      },
      {
         "orientamento": "V",
         "posizione": [
            10,
            26
         ],
         "lunghezza": 9
      },
      {
         "orientamento": "H",
         "posizione": [
            10,
            29
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            10,
            33
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            11,
            2
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            11,
            36
         ],
         "lunghezza": 8
      },
      {
         "orientamento": "H",
         "posizione": [
            12,
            4
         ],
         "lunghezza": 7
      },
      {
         "orientamento": "H",
         "posizione": [
            12,
            15
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "H",
         "posizione": [
            12,
            20
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            12,
            27
         ],
         "lunghezza": 8
      },
      {
         "orientamento": "H",
         "posizione": [
            12,
            39
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            13,
            4
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            13,
            18
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "V",
         "posizione": [
            13,
            22
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            13,
            34
         ],
         "lunghezza": 8
      },
      {
         "orientamento": "H",
         "posizione": [
            14,
            1
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            14,
            6
         ],
         "lunghezza": 7
      },
      {
         "orientamento": "V",
         "posizione": [
            14,
            16
         ],
         "lunghezza": 7
      },
      {
         "orientamento": "H",
         "posizione": [
            14,
            19
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            14,
            23
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "H",
         "posizione": [
            14,
            28
         ],
         "lunghezza": 5
      },
      {
         "orientamento": "H",
         "posizione": [
            14,
            37
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            15,
            6
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            15,
            12
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            15,
            28
         ],
         "lunghezza": 6
      },
      {
         "orientamento": "V",
         "posizione": [
            15,
            32
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "H",
         "posizione": [
            16,
            2
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            16,
            8
         ],
         "lunghezza": 5
      },
      {
         "orientamento": "H",
         "posizione": [
            16,
            20
         ],
         "lunghezza": 5
      },
      {
         "orientamento": "H",
         "posizione": [
            16,
            29
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            16,
            38
         ],
         "lunghezza": 5
      },
      {
         "orientamento": "V",
         "posizione": [
            17,
            2
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "V",
         "posizione": [
            17,
            20
         ],
         "lunghezza": 4
      },
      {
         "orientamento": "V",
         "posizione": [
            17,
            22
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            18,
            4
         ],
         "lunghezza": 7
      },
      {
         "orientamento": "V",
         "posizione": [
            18,
            12
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            18,
            24
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "H",
         "posizione": [
            18,
            30
         ],
         "lunghezza": 3
      },
      {
         "orientamento": "V",
         "posizione": [
            19,
            4
         ],
         "lunghezza": 2
      },
      {
         "orientamento": "H",
         "posizione": [
            20,
            1
         ],
         "lunghezza": 20
      },
      {
         "orientamento": "H",
         "posizione": [
            20,
            22
         ],
         "lunghezza": 19
      }
   ],
   "iniziali": [
      [
         0,
         19
      ]
   ],
   "finale": [
      [
         20,
         21
      ]
   ],
   "costi": [
      [
         9,
         25,
         15
      ],
      [
         10,
         25,
         10
      ],
      [
         12,
         19,
         15
      ],
      [
         13,
         24,
         15
      ]
   ]
}
```

To run the application:
```console
foo@bar:~$ python main.py
```

## How to run unittest
To run unittest you can execute the TestMaze.py under test directory to run all test like:
```console
foo@bar:~$ python TestMaze.py
```
Or you can run directly the module you want to test, if the module contains a main with doctest import, with the following command:
```python
# maze.py

# ...

if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

<br>

```console
foo@bar:~$ python maze.py -v
```

Or if the module doesnt contains the doctest import:

```console
foo@bar:~$ python -m doctest maze.py -v
```
## Some useful information
Here you can find a diagram that graph possible functionalities of this tool.
![](./diagram/usecase.drawio.png)
