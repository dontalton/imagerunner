from os import path as bytes
import rados
import rbd


class CephDriver(object):

    def __init__(self, rawimage, metadata, pool, config='/etc/ceph/ceph.conf', **kwargs):

        self.rawimage = rawimage
        self.metadata = metadata
        self.pool = pool
        self.size = bytes.getsize(rawimage)
        self.config = config
        self.cinder = kwargs['cinder']

    def load(self):

        size_in_gb = self.size

        with rados.Rados(conffile=self.config) as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.create(ioctx, self.rawimage, self.size)
                with rbd.Image(ioctx, self.rawimage) as image:
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

    def read(self):

        with rados.Rados(conffile=self.config) as cluster:
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

    def delete(self, volname):
        with rados.Rados(conffile=self.config) as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.remove(ioctx, volname)

    def rename(self, src, dest):
        with rados.Rados(conffile=self.config) as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.rename(ioctx, src, dest)
