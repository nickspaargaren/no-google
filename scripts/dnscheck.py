import dns.resolver
import sys

def check_domain(domain):
    try:
        # Query for 'A' records
        dns.resolver.resolve(domain, "A")
        has_a_record = True
    except (dns.resolver.NXDOMAIN, Exception):
        has_a_record = False
    
    try:
        # Query for 'NS' records
        dns.resolver.resolve(domain, "NS")
        has_ns_record = True
    except (dns.resolver.NXDOMAIN, Exception):
        has_ns_record = False

    return not has_a_record and not has_ns_record

def main():
    found_domains = 0
    
    with open("../pihole-google.txt") as f:
        for line in f:
            domain = line.strip()  # strip whitespace
            if domain and not domain.startswith("#"):
                if check_domain(domain):
                    print(f"Domain with no A or NS records: {domain}")
                    found_domains += 1
                    if found_domains >= 10:  # Exit early to reduce requests
                        sys.exit(1)
    
    if found_domains > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
