#!/usr/bin/python

import shutil
import os
import sys
from dnsimple import DNSimple
import re
import configparser

if os.getuid() != 0:
    print "This script requires \033[91msudo\033[0m to execute. Please run again wil evelated permissions!"
    sys.exit(1)

#config file setup
config = configparser.ConfigParser()
config.read('config.ini')

#config.ini variables
site_root_base = config['host']['site_root_base']
conf_base = config['host']['conf_base']
dnsimple_api_token = config['dnsimple']['api_token']
dnsimple_email_address = config['dnsimple']['email_address']
use_dnsimple = int(config['dnsimple']['use'])

#directory where virtual host conf files are held
conf_dir = conf_base

#get all files in directory
conf_files = os.listdir(conf_dir)

#counter
conf_count = 0

#print out each file found in the conf directory
for conf_file in conf_files:
    print "("+str(conf_count)+")"+conf_file
    conf_count += 1

#prompt for virtual host to remove
del_choice = int(raw_input("Which virtual host would you like to remove? ")) 

#determine file based on config choice in list
del_file = conf_files[del_choice]

#build full file location
del_file_location = conf_dir+del_file

#valid answers that will allow script to proceed
yes = set(['yes','y'])

#confirm deletion... people are stupid
confirm = raw_input("Confirm deletion of "+del_file+"?[y/N] ").lower()

#if deletion confirmed from set
if confirm in yes:
    #chop the .conf off to get the fqdn
    fqdn=del_file[:-5]
    #grab just the subdomain portion from the fqdn
    subdomain = fqdn.split('.')[0]
    
    #get the base domain name out of the fqdn    
    base_domain = re.sub("^[^.]*\.(?=\w+\.\w+$)", "", fqdn)

    #determine the site root
    site_root = site_root_base+fqdn+"/"

    if use_dnsimple == 1:
        #create DNSimple object
        dns = DNSimple(email=dnsimple_email_address, api_token=dnsimple_api_token)
    
        #read in all records of domain from dnsimple
        records = dns.records(base_domain)

        #declare variable for record it (to be determined below)
        record_id = None

        #iterate through the list of dictionary objects
        for record in records:
            #access the record key and the nested name key
            record_name = record['record']['name']
    
            #see if what you just found matches the sub domain you're looking for
            if record_name == subdomain:
                #if it is, access the nested id key and store it
                record_id = record['record']['id']
                break
 
        #if the variable has data (determined above)
        if record_id:
            #use DNSimple API to remove the record
            dns.delete_record(base_domain, record_id)
    else:
        print "Error! No DNS record found for deletion."
        sys.exit(0)
        
    #remove the conf file
    os.remove(del_file_location)
    #remove the site file structure and contents
    shutil.rmtree(site_root)

else:
    print "Aborting!"
