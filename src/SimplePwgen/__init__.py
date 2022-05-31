import os

version_file = os.path.abspath(os.path.dirname(__file__))+'/VERSION'
__version__ = open(version_file, 'r').readlines()
