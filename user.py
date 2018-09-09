import json
import web3
from web3 import Web3
from web3.contract import ConciseContract
import _thread
import logging
import numpy as np

def new(user):
  
  email = user.get('email')
  address = user.get('address')
  import settings
  mydb = settings.mydb
  w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/KZSQapS5wjr4Iw7JhgtE"))
  private_key = "4944d078bfc34676f0e4fb942e29a1c3b18c347b51d0a648e936a4953115de6c"
  acct = w3.eth.account.privateKeyToAccount("0x%s" % private_key)
  w3.eth.defaultAccount = acct
  #database.init()
 #mydb = pickledb.load('/data/my.db', False)

  #logger = logging.getLogger('user')
  #logger.info("email: %s" % email)
  #logger.info("address: %s" % address)

  if not email in mydb:
    oroxy_abi = open("/app/Proxy.abi", "r").read().replace('\n','')

    #contract = file_object  = open("/app/SignatureBouncer.sol", "r")

    # TODO: add pub key

    #compiled_sol = compile_source(contract) # Compiled source code
    #contract_interface = compiled_sol['<stdin>:Greeter']

    try:
      proxy_abi = open("/app/Proxy.abi", "r").read().replace('\n','')
      abi = open("/app/Factory.abi", "r").read().replace('\n','')
    #bytecode = open("/app/SignatureBouncer.byte", "r").read().replace('\n','').encode("utf-8").hex()
    #bytecode = Web3.toHex(text=open("/app/SignatureBouncer.byte", "r").read().replace('\n',''))
      bytecode = open("/app/Factory.byte", "r").read().replace('\n','')

#  w3 = Web3(Web3.EthereumTesterProvider())
    #w3.eth.defaultAccount = w3.eth.accounts[0]

      Factory = w3.eth.contract(abi=abi, bytecode=bytecode)
      construct_tx = Factory.constructor().buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')})

      signed = acct.signTransaction(construct_tx)

      dictionary = {}
      dictionary["address"] = address
    
      tx = w3.eth.sendRawTransaction(signed.rawTransaction)
    
      def waitForResult(tx_hash):
        contract_tx = w3.eth.waitForTransactionReceipt(tx_hash)
        dictionary["contract"] = contract_tx.contractAddress
        cont = w3.eth.contract(address=contract_tx.contractAddress, abi=abi)
        dictionary["proxy_address"] = cont.functions.libraryAddress().call({'from': acct.address})
        proxy = w3.eth.contract(address=dictionary["proxy_address"], abi=proxy_abi)
        t = proxy.functions.init(address, address).buildTransaction({
          'from': acct.address,
          'nonce': w3.eth.getTransactionCount(acct.address),
          'gas': 1728712,
          'gasPrice': w3.toWei('21', 'gwei')})
        s = acct.signTransaction(t)
        w3.eth.sendRawTransaction(s.rawTransaction)
        mydb[email] = dictionary
        np.save('dict.npy', mydb)

      _thread.start_new_thread(waitForResult, (tx,))

      return tx.hex()

    except Exception as e:
      return "ERROR: %s" % e

  return "no"
