#coding=utf-8


roundcontrast = {
    '不明确':0,
    '尚未获投':1, '种子轮':1, '天使轮':1, 'Pre-A轮':1,
    'A轮':3, 'A+轮':3, 'Pre-B轮':3, 'B轮':3, 'B+轮':3,
    'C轮':5, 'C+轮':5, 'D轮':5, 'D+轮':5,
    'E轮':7, 'F轮-上市前':7, '新三板':7, '战略投资':7,
    '已上市':9, '已被收购':9, '并购':9
}

transroundcontrast = {
    '天使轮':2, 'Pre-A轮':2,
    'A轮':2, 'A+轮':2, 'B轮':4, 'B+轮':4,
    'C轮':4, 'C+轮':4, 'D轮':6, 'D+轮':6,
    'E轮':6, 'F轮-上市前':6, '新三板':8, '战略投资':8,
}


def savedata(data):
    with open('test8-1.csv', 'a') as f:
        f.write(','.join(data))
        f.write('\n')


i = 1
f = open('test7-5.csv', 'r')
lines = f.readlines()
for line in lines:
    data = line.split(',')
    roundstr = data[-4]
    roundlist = [0 for x in range(10)]
    index1 = roundcontrast.get(roundstr, 0)
    index2 = transroundcontrast.get(roundstr, None)
    if index1:
        roundlist[index1] = 1
    if index2:
        roundlist[index2] = 1
    data.extend(roundlist)
    savedata(map(lambda x: str(x).replace('\r\n', ''), data))
    print i
    i += 1
f.close()





