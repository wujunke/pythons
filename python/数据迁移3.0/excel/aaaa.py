#coding=utf-8
import os


def eachFile(filepath):
    filelist = []
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if '.DS_Store' not in child:
            filelist.append(child)
    return filelist




filepathlist = [
'/Users/investarget/Desktop/投资机构/投资机构（前200）',
'/Users/investarget/Desktop/投资机构/投资机构（前400）',
'/Users/investarget/Desktop/投资机构/投资机构（前600）',
'/Users/investarget/Desktop/投资机构/投资机构（前800）',
'/Users/investarget/Desktop/投资机构/投资机构（前1000）',
'/Users/investarget/Desktop/投资机构/投资机构（前1200）',
'/Users/investarget/Desktop/投资机构/投资机构（前1400）',
'/Users/investarget/Desktop/投资机构/投资机构（前1600）',
'/Users/investarget/Desktop/投资机构/投资机构（前1800）',

]

allfile = []
for path in filepathlist:

    filelist = eachFile(path)
    allfile = allfile + filelist

dic = {}
for path in allfile:
    filename = path.split('/')[-1]
    if dic.get(filename, None):
        dic[filename] = dic[filename] + [path]

    else:
        dic[filename] = [path]

for key,value in dic.items():
    if len(value) > 1:
        for path in value:
            print path