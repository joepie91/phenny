#!/usr/bin/env python
# coding=utf-8
"""
github.py - Phenny GitHub Watching Module
Copyright 2012, Sven Slootweg (joepie91), cryto.net
Licensed under the WTFPL.

I live off donations entirely. If you appreciate this module and wish to
donate something, even if just a little, have a look on my donation page
over at http://cryto.net/~joepie91/donate.html - Thanks!
"""

import time, re, threading, json, urllib, sys

try:
	import dateutil.parser
except ImportError, e:
	print "Could not import dateutil.parser, install python-dateutil or the GitHub watcher will not work!"

watcher_started = False
watched_users = []

def update_config():
	global watched_users
	json.dump(watched_users, open("gh_watched.json", "w"))
	
def read_config():
	global watched_users
	try:
		watched_users = json.load(open("gh_watched.json", "r"))
	except Exception, e:
		pass
	
read_config()

def parse_github_feed(url):
	entries = []
	
	feed = json.load(urllib.urlopen(url))
	
	for entry in feed:
		try:
			commits = [commit[2] for commit in entry['payload']['shas']]
		except KeyError, e:
			continue
		
		user = entry['actor']
		
		try:
			repo = entry['repository']['name']
		except KeyError, e:
			# Not a repository event?
			continue
			
		url = entry['url']
		
		try:
			branch = entry['payload']['ref'].replace("refs/heads/", "")
		except Exception, e:
			branch = "?"
			
		date = dateutil.parser.parse(entry['created_at']).timetuple()
		
		entries.append({
			"user": user,
			"repository": repo,
			"branch": branch,
			"timestamp": date,
			"commits": commits,
			"url": url	
		})
		
	return entries

class GithubWatcher(threading.Thread):
	def __init__(self, username, phenny):
		self.url = "https://github.com/%s.json" % username
		self.last_timestamp = 0
		self.phenny = phenny
		
		data = parse_github_feed(self.url)
		for entry in data:
			stamp = time.mktime(entry['timestamp'])
			if stamp > self.last_timestamp:
				self.last_timestamp = stamp
		
		threading.Thread.__init__(self)
	
	def run(self):
		while True:
			top_timestamp = 0
			
			try:
				data = parse_github_feed(self.url)
			except Exception, e:
				# Back off
				sys.stderr.write("WARNING: Something went wrong! %s" % repr(e))
				time.sleep(120)
				continue
				
			data.reverse()
			
			for entry in data:
				stamp = time.mktime(entry['timestamp'])
				if stamp > self.last_timestamp:
					commits = ", ".join([u"'\u000302%s\u000f'" % commit for commit in entry['commits']])
					self.phenny.say(u"\u000304%s\u000f made %s commit(s) to \u0002\u000303%s\u000f on branch \u0002\u000310%s\u000f: %s (%s)" % (entry['user'], len(entry['commits']), entry['repository'], entry['branch'], commits, entry['url']))
					if stamp > top_timestamp:
						top_timestamp = stamp
						
			if top_timestamp != 0:
				self.last_timestamp = top_timestamp
				
			time.sleep(30)

def start_github(phenny, input):
	global watcher_started, watched_users
	
	if watcher_started == False:
		for user in watched_users:
			t = GithubWatcher(user, phenny)
			t.start()
		watcher_started = True
		phenny.say("Now watching GitHub for users %s." % (", ".join(watched_users)))
	else:
		phenny.say("Already watching GitHub.")
	
start_github.commands = ['startgh']
start_github.priority = 'medium'
start_github.example = ".startgh"

def add_github(phenny, input):
	global watched_users
	
	if len(watched_users) > 5:
		# Really basic way to prevent people from spamming non-existent account watch requests.
		return phenny.reply("Maximum amount of watchable accounts reached.")
	
	user = input.group(2)
	
	if not user:
		return phenny.reply("No user specified.")
	
	phenny.say("User %s is now being watched." % user)
		
	watched_users.append(user)
	t = GithubWatcher(user, phenny)
	t.start()
	
	update_config()

add_github.commands = ['addgh']
add_github.priority = 'medium'
add_github.example = ".addgh"
