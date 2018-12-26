#coding=utf-8
import json
from  huaxing_url import *

orglist = []

with open('res', 'r') as f:
    lines = f.readlines()

for line in lines:
    orglines = replaceRes0(line)
    orgs = json.loads(orglines)
    orglist.extend(orgs)


orgdic = {}

for org in orglist:
    if orgdic.get(org['INST_ID']):
        pass
    else:
        orgdic[org['INST_ID']] = org


with open('orglist', 'w') as f:
    for org in orgdic.values():
        f.write(json.dumps(org))
        f.write('\n')

