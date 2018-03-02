#!/usr/bin/env python
starts = []
ends = []
lines = open("rainbow", "r").readlines()
for line in lines:
    split = line.strip().split(" ")
    starts.append(split[0])
    ends.append(split[1])

def reduc(hsh):
    plain = hsh[0:chars-1]
    return plain

def makeHash(plain):
    key = binascii.unhexlify(("0"*(32-chars)) + ("0" * (chars-len(str(plain)))) + str(plain))
    IV = 16 * '\x00'
    #IV = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
    return binascii.hexlify(encryptor.encrypt("\x00"*16))
    
def findpass(hsh, collisions):
    print ""

def crack(hsh):
    i = 0
    use = hsh
    while i < len(ends):
        if use in ends:
            collisions = []
            for i in range(0, len(ends)):
                if ends[i] == use:
                    collisions.append(i)
            findpass(hsh, collisions)
            return
        use = makeHash(reduc(use))
        i += 1
    print "Failure"
