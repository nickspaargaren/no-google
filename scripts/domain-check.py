import re

newfile = open('../check-domains.txt', 'w')

with open('../pihole-google.txt', 'r') as main:

  for line in main:
    if not '#' in line and not ':' in line:
      line = re.sub(r"^.*\.(.*\..*)", "", line)
      if line != '\n':
        newfile.write(line.rstrip("\n") + '\n')
