import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--type", nargs="?", choices=["duplicates", "regex"], help="Test Type"
)

args = parser.parse_args()

counts = {}
with open("../pihole-google.txt") as f:
    for line in f:
        domain = line.strip()  # strip whitespace
        if domain:
            if domain in counts:  # duplicate line, inc count
                counts[domain] = counts[domain] + 1
            else:
                counts[domain] = 1  # new entry
f.close()

if args.type == "duplicates":
    for domain, count in counts.items():
        if count > 1:
            assert False, (
                domain
                + " occurred more than one time in pihole-google.txt, please remove duplicate domains."
            )

if args.type == "regex":
    for domain, count in counts.items():
        if ".l.google.com" in domain:
            assert (
                False
            ), "A l.google.com domain occurred in pihole-google.txt, please remove regex domains."
        if ".googlevideo.com" in domain:
            assert (
                False
            ), "A googlevideo.com domain occurred in pihole-google.txt, please remove regex domains."


def test_succes():
    assert True
