from datetime import date
today = date.today()

class temporary:
  title = ''
  categories = []

def Create(title, categories):
  file_name = title.strip('#').rstrip('\n').replace(' ', '').lower()

  newfile = open(file_name + '.txt', 'w')
  newfile.write('#This blocklist helps Pi-hole\'s admin restrict access to Google and its domains.'+'\n')
  newfile.write('#Last updated: ' + today.strftime('%d-%m-%Y') +'\n')
  newfile.write(title +'\n')

  for url in categories:
    newfile.write('0.0.0.0 ' + url + '\n')


with open('../pihole-google.txt', 'r') as main:

  for line in main:

    if '#' in line:

      if temporary.title and temporary.categories:
        Create(temporary.title, temporary.categories)
        temporary.title = ''
        temporary.categories = []

      temporary.title = line

    elif not '#' in line:
      temporary.categories.append(line.rstrip('\n'))