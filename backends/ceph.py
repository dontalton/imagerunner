from os import path as bytes
import json
import rados
import rbd
import requests
import yaml


class Ceph(object):


    def __init__(self, rawimage, metadata, cephpool, token):

        self.rawimage = rawimage
        self.metadata = metadata
        self.cephpool = cephpool
        self.token = token
        self.size = bytes.getsize(rawimage)
        self.creds = yaml.load(open('config.yaml'))

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

        self._create_cinder_volume()


    def _read_from_ceph(self):

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

    def _delete_from_ceph(self, volid):
        with rados.Rados(conffile='/etc/ceph/ceph.conf') as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.remove(ioctx, volid)

    def _rename_in_ceph(self, src, dest):
        with rados.Rados(conffile='/etc/ceph/ceph.conf') as cluster:
            with cluster.open_ioctx(self.cephpool) as ioctx:
                block_device = rbd.RBD()
                block_device.rename(ioctx, src, dest)



    def _create_cinder_volume(self):

        # create cinder volume via api using actual raw image size
        auth = self.creds['openstack']
        url = auth['cinderurl'] + auth['tenantid'] + '/volumes'
        headers = {'Content-Type':'application/json', 'X-Auth-Token':self.token}
        data = {'volume': {'status':'creating', 'size':'1', 'attach_status':'detached', 'bootable':'true'}}
        r = requests.post(url, headers=headers, data=json.dumps(data))
        response = r.json()
        volid = response['volume']['id']

        # flag the cinder volume as bootable
        booty = {'os-set_bootable':{'bootable':True}}
        booturl = url + '/' + volid + '/action'
        s = requests.post(booturl, headers=headers, data=json.dumps(booty))

        # use rbd client to delete the cinder created image, then rename our own
        self._delete_from_ceph(volid=str(volid)) # ceph wants a string, not unicode
        self._rename_in_ceph(src=self.rawimage, dest=volid)
        return
