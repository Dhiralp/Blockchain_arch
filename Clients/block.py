# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 16:07:29 2020

@author: dhiral
"""
import os
import json
import datetime
import hashlib
import base64
from Crypto.PublicKey import RSA


final_files = []

def write_json(path,json_dict):
    json_object = json.dumps(json_dict)   
    f = open(path+"\\user_config.json","w")
    f.write(json_object)
    f.close()

def get_dict(path):
    f = open(path+"\\user_config.json","r")
    json_dict = json.loads(f.read())
    return json_dict

def verify(publickey,data,sign):
     return publickey.verify(data,(int(base64.b64decode(sign)),))

    
def read_transactions():
    path = os.getcwd()+"//Pending Transaction//"
    unver_files = []
    for r,d,f in os.walk(path):
        transactions = f
        if len(f)<1:
            return
    veri_trans = []
    ids = {}
    for r,d,f in os.walk(os.getcwd()):
        for i in d:
            if not i.endswith("__") and "Pending transaction" not in i and "Processed transaction" not in i:
                ids[i] = json.loads(open(os.getcwd()+'//'+i+'//user_config.json','r').read())['Address']
                
    sender = {}
    receiver = {}
    for i in transactions:
        with open(path+i) as f:
            data = json.load(f)
            sign = data['Signature'].encode('utf-8')
            digit = {}
            for j in data:
                digit[j] = data[j]
            del data['Signature']
            for addr in ids:
                if ids[addr] == data['From']:
                    sender = get_dict(os.getcwd()+"\\"+addr)
                elif ids[addr] == data['To']:
                    receiver = get_dict(os.getcwd()+"\\"+addr)
            publickey = RSA.importKey(open(os.getcwd()+"\\"+sender["Username"]+"\\"+"\\public.pem",'r').read())
            #print(verify(publickey,hashlib.sha256(str(data).encode()).hexdigest().encode(),sign))
            #print(data)    #Data
            #print(i)   #File name
            if verify_transaction(i,digit) and verify(publickey,hashlib.sha256(str(data).encode()).hexdigest().encode(),sign):
                veri_trans.append(digit)
                print(sender)
                print(receiver)
                sender["Current Balance"] = int(sender["Current Balance"]) - int(data["Amount"])
                receiver["Current Balance"] = int(receiver["Current Balance"]) + int(data["Amount"])
                write_json(os.getcwd()+"\\"+sender["Username"],sender)
                write_json(os.getcwd()+"\\"+receiver["Username"],receiver)
            else:
                print(i+" will be deleted as it failed to verify")
                unver_files.append(i)
    for i in unver_files:
        os.remove(path+i)
    files = []
    count = 0
    if len(veri_trans) < 1:
        return
    for i in veri_trans:
        files.append(str(i).encode('utf-8'))
    m = hashlib.sha256()
    if len(files)%2 == 0:
       even_hashing(count,m,files)
    else:
        odd_hashing(count,m,files)
    final_json = {}
    for r,d,f in os.walk(os.getcwd()+"\\Processed transaction"):
        final_json["Height"] = len(f)
    final_json["Root Hash"] = str(final_files[len(final_files)-1])
    final_json["Previous Hash"] = prev_hash()
    #final_json["Height"] = math.ceil(len(files)/2)+1
    final_json["Time"] = str(datetime.datetime.now())
    #print(final_json)
    print(veri_trans)
    process_trans(final_json,veri_trans)
    delete_transactions()
    
def process_trans(final_json,veri_trans):
    root_json = {}
    root_json["Block header"] = final_json
    root_json["Block Body"] = []
    for r,d,f in os.walk(os.getcwd()+"\\Pending Transaction\\"):
        for i in f:
            root_json["Block Body"].append(i)
    json_object = json.dumps(root_json)   
    name_json = json.dumps(root_json["Block header"])   
    hash_op = hashlib.sha256(name_json.encode()).hexdigest()
    name = str(hash_op)+'.json'
    fo = open(os.getcwd() + "\\Processed transaction\\"+name,"w")
    fo.write(str(json_object))
    fo.close()

def delete_transactions():
    for r,d,f in os.walk(os.getcwd()+"\\Pending Transaction\\"):
        for i in f:
            os.remove(os.getcwd()+"\\Pending Transaction\\"+i)

def verify_transaction(name,data):
    if data["Time"] > str(datetime.datetime.now()):
        return False
    elif len(data["From"].strip()) < 1:
        return False
    elif len(data["From"].strip()) < 1:
        return False
    for i in data["Amount"]:
        if not i.isdigit():
            return False
    json_object = json.dumps(data)   
    hash_op = hashlib.sha256(json_object.encode()).hexdigest()
    if not hash_op+".json" == name:
        return False
    return True

def prev_hash():
    latest_hash = {"Hash":"","Time":""}
    if not os.path.isdir(os.getcwd() + "\\Processed transaction\\"):
        os.mkdir(os.getcwd() + "\\Processed transaction\\")
    for r,d,f in os.walk(os.getcwd() + "\\Processed transaction\\"):
        if(len(f)>0):
            for i in f:
                with open(os.getcwd()+"\\Processed transaction\\"+i) as f:
                    data = json.load(f)
                    if data["Block header"]["Time"]>latest_hash["Time"]:
                        latest_hash["Time"] = data["Block header"]["Time"]
                        latest_hash["Hash"] = i[:-5]
        else:
            latest_hash["Hash"] = '0'*64
    return latest_hash["Hash"]

def odd_hashing(count,m,files):
    #print('Odd files : ',len(files))
    new_data = files[len(files)-1]
    files.append(new_data)
    even_hashing(count,m,files)


def even_hashing(count,m,files):
    
    file2 = []
    
    if files:
        #print('Even files : ',len(files))
        if len(files)>2:
            for i in range(0,len(files),2):
                hash2 = even_hashing(count,m,files[i:i+2])
                file2.append(hash2)
            
            #print('File_2',len(file2)) 
            if len(file2)%2 == 0:
                even_hashing(count,m, file2)
            else:
                odd_hashing(count,m,file2)
        elif len(files) == 2:
            m.update(files[0])
            h1 = m.hexdigest()
            m.update(files[1])
            h2 = m.hexdigest()
            m.update((h1+h2).encode())
            final_files.append(m.hexdigest())
            return m.hexdigest()