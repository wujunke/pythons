#coding=utf-8
import copy

orgeventlist = []

f = open('investevent.csv', 'r')
lines = f.readlines()
for line in lines:
    li1 = line.split(',')
    orgeventlist.append(li1)
f.close()


eventlist = []

f2 = open('test7-44.csv', 'r')
lines = f2.readlines()
for line in lines:
    li = line.replace('\r', '').replace('\n', '').split(',')
    eventlist.append(li)
f2.close()


reslist = []


lastcom_id = None
for event in eventlist:
    nowcom_id = event[0]
    if lastcom_id:
        if nowcom_id == lastcom_id:
            pass
        else:
            lastcom_id = nowcom_id
            for orgevent in orgeventlist:
                if orgevent[5] == nowcom_id:
                    newevent = copy.deepcopy(event)
                    newevent.append(orgevent[3])
                    newevent.append(orgevent[4])
                    newevent.append(orgevent[6])
                    newevent.append(orgevent[7])
                    reslist.append(newevent)
    else:
        lastcom_id = nowcom_id
        for orgevent in orgeventlist:
            if orgevent[5] == nowcom_id:
                newevent = copy.deepcopy(event)
                newevent.append(orgevent[3])
                newevent.append(orgevent[4])
                newevent.append(orgevent[6])
                newevent.append(orgevent[7])
                reslist.append(newevent)




with open('test7-5.csv', 'a') as f:
    for res in reslist:
        f.write(','.join(res))
        # f.write('\n')




