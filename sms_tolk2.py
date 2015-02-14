#!/usr/bin/python
# Python 2.7.3 script that matches a string against XML document.

#TODO: Classify. Make a command object.

import xml.etree.ElementTree as ET
import re
import sys

# Test commands
#cmd_string = "int port-channel0/12 ip 192.168.1.1/29"
#cmd_string = "int f0/12 down"
#cmd_string = "route static 209.128.3.1/24 s0/1/0"
cmd_string = "route default s0/1/0"
# Makes string lowercase and splits it of at space,enter,tab etc..
cmd_list = cmd_string.lower().split()

# Define patterns for IP address, interface identifier ...
re_ipaddress = re.compile("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/?(\d{1,2})?$")
re_interface = re.compile("^([a-z-]+\d{1,2}(/\d{1,2})*?)$")

# Parse the XML file to tree.
tree = ET.parse('cmdtable2.xml')
root = tree.getroot()

# Function to convert /24 to 255.255.255.0
# code.activestate.com/recipies/576483-convert-subnetmask-from-cidr-notation-to-dotdecima/
def cidrToDotted(mask):
	if mask == "":
		return ""
	else:
		mask = int(mask)
		bits = 0
		for i in xrange(32-mask,32):
			bits |= (1<<i)
		return "%d.%d.%d.%d" % ((bits & 0xff000000) >> 24, (bits & 0xff0000) >> 16, (bits & 0xff00) >> 8, (bits & 0xff))

# Build the actual command to be sent to the device
def buildCommand(cmd):
	cmd = cmd.replace("#INTERFACE", str_interface)	
	cmd = cmd.replace("#IPADDRESS", str_ip)
	cmd = cmd.replace("#MASK", cidrToDotted(str_mask))	
	return cmd

# Build a search string for etree iterfind function
xpath_str = ""
# Variables to hold IP address, subnet mask and interface identifier
str_ip = ""
str_mask = ""
str_interface = ""

for i in range(len(cmd_list)):
	# Check if current cmd is an IP address or an interface identifier
	match_ip = re_ipaddress.match(cmd_list[i])
	match_int = re_interface.match(cmd_list[i])
	if match_ip:
		# TODO: Handle multiple instances of IP addresses in a command
		str_ip = match_ip.group(1)
		str_mask = match_ip.group(2)
	elif match_int:
		str_interface = match_int.group(1)
	else:
		# Build each level of search based on number of items in cmd_list
		xpath_str += cmd_list[i] + "/" 

# Remove the last / from the search string
xpath_str = xpath_str[:-1]

# Find XML nodes that match the search string and print the command
for cmd in root.iterfind(xpath_str):
	# Print the text inside the xml tag (i.e the actual command to be sent to the Cisco device
	print "\nCOMMAND: " + buildCommand(cmd.text) + "\n"

# Print the matched IP address and interface identifier
if str_ip: print "IP ADDRESS: " + str_ip
if str_mask: print "SUBNET MASK: " + cidrToDotted(str_mask)
if str_interface: print "INTERFACE: " + str_interface
