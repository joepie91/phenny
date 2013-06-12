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

import time, re, threading

try:
	import feedparser
except ImportError, e:
	print "WARNING: feedparser module not found, GitHub watcher will not work!"

watcher_started = False

def parse_github_feed(url):
	entries = []
	
	feed = feedparser.parse(url)
	
	for entry in feed.entries:
		commits = [commit.strip() for commit in re.findall("<blockquote>(.*?)<\/blockquote>", entry.summary, re.DOTALL)]
		
		if len(commits) == 0:
			commits = [entry.title]
		
		link_match = re.search("\/([^/]+)\/([^/]+)\/compare", entry.link)
		user = link_match.group(1)
		repo = link_match.group(2)
		date = entry.published_parsed
		
		entries.append({
			"user": user,
			"repository": repo,
			"timestamp": date,
			"commits": commits	
		})
		
	return entries

class GithubWatcher(threading.Thread):
	def __init__(self, username, phenny):
		self.url = "https://github.com/%s.atom" % username
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
			data = parse_github_feed(self.url)
			
			for entry in data:
				stamp = time.mktime(entry['timestamp'])
				if stamp > self.last_timestamp:
					self.phenny.say("%s made %s commit(s) to %s: %s" % (entry['user'], len(entry['commits']), entry['repository'], ", ".join(["'%s'" % commit for commit in entry['commits']])))
					if stamp > top_timestamp:
						top_timestamp = stamp
						
			if top_timestamp != 0:
				self.last_timestamp = top_timestamp
				
			time.sleep(30)

def start_github(phenny, input):
	global watcher_started
	
	if watcher_started == False:
		t = GithubWatcher("joepie91", phenny)
		t.start()
		watcher_started = True
		phenny.say("Now watching GitHub.")
	
start_github.commands = ['startgh']
start_github.priority = 'medium'
start_github.example = ".startgh"
