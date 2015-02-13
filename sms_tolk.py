#!/usr/bin/python
#Python 2.7.3, Script that matches a string against XML document.

import xml.etree.ElementTree as ET
import re
import sys

#Parse the XML file to tree.
tree = ET.parse('cmdtable.xml')
root = tree.getroot()

#Test command to match XML document.
cmdstring = "int ip"
#Makes string lowercase and splits it of at space,enter,tab etc..
cmd_list = cmdstring.lower().split()
#Int to go over cmd list
y = 0
match = []

for i in root.iter():	#Iterates over XML tree
	target = i.attrib.get('name') #Gets name value from the current element
	if target !=  None: 
		try: #Try as long as except doesn't happend.
			if target == cmd_list[y]: #IF attribute name matches correspondening command in cmd_list.
				match.append(target) #Then add that the match to another list
				y = y + 1 #Increase int variable that irerates over cmd_list
				print "Match", match #To analyze results
				continue #Continue with previous for-loop, but start from the top.
			else: #If no match
				print "No match" #To analyze results
					
		except IndexError:#If cmd_list runs out of commands to match i.e. 'IndexError'
			cmderr_msg = 32 #Error message for End of Command list.
			print "Error:32, EoC"
			break
