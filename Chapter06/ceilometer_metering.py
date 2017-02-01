#!/usr/bin/env python

import requests #http://docs.python-requests.org/en/latest
import json

KEYSTONE_URL = 'http://controller01:5000/v2.0/'
TENANT       = 'demo'
USERNAME     = 'demo'
PASSWORD     = 'secret'

r = requests.post("%s/tokens"% (KEYSTONE_URL,), json={
  "auth": {
    "tenantName": TENANT,
    "passwordCredentials": {
      "username": USERNAME,
      "password": PASSWORD,
    }
  }
})

if r.ok:
  token = r.json()['access']['token']['id']
else:
  raise Exception(r.text)

# Place the token in the X-Auth-Token header
headers = {'X-Auth-Token': token}

# Find the link to the Ceilometer API in the service catalog:
for service in r.json()['access']['serviceCatalog']:
  if service['type'] == 'metering':
    metering_endpoint = service['endpoints'][0]['publicURL']

tenant_id = r.json()['access']['token']['tenant']['id']
filter = {'q.field': 'project', 'q.value': tenant_id}
statistics = requests.get("%s/v2/meters/instance/statistics"% (metering_endpoint,), headers=headers)

print statistics.json()[0]['duration']
