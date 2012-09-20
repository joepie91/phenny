#!/usr/bin/env python
# coding=utf-8
"""
ipinfo.py - Phenny IP Information Module
Copyright 2012, Sven Slootweg (joepie91), cryto.net
Licensed under the WTFPL.

I live off donations entirely. If you appreciate this module and wish to
donate something, even if just a little, have a look on my donation page
over at http://cryto.net/~joepie91/donate.html - Thanks!
"""

import subprocess, json, urllib

def ping(phenny, input):
	try:
		host = input.group(2)
		ping_interval = "0.5"
		
		print "Ping issued for host %s" % host
		
		responses = []
		ping = subprocess.Popen(["ping", "-c", "4", "-i", ping_interval, host], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		out, error = ping.communicate()
		
		for line in out.splitlines():
			if line.strip() != "":
				if line.startswith("PING"):
					pass
				elif line.startswith("rtt"):
					stats_block = line.split()[3]
					stats = stats_block.split("/")
					pmin = float(stats[0])
					pavg = float(stats[1])
					pmax = float(stats[2])
					pmdev = float(stats[3])
				elif line.startswith("-"):
					pass
				elif "transmitted" in line:
					packetloss = int(line.split()[5].replace("%", ""))
				else:
					parts = line.split()
					
					if "(" in line:
						responding_host = parts[3]
						time = parts[7]
					else:
						responding_host = parts[3][:-1]
						time = parts[6]
						
					ms = float(time.split("=")[1])
					
					responses.append({
						'host': responding_host,
						'time': ms
					})
			
		phenny.say("min %s, avg %s, max %s, mdev %s, packet loss %s" % (pmin, pavg, pmax, pmdev, packetloss))
	except:
		phenny.say("Ping failed. Are you sure you specified a valid hostname or IP?")
	
ping.commands = ['ping']
ping.priority = 'medium'
ping.example = ".ping cryto.net"

def lookup(phenny, input):
	try:
		ip = input.group(2)
		data = json.loads(urllib.urlopen("http://ip-api.com/json/%s" % ip).read())
		
		if data['as'] == None:
			data['as'] = "Unknown AS"
		
		if data['status'] == "success":
			phenny.say("IP: %s (%s)" % (ip, data['reverse']))
			phenny.say("Location: %s, %s, %s (%s)" % (data['city'], data['regionName'], data['country'], data['countryCode']))
			phenny.say("ISP: %s" % data['isp'])
			phenny.say("Organization: %s (%s)" % (data['org'], data['as']))
			phenny.say("Coordinates: latitude %s, longitude %s" % (data['lat'], data['lon']))
		else:
			phenny.say("IP-API indicated the request failed. Are you sure the IP you specified is valid?")
		
	except:
		phenny.say("Could not look up IP. Either you specified an invalid IP, or IP-API is down.")
		raise
		
lookup.commands = ['lookup']
lookup.priority = 'medium'
lookup.example = ".lookup 8.8.8.8"
