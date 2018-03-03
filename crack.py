#!/usr/bin/env python
import sys
import binascii
import base64
import hashlib
from Crypto.Cipher import AES

toCrack = sys.argv[1]
aes = 0
starts = []
ends = []
lines = open("rainbow", "r").readlines()
i = 0
for line in lines:
    split = line.strip().split(" ")
    starts.append((split[0]))
    ends.append((split[1]))
    i += 1

chars = len(starts[0])
n = chars * 4


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
    while i < len(ends):
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
    top = len(ends)
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
