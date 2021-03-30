# Blockchain_arch

How to run:

1. Initialization:

Run wallet.py from each of the folders present in CLIENTS folder, it will create RSA public, private keys, and config file which will have name, time-stamp,balance, and address.
The address is the hash or the checksum of the public key.
You can change the balance manually from the config json file.

2. Miners:

Go to the NODES folder, and run run_5_nodes.py, it will initialize 5 miners each conected to each other in a circular format. When the transactions are processed,
each miner will solve a puzzle, the first one to finish it will get coin based transaction fee and will process all the transactions after verifying each of them after
decrypting with the key. 


3. Transaction:

Run main.py from CLIENTS folder, menu will popup to check the balance and tranfer to other users. When the transaction is made, it is saved in a json format and digital
signature is added for further verification. Then the transaction is sent to a node which forwards it to all the nodes and saved locally into a folder called "Pending transaction".

4. Processing :

When the desired amount of pending transactions are made, the miner will process all the pending transactions and make changes to each wallets of the user who are involved in the 
trasactions and update the balances. You can find the processed transactions in "Processed transaction" folder present in each nodes, and the folder "Local Block" will contain the 
blockchain with previous block, initial block, height of the chain, etc..
