# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 08:57:28 2020

@author: dhiral
"""
import os
import sys
sys.path.insert(1,  '\\'.join(os.getcwd().split('\\')))
from gossip_class import GossipNode
from wallet import wallet_class

wal = wallet_class(os.getcwd()+'\\node_4')


# port for this node
port = 5013
# ports for the nodes connected to this node
connected_nodes = [5011,5014]

node = GossipNode(port, connected_nodes,os.getcwd()+'\\node_4')