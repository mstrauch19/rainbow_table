#!/usr/bin/env python
starts = []
ends = []
lines = open("rainbow", "r").readlines()
for line in lines:
    split = line.strip().split(" ")
    starts.append(split[0])
    ends.append(split[1])

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
