#!/usr/bin/python
import sys
import os
import grp
import pwd
from dnsimple import DNSimple
from requests import get
import configparser

#config file setup
config = configparser.ConfigParser()
config.read('config.ini')

#config.ini variables
site_root_base = config['host']['site_root_base']
conf_base = config['host']['conf_base']
default_user = config['host']['default_user']
default_group = config['host']['default_group']
dnsimple_api_token = config['dnsimple']['api_token']
dnsimple_email_address = config['dnsimple']['email_address']

#ip address of requesting server
ip = get('http://api.ipify.org').text

#domain components 
base = raw_input('Enter the base domain name: ')
prefix = raw_input('Enter the domain prefix: ')
fqdn = prefix+"."+base

#file and directories
site_root = site_root_base+fqdn
public_html = site_root+'/public_html'
conf_file = conf_base+fqdn+'.conf'

#gid information for the default group
groupinfo = grp.getgrnam(default_group)
gid = groupinfo.gr_gid

#uid information for the default user
userinfo = pwd.getpwnam(default_user)
uid = userinfo.pw_uid

#check if the desired site exists on this box
if not os.path.exists(site_root):
    os.makedirs(site_root)
    os.chmod(site_root, 0770)
    os.chown(site_root, uid, gid)
    
    os.makedirs(public_html)
    os.chmod(public_html, 0774)
    os.chown(public_html, uid, gid)

    #write the virtual host configuration file
    outfile = open(conf_file, 'w')

    outfile.write("<VirtualHost *:80>\n")
    outfile.write("\tServerName "+fqdn+"\n")
    outfile.write("\tDocumentRoot "+public_html+"\n")
    outfile.write("\tErrorLog /var/log/httpd/"+fqdn+".log\n")
    outfile.write("\tCustomLog /var/log/httpd/"+fqdn+".log combined\n")
    outfile.write("</VirtualHost>")

    outfile.close()

    #create DNSimple object
    dns = DNSimple(email=dnsimple_email_address, api_token=dnsimple_api_token)
    #create a dictionary with record data
    new_record = {'record_type' : 'A', 'name' : prefix, 'content' : ip}
    #add the record
    dns.add_record(base, new_record)
