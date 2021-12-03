from datetime import date
today = date.today()

newfile = open('../google-domains', 'w')
newfile.write('# This blocklist helps Pi-hole\'s admin restrict access to Google and its domains.'+'\n')
newfile.write('# Last updated: ' + today.strftime('%d-%m-%Y') +'\n')

with open('../pihole-google.txt', 'r') as main:

  for line in main:
    if '#' in line:
      newfile.write('# ' + line[2:])
    elif not '#' in line:
      newfile.write('0.0.0.0 ' + line.rstrip("\n") + '\n')