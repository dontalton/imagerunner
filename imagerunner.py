from utils import *
from backends import ceph

creds = yaml.load(open('config.yaml'))

seff = ceph.Ceph(rawimage='lol', metadata='there', cephpool='rbd', token=token())
seff.load_into_ceph()
