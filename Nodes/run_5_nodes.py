# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 19:59:00 2020

@author: dhiral
"""



"""
subprocess.Popen(["python", "test.py", "python", "test.py"])

import subprocess

process = subprocess.Popen("python node_1//node.py", creationflags=subprocess.CREATE_NEW_CONSOLE)
from subprocess import Popen,CREATE_NEW_CONSOLE,PIPE

Popen(["python", "node_1/node.py"],creationflags=CREATE_NEW_CONSOLE)
Popen(["python", "node_2/node.py"],creationflags=CREATE_NEW_CONSOLE)
"""
#bot1 = Popen(["lxterminal", "-e", "python", "-i", "node_1/node.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)

#import os
from subprocess import Popen,CREATE_NEW_CONSOLE

#run secondary script 1
Popen(["python","-i", "node_1/node.py"],creationflags=CREATE_NEW_CONSOLE)
Popen(["python","-i", "node_2/node.py"],creationflags=CREATE_NEW_CONSOLE)
Popen(["python","-i", "node_3/node.py"],creationflags=CREATE_NEW_CONSOLE)
Popen(["python","-i", "node_4/node.py"],creationflags=CREATE_NEW_CONSOLE)
Popen(["python","-i", "node_5/node.py"],creationflags=CREATE_NEW_CONSOLE)