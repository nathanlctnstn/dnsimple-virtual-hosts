#!/usr/bin/python
import sys
import os
import grp
import pwd
from dnsimple import DNSimple
from requests import get
import configparser

if os.getuid() != 0:
    print "This script requires \033[91msudo\033[0m to execute. Please run again wil evelated permissions!"
    sys.exit(1)

#config file setup
config = configparser.ConfigParser()
config.read('config.ini')

#config.ini variables
server_conf = config['host']['server_conf']
site_root_base = config['host']['site_root_base']
conf_base = config['host']['conf_base']
default_user = config['host']['default_user']
default_group = config['host']['default_group']
dnsimple_api_token = config['dnsimple']['api_token']
dnsimple_email_address = config['dnsimple']['email_address']
use_dnsimple = int(config['dnsimple']['use'])

#check variables
conf_line = "IncludeOptional "+conf_base+"*.conf"
read_file = open(server_conf)
append_file = open(server_conf, "a")

if not conf_line in read_file:
    read_file.close()
    open(server_conf, "a").write("\n#Include virtual host configuration files\n"+conf_line)
    append_file.close()
    sys.exit(1)
    
#ip address of requesting server
ip = get('http://api.ipify.org').text

if use_dnsimple == 1:
    dns = DNSimple(email=dnsimple_email_address, api_token=dnsimple_api_token)

    domains = dns.domains()
    domainList = list()

    print "==AVAILABLE DOMAINS=="   

    counter = 1
    for domain in domains:
        domainList.append(domain['domain']['name'])
        print str(counter)+")"+domain['domain']['name']
        counter += 1
    
    domain_choice = int(raw_input('Enter number of base domain: '))
    base = domainList[domain_choice-1]
    
else:    
    #domain components 
    base = raw_input('Enter the base domain name: ')

#get subdomain (prefix)
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
    
    if use_dnsimple == 1:
        #create a dictionary with record data
        new_record = {'record_type' : 'A', 'name' : prefix, 'content' : ip}
        #add the record
        dns.add_record(base, new_record)
