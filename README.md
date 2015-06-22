# imagerunner
An image processing and conversion tool for large cloud deployments.

Imagerunner allows for the batch conversion between image formats. A problem that many cloud providers have is clients bringing their own images; they are often in varying formats.

Imagerunner will become a modular conversion system. The foundation of Imagerunner is based on a distributed that queue that monitors a source location for image files. Upon detecting a file, the conversion process commences and the file is delivered to the target location in the target format, and with any necessary metadata.

The first implementation target Ceph and Cinder for images that are "pets". The workflow is:

Image is detected in source directory, and any image metadata is stored in a corresponding YAML file.  
The file is renamed to a temporary working file.  
The file is converted to RAW.  
Once the conversion to RAW is complete, the file is then loaded into Ceph directly using python-rados.  
Once the RAW image is placed into RADOS, and the UUID returned, an API query is constructed to create a Cinder volume   from the Ceph UUID and metadata. Once this is complete, the volume will be available and bootable.  
