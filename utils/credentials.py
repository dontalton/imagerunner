import yaml

config = yaml.load(open('../config.yaml'))

os_user = config['openstack']['user']
os_password = config['openstack']['password']
os_authurl = config['openstack']['authurl']
os_tenant = config['openstack']['tenant']
