#!/usr/bin/python3
from web3 import Web3, HTTPProvider
import os

def get_w3():
    return Web3(HTTPProvider('https://'+os.environ['ETH_NETWORK']+'.infura.io/v3/'+os.environ['INFURA_API_KEY']))

def get_address(priv_hex):
    w3 = get_w3()
    return w3.eth.account.privateKeyToAccount(priv_hex).address

def handle_transaction(txn_func, *args, **kwargs):
    """Handles a transaction that updates the contract state by locally
    signing, building, sending the transaction and returning a transaction
    receipt.

    >>> gas = 4712388
    >>> hmtoken_contract = get_hmtoken()
    >>> txn_func = hmtoken_contract.functions.transfer
    >>> func_args = [job.job_contract.address, hmt_amount]
    >>> txn_info = {
    ... "gas_payer_priv": job.gas_payer_priv,
    ... "gas": gas
    ... }
    >>> txn_hash = handle_transaction(txn_func, *func_args, **txn_info)

    Args:
        txn_func: the transaction function to be handled.
        *args: all the arguments the function takes.
        **kwargs: the transaction data used to complete the transaction.

    Returns:
        txn_hash: ethereum transaction id (sha256 hash bytes)
    """
    gas_payer_priv = kwargs["gas_payer_priv"]
    gas = kwargs["gas"]

    w3 = get_w3()
    gas_payer = w3.eth.account.privateKeyToAccount(gas_payer_priv).address
    nonce = w3.eth.getTransactionCount(gas_payer)

    txn_dict = txn_func(*args).buildTransaction({
        'from': gas_payer,
        'gas': gas,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.signTransaction(
        txn_dict, private_key=gas_payer_priv)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash


def handle_simple_transaction(sender_priv, amount_eth, receiver_address, gas_price_gwei):
    w3 = get_w3()
    sender_address = w3.eth.account.privateKeyToAccount(sender_priv).address
    nonce = w3.eth.getTransactionCount(sender_address)
    txn_dict = {
        'nonce': nonce,
        'from': sender_address,
        'to': receiver_address,
        'value': w3.toWei(amount_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.toWei(gas_price_gwei, 'gwei'),
    }
    signed_txn = w3.eth.account.signTransaction(
        txn_dict, private_key=sender_priv)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash
