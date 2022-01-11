import json
import sys
from collections import OrderedDict, defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, List


class PiHoleDomainConverter:

    INPUT_FILE = "pihole-google.txt"
    PARSED_FILE = "google-domains"
    ADGUARD_FILE = "pihole-google-adguard.txt"
    CATEGORIES_PATH = "categories"

    FILE_HEADER = "This blocklist helps Pi-hole's admin restrict access to Google and its domains."

    def __init__(self):
        self.data: Dict[List] = OrderedDict()
        self.timestamp: str = date.today().strftime("%d-%m-%Y")

    def read(self):
        """
        Read input file into `self.data`, a dictionary mapping category names to lists of member items.
        """
        with open(self.INPUT_FILE, "r") as f:
            category = None
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    category = line.lstrip("# ")
                    self.data.setdefault(category, [])
                else:
                    if category is None:
                        raise ValueError("Unable to store item without category")
                    self.data[category].append(line)

    def dump(self):
        """
        Output data in JSON format on STDOUT.
        """
        print(json.dumps(self.data, indent=4))

    def parsed(self):
        """
        Write data to unified text file.
        """
        with open(self.PARSED_FILE, "w") as f:
            f.write(f"# {self.FILE_HEADER}\n")
            f.write(f"# Last updated: {self.timestamp}\n")
            for category, entries in self.data.items():
                f.write(f"# {category}\n")
                for entry in entries:
                    f.write(f"0.0.0.0 {entry}\n")

    def adguard(self):
        """
        Write data in "adguard" format.
        """
        with open(self.ADGUARD_FILE, "w") as f:
            f.write(f"! {self.FILE_HEADER}\n")
            f.write(f"! Last updated: {self.timestamp}\n")
            for category, entries in self.data.items():
                f.write(f"! {category}\n")
                for entry in entries:
                    f.write(f"||{entry}^\n")

    def categories(self):
        """
        Write data to individual per-category files.
        """

        def write_file(path, category, entries, line_prefix=""):
            """
            Generic function to write per-category file in both flavours.
            """
            with open(path, "w") as f:
                f.write(f"# {self.FILE_HEADER}\n")
                f.write(f"# Last updated: {self.timestamp}\n")
                f.write(f"# {category}\n")
                f.write(f"\n")
                for entry in entries:
                    f.write(f"{line_prefix}{entry}\n")

        for category, entries in self.data.items():

            # Compute file names.
            filename = category.replace(" ", "").lower()
            filepath = Path(self.CATEGORIES_PATH).joinpath(filename)
            text_file = filepath.with_suffix(".txt")
            parsed_file = str(filepath) + "parsed"

            # Write two flavours of per-category file.
            write_file(text_file, category, entries, line_prefix="0.0.0.0 ")
            write_file(parsed_file, category, entries)

    def duplicates(self):
        hashes = defaultdict(int)
        for category, entries in self.data.items():
            for entry in entries:
                hashes[hash(entry)] += 1
        for category, entries in self.data.items():
            for entry in entries:
                hashvalue = hash(entry)
                if hashvalue in hashes:
                    count = hashes[hashvalue]
                    if count > 1:
                        print(
                            f"Domain {entry} found {count} times, please remove duplicate domains."
                        )
                        hashes[hashvalue] = 0


def run(action):

    # Create converter instance and read input file.
    converter = PiHoleDomainConverter()
    converter.read()

    # Invoke special action "json".
    if action == "json":
        converter.dump()
        sys.exit()

    # Either invoke specific action, or expand to all actions.
    if action == "all":
        subcommands = action_candidates
    else:
        subcommands = [action]

    # Invoke all actions subsequently.
    for action in subcommands:
        print(f"Invoking subcommand '{action}'")
        method = getattr(converter, action)
        method()


if __name__ == "__main__":

    # Read subcommand from command line, with error handling.
    action_candidates = ["parsed", "adguard", "categories", "duplicates"]
    special_candidates = ["all", "json"]
    subcommand = None
    try:
        subcommand = sys.argv[1]
    except:
        pass
    if subcommand not in action_candidates + special_candidates:
        print(
            f"ERROR: Subcommand not given or invalid, please use one of {action_candidates + special_candidates}"
        )
        sys.exit(1)

    # Invoke subcommand.
    run(subcommand)
