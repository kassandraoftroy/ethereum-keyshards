from eth_tx import handle_simple_transaction
from shamir_prime import Share, interpolate_at_zero
import json, binascii

'''
NOTE: MUST SET INFURA PROVIDER THROUGH ENVIRONMENT VARIABLES FOR THESE SCRIPTS TO WORK

ETH_NETWORK:  must be ropsten or mainnet
INFURA_API_KEY: must be an infura project id
'''

def send_ether(keyshard_filepaths, amount_ether, receiver_address, gas_price_gwei):
	shares = []
	threshold = None
	id_check = None
	for fpath in keyshard_filepaths:
		with open(fpath, "r") as f:
			obj = json.loads(f.read())
			shares.append(Share(obj["Index"], obj["Value"], obj["Prime"]))
			if id_check==None:
				id_check = obj["ID"]
			else:
				if id_check != obj["ID"]:
					raise ValueError("Keyshard IDs do not match!")
			if threshold == None:
				threshold = obj["Threshold"]
			else:
				if threshold != obj["Threshold"]:
					raise ValueError("Keyshard thresholds do not match!")
	if len(shares) < threshold+1:
		raise ValueError("Not enough keyshards submitted!")

	secret_int = interpolate_at_zero(shares)
	sk = hex(secret_int)[2:]
	txh = handle_simple_transaction(sk, amount_ether, receiver_address, gas_price_gwei)
	return binascii.hexlify(txh).decode()

