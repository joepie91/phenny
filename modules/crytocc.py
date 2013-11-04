#!/usr/bin/env python
# coding=utf-8
"""
bitcoin.py - Phenny channel welcoming module
Copyright 2012, Sven Slootweg (joepie91), cryto.net
Licensed under the WTFPL.

I live off donations entirely. If you appreciate this module and wish to
donate something, even if just a little, have a look on my donation page
over at http://cryto.net/~joepie91/donate.html - Thanks!
"""

import requests, json

def welcome(phenny, input):
	phenny.say("%s: welcome to %s! Please be aware that this channel is publicly logged, and make sure to read the rules in the channel topic. You may hide messages from the public logs by prefixing them with [off]." % (input.group(2), input.sender))
	
welcome.commands = ['welcome']
welcome.priority = 'high'
welcome.example = ".welcome joepie91"
