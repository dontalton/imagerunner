import json
import requests
import yaml
import credentials as creds

class KeystoneToken(object):

    def token(self):

        headers = {'Content-Type':'application/json'}
        payload = {'auth': {'tenantName':creds.os_tenant,'passwordCredentials':{'username':creds.os_user,'password':creds.os_password}}}
        r = requests.post(creds.os_authurl, data=json.dumps(payload), headers=headers)
        response = json.loads(r.text)
        return response['access']['token']['id']
