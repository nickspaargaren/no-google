import dns.resolver


def check_domain(domain):
    try:
        answer = dns.resolver.resolve(domain, "A")
        if answer.qname:
            return True
        return False
    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ):
        return False


with open("../pihole-google.txt") as f:
    for line in f:
        domain = line.strip()  # strip whitespace
        if not domain.startswith("#"):
            if domain:
                if not check_domain(domain):
                    print(domain)

f.close()
