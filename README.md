## dnsimple-virtual-hosts
Just a warning... I've been using these scripts as an excuse to teach myself Python so I'm sure they're not pretty!

#### Abstract

DNSimple and Apache/HTTPD virtual host management scripts. Using these scripts virtual hosts can be automatically allocated and deallocated on the local file system and on DNS simple leveraging the API.

Allocation includes:
* Directory structure/permissions
* Config file creation
* DNS record creation

Deallocation includes:
* Complete removal of directory structure
* Removal of config file
* Removal of DNS record

#### Use
The addVirtualHost.py script will check for the existance of the virtual host config file directory (conf_base in the conf.ini file) and for the inclusion of that directiory in your webserver configuration file (server_conf in the conf.ini file). If either of these are not found, they will be automatically created.

Setup the config.ini file to your liking. These scripts can be used without the DNSimple API, that parameter needs to be set in the config.ini file.

These scripts need to be run as <code>sudo</code> so they can modify files within <code>/etc/httpd/virtual-hosts</code>

Run either the add or remove script and restart the Apache/HTTPD service once execution is complete

#### Package requirements
Using pip, install:
* dnsimple
* configparser

#### Planned future improvements
* Base HTTPd setup script
* setup.py for package requirements and inclusion in bin
