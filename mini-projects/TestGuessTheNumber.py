__author__ = 'sachin'

import os
import sys
print "PYTHONPATH=", os.environ['PYTHONPATH'].split(os.pathsep)
print "PROJECT_HOME=", os.environ['PROJECT_HOME'].split(os.pathsep)

sys.path.append("./Library")


import GuessTheNumber
