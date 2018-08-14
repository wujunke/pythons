#coding=utf-8
import json

orglist = []

with open('name_id_comparetable', 'r') as f:
    lines = f.readlines()
    for line in lines:
        orglist.append(json.loads(line))



max_id = orglist[-1]['itjuzi_id']

