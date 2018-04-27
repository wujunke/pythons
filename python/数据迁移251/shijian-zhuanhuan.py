# createdtime = data.pop('createdtime', None)
# if createdtime not in ['None', None, u'None', 'none']:
#     data['createdtime'] = datetime.datetime.strptime(createdtime.encode('utf-8')[0:19], "%Y-%m-%d %H:%M:%S")
# else:
#     data['createdtime'] = datetime.datetime.now()
# lastmodifytime = data.pop('lastmodifytime', None)
# if lastmodifytime not in ['None', None, u'None', 'none']:
#     data['lastmodifytime'] = datetime.datetime.strptime(lastmodifytime.encode('utf-8')[0:19], "%Y-%m-%d %H:%M:%S")