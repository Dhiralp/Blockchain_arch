# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 04:21:53 2020

@author: dhiral
"""
import json
import hashlib
import sys
import os
import time
import block as bl


def solve_puzzle(block):
    found = False
    target = block["Target"]
    nonce = int(block["Nonce"])
    while not found:
        block["Nonce"] = str(nonce)
        jsonvalue=json.dumps(block)
        #print(jsonvalue)
        blockhash=hashlib.sha256(jsonvalue.encode('utf-8')).hexdigest()
        #print(blockhash)
        if str(blockhash)[0:len(target)]==target:
            found=True 
        nonce=nonce+1
        #print("Nonce : ",str(blockhash)[0:len(target)])
        #print("\n")
    block["Nonce"] = str(nonce)
    print(nonce)
solve_puzzle(json.loads(sys.argv[1]))

