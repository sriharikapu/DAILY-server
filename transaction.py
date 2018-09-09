import json
import web3
from web3 import Web3
from web3.contract import ConciseContract
import _thread
import logging

def send(send):

  email = send.get('email')
  to = send.get('to')
  amount = send.get('amount')
  address = send.get('address')
  signature = send.get('signature')

  import settings
  mydb = settings.mydb 
  
  if email in mydb:
    proxy_abi = open("/app/Proxy.abi", "r").read().replace('\n','')
    contract_address = email[email]['proxy_address']
        
    w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/KZSQapS5wjr4Iw7JhgtE"))
    private_key = "4944d078bfc34676f0e4fb942e29a1c3b18c347b51d0a648e936a4953115de6c"
    acct = w3.eth.account.privateKeyToAccount("0x%s" % private_key)
    w3.eth.defaultAccount = acct 
     
    Proxy = w3.eth.contract(address=contract_address, abi=proxy_abi)

    construct_f = contract.functions.forward(Web3.toBytes(text=signature), address, to, Web3.toInt(int(float(amount))), Web3.toBytes(text=""))

    construct_tx = construct_f.buildTransaction({
      'from': acct.address,
      'nonce': w3.eth.getTransactionCount(acct.address),
      'gas': 1728712,
      'gasPrice': w3.toWei('21', 'gwei')})
    
    signed = acct.signTransaction(construct_tx)
    tx = w3.eth.sendRawTransaction(signed.rawTransaction)

    return tx

  return "no"
