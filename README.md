# Imagerunner
#### An image conversion and processing tool for large OpenStack cloud deployments.

Imagerunner converts and load guest images into Cinder and Glance. Many cloud providers have clients bringing their own images, and they are often in varying formats. IR attempts to reduce the pain associated with converting these images.

IR is a modular system. It monitors a source location for image files. Once a file is detected, IR converts it to the target format, loads it to the storage backend, and finally creates an associated volume or image. 

The first driver implementation is for Ceph-backed Cinder volumes that are sourced from VMDK images.  
  
The Ceph+Cinder workflow is:

1. Image is detected in source directory, and any image metadata is stored in a corresponding YAML file.  
2. The file is renamed to a temporary working file.  
3. The file is converted to RAW.  
4. Once the conversion to RAW is complete, the file is then loaded into Ceph directly using a RADOS context.
5. A Cinder volume with the same (reported) size of the Ceph RBD is created.
6. This new Cinder volume is marked bootable.
7. The Cinder-created volume's RBD is deleted from Ceph.
8. The IR-created RBD is renamed to the Cinder-created volume RBD name.  
  
We have to do this workaround since we cannot pass an existing RBD value when creating a Cinder volume.
