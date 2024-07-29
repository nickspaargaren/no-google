import dns.resolver


def check_domain(domain):
    try:
        # Query for 'A' records
        answers = dns.resolver.resolve(domain, "A")
        # If we get any answers, the domain has a response
        return bool(answers)
    except dns.resolver.NXDOMAIN:
        # No answer or domain does not exist or request timed out
        return False


def main():
    with open("../pihole-google.txt") as f:
        for line in f:
            domain = line.strip()  # strip whitespace
            if domain and not domain.startswith("#"):
                if not check_domain(domain):
                    print(f"No DNS response for domain: {domain}")


if __name__ == "__main__":
    main()
