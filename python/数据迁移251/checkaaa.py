import json

file1 = open('user-old_new_id','r')
file2 = open('userid','r')


res = []
for line in file1:
    if len(line) > 10:
        res.append(json.loads(line.replace('\n', '')))


for line in file2:
    inlist = False
    line = int(line.replace('\n', ''))
    for dic in res:
        if line == dic['old']:
            inlist = True
    if not inlist:
        print line