#!/usr/bin/python

from base64 import b64encode
from bs4 import BeautifulSoup

import json
import os
import requests

URL = 'https://vyos.net/get/nightly-builds/'

# Get page containing list of nightly ISOs
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# Find div containing ISO list
section = soup.find_all('div', attrs={'id': 'rolling-current'})[0]

# Grab all the ISO names from list
isos = []
for iso in section.find_all('a'):
    isos.append(iso.contents[0])

# only get the version, eg 1.4-rolling-202307141223
latest = '-'.join(isos[0].split('-')[1:4])

# Read GITHUB_TOKEN from envvar
envvar = os.getenv('GITHUB_TOKEN')
if not envvar:
    os.exit(1)

github_token = b64encode(envvar.encode('utf-8')).decode('utf-8')

# Check if GitHub already has the tag
auth = {'Authorization': f'Bearer {github_token}'}
registry = 'https://ghcr.io/v2/routedbits/vyos/tags/list'

# Get existing tags from GitHub Registry
tags = requests.get(registry, headers=auth).json()['tags']

if latest in tags:
    print('skipbuild')
else:
    print(latest)
