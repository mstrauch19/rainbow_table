#!/usr/bin/env python
import base64
import hashlib
from Crypto.Cipher import AES
import sys
import binascii
import os
import random

digits = sys.argv[1]
n = int(digits)
chars = n // 4


def reduc(hsh, col):
    plain = hsh[0:chars]
    plainint = (int(plain, 16) + col) % (2**n)
    return ((str(hex(plainint))[2:]).zfill(chars)).replace("L", "")

def makeHash(plain):
    key = binascii.unhexlify(("0"*(32-chars)) + str(plain))
    IV = 16 * '\x00'
    #IV = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
    print binascii.hexlify(encryptor.encrypt("\x00"*16))
    return binascii.hexlify(encryptor.encrypt("\x00"*16))

def gen_table():
    random.seed(16)
    length = 2**(n // 2)
    tablesize = length
    starts = []
    ends = []

    depth = 0
    while depth < tablesize:
        count = 0
        plain = (str(hex(random.randrange(0,2**n)))[2:]).zfill(chars)
        plain = plain.replace("L", "")
        start = plain
        while count < length:
            hsh = makeHash(plain)
            plain = reduc(hsh,count)
            count += 1
        starts.append(start)
        ends.append(makeHash(plain))
        depth += 1
    return [starts,ends]
print makeHash("ABCABC") 
data = gen_table()
f = open("rainbow", "w");
for i in range(len(data[0])):
    f.write(str(data[0][i]) + " " + str(data[1][i]) + "\n")
