#!/usr/bin/env python

sys.path.append("/home/don/imagerunner") 

# pseudocode

def monitordir:
    files = glob.glob(path/regex) # eg glob.glob('dir/*[0-9].*')
    if files:
      for file in files:
        if os.stat(file).mtime > 5 minutes:
          if os.path.splitext(file) == '.vmdk' or '.qcow2' or 'whatev':
            if os.path.isfile(file.strip(extention) + '.yaml':
              file.convert(file)
              file.load_to_storage(rawfile)
              file.make_volume_or_image(rawfile)
              file.delete(file, rawfile)
              sleep(sometime)
            else:
              print 'no yaml file found'
        else
          next file

while True:
	monitordir()
