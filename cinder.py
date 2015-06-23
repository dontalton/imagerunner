from time import sleep
import json
import rados
import rbd
import requests
import yaml


class Cinder(object):


    def __init__(self, keystone_token=None, bootable=False, volume, metadata):

        self.token = keystone_token
        self.bootable = bootable
        self.volume = volume
        self.metadata = metadata
        self.size = bytes.getsize(volume)
        self.creds = yaml.load(open('config.yaml'))

    def create(self, volume, metadata=None):

        # create cinder volume via api using actual raw image size
        try:
            auth = self.creds['openstack']
            url = auth['cinderurl'] + auth['tenantid'] + '/volumes'
            headers = {'Content-Type':'application/json', 'X-Auth-Token':self.token}
            data = {'volume': {'status':'creating', 'size':'1', 'attach_status':'detached', 'bootable':'true'}}
            r = requests.post(url, headers=headers, data=json.dumps(data))
            response = r.json()
            volid = response['volume']['id']
            volpre = 'volume-' + volid
            volname = str(volpre)
        except:
            print "Failed to create the Cinder volume"

        # flag the cinder volume as bootable
        if self.bootable = True:
            try:
                booty = {'os-set_bootable':{'bootable':True}}
                booturl = url + '/' + volid + '/action'
                s = requests.post(booturl, headers=headers, data=json.dumps(booty))
            except:
                print "Failed to make the volume bootable"

        return volname
