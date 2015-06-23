#!/usr/bin/env python

from utils import *
from backends import ceph

creds = yaml.load(open('config.yaml'))

seff = ceph.Ceph(rawimage='testimage', metadata=None, cephpool='volumes', token=token())
print seff.load_into_ceph()
