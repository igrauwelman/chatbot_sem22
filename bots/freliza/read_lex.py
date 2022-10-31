with open("original/montablefff.txt", "r", encoding='iso8859-1') as f:
    entries = f.readlines()

for entry in entries:
    fields = entry[:-1].split("\t")
    print("{}##{}##{}".format(fields[0], fields[1], fields[2]))