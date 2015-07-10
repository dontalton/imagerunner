from os import path as bytes
import rados
import rbd
import uuid
import yaml


class CephDriver(object):

    def __init__(self, rawimage, metadata=None):

        self.config = yaml.load(open('config.yaml'))
        self.rawimage = rawimage
        self.metadata = metadata
        self.cephpool = self.config['storage']['ceph']['pool']
        self.cephconf = self.config['storage']['ceph']['config']
        self.size = bytes.getsize(rawimage)
        self.rbdname = str(uuid.uuid4())

    def load(self):

        size_in_gb = self.size

        with rados.Rados(conffile=self.cephconf) as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.create(ioctx, self.rbdname, self.size)
                with rbd.Image(ioctx, self.rbdname) as image:
                    image.lock_exclusive('totallylocked')
                    with open(self.rawimage) as file:
                        chunk = 8192
                        offset = 0
                        while True:
                            image_buffer = file.read(chunk)
                            if not image_buffer:
                                image.unlock('totallylocked')
                                image.close()
                                break
                            image.write(image_buffer, offset)
                            offset = offset + chunk

    def _read(self):

        with rados.Rados(conffile=self.cephconf) as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                with rbd.Image(ioctx, self.rbdname) as image:
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

    def delete(self, volname):
        with rados.Rados(conffile=self.cephconf) as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.remove(ioctx, volname)

    def rename(self, src, dest):
        with rados.Rados(conffile=self.cephconf) as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.rename(ioctx, src, dest)
