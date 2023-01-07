import sys
import os

# Search modules and pack in the folder above 
parent_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import doctest
import unittest

# Import Unittest from DOCTEST inside Maze class
def mazePackTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite("utilities.maze"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(mazePackTestSuite())