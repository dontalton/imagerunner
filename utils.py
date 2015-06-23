import json
import requests
import yaml

creds = yaml.load(open('config.yaml'))

def token():
    auth = creds['openstack']
    headers = {'Content-Type':'application/json'}
    payload = {'auth': {'tenantName':auth['tenant'],'passwordCredentials':{'username':auth['user'],'password':auth['password']}}}
    r = requests.post(auth['authurl'], data=json.dumps(payload), headers=headers)
    response = json.loads(r.text)
    return response['access']['token']['id']

print token()
