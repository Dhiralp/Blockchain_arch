# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 09:30:11 2020

@author: dhiral
"""

from Crypto.PublicKey import RSA
import os
import hashlib
import json
import transaction as tran



def create_prv_pub(path):
    private = 0
    public = 0
    for r,d,f in os.walk(path):
        for i in f:
            if "private" in i and i.endswith(".pem"):
                private = 1
            elif "public" in i and i.endswith(".pem"):
                public = 1
    if private == 0 or public == 0:  
        key = RSA.generate(1024)
        f = open(path+"\\private.pem", "wb")
        f.write(key.exportKey('PEM'))
        f.close()
        
        pubkey = key.publickey()
        f = open(path+"\\public.pem", "wb")
        f.write(pubkey.exportKey('OpenSSH'))
        f.close()



def write_json(path,json_dict):
    json_object = json.dumps(json_dict)   
    f = open(path+"\\user_config.json","w")
    f.write(json_object)
    f.close()
    
def get_public(path):
    f = open(path+"\\public.pem", "r")
    public = f.read()
    f.close()
    return public

def user_config(path):
    conf = 0
    for r,d,f in os.walk(path):
        if "user_config.json" in f:
            conf = 1
    if conf == 0:
        dirs = path.split("\\")
        json_dict["Username"] = dirs[len(dirs)-1]
        public = get_public(path)
        hash_op = hashlib.sha256(public.encode()).hexdigest()
        json_dict["Address"] = hash_op
        json_dict["Current Balance"] = 100
        write_json(path,json_dict)
        

    
            
def get_dict(path):
    f = open(path+"\\user_config.json","r")
    json_dict = json.loads(f.read())
    return json_dict


def get_dirs():
    for r,d,f in os.walk("\\".join(os.getcwd().split("\\")[:-1])):
        return d
    
def get_prev_dir():
    return "\\".join(os.getcwd().split("\\")[:-1])


json_dict = get_dict(os.getcwd())
create_prv_pub(os.getcwd())
user_config(os.getcwd())


print("\nCurrent Wallet owned by : ",json_dict["Username"])
print("Current Wallet address : ",json_dict["Address"])
print("\n\n-------------------MENU--------------------")
print("\n1. Check their current balance of the \"currency\" owned by the wallet")
print("\n2. Check the current balance of the \"currency\" owned by another wallet by providing the address for that wallet")
print("\n3. Create a transaction to send some \"currency\" to a specified wallet address")
ch = int(input("Your Choice : "))

if ch == 1:
    print("Your current balance is : ",get_dict(os.getcwd())["Current Balance"])
    
    
if ch == 2:
    print("\nUsers : ")
    usr_dict = {}
    dirs = get_dirs()
    count = 1
    for i in dirs:
        if i != json_dict["Username"] and not i.endswith("__") and "Pending transaction" not in i and "Processed transaction" not in i and "Digital Signatures" not in i:
            print(str(count), ". ",i)
            usr_dict[count] = i
            count = count + 1
    usr = int(input("\nChoose a user :"))
    create_prv_pub(get_prev_dir()+"\\"+usr_dict[usr])
    user_config(get_prev_dir()+"\\"+usr_dict[usr])
    json_dict = get_dict(get_prev_dir()+"\\"+usr_dict[usr])
    print("Wallet owned by : ",json_dict["Username"])
    print("Wallet Balance : ",json_dict["Current Balance"])

if ch == 3:
    tran.transaction(os.getcwd())