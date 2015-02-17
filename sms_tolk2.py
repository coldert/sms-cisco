#!/usr/bin/python
# Python 2.7.3 script that matches a string against XML document.

import xml.etree.ElementTree as ET
import re
import sys

# Parse the XML file to tree.
tree = ET.parse('cmdtable2.xml')
root = tree.getroot()

# Define patterns for IP address, interface, AD, placeholder ...
re_ipaddress = re.compile("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/?(\d{1,2})?$")
re_interface = re.compile("^([a-z-]+\d{1,2}(/\d{1,2})*?)$")
re_ad = re.compile("^ad(\d*)$")
re_placeholder = re.compile(r"#.*\b")

# Variables to hold IP address, subnet mask and interface identifier
str_ip = []
str_interface = []
str_ad = []

def command_handler(cmd):
	# Makes string lowercase and splits it of at space,enter,tab etc..
	cmd_list = cmd_string.lower().split()

	# Build a search string for etree iterfind function
	xpath_str = ""

	for i in range(len(cmd_list)):
		# Check if current cmd is an IP address or an interface identifier
		match_ip = re_ipaddress.match(cmd_list[i])
		match_int = re_interface.match(cmd_list[i])
		match_ad = re_ad.match(cmd_list[i])
		if match_ip:
			str_mask = " " + cidr_to_dotted(int(match_ip.group(2))) if (match_ip.group(2)) else "";
			str_ip.append(match_ip.group(1) + str_mask)
		elif match_int:
			str_interface.append(match_int.group(1))
		elif match_ad:
			str_ad.append(match_ad.group(1))
		else:
			# Build each level of search based on number of items in cmd_list
			xpath_str += cmd_list[i] + "/" 

	# Remove the last / from the search string
	xpath_str = xpath_str[:-1]

	# Find XML nodes that match the search string and print the command
	for cmd in root.iterfind(xpath_str):
		command = cmd.text
		# Loop through all ip-addresses and interfaces and put the in the right place in the command
		for i in range(len(str_ip)):
			command = command.replace("#IPADDRESS", str_ip[i], 1)
		for i in range(len(str_interface)):
			command = command.replace("#INTERFACE", str_interface[i], 1)
		for i in range(len(str_ad)):
			command = command.replace("#AD", str_ad[i], 1)	
		# Remove all unused placeholders
		command = re_placeholder.sub("", command)
	return command

# Function to convert /24 to 255.255.255.0
# code.activestate.com/recipies/576483-convert-subnetmask-from-cidr-notation-to-dotdecima/
def cidr_to_dotted(mask):
	bits = 0
	for i in xrange(32-mask,32):
		bits |= (1<<i)
	return "%d.%d.%d.%d" % ((bits & 0xff000000) >> 24, (bits & 0xff0000) >> 16, (bits & 0xff00) >> 8, (bits & 0xff))

# TEST COMMANDS
#cmd_string = "int s0/1/2 ip 192.168.1.1/29"
#cmd_string = "int f0/12 down"
#cmd_string = "route static 209.128.3.0/24 s0/1/0 209.128.3.3 ad150"
#cmd_string = "route default s0/1/0 192.168.24.254"
#print command_handler(cmd_string)