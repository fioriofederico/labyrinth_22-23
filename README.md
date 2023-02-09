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
* Whichever choice you make, relaunch the code

## Example of a json file for a maze
```json
{
    "larghezza": 5,
    "altezza": 5,
    "pareti": [
        {
            "orientamento": "H",
            "posizione": [
                0,
                2
            ],
            "lunghezza": 3
        },
        {
            "orientamento": "H",
            "posizione": [
                4,
                0
            ],
            "lunghezza": 2
        },
        {
            "orientamento": "H",
            "posizione": [
                4,
                3
            ],
            "lunghezza": 2
        },
        {
            "orientamento": "v",
            "posizione": [
                0,
                0
            ],
            "lunghezza": 2
        },
        {
            "orientamento": "v",
            "posizione": [
                3,
                0
            ],
            "lunghezza": 2
        },
        {
            "orientamento": "v",
            "posizione": [
                0,
                2
            ],
            "lunghezza": 2
        },
        {
            "orientamento": "v",
            "posizione": [
                0,
                4
            ],
            "lunghezza": 5
        }
    ],
    "iniziali": [
        [
            2,
            0
        ],
        [
            0,
            1
        ]
    ],
    "finale": [
        [
            4,
            2
        ]
    ],
    "costi": [
        [
            2,
            2,
            90
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
