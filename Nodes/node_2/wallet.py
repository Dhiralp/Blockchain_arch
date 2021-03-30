# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 09:30:11 2020

@author: dhiral
"""

from Crypto.PublicKey import RSA
import os
import hashlib
import json


class wallet_class:

    def __init__(self,path):
        self.path = path
        self.create_prv_pub(self.path)
        self.user_config(self.path)
        json_dict = self.get_dict(self.path)
        print("\nCurrent Wallet owned by : ",json_dict["Username"])
        print("Current Wallet address : ",json_dict["Address"])
        print("Your current balance is : ",self.get_dict(self.path)["Current Balance"])

    def create_prv_pub(self,path):
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



    def write_json(self,path,json_dict):
        json_object = json.dumps(json_dict)   
        f = open(path+"\\user_config.json","w+")
        f.write(json_object)
        f.close()
    
    def get_public(self,path):
        f = open(path+"\\public.pem", "r+")
        public = f.read()
        f.close()
        return public

    def user_config(self,path):
        json_dict = {}
        conf = 0
        for r,d,f in os.walk(path):
            if "user_config.json" in f:
                conf = 1
        if conf == 0:
            dirs = path.split("\\")
            json_dict["Username"] = dirs[len(dirs)-1]
            public = self.get_public(path)
            hash_op = hashlib.sha256(public.encode()).hexdigest()
            json_dict["Address"] = hash_op
            json_dict["Current Balance"] = 100
            self.write_json(path,json_dict)
        
            
    def get_dict(self,path):
        f = open(path+"\\user_config.json","r+")
        #print(f.read())
        json_dict = json.loads(f.read())
        return json_dict


    def get_dirs():
        for r,d,f in os.walk("\\".join(os.getcwd().split("\\")[:-1])):
            return d
    
    def get_prev_dir():
        return "\\".join(os.getcwd().split("\\")[:-1])

    





    
    
