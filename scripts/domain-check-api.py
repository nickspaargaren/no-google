import whois
import time
import re


def get_domain(url: str) -> str:
    """
    A function that extracts the domain name from a `url`
    """
    domain = re.findall("(?<=\.)[^.]+\.[^.]+$", url)
    if domain != []:
        return domain[0]
    else:
        return url


def remove_duplicates(mylist: list[str]):
    return list(dict.fromkeys(mylist))


def get_domains():
    with open("../pihole-google.txt", "r") as main:
        for line in main:
            if not "#" in line and not ":" in line:
                line = get_domain(line)
                if line != "\n" and line != []:
                    line = re.sub(r"\n", "", line)
                    yield line


def is_registered(domain):
    """
    A function that checks whether a domain is registered and retrieves its whois information.
    """
    time.sleep(1)
    try:
        w = whois.whois(domain, flags=whois.NICClient.WHOIS_QUICK)
    except Exception:
        return False
    else:
        return [w.domain_name, w.org, w.name_servers]


# iterate over domains
domains = remove_duplicates(get_domains())

for domain in domains:
    print(domain, is_registered(domain.rstrip("\n")))
