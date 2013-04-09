#!/usr/bin/env python
# coding=utf-8
"""
bitcoin.py - Phenny Bitcoin exchange rate module
Copyright 2012, Sven Slootweg (joepie91), cryto.net
Licensed under the WTFPL.

I live off donations entirely. If you appreciate this module and wish to
donate something, even if just a little, have a look on my donation page
over at http://cryto.net/~joepie91/donate.html - Thanks!
"""

import requests, json

def getrate(phenny, input):
	response = requests.get("http://blockchain.info/ticker")
	data = json.loads(response.text)
	
	phenny.say("1 BTC = $%.2f, 1 BTC = €%.2f" % (data["USD"]["15m"], data["EUR"]["15m"]))
	
getrate.commands = ['bitcoin']
getrate.priority = 'high'
getrate.example = ".bitcoin"
