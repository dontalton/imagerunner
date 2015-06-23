from os import path as bytes
import json
import rados
import rbd
import requests
import yaml


def read_from_ceph(vol, pool):

    with rados.Rados(conffile='/etc/ceph/ceph.conf') as cluster:
        with cluster.open_ioctx(pool) as ioctx:
            with rbd.Image(ioctx, vol) as image:
                chunk = 8192
                offset = 0
                output = open(vol + '.fromcluster', 'a')
                while True:
                    try:
                        image_buffer = image.read(offset, chunk)
                        if not image_buffer:
                            break
                        output.write(image_buffer)
                        offset = offset + chunk
                    except rbd.InvalidArgument:
                        break

read_from_ceph(vol='volume-b39e8638-a6a5-400d-8027-d30683c07f20', pool='volumes')
