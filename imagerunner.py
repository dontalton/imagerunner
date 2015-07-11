#!/usr/bin/env python

from drivers import disk
from drivers.openstack import cinder
from drivers.storage import ceph
import os
import sys
import time
import yaml

sys.path.append("/home/don/imagerunner") 
config = yaml.load(open('config.yaml'))
disk_path = config['working_directory']
disk_extensions = ['raw', 'vmdk', 'qcow2']


while True:

    files = [ file for file in os.listdir(disk_path) if any([file.endswith(ext) for ext in disk_extensions])]

    for file in files:
        now = time.time()
        file = disk_path + file    #naughty
        file_base = os.path.splitext(file)[0]
        file_extension = os.path.splitext(file)[1][1:]

        # need a test so we can just skip files that are not disk images
        # right now this just checks for a yaml file for ALL files
        # we'll also need to check for an existing raw file and delete it if there is no lock
        # oh, and add lock files too

        # make sure the new files haven't been touched for 5+ minutes so we know they're done being uploaded
        if now - os.stat(file).st_mtime > (5 * 60):
            if os.path.isfile(file_base + '.yaml'):
                try:
                    # converting file
                    foo = disk.Disk() 
                    rawsize = foo.convert(file)

                    # put the file into ceph, get a temp uuid name back
                    rados = ceph.CephDriver(rawimage=file_base + '.raw')
                    rbd_name = rados.load()

                    # create a cinder volume that we will attach the rbd to
                    block_storage = cinder.Cinder(bootable=True, metadata='blah')
                    cinder_volume = block_storage.create()

                    # delete the volume cinder created, then rename our converted volume to the 
                    # same name that we just deleted. unfortunately it has to be like this
                    rados.delete(volname=cinder_volume)
                    rados.rename(src=rbd_name, dest=cinder_volume)
                                
                except:
                    print "hit some error", sys.exc_info()[0]
                    raise
        else:
            print "logging: no yaml file exists, move on to the next file"

        time.sleep(5) # will be based on last processed file size, eg ceph will be longer than nfs to let peering complete, etc.
