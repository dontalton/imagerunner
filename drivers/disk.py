import os
import subprocess
import yaml


class Disk(object):

#    def __init__(self, image):
#        self.image = image

    def getsize(self, rawimage):
        size_in_gb = os.path.getsize(rawimage) / 1073741824
        if size_in_gb < 1:
            size_in_gb = 1
        return size_in_gb

    def convert(self, image):

        file_base = os.path.splitext(image)[0]
        file_extension = os.path.splitext(image)[1][1:]
        config = yaml.load(open('config.yaml'))
        disk_path = config['working_directory']

        rawimage = file_base + '.raw'
        # i should probably create a lock file here, something I can test for in imagerunner.py maybe?
        # like if file.lock then next
        subprocess.call(['/usr/bin/qemu-img', 'convert', '-f', file_extension, '-O', 'raw', image, rawimage])
        if os.path.isfile(rawimage):
            size = self.getsize(rawimage)
            return size
        else:
            return "something broke during conversion"
