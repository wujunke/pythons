f = open('train-6.csv', 'r')
lines = f.readlines()

def savedata(data):
    with open('test8-3.csv', 'a') as f:
        f.write(','.join(data))
        # f.write('\n')
i = 0

for line in lines:
    data = line.replace('\r\n', '').split(',')
    if i > 0:
        for x in range(6, 6 + 42):  # tag
            if int(data[x]) == 0:
                data[x] = -0.5
        for x in range(-10, 0):     # round
            if int(data[x]) == 1:
                data[x] = 3
    savedata(map(lambda x: str(x).replace('\r\n', ''), data))
    i += 1

f.close()