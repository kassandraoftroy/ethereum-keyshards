#!/usr/bin/python3
from secrets import randbelow

SECP256K1 = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

class Share:
	
	def __init__(self, x, y, prime):
		assert x < prime, "player index too large"
		self.x = x
		self.y = y%prime
		self.prime = prime

	# Overload addition operator for homomorphic share addition
	# Displays additive homomorphic property of shamir secret sharing
	def __add__(self, other):
		assert self.prime == other.prime, "mismatching prime modulus"
		assert self.x == other.x, "mismatching player index"
		return Share(self.x, self.y+other.y, self.prime)

	def __str__(self):
		return f"({self.x}, {self.y})"

	def __repr__(self):
		return f"({self.x}, {self.y})"


def make_shares(threshold, n_parties, secret, prime=SECP256K1):
	assert threshold+1 <= n_parties, "cannot require more shares than number of parties for reconstruction"
	assert secret < prime, "secret cannot be larger than prime modulus"
	coefficients = [secret] + [__randrange(1, prime) for _ in range(threshold)]
	return [Share(i+1, evaluate_polynomial(coefficients, i+1, prime), prime) for i in range(n_parties)]

# Lagrange interpolation at f(0) recovers the secret value
# Note: No error detection or correction of shares, i.e. passive security only (does not tolerate false shares, only missing ones).
# Active security (error correction and cheater detection) is possible but requires a heavier reconstruction alg (it's similar to Reed Solomon Codes).
def interpolate_at_zero(shares):
	prime = shares[0].prime
	for s in shares[1:]:
		assert s.prime == prime, "mismatching prime modulus in shares"
	secret = 0
	for i in range(len(shares)):
		origin = shares[i].x
		originy = shares[i].y
		numerator = 1
		denominator = 1
		for k in range(len(shares)):
			if k != i:
				current = shares[k].x
				negative = (-1*current)%prime
				added = (origin - current)%prime
				numerator = numerator * negative%prime
				denominator = denominator * added%prime
		secret += originy*numerator*mod_inv(denominator, prime)%prime
	return secret%prime

def evaluate_polynomial(coefficients, x_value, prime):
	result = coefficients[-1]
	for i in range(2, len(coefficients)+1):
		result = result*x_value
		result = result + coefficients[-i]
	return result%prime

# modular math
def mod_inv(x, p):
	assert gcd(x, p) == 1, "Divisor %d not coprime to modulus %d" % (x, p)
	z, a = (x % p), 1
	while z != 1:
		q = - (p // z)
		z, a = (p + q * z), (q * a) % p
	return a

def rand_int(prime=SECP256K1):
	return __randrange(1, prime-1)

def prod(nums):
	return reduce(mul, nums, 1)

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

# cryptographically secure random number generation in a given range
def __randrange(lower, upper):
	return randbelow(upper-lower)+lower
