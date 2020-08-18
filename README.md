# keyshards

This is a simple python package for generating sharded ethereum accounts where a certain number of shards are needed to reconstruct the account's private key. We use Shamir Secret Share over a prime ring so that shards reveal no information about the underlying key until more than the threshold of shards are brought together. 

Keyshard files can be input directly into a process that unlocks the key and spends ether so that no party is ever required to see or manipulate the underlying private key.

Key generation similarly never directly displays or stores the private key, however until keyshards are distributed across parties/machines the key is not fully secure (whenever more than a threshold of keyshards are on the same machine, the key is reconstructable and thus, potentially at risk). We suggest that key generation and distribution is done offline and in as secure of a setting as possible.

## Installation

python 3.5+

clone this repository and enter the root directory

## Usage

You need to set two environment variables for the keyshards script to work:

ETH_NETWORK : set as `ropsten` for testing or `mainnet` when transacting real ether

INFURA_API_KEY : a valid infura project id (you can get one for free by signing up at https://infura.io )

### Generating an account:

```
>>> from keyshards import generate_new_account
>>> generate_new_account('anyIdString', 1, 2, output_dir="/Users/home/Desktop")
'0xMyNewEthereumAddress'
```

Here we generate the keyshards to a fresh ethereum account and return the account's public address. Keyshards are in json format and are left in the output_dir which is your homepath by default, butt can be reset as above.

`generate_new_account` takes three arguments:

- `id_string` : any string that uniquely identifies these shares
- `threshold` : the threshold number of shares
- `n_shares` : the total number of shares

as well as the output_dir optional argument.

NOTE: It takes `threshold+1` shares to be able to reconstruct the key. The code example above has `threshold=1` and `n_shares=2`, which simply means it takes BOTH shares to unlock the key. If `threshold=2` and `n_shares=10` then any 3 of the 10 created shares could reconstruct the key and control the account.

### Sending ether with keyshards

Once you've collected enough keyshards to control the account you can send ether in one simple command:

```
>>> from keyshards import generate_new_account
>>> shard_filepaths = ['path/to/first/shard', 'path/to/second/shard', ...]
>>> amount_eth = 1.0
>>> gas_price_gwei = 50
>>> receiver = '0xSomeOtherEthereumAddress'
>>> send_ether(shard_filepaths, amount_eth, receiver, gas_price_gwei)
'dbb92bf01056369427f2c1c384eb5ce775cdfbc515c55a3197a85a8fd562bba6'
```

Here we input the collected keyshard files and the transaction details into the `send_ether()` method and the transaction id hex is returned.

`send_ether` takes four arguments:

- `keyshard_filepaths` : a list containing the full path to each keyshard file
- `amount_eth` : an amount of ether
- `receiver_address` : ethereum address receiving the amount of ether
- `gas_price_gwei` : a gas price for the transaction, denominated in gwei ( see current gas prices at https://www.ethgasstation.info )

Thats it!