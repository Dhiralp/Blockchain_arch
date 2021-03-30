# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:43:31 2020

@author: dhiral
"""

import datetime
import hashlib
import json
import os, base64
import socket
from Crypto.PublicKey import RSA


def send_to_miner(ascii_data):
    node = socket.socket(type=socket.SOCK_DGRAM)
    hostname = socket.gethostname()
    port = 5001
    node.bind((hostname, port))
    node.sendto(ascii_data, (hostname, 5010))

def get_dict(path):
    f = open(path+"\\user_config.json","r")
    json_dict = json.loads(f.read())
    return json_dict

def sign(path,data):
    key = RSA.importKey(open(path+"\\private.pem",'r').read())
    return base64.b64encode(str((key.sign(data,''))[0]).encode())



def get_dirs():
    for r,d,f in os.walk("\\".join(os.getcwd().split("\\")[:-1])):
        return d
    
def get_prev_dir():
    return "\\".join(os.getcwd().split("\\")[:-1])


def save_hash(json_dict):     
    json_object = json.dumps(json_dict)   
    send_to_miner(json_object.encode('ascii'))


def write_json(path,json_dict):
    json_object = json.dumps(json_dict)   
    f = open(path+"\\user_config.json","w")
    f.write(json_object)
    f.close()

def transaction(path):
    tran_dict = {}
    tran_dict["Time"] = str(datetime.datetime.now())
    
    sender = get_dict(path)
    print("Senders Name : ",sender["Username"])
    print("Senders Address : ",sender["Address"])
    tran_dict["From"] = sender["Address"]
    
    usr_dict = {}
    count = 1
    for r,d,f in os.walk(get_prev_dir()):
        for i in d:
            if i != sender["Username"] and not i.endswith("__") and "Pending transaction" not in i and "Processed transaction" not in i:
                print(str(count), ". ",i)
                usr_dict[count] = i
                count = count + 1
    usr = int(input("Choose another user : "))
    receiver = get_dict(get_prev_dir()+"\\"+usr_dict[usr])
    print("Receiver's Name : ",receiver["Username"])
    print("Receiver's Address : ",receiver["Address"])
    tran_dict["To"] = receiver["Address"]
    amt = int(input("Amount : "))
    #print(amt > int(sender["Current Balance"]))
    if amt < int(sender["Current Balance"]) and amt > 0:
        tran_dict["Amount"] = str(amt)
        tran_dict["Signature"] = str(sign(os.getcwd(),hashlib.sha256(str(tran_dict).encode()).hexdigest().encode()))[2:-1]
        print(tran_dict)
        save_hash(tran_dict)
        """
        write_json(path,sender)
        
        write_json(get_prev_dir()+"\\"+usr_dict[usr],receiver)"""
    else:
        print("Sender only has ",sender["Current Balance"]," to spare")
    
    



