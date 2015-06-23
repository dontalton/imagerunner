#!/usr/bin/env python

from utils import *
from formats import vmdk as image
from drivers import ceph as storage
import cinder

# if using cinder
size = image.convert('image')
target_vol = cinder.create(size)
driver.load(target_vol)

# if using glance
# blah

# if using nfs
# blah
