__author__ = 'sachin'

import os
import sys
print "PYTHONPATH=", os.environ['PYTHONPATH'].split(os.pathsep)
print "PROJECT_HOME=", os.environ['PROJECT_HOME'].split(os.pathsep)

library = os.environ['PROJECT_HOME'] + "/Library"
os.environ["PATH"] += os.pathsep + library
sys.path.append(library)


#Sample test file
import Pong
