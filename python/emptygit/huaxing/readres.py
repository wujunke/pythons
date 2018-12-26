#coding=utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


with open('fields', 'r') as f:
    fields = f.read()
fields = json.loads(fields)

with open('res', 'r') as f:
    content = f.read().replace('\n','').replace('\t','')


for field in fields:
    field_name = str(field[u'name']) + ':'
    newName = '"%s"' % field_name + ':'
    content = content.replace(field_name, newName)


res = json.loads(content)


with open('orglist', 'a') as f:
    for org in res:
        f.write(json.dumps(org))
        f.write('\n')
