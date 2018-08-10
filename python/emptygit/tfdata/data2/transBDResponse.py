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
    '505':[23550, 13683, 3398, 4600, 606, 29340, 33511, 4830, 30383, 9586, 528, 4706, 30819, 23590, 2619, 31920, 732, 7698, 6747, 4725, 24417, 28762, 23619, 6963, 6695, 24358, 788, 30161, 24333, 4339, 23572, 32824, 97, 3536, 31120, 3372, 30995, 33623, 28339, 4156, 188, 30703, 30119, 13600, 4368, 24318, 24197, 10076, 31078, 414],
    '513':[5177, 4761, 23658, 28312, 4830, 24417, 414, 605, 6747, 606, 4600, 4891, 4851, 249, 24127, 178, 489, 7319, 456, 4957, 29643, 782, 644, 33484, 3744, 4809, 6785, 13847, 24046, 5050, 7968, 732, 4544, 7786, 873, 24344, 175, 4890, 4545, 6776, 528, 5153, 826, 4340, 3466, 3293, 5305, 970, 33445, 24131],
    '519':[13683, 4600, 606, 4830, 732, 4725, 24417, 6695, 24358, 6747, 628, 3398, 31074, 30819, 788, 30776, 188, 414, 7247, 249, 528, 926, 33441, 33487, 989, 644, 8155, 6281, 30909, 4563, 6963, 3355, 5330, 539, 4097, 380, 28894, 659, 1075, 945, 7542, 125, 5004, 33573, 9400, 627, 807, 4829, 7203, 26101],
    '520':[13519, 24324, 26101, 32308, 13683, 10328, 33441, 23817, 72, 6857, 30780, 4726, 178, 24417, 3980, 3514, 628, 230, 3860, 788, 7313, 24499, 4209, 3685, 113, 3439, 33807, 1234, 48, 3759, 768, 375, 6747, 3470, 10407, 5021, 4714, 9405, 33623, 6695, 7922, 4733, 627, 954, 285, 553, 31052, 7584, 5305, 297],
    '521':[7089, 6800, 28311, 7491, 23600, 5013, 33372, 4755, 10187, 7028, 6602, 30750, 30531, 4440, 847, 23596, 24255, 287, 33418, 28, 24484, 4304, 23717, 1409, 23547, 7577, 30161, 716, 909, 31095, 7566, 24417, 13676, 4589, 160, 4425, 322, 30908, 24388, 30178, 28352, 7572, 3397, 23590, 4209, 29425, 4763, 24387, 4927, 4872]
}

for key, value in predictres.items():
    checkPredictResult(value, key)

