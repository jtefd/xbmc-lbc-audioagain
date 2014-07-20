#!/usr/bin/env python

import urllib2
import urllib
import re
import os.path

from BeautifulSoup import BeautifulSoup 
from cookielib import CookieJar
from xml.dom.minidom import parseString

class LBCAudioAgain:
	base_url = 'http://lbc.audioagain.com/'
	feeds_url = base_url + '?action=feeds'
	login_url = base_url + '?action=logout'
	
	feed_url_prefix = base_url + 'podcast.php?channel='
	
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	
	def __init__(self, username, password):
		self.username = username
		self.password = password
		
	def get_feeds(self):
		feeds = dict()
		
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		
		data = urllib.urlencode(
			{
				'login_popup_form_playerpane_url':'',
				'user_name':self.username,
				'password':self.password,
				'Submit':'Log In'
			}
		)
		
		request_login_form = urllib2.Request(self.login_url)
		opener.open(request_login_form, data)
		
		request_feed_list = urllib2.Request(self.feeds_url)
		response = opener.open(request_feed_list)
		
		content = response.read();
		
		parser = BeautifulSoup(content)
		
		for div in parser.findAll('div'):
			title = None
			feed_id = None
					
			for a_node in div.findAll('a'):
				titles = re.compile('player=showchannel').findall(a_node['href'])
				
				if len(titles) == 1:
					title = a_node.text
					
				links = re.compile('http://.+podcast\.php\?channel=(.+)$').findall(a_node['href'])
					
				if len(links) == 1:
					feed_id = links[0]
					
			if title != None and feed_id != None:
				feeds[feed_id] = title
		return feeds
	
	def get_feed_url(self, feed_id):
		feed_url = self.feed_url_prefix
		feed_url += feed_id
		
		return feed_url
	
	def get_feed_content(self, feed_id):
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, self.base_url, self.username, self.password)

		handler = urllib2.HTTPBasicAuthHandler(password_mgr)

		opener = urllib2.build_opener(handler)

		try:
			response = opener.open(self.get_feed_url(feed_id))
			
			content=response.read()
			response.close()
			
			return content
	
		except urllib2.HTTPError:
			return None
		
	def get_feed_image(self, feed_id, cache_directory):
		img_path = os.path.join(cache_directory, feed_id + '.jpg')
		
		if not os.path.exists(img_path):
			try:
				image_node = parseString(self.get_feed_content(feed_id)).getElementsByTagName("itunes:image")
				
				urllib.urlretrieve(image_node[0].attributes['href'].value, img_path)
			except:
				print "Failed to retrieve feed image for " + feed_id
				img_path = os.path.join(cache_directory, 'default.jpg')
		
		return img_path
	
	def get_feed_episodes(self, feed_id):
		eps = dict()			
			
		item_node = parseString(self.get_feed_content(feed_id)).getElementsByTagName("item")
			
		for item in item_node:
			eps[item.getElementsByTagName("enclosure")[0].attributes["url"].value] = item.getElementsByTagName("title")[0].firstChild.data		
			
		return eps