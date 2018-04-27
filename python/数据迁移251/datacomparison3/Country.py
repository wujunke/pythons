import json

import requests
from config import baseurl, headers


def getAllCountry():

    res = json.loads(requests.get(baseurl+'source/country',headers=headers).content)
    re = res.get('result')
    return re

allcountry = getAllCountry()


def getCountryId(countryname):
    reid = None
    for country in allcountry:
        if country.get('countryC') == countryname:
            reid = country.get('id')
    return reid