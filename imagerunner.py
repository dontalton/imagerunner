#!/usr/bin/env python

from os import listdir
import sys
import yaml
sys.path.append("/home/don/imagerunner") 
config = yaml.load(open('config.yaml'))

vmdk = config['enabled_image_drivers']['vmdk']
qcow2 = config['enabled_image_drivers']['vmdk']
raw = config['enabled_image_drivers']['vmdk']
