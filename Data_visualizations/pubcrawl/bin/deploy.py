#!/usr/bin/env python

import paramiko
import sys
from os.path import expanduser 
import time

# 1. SSH to box:

print "Connecting to box"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('ec2-34-229-40-206.compute-1.amazonaws.com', username = 'beerweek', key_filename = expanduser("~") + "/.ssh/id_rsa")

# 5. Git pull from bitbucket

ssh.exec_command("rm -rf pubcrawl; git clone git@bitbucket.org:kejnn/pubcrawl.git")
print "Pull from BitBucket successful"
time.sleep(10)

ssh.exec_command("touch /srv/shiny-server/delme")
time.sleep(2)
ssh.exec_command("rm -rf /srv/shiny-server/*")
time.sleep(2)
ssh.exec_command("cp -rf ~/pubcrawl/shiny-server/. /srv/shiny-server/")
time.sleep(2)
ssh.exec_command("cp -f ~/pubcrawl/shiny-server/ /srv/shiny-server/")
time.sleep(2)
ssh.exec_command("sudo systemctl stop shiny-server")
time.sleep(2)

ssh.exec_command("sudo systemctl start shiny-server")

print "Script fully executed ... exiting" 
ssh.close()
## EOF ##
