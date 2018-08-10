#coding=utf-8


taglist = {}
tagfile = open('project_tags.csv', 'r')
lines = tagfile.readlines()
for l in lines:
    proj_id = l.split(',')[0]
    tag_id = int(l.split(',')[1].replace('\n', ''))
    if tag_id <= 18:
        pass
    else:
        tag_id = tag_id - 14
    if taglist.get(str(proj_id), 'null') == 'null':
        taglist[str(proj_id)] = [tag_id]
    else:
        taglist[str(proj_id)].append(tag_id)
tagfile.close()

proj_tags = {}
for proj, tags in taglist.items():
    newtags = []
    for i in range(1, 43):
        if i in tags:
            newtags.append(5)
        else:
            newtags.append(-0.5)

    proj_tags[proj] = map(str, newtags)
    print proj
    print ','.join(proj_tags[proj])

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


haituoroundcontrast = {
    '不明确':0,
    '尚未获投':1, '种子轮':1, '天使轮':1, 'Pre-A轮':1,
    'A轮':3, 'A+轮':3, 'Pre-B轮':3, 'B轮':3, 'B+轮':3,
    'C轮':5, 'C+轮':5, 'D轮':5, 'D+轮':5,
    'E轮':7, 'F轮-上市前':7, '新三板':7, '战略投资':7,
    '已上市':9, '已被收购':9, '并购':9
}

haituotransroundcontrast = {
    '天使轮':2, 'Pre-A轮':2,
    'A轮':2, 'A+轮':2, 'B轮':4, 'B+轮':4,
    'C轮':4, 'C+轮':4, 'D轮':6, 'D+轮':6,
    'E轮':6, 'F轮-上市前':6, '新三板':8, '战略投资':8,
}



lines = [

]
for line in lines:
    roundstr = ''
    roundlist = [0 for x in range(10)]
    index1 = roundcontrast.get(roundstr, 0)
    index2 = transroundcontrast.get(roundstr, None)
    if index1:
        roundlist[index1] = 1
    if index2:
        roundlist[index2] = 1
    print ','.join( map(str, roundlist))
