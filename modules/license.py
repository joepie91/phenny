#!/usr/bin/env python
# coding=utf-8
"""
license.py - Phenny TL;DR Legal module
Copyright 2012, Sven Slootweg (joepie91), cryto.net
Licensed under the WTFPL.

I live off donations entirely. If you appreciate this module and wish to
donate something, even if just a little, have a look on my donation page
over at http://cryto.net/~joepie91/donate.html - Thanks!
"""

import subprocess, json, urllib, re, sys, requests

def getlicense(phenny, input):
	query = input.group(2)
	req = requests.get("http://tldrlegal.com/search", params={"q": query, "c": "[]"})
	
	
	if len(req.history) == 1:
		# We have to pick a license. Grab the top one.
		matches = re.search("href='(\/license\/[^']+)'", req.text)
		
		if matches is None:
			phenny.say("Sorry, could not find any licenses for that search term.")
			return
		
		req = requests.get("http://tldrlegal.com%s" % matches.group(1))
	elif req.url == "http://www.tldrlegal.com/license/404":
		phenny.say("Sorry, could not find any licenses for that search term.")
		return
	
	if req.status_code != 200:
		phenny.say("Something went wrong.")
		return
	
	#print req.text
	title = re.search("<h1>(.+) Explained<\/h1>", req.text).group(1)
	description = re.search("<div id='license_desc' class='tl-box-center upshadow'><div class='header'>Quick Summary:<\/div><p>(.+?)<\/p>", req.text).group(1)
	
	phenny.say("%s: %s %s" % (title, description, req.url))
	
getlicense.commands = ['license']
getlicense.priority = 'high'
getlicense.example = ".license wtfpl"
