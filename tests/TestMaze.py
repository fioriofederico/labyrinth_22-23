import sys
# Search modules and pack in the folder above 
sys.path.append('../')

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