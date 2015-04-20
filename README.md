## dnsimple-virtual-hosts
Just a warning... I've been using these scripts as an excuse to teach myself Python so I'm sure they're not pretty!

#### Abstract

DNSimple/Apache virtual host management scripts. Using these scripts virtual hosts can be automatically allocated and deallocated on the local file system and on DNS simple leveraging the API.

Allocation includes:
* Directory structure/permissions
* Config file creation
* DNS record creation

Deallocation includes:
* Complete removal of directory structure
* Removal of config file
* Removal of DNS record

#### Use
Setup the config.ini file to your liking. These scripts can be used without the DNSimple API, that parameter needs to be set in the config.ini file.

These scripts need to be run as <code>sudo</code> so they can modify files within <code>/etc/httpd/VIRTUAL_HOST_DIRECTORY</code>

#### Package requirements
Using pip, install:
* dnsimple
* configparser

#### Planned future improvements
* Base HTTPd setup script
* setup.py for package requirements and inclusion in bin
