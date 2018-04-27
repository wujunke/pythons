import json

import requests
from config import baseurl, headers


def getAllTitle():

    res = json.loads(requests.get(baseurl+'source/title',headers=headers).content)
    re = res.get('result')
    return re

alltitle = getAllTitle()

def getTitleId(titlename):
    reid = None
    for title in alltitle:
        if title.get('nameC') == titlename:
            reid = title.get('id')
    return reid