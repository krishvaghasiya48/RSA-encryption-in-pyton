# Python Module for Encryption and Decryption by RSA Algorithm

from random import choice

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
          71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
          151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
          317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
          419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
          503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
          607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
          701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
          811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
          911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

def choose_distinct_primes():
    while True:
        p = choice(primes)
        q = choice(primes)
        if p != q:
            return [p, q]


def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def modinv(phi, m):
    for x in range(1, m):
        if (phi * x) % m == 1:
            return x
    return None

def coprimes(phi):
    l = []
    for x in range(2, phi):
        if gcd(phi, x) == 1 and modinv(x, phi) != None:
            l.append(x)
        if len(l) > 5: break
    for x in l:
        if x == modinv(x, phi):
            l.remove(x)
    return l

def key_generator():
    p, q = choose_distinct_primes()
    n = p * q
    phi = (p-1) * (q-1)  # Euler's function (totient)
    e = choice(coprimes(phi))
    d = modinv(e, phi)
    
    public_key = [e, n]
    private_key = [d, n]
    return [public_key, private_key]


def encrypt_block(m, e, n):
    return pow(m, e, n)

def decrypt_block(c, d, n):
    return pow(c, d, n)

def encrypt_string(s, public_key):
    e, n = public_key
    return ''.join([chr(encrypt_block(ord(x), e, n)) for x in list(s)])

def decrypt_string(s, private_key):
    d, n = private_key
    return ''.join([chr(decrypt_block(ord(x), d, n)) for x in list(s)])

