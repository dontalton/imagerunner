# Imagerunner
#### An image processing and conversion tool for large cloud deployments.

Imagerunner allows for the batch conversion between image formats. A problem that many cloud providers have is clients bringing their own images; they are often in varying formats.



Imagerunner will become a modular conversion system. The foundation of Imagerunner is based on a distributed that queue that monitors a source location for image files. Upon detecting a file, the conversion process commences and the file is delivered to the target location in the target format, and with any necessary metadata.



The first implementation targets Ceph and Cinder for VMDK images that are "pets". The workflow is:

1. Image is detected in source directory, and any image metadata is stored in a corresponding YAML file.  
2. The file is renamed to a temporary working file.  
3. The file is converted to RAW.  
4. Once the conversion to RAW is complete, the file is then loaded into Ceph directly using python-rados.
5. At some point we will get fancy with VMWare and pull VMDKs directly from vSphere for batch conversions.



Once the RAW image is placed into RADOS, and the ID returned, an API query is constructed to create a Cinder volume from the Ceph UUID and metadata. Once this is complete, the volume will be available and bootable in Nova.
