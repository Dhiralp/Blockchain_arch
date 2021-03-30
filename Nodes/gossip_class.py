# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 08:12:59 2020

@author: dhiral
"""

import random
import socket
from threading import Thread
import time
import hashlib
import os
import json
import block as bl
import shutil
from os import path

class GossipNode:
    # hold infected nodes
    infected_nodes = []

    # initialization method.
    # pass the port of the node and the ports of the nodes connected to it
    
    def __init__(self, port, connected_nodes, file_path):
        
        self.node = socket.socket(type=socket.SOCK_DGRAM)
        self.hostname = socket.gethostname()
        self.port = port
        self.node.bind((self.hostname, self.port))
        self.susceptible_nodes = connected_nodes
        self.backup = [i for i in self.susceptible_nodes]
        self.path = file_path
        print("Node started on port {0}".format(self.port))
        print("Susceptible nodes =>", self.susceptible_nodes)

        # call the threads to begin the magic
        self.start_threads()

    def save_file(self,message):
        
        hash_op = hashlib.sha256(message.encode()).hexdigest()
        name = str(hash_op)+'.json'
        if not os.path.isdir(self.path+'//Pending Transactions//'):
                os.mkdir(self.path+'//Pending Transactions//')
        if path.isdir(self.path + "\\Pending Transactions\\"+name):
            return
        for r,d,f in os.walk(self.path+"\\Pending Transactions\\"):
            if len(f) > 5:
                try:
                    bl.read_transactions(self.path + "\\Pending Transactions")
                except Exception:
                    continue
            else:
                if path.isdir("//".join(self.path.split("\\")[:-1])+'//temp//'):
                    shutil.rmtree("//".join(self.path.split("\\")[:-1])+'//temp//', ignore_errors=True)
        fo = open(self.path + "\\Pending Transactions\\"+name,"w+")
        blocks = json.loads(message)
        fo.write(message)
        fo.close()
        print("Send block from : "+"//".join(self.path.split("\\")[:-1])+'//BlockChain//')
        for r,d,f in os.walk("//".join(self.path.split("\\")[:-1])+'//BlockChain//'):
            if len(f)>0:
                print(f)
                for blocks in f:
                    fo = open("//".join(self.path.split("\\")[:-1])+'//BlockChain//'+blocks)
                    #print(blocks + "   :     "+fo.read())
                    self.transmit_message(fo.read())
        #self.read_transactions(self.path)
        
        
    def save_config_file(self, data):
        fo = open(self.path + "\\communication_log.txt","a+")
        fo.write("\n"+data)
        fo.close()
        
    def input_message(self):
        while True:            
            message_to_send = input("Enter  content:\n")
            if message_to_send == 'exit':
                quit()
            self.transmit_message(message_to_send)
    def receive_message(self):
        while True:
            exists = 0
            bl_ext = 0
            try:
                message_to_forward, address = self.node.recvfrom(2048)
            except socket.error:
                continue;
            message = message_to_forward.decode('ascii')
            block = json.loads(message)
            print("Recv : "+message)
            if 'Block header' in block:
                print(type(block['Block header']))
                print(type(block['Block Body']))
                message_body = json.dumps(block)
                msg_js = json.dumps(block['Block header'])   
                hash_op = hashlib.sha256(msg_js.encode()).hexdigest()
                name = hash_op+'.json'
                print("Path here is : "+"//".join(self.path.split("\\"))+'//Local Block//')
                if not os.path.isdir("//".join(self.path.split("\\"))+'//Local Block//'):
                    os.mkdir("//".join(self.path.split("\\"))+'//Local Block//')
                for r,d,f in os.walk("//".join(self.path.split("\\"))+'//Local Block//'):
                    print("names : "+str(f))
                    if name in f:
                        bl_ext = 1
                if bl_ext == 0:
                    fo2 = open(self.path + "//Local Block//"+name,"w+")                    
                    fo2.write(message_body)
                    fo2.close()
                    self.transmit_message(message_body)
                    bl_ext = 1
            else:
                hash_op = hashlib.sha256(message.encode()).hexdigest()
                if not os.path.isdir(self.path+'//Pending Transactions//'):
                    os.mkdir(self.path+'//Pending Transactions//')
                for r,d,f in os.walk(self.path+'//Pending Transactions//'):
                    if str(hash_op)+'.json' in f:
                        exists = 1
                    #self.node.sendto("File already exists".encode('ascii'), (self.hostname, int(address[1])))
                if exists == 0:
                #self.susceptible_nodes.remove(address[1])
                    tim = time.ctime(time.time())
                    GossipNode.infected_nodes.append(address[1])
                    print("\nMessage is: '{0}'.\nReceived at [{1}] from [{2}]\n"
                          .format(message_to_forward.decode('ascii'), tim, address[1]))
                    
                    log = 'Time : '+tim + '\t Receiver : ' + str(self.port) + '\t  Sender : '+str(address[1]) + '\t Data : '+message_to_forward.decode('ascii')[:10]
                    self.save_config_file(log)
                    self.transmit_message(message_to_forward.decode('ascii'))
                    self.save_file(message_to_forward.decode('ascii'))
                    exists = 1
        self.susceptible_nodes = [i for i in self.backup]
        

    def transmit_message(self, message):        
        
        while self.susceptible_nodes:
            selected_port = random.choice(self.susceptible_nodes)
            tim = time.ctime(time.time())
            print("\n")
            print("-"*50)
            print("Susceptible nodes =>", self.susceptible_nodes)
            print("Infected nodes =>", GossipNode.infected_nodes)
            print("Port selected is [{0}]".format(selected_port))
            message = message #+"\n"+str(time.ctime(time.time()))
            try:
                self.node.sendto(message.encode('ascii'), (self.hostname, selected_port))
            except socket.error:
                print ("Caught exception socket.error :")
                continue;
            hash_op = hashlib.sha256(message.encode()).hexdigest()
            if not os.path.isdir(self.path+'//Pending Transactions//'):
                os.mkdir(self.path+'//Pending Transactions//')
            
            self.susceptible_nodes.remove(selected_port)
            GossipNode.infected_nodes.append(selected_port)
            log = 'Time : '+tim + '\t Receiver : ' + str(selected_port) + '\t  Sender : '+str(self.port) + '\t Data : '+message[:10]
            self.save_config_file(log)
            print("Message: '{0}' sent to [{1}].".format(message, selected_port))
            print("Susceptible nodes =>", self.susceptible_nodes)
            print("Infected nodes =>", GossipNode.infected_nodes)
            print("-"*50)
            print("\n")
            
        self.susceptible_nodes = [i for i in self.backup]

    def start_threads(self):
        
        Thread(target=self.input_message).start()
        Thread(target=self.receive_message).start()