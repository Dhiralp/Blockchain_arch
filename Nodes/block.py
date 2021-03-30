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
import shutil

final_files = []

def solve_puzzle(path,block):
    found = False
    target = block["Target"]
    nonce = int(block["Nonce"])
    #print("Path : "+path)
    path = "//".join(path.split("\\")[:-2])+"//temp//"
    #print("Path : "+path)
    init_files = 0
    if not os.path.isdir(path):
        os.mkdir(path)
    files = init_files
    x = {}
    x['found'] = 0
    print("\nInitfiles : "+str(init_files))
    while (not found) and (files == init_files):
        for r,d,f in os.walk(path):
            files = len(f)
            if files != init_files:
                x['found'] = 1
                break
        block["Nonce"] = str(nonce)
        jsonvalue=json.dumps(block)
        #print(jsonvalue)
        blockhash=hashlib.sha256(jsonvalue.encode('utf-8')).hexdigest()
        #print(blockhash)
        if str(blockhash)[0:len(target)]==target:
            found=True 
        nonce=nonce+1
        #print("Nonce : ",str(blockhash)[0:len(target)])
        print("Files : "+str(files))
    block["Nonce"] = str(nonce)
    x['Block'] = block
    return x

    
def write_json(path,json_dict):
    json_object = json.dumps(json_dict)   
    f = open(path+"\\user_config.json","w")
    f.write(json_object)
    f.close()

def get_dict(path):
    f = open(path+"\\user_config.json","r")
    #print(f.read())
    json_dict = json.loads(f.read())
    return json_dict

def verify(publickey,data,sign):
     return publickey.verify(data,(int(base64.b64decode(sign)),))

def coin_based_transaction(path):
    tran_dict = {}
    tran_dict["Time"] = str(datetime.datetime.now())
    tran_dict["From"] = " "
    parent_path = path.split("\\")[:-1]
    print("\n\n\nParent Path : ",parent_path)
    parent_path = "\\".join(parent_path)
    node_dir = get_dict(parent_path)
    tran_dict["To"] = node_dir['Address']
    tran_dict["Amount"] = "10"
    tran_dict["Signature"] = " "
       
    #tran_dict = json.dumps(tran_dict)   
    #hash_op = hashlib.sha256(tran_dict.encode()).hexdigest()
    return str(tran_dict).encode('utf-8')

def read_transactions(path):
    #path = os.getcwd()+"//Pending Transaction//"
    #print("Path : "+str(path))
    unver_files = []
    for r,d,f in os.walk(path):
        transactions = f
        if len(f)<1:
            return
    veri_trans = []
    ids = {}
    child_path = os.getcwd().split("\\")[:-1]
    child_path.append("Clients")
    child_path = "//".join(child_path)
            
    for r,d,f in os.walk(child_path):
        for i in d:
            if not i.endswith("__") and "Pending transaction" not in i and "Local Block" not in i and "BlockChain" not in i:
                ids[i] = json.loads(open(child_path+'//'+i+'//user_config.json','r').read())['Address']
    #print(transactions)      
   
    sender = {}
    receiver = {}
    for i in transactions:
        #print("Path : "+str(path+"\\"+i))
        
        with open(path+"\\"+i) as f:
            data = json.load(f)
            sign = data['Signature'].encode('utf-8')
            #print(str(sign))
            digit = {}
            for j in data:
                digit[j] = data[j]
            del data['Signature']
            for addr in ids:
                #print(child_path+"\\"+addr)
                if ids[addr] == data['From']:
                    sender = get_dict(child_path+"\\"+addr)
                elif ids[addr] == data['To']:
                    receiver = get_dict(child_path+"\\"+addr)
            publickey = RSA.importKey(open(child_path+"\\"+sender["Username"]+"\\"+"\\public.pem",'r').read())
            #print(verify(publickey,hashlib.sha256(str(data).encode()).hexdigest().encode(),sign))
            #print(data)    #Data
            #print(i)   #File name
            node = path.split("\\")
            
            node = node[len(node)-2]
            
            if verify_transaction(i,digit) and verify(publickey,hashlib.sha256(str(data).encode()).hexdigest().encode(),sign):
                veri_trans.append(digit)
                #print(sender)
               # print(receiver)
            else:
                print(i+" will be deleted as it failed to verify")
                unver_files.append(i)
    
    for i in unver_files:
        os.remove(child_path+'\\'+i)
    files = [coin_based_transaction(path)]
    count = 0

    if len(veri_trans) < 1:
        return
    for i in veri_trans:
        files.append(str(i).encode('utf-8'))
    m = hashlib.sha256()
    #print("\n\nFiles:\n")
    #print(files)
    #print("\n\n\n")
    if len(files)%2 == 0:
        even_hashing(count,m,files)
    else:
        odd_hashing(count,m,files)
    final_json = {}
    pre = path.split("\\")[:-1]
    pre = "//".join(pre)
    #print(pre)
    if not os.path.isdir(pre + "//Local Block"):
        os.mkdir(pre + "//Local Block")
    for r,d,f in os.walk(pre+"//Local Block"):
        #print("Here")
        final_json["Height"] = len(f)
    final_json["Root Hash"] = str(final_files[len(final_files)-1])
    final_json["Previous Hash"] = prev_hash(path)
    #final_json["Height"] = math.ceil(len(files)/2)+1
    final_json["Time"] = str(datetime.datetime.now())
    final_json["Target"] = '000'
    final_json["Nonce"] = '0'
    #subprocess.Popen(["python", "-i","puzzle.py",final_json])
    #print("\n\n\n\nThis is the path"+path)
    x = solve_puzzle(path,final_json)
    if x['found'] == 0:
        final_json = x['Block']
        sender["Current Balance"] = int(sender["Current Balance"]) - int(data["Amount"])
        receiver["Current Balance"] = int(receiver["Current Balance"]) + int(data["Amount"])
        write_json(child_path+"//"+sender["Username"],sender)
        write_json(child_path+"//"+receiver["Username"],receiver)
        node_dir = get_dict(pre)
        node_dir["Current Balance"] = int(node_dir["Current Balance"]) + 10
        write_json(pre,node_dir)
    else:
        delete_transactions(path)
        return
    print(final_json)
    #print(final_json)
    #print(final_json)
    #print(veri_trans)
    
    process_trans(final_json,veri_trans,path,child_path)
    delete_transactions(path)
    
def process_trans(final_json,veri_trans,path,child_path):
    root_json = {}
    root_json["Block header"] = final_json
    root_json["Block Body"] = []
    pre = path.split("\\")[:-1]
    pre = "//".join(pre)
    for r,d,f in os.walk(pre+"//Pending Transactions"):
        #print("Here")
        for i in f:
            root_json["Block Body"].append(i)
    json_object = json.dumps(root_json)   
    name_json = json.dumps(root_json["Block header"])   
    hash_op = hashlib.sha256(name_json.encode()).hexdigest()
    name = str(hash_op)+'.json'
    pre = path.split("\\")[:-2]
    pre = "//".join(pre)
    node = path.split("\\")
    node = node[len(node)-2]
    #fo = open(pre + "\\Local Block\\"+name,"w")
    if not os.path.isdir(pre + "//BlockChain"):
        os.mkdir(pre + "//BlockChain")
    if not os.path.isdir(pre + "//temp"):
        os.mkdir(pre + "//temp")
    fo2 = open(pre + "\\BlockChain\\"+name,"w")
    fo3 = open(pre + "\\temp\\"+name,"w")
    fo2.write(str(json_object))
    fo3.write(str(json_object))
    fo2.close()
    fo3.close()
    
    #fo.write(str(json_object))
    #fo.close()

def delete_transactions(path):
    #print("\n\nDelete called \n")
    pre = path.split("\\")[:-1]
    pre = "//".join(pre)
    path = pre
    #print("Delte Path : "+pre+"//Pending Transactions")
    for r,d,f in os.walk(pre+"//Pending Transactions"):
        #print(f)
        for i in f:
            if not os.path.isdir(pre+'//Processed Transactions//'):
                os.mkdir(pre+'//Processed Transactions//')
            #print("removing : "+pre+"//Pending Transactions//"+i)
            shutil.move(pre+"//Pending Transactions//"+i, pre+"//Processed Transactions//"+i) 
            

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

def prev_hash(path):
    pre = path.split("\\")[:-1]
    pre = "//".join(pre)
    path = pre
    latest_hash = {"Hash":"","Time":""}
    if not os.path.isdir(path + "\\Local Block\\"):
        os.mkdir(path + "\\Local Block\\")
    for r,d,f in os.walk(path + "\\Local Block\\"):
        if(len(f)>0):
            for i in f:
                with open(path+"\\Local Block\\"+i) as f:
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
                file2.append(hash2.encode())
            
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