counts = { }
with open("../pihole-google.txt") as f: 
    for line in f:
        stripline = line.strip() # strip whitespace
        myhash = hash(stripline) 
        if myhash:
            if myhash in counts: # duplicate line, inc count
                counts[myhash] = counts[myhash]+1 
            else:
                counts[myhash] = 1 # new entry 
f.close()

#re-read file, and print out duplicate lines 
with open("../pihole-google.txt") as f: 
    for line in f:
        stripline = line.strip() 
        myhash = hash(stripline) 
        if myhash:
            if counts[myhash]>1: 
                # print duplicate line and count
                assert False, stripline + " occurred more than one time in pihole-google.txt, please remove duplicate domains."
                # after printing dup, clear ctr so prints once
                counts[myhash] = 0

f.close()