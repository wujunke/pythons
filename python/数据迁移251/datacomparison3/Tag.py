import json

import requests
from config import baseurl, headers


def getAllTag():

    res = json.loads(requests.get(baseurl+'source/tag',headers=headers).content)
    re = res.get('result')
    return re

alltags = getAllTag()

def getTagId(tagname):
    tagid = None
    for tag in alltags:
        tagnameC = tag.get('nameC')
        if tagnameC == tagname:
            tagid = tag.get('id')
    return tagid