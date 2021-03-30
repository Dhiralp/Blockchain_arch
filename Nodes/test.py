# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 04:58:52 2020

@author: dhiral
"""
import subprocess


process = subprocess.Popen(["python","puzzle.py",'{"Height": 0, "Root Hash": "65df595f4513cc36871ba8421bc0d56c2cdd92edff59875555add97620c3bdc0", "Previous Hash": "0000000000000000000000000000000000000000000000000000000000000000", "Time": "2020-11-20 08:52:32.721908", "Target": "000", "Nonce": "0"}'], stdout=subprocess.PIPE,creationflags=subprocess.CREATE_NEW_CONSOLE)


#
stdout = process.communicate()[0]
print("Here : "+str(stdout.decode()))
process.kill()