from web3 import Web3
import pickledb
import numpy as np

#def mydb():
#  return pickledb.load('/data/my.db', False)

mydb = np.load('dict.npy').item() 
