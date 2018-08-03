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
            newtags.append(0)
    proj_tags[proj] = newtags

proj_round = {
    '505': (1+1) / 18.0,
    '520': (1+1) / 18.0,
    '521': (8+1) / 18.0,
}

proj_patent = {
    '505': 1,
    '520': 0,
    '521': 0,
}


proj_money = {
    '505': 0,
    '520': 0,
    '521': 0.62,
}

proj_top = {
    '505': 0,
    '520': 0,
    '521': 1,
}


proj_fund = {
    '505': 0,
    '520': 0,
    '521': 0,
}

BDlist = []
BDlistfile = open('tmporg2.csv', 'r')
BDlistlines = BDlistfile.readlines()
for l in BDlistlines:
    BDlist.append(l.replace('\n', '').split(','))
BDlistfile.close()



def savedata(data):
    with open('orgbd.csv', 'a') as f:
        f.write(','.join(data))
        f.write('\n')




for bd in BDlist:
    # data = []
    # data.append('com_id')
    # data.append('com_name')
    # data.append('round')
    # data.append('tag')
    # data.append('com_full_name')
    # data.append('top')
    # data.append('investor')
    # data.append('money')
    # data.append('patent')
    # data.append('org_id')
    # data.append('fund')
    # data.extend(proj_tags[str(proj)])
    # savepredictdata(data)


    proj = bd[0]
    bd.extend(proj_tags[str(proj)])
    bd.append(proj_round[str(proj)])
    bd.append(proj_patent[str(proj)])
    bd.append(proj_money[str(proj)])
    bd.append(proj_top[str(proj)])
    bd.append(proj_fund[str(proj)])


