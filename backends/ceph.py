from os import path as bytes
from imagerunner import utils as creds
import rados
import rbd
import requests
import yaml

print creds.os_user


class Ceph(object):

    # Usage:
    # ceph = Ceph(rawimage='myimage', metadata='there', cephpool='rbd')
    # ceph.load()   this sends the file to the cluster
    # ceph.read()   reads it back from the cluster if you want to check bytes; for testing only

    def __init__(self, rawimage, metadata, cephpool):

        self.rawimage = rawimage
        self.metadata = metadata
        self.cephpool = cephpool
        self.size = bytes.getsize(rawimage)

    def load_into_ceph(self):

        with rados.Rados(conffile='/etc/ceph/ceph.conf') as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.create(ioctx, self.rawimage, self.size)
                with rbd.Image(ioctx, self.rawimage) as image:
                    image.lock_exclusive('totally_locked')
                    with open(self.rawimage) as file:
                        chunk = 8192
                        offset = 0
                        while True:
                            image_buffer = file.read(chunk)
                            if not image_buffer:
                                image.unlock('totally_locked')
                                image.close()
                                break
                            image.write(image_buffer, offset)
                            offset = offset + chunk

    def read_from_ceph(self):

        with rados.Rados(conffile='/etc/ceph/ceph.conf') as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                with rbd.Image(ioctx, self.rawimage) as image:
                    chunk = 8192
                    offset = 0
                    output = open(self.rawimage + '.fromcluster', 'a')
                    while True:
                        try:
                            image_buffer = image.read(offset, chunk)
                            if not image_buffer:
                                break
                            output.write(image_buffer)
                            offset = offset + chunk
                        except rbd.InvalidArgument:
                            break

    def create_cinder_volume(self):
        pass
        # get the size of the actual raw image
        # create cinder volume via api using actual raw image size
        # use rbd client to delete the cinder-created rbd file
        # rename the rawimage rbd to whatever the cinder-created uuid name is
