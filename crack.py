#!/usr/bin/env python
import sys
import binascii
import base64
import hashlib
from Crypto.Cipher import AES
import pickle
import random

toCrack = sys.argv[2]
aes = 0
starts = []
ends = []
lines = open("rainbow", "rb")
a= "a"
while a != "":
    a= lines.read(16)
    if a != "":
        ends.append(binascii.hexlify(a))
n = int(sys.argv[1])
chars = n/4

random.seed(16)
i = 0
while i < len(ends):
    plain = (str(hex(random.randrange(0,2**n)))[2:]).zfill(chars)
    plain = plain.replace("L","")
    starts.append(plain)
    i += 1

def reduc(hsh, col):
    plain = hsh[0:chars]
    plainint = (int(plain, 16) + col) % (2**n)
    return ((str(hex(plainint))[2:]).zfill(chars)).replace("L", "")

def makeHash(plain):
    global aes
    aes += 1
    key = binascii.unhexlify(("0"*(32-chars)) + str(plain))
    IV = 16 * '\x00'
    #IV = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
    #print binascii.hexlify(encryptor.encrypt("\x00"*16))
    return binascii.hexlify(encryptor.encrypt("\x00"*16))
    
def findpass(hsh, collisions):
    global aes
    chains = {}
    for index in collisions:
        chains[index] = starts[index]
    i = 0
    while i < 2**(n/2):
        for index in chains.keys():
            nxt = makeHash(chains[index])
            if nxt == hsh:
                print "The password is: " + str(chains[index])
                print "AES evaluated " + str(aes) + " times"
                return True
            else:
                chains[index] = reduc(nxt, i)
        i += 1
    return False

def crack(hsh):
    top = 2 ** (n/2)
    i = top
    use = hsh
    while i >= 0:
        use = hsh
        curr = i
        while curr < top:
            use = makeHash(reduc(use,curr))
            curr += 1
        if use in ends:
            collisions = []
            for ind in range(0, len(ends)):
                if use == ends[ind]:
                    collisions.append(ind)
            if findpass(hsh,collisions):
                return
        i -= 1
    print "Failure"
    print aes
try:
    crack(toCrack)
except KeyboardInterrupt:
    print "Aes was run " +str(aes)+" times"
