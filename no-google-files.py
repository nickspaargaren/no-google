with open('pihole-google.txt', 'r') as f:

  
  for line in f:
    if '#' in line:
      file_name = "categories/"+line.strip("#").rstrip("\n").replace(" ", "").lower()
      print(file_name)
      

      newfile = open(file_name + ".txt", "w")

      newfile.write('test')
      
  