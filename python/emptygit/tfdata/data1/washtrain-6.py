f = open('train-6.csv', 'r')
lines = f.readlines()

def savedata(data):
    with open('test8-2.csv', 'a') as f:
        f.write(','.join(data))
        f.write('\n')
i = 0

for line in lines:
    data = line.replace('\r\n', '').split(',')
    if i > 0:
        for x in range(-9, 1):
            if int(data[x]) == 3:
                data[x] = 1
    savedata(map(lambda x: str(x).replace('\r\n', ''), data))
    i += 1

f.close()