#!/usr/bin/python
# 
# CSV logging script for stock dump1090
#
# Uses the Requests library to compare the state of planes in view
# and prints changes to standard out
#
# Start dump1090
# modify this script to point to your dump1090 URL if different
# run the script and pipe the output to a file eg:
#
# nohup ./comparer.py >> data.csv 2> data.err < /dev/null &
#
# @th0ma5 on twitter
# http://th0ma5w.github.io
#

import requests, json, datetime, time

import os

import scrollphathd
from scrollphathd.fonts import font3x5 
scrollphathd.set_brightness(0.5)

get_data = lambda : json.loads(requests.get('http://localhost:8080/data.json').content)  
# changed URL

data_diff = lambda new,old : [x for x in new if x not in old]
make_date = lambda : str(datetime.datetime.now())

old_data = []

os.system('clear')
while True:
	flights =[]
	print "--------------------------------"
        print "--      Flight Tracker        --"
        print "--------------------------------"

        try:
                new_data = get_data()
                diffs = data_diff(new_data,old_data)
                old_data = new_data
                if len(diffs) > 0:
                        diff_lines = [','.join([str(y).strip() for y in [make_date()] + x.values()]) for x in diffs]
                        for line in diff_lines:
				if line[32]==",":
					line=""
				else: 
					line = line[32:39]
				if line !="":
					line=line.replace(",","")
#					print line
					flights.append(line)
        except:
                pass
	print "--------------------------------"
	print "--  Sending list to display   --"
	print "--------------------------------"
	for item in flights:
		item = " " + item
		print (item)
		scrollphathd.write_string(item,x=15,y=0)
		length_of_message=len(item)
		line_length=(length_of_message*5)+10
		while line_length >0:
			scrollphathd.show()
			scrollphathd.scroll()
			time.sleep(0.1)
			line_length-=1
		time.sleep(0.1)
		scrollphathd.clear()
		for x in range(0,21):
			for y in range (0,7):
				scrollphathd.set_pixel((20-x),y,1)
			time.sleep(0.01)
			scrollphathd.show()
		scrollphathd.clear()
	print "--------------------------------"
	print "--   sleeping for 5 seconds  ---"
	print "--------------------------------"
        time.sleep(5) 
	os.system('clear')
