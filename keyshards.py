#!/usr/bin/python3
from shamir_prime import *
from eth_tx import handle_simple_transaction, get_address
import json, binascii, os, sys

'''
NOTE: MUST SET INFURA PROVIDER THROUGH ENVIRONMENT VARIABLES FOR THESE SCRIPTS TO WORK

ETH_NETWORK:  must be ropsten or mainnet
INFURA_API_KEY: must be a valid infura project id
'''

HOME = str(os.path.expanduser("~"))

def getKey(keyshard_filepaths):
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
	return hex(secret_int)

def send_ether(keyshard_filepaths, amount_ether, receiver_address, gas_price_gwei):
	sk = getKey(keyshard_filepaths)
	txh = handle_simple_transaction(sk[2:], amount_ether, receiver_address, gas_price_gwei)
	return binascii.hexlify(txh).decode()

def generate_new_account(id_string, threshold, n_shares, output_dir=HOME):
	skint = rand_int()
	shares = make_shares(threshold, n_shares, skint)
	for s in shares:
		j = {"ID": id_string, "Algorithm": "SHAMIR-PRIME", "Index": s.x, "Value": s.y, "Prime": SECP256K1, "Threshold": threshold}
		fpath = os.path.join(output_dir, f'{s.x}-{id_string}.json')
		with open(fpath, "w") as f:
			json.dump(j, f, indent=4)
	addr = get_address(hex(skint)[2:])
	return addr

if __name__=='__main__':
	paths = sys.argv[1:]
	print(getKey(paths))
