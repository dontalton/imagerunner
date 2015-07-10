# Imagerunner
#### An image conversion and processing tool for large OpenStack cloud deployments.

Imagerunner automatically converts guest disk images and loads them into your storage system. Many cloud providers have clients bringing their own images, and they are often in varying formats and are a pain to manage. IR attempts to reduce the pain associated with converting these images.

IR is a modular system. It monitors a source location for image files. Once a file is detected, IR converts it to the target format, loads it to the storage backend, and finally creates an associated volume or image. IR accepts metadata, such as setting a Cinder volume bootable, or a custom key,value. This is achieved by placing a image-associated YAML file in the watched directory

The Ceph+Cinder workflow is:

1. The image and metadata are detected in source directory.  
2. The image is converted to RAW.  
3. Once the conversion to RAW is complete, the RAW image is then loaded into Ceph automatically.  
4. Once the image is stored in Ceph, the Cinder/Glance entry is automatically created.
5. IR will then clean up working data. It will also take a configurable pause, so as not to trash your storage performance.

  
### Coming soon
The first driver implementation is Ceph (complete).  
  
TODO: I'll be adding NFS/S3 for sure, and others on request.
