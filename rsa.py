import random
from math import gcd


def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_keys():
    primes = [i for i in range(100, 300) if is_prime(i)]
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
    n = p * q
    phi = (p-1)*(q-1)
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)
    d = modinv(e, phi)
    return ((e, n), (d, n))




def encrypt_message(message: str, enc_key: tuple):
    codes = [ord(el) for el in message]
    encoded_symbols = [(el ** enc_key[0]) % enc_key[1] for el in codes]

    return encoded_symbols

def decrypt_message(cypher, private_key):
    return "".join([chr((el ** private_key[0]) % private_key[1]) for el in cypher])

if __name__ == "__main__":
    public, private = generate_keys()
    print('Encrypting "I love mandarins"')
    cyph = encrypt_message("I love mandarins", public)

    # print(cyph)
    print("-"*30)
    print("Encoded message:  " + "".join([chr(el) for el in cyph]))
    print("-"*30)

    decode = decrypt_message(cyph ,private)

    print("Decoded message: " + decode)
