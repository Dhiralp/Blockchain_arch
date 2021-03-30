# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 10:29:18 2020

@author: dhiral
"""

import block as bl
import os
    

while(True):
    trans = 0
    process = 0
    for r,d,f in os.walk(os.getcwd()+"//Pending transaction"):
        trans = len(f)
    print("\n\nCurrently there are "+str(trans)+" pending transactions")
    for r,d,f in os.walk(os.getcwd()+"//Processed Transaction"):
        process = len(f)
    print("Currently there are "+str(process)+" processed transactions")
    print("--------------Menu------------")
    print("1. Process a transaction")
    print("2. Exit")
   # print("Currently there are "+str(len(trans))+" pending transactions.")
    ch = int(input("Your Choice : "))
    
    if ch == 1:
        bl.read_transactions()
    elif ch == 2:
        break;
    else:
        print("Please Try again ")
    
