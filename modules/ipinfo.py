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

import subprocess, json, urllib, re

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
	host = input.group(2)
	
	if re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", host):
		try:
			ip = host
			data = json.loads(urllib.urlopen("http://ip-api.com/json/%s" % ip).read())
			
			if data['status'] == "success":
				if data['as'] == None:
					data['as'] = "Unknown AS"
					
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
	else:
		dig = subprocess.Popen(["dig", "any", host], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		out, error = dig.communicate()
		
		records = {
			"A": [],
			"AAAA": [],
			"MX": [],
			"TXT": [],
			"SPF": [],
			"NS": [],
			"SOA": [],
			"CNAME": []
		}
		
		for line in out.splitlines():
			if line.startswith(";"):
				pass
			elif line.strip() == "":
				pass
			else:
				parts = re.split("\s+", line)
				
				try:
					records[parts[3]].append(" ".join(parts[4:]))
				except:
					pass
		
		phenny.say("DNS records for %s:" % host)
		
		if len(records["SOA"]) > 0:
			for record in records["SOA"]:
				phenny.say("SOA: %s" % record)
			
		if len(records["NS"]) > 0:
			phenny.say("NS: %s" % ", ".join(records["NS"]))
		
		if len(records["CNAME"]) > 0:
			phenny.say("CNAME : %s" % ", ".join(records["CNAME"]))
			
		if len(records["A"]) > 0:
			phenny.say("A: %s" % ", ".join(records["A"]))
		
		if len(records["AAAA"]) > 0:
			phenny.say("AAAA: %s" % ", ".join(records["AAAA"]))
		
		if len(records["MX"]) > 0:
			phenny.say("MX: %s" % ", ".join(records["MX"]))
		
		if len(records["TXT"]) > 0:
			for record in records["TXT"]:
				phenny.say("TXT: %s" % record)
		
		if len(records["SPF"]) > 0:
			for record in records["SPF"]:
				phenny.say("SPF: %s" % record)
		
		
		
lookup.commands = ['lookup']
lookup.priority = 'medium'
lookup.example = ".lookup 8.8.8.8"
