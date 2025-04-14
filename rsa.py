import random
import math
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
    while math.gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)
    d = modinv(e, phi)
    return ((e, n), (d, n))




def encrypt_message(message: str, enc_key: tuple):

    codes = [ord(el) for el in message]
    encoded_symbols = [str((el ** enc_key[0]) % enc_key[1]) for el in codes]

    return " ".join(encoded_symbols) if encoded_symbols else None

def decrypt_message(cypher, private_key):
    cypher = [int(el) for el in cypher.split()]
    return "".join([chr((el ** private_key[0]) % private_key[1]) for el in cypher])


if __name__ == "__main__":
    e, d =  generate_keys()
    m = encrypt_message("I WANT to bReak free!", e)

    print(m)

    print(decrypt_message(m, d))
