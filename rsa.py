import random
import math


def modinv(a, m):
    m0 = m
    x0 = 0
    x1 = 1

    while a > 1:

        remainder = a // m
        a, m = m, a % m
        x0, x1 = x1 - remainder * x0, x0
    return x1 % m0


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_keys():
    primes = []
    for i in range(100, 300):
        if is_prime(i):
            primes.append(i)
    random1 = random.choice(primes)
    random2 = random.choice(primes)
    n = random1 * random2
    phi = (random1 - 1) * (random2 - 1)
    e = 65537
    while math.gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)
    d = modinv(e, phi)
    return ((e, n), (d, n))


def encrypt_message(message: str, enc_key: tuple):
    enc_key = (int(enc_key[0]), int(enc_key[1]))
    codes = [ord(el) for el in message]
    encoded_symbols = " ".join([str((el ** enc_key[0]) % enc_key[1]) for el in codes])

    return encoded_symbols

def decrypt_message(cypher, private_key):
    private_key = (int(private_key[0]), int(private_key[1]))

    return "".join([chr((int(el) ** private_key[0]) % private_key[1]) for el in cypher.split()])
