from web3 import Web3, HTTPProvider
import os

def get_w3():
    return Web3(HTTPProvider('https://'+os.environ['ETH_NETWORK']+'.infura.io/v3/'+os.environ['INFURA_API_KEY']))

def handle_transaction(txn_func, *args, **kwargs):
    """Handles a transaction that updates the contract state by locally
    signing, building, sending the transaction and returning a transaction
    receipt.

    >>> credentials = {
    ... 	"gas_payer": "0x1413862C2B7054CDbfdc181B83962CB0FC11fD92",
    ... 	"gas_payer_priv": "28e516f1e2f99e96a48a23cea1f94ee5f073403a1c68e818263f0eb898f1c8e5"
    ... }
    >>> rep_oracle_pub_key = b"2dbc2c2c86052702e7c219339514b2e8bd4687ba1236c478ad41b43330b08488c12c8c1797aa181f3a4596a1bd8a0c18344ea44d6655f61fa73e56e743f79e0d"
    >>> job = Job(credentials=credentials, escrow_manifest=manifest)
    >>> job.launch(rep_oracle_pub_key)
    True

    >>> gas = 4712388
    >>> hmt_amount = int(job.amount * 10**18)
    >>> hmtoken_contract = get_hmtoken()
    >>> txn_func = hmtoken_contract.functions.transfer
    >>> func_args = [job.job_contract.address, hmt_amount]
    >>> txn_info = {
    ... "gas_payer": job.gas_payer,
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
    gas_payer = kwargs["gas_payer"]
    gas_payer_priv = kwargs["gas_payer_priv"]
    gas = kwargs["gas"]

    w3 = get_w3()
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
