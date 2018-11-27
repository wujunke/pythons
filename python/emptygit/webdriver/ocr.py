from aip import AipOcr
from datetime import datetime

APP_ID = '11546435'
API_KEY = 'w9646O4Ug0H2XNwXQX0WLcen'
SECRET_KEY = '4kPgOiOsSGH35asD1ifi3SzBgniLY00u'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
moneyshot1 = get_file_content('moneyshot1.png')



# print(datetime.now())
# moneyress1 = client.numbers(moneyshot1)
# print(datetime.now())
# print moneyress1
# {u'log_id': 3241848224901487867, u'words_result_num': 1, u'words_result': [{u'location': {u'width': 38, u'top': 0, u'height': 13, u'left': 0}, u'words': u'89300'}]}

print(datetime.now())
moneyress1 = client.basicGeneral(moneyshot1)
print(datetime.now())
print moneyress1
# {u'log_id': 8147114817391951675, u'words_result_num': 1, u'words_result': [{u'words': u'89300'}]}


