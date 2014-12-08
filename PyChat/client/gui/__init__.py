import sys
from os.path import realpath, dirname

sys.path.append(dirname(realpath(__file__)) + '/..')
import error # access to error module

sys.path.append(dirname(realpath(__file__)) + '/../..')
import server # access to server package
