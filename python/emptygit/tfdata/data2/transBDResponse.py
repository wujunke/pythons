#coding=utf-8
import copy

WEIGHT_TAG = 5
WEIGHT_TAG_NEGA = -0.5
WEIGHT_ROUND = 3
WEIGHT_ROUND_NEGA = 0


def transTag(tags):
    assert isinstance(tags, (list, tuple)), 'tags-(%s) 不是数组或者元组类型'% tags
    newTags = []
    for tag in tags:
        assert isinstance(tags, (list, tuple)), 'tag-(%s) 不是int类型' % tag
        if tag > 18:
            tag = tag - 14
        newTags.append(tag)
    resTags = []
    for i in range(1, 43):
        if i in newTags:
            resTags.append(WEIGHT_TAG)
        else:
            resTags.append(WEIGHT_TAG_NEGA)
    return resTags






projDic = {}
f1 = open('projdata.csv', 'r')
lines = f1.readlines()
for line in lines:
    data = line.replace('\n', '').split(',')
    projDic[data[0]] = data
f1.close()

bdlist = []
f2 = open('bdresponse.csv', 'r')
lines = f2.readlines()
for line in lines:
    bdlist.append(line.replace('\n', '').split(','))
f2.close()


def savedata(data):
    with open('test8-4.csv', 'a') as f:
        f.write(','.join(data))
        f.write('\n')

# for bd in bdlist:
#     if projDic[bd[0]]:
#         newlist = copy.deepcopy(projDic[bd[0]])
#         newlist[-12] = bd[1]
#
#         newlist.append(bd[2])
#         savedata(newlist)




def checkPredictResult(predictList, proj_id):
    rep = False
    for org_id in predictList:
        for bd in bdlist:
            if proj_id == bd[0] and str(org_id) == bd[1] :
                newlist = copy.deepcopy(projDic[proj_id])
                newlist[-12] = str(org_id)
                newlist.append(bd[2])
                savedata(newlist)
                rep = True
                break
        if rep:
            break




predictres = {
   '521':[7089, 6800, 28311, 7491, 23600, 5013, 33372, 4755, 10187, 7028, 6602, 30750, 30531, 4440, 847, 23596, 24255, 287, 33418, 28, 24484, 4304, 23717, 1409, 23547, 7577, 30161, 716, 909, 31095, 7566, 24417, 13676, 4589, 160, 4425, 322, 30908, 24388, 30178, 28352, 7572, 3397, 23590, 4209, 29425, 4763, 24387, 4927, 4872]
}

for key, value in predictres.items():
    checkPredictResult(value, key)

