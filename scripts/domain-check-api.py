import whois # pip install python-whois
import time

import re

def get_domains():
  with open('../pihole-google.txt', 'r') as main:
    for line in main:
      if not '#' in line and not ':' in line:
        line = re.sub(r"^.*\.(.*\..*)", "", line)
        if line != '\n':
            yield line.rstrip("\n") + '\n'

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

# iterate over domains
for domain in get_domains():
    print(domain, is_registered(domain.rstrip("\n")))