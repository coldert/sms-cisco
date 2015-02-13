#!/usr/bin/python

import paramiko

#ssh = paramiko.SSHClient()
#ssh.connect('192.168.1.1',username='landizz',password='admin')

cmd = raw_input("Please insert the short command: ")


import xml.etree.ElementTree as ET

tree = ET.parse('cmdtable.xml')
root = tree.getroot()

for child in root.iter():
	print child.get('name'), child.text


