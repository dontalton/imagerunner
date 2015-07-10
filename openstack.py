import json
import requests
import yaml

class Openstack(object):

    def __init__(self):
        self.config = yaml.load(open('config.yaml'))
        self.auth = self.config['credentials']['openstack']
        self.url = self.auth['authurl']
        self.username = self.auth['username']
        self.password = self.auth['password']
        self.tenant = self.auth['tenant']
        self.headers = {'Content-Type':'application/json'}
        self.data = {'auth': {'tenantName':self.tenant, 'passwordCredentials':{'username':self.username, 'password':self.password}}}

    def get_url(self, service=None):
        # service should be either 'cinder' or 'glance'
        r = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
        response = r.json()
        tenant = response['access']['token']['tenant']['id']
        catalog = response['access']['serviceCatalog']

        for entry in catalog:
            if entry['type'] == 'volumev2':
                cinder_url = entry['endpoints'][0]['publicURL'].replace(tenant, '')
            if entry['type'] == 'image':
                glance_url = entry['endpoints'][0]['publicURL'].replace(tenant, '') + '/'

        if service == 'cinder':
            return cinder_url
        elif service == 'glance':
            return glance_url
        else: return None

    def get_token(self):
        r = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
        response = r.json()
        token = response['access']['token']['id']
        return token
