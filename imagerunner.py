#!/usr/bin/env python

import sys
sys.path.append("/home/don/imagerunner") 

from os import listdir
import yaml

from imagerunner.drivers.disk import disk

config = yaml.load(open('config.yaml'))

#get image type based on filename
#eg aw.vmdk blah.qcow2
