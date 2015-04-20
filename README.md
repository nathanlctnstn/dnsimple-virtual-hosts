## dnsimple-virtual-hosts
DNSimple/Apache virtual host management scripts. Using these scripts virtual hosts can be automatically allocated and deallocated on the local file system and on DNS simple leveraging the API.

Allocation includes:
* Directory structure/permissions
* Config file creation
* DNS record creation

Deallocation includes:
* Complete removal of directory structure
* Removal of config file
* Removal of DNS record

### Package requirements
Using pip, install:
* dnsimple
* configparser

### Planned future improvements
* Base HTTPd setup script
* setup.py for package requirements and inclusion in bin
