print("Starting...")
database = []
datafiles = ['summoners_1.txt', 'summoners_2.txt']

for datafile in datafiles:
    f = open(datafile, 'r')
    for line in iter(f):
        database.append((line.split(' ', maxsplit=1)[0], line.split(' ', maxsplit=1)[1]))
    f.close()

database = list(set(database))

with open("combined.txt", "a") as f:
    for data in database:
        f.write(str(data[0]) + ' ' + str(data[1]))

print("Finished")