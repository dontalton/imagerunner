from os import path as bytes


class VMDK(object):

    def __init__(self, image):

        self.info = yaml.load(open('config.yaml'))
        self.tmp_storage = self.info['images']['source_location']
        self.image = tmp_storage + image

    def getsize(self, rawimage):

        size_in_gb = bytes.getsize(rawimage) / 1073741824
        if size_in_gb < 1:
            size_in_gb = 1

        return size_in_gb

    def convert(self):
        # convert image
        # foo = getsize(rawimage)
        # return foo
