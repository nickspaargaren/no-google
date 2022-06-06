import json

import whois # pip install python-whois
import time

def is_registered(domain):
    """
    A function that checks whether a `domain` is can get whois info
    """
    time.sleep(1)
    try:
        w = whois.whois(domain, flags=whois.NICClient.WHOIS_QUICK)
    except Exception:
        return False
    else:
        return [w.domain_name, w.org, w.name_servers]

domains = open("../check-domains.txt", "r")

# iterate over domains
for domain in domains.readlines():
    print(domain, is_registered(domain.rstrip("\n")))