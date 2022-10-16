counts = { }
with open("../pihole-google.txt") as f: 
    for line in f:
        domain = line.strip() # strip whitespace
        if domain:
            if domain in counts: # duplicate line, inc count
                counts[domain] = counts[domain]+1 
            else:
                counts[domain] = 1 # new entry 
f.close()

for domain, count in counts.items():
    if count > 1:
        assert False, domain + " occurred more than one time in pihole-google.txt, please remove duplicate domains."

def test_succes():
    assert(True)