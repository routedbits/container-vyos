#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import json
import os


URL = 'https://vyos.net/get/nightly-builds/'

# Get page containing list of nightly ISOs
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

section = soup.find_all('div', attrs={'id': 'rolling-current'})[0]

isos = []
for iso in section.find_all('a'):
    isos.append(iso.contents[0])

# only get the version, eg 1.4-rolling-202307141223
latest = '-'.join(isos[0].split('-')[1:4])

print(latest)
