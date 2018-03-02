#!/usr/bin/env python
import base64
import hashlib
from Crypto.Cipher import AES
import sys
import binascii
import os

digits = sys.argv[1]
n = int(digits)
chars = n // 4


def reduc(hsh):
    plain = hsh[0:chars-1]
    return plain

def makeHash(plain):
    key = binascii.unhexlify(("0"*(32-chars)) + ("0" * (chars-len(str(plain)))) + str(plain))
    IV = 16 * '\x00'
    #IV = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
    return binascii.hexlify(encryptor.encrypt("\x00"*16))

def gen_table():
    length = 2**(n // 2)
    tablesize = length
    print tablesize
    starts = []
    ends = []

    depth = 0
    while depth < tablesize:
        count = 0
        plain = 4 * depth
        while count < length:
            hsh = makeHash(plain)
            plain = reduc(hsh)
            count += 1
        starts.append(depth * 4)
        ends.append(makeHash(plain))
        depth += 1
    return [starts,ends]
 
data = gen_table()
f = open("rainbow", "w");
for i in range(len(data[0])):
    f.write(str(data[0][i]) + " " + str(data[1][i]) + "\n")
