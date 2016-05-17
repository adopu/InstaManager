import requests
import random
import time
import datetime
import logging
import json
import atexit
import signal
import itertools

import selfie_scraper
import selfie_filter

class InstaManager:

	url = {
		'home' : 'https://www.instagram.com/'
		'login' : 'https://www.instagram.com/accounts/login/ajax/'
		'logout' : 'https://www.instagram.com/accounts/logout/'
		'tags' : 'https://www.instagram.com/explore/tags/'
		'likes' : 'https://www.instagram.com/web/likes/%s/like/'
	}
	user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
	accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
	like_count = 0
	media_by_tag = 0
	login_status = False
	error_400_count = 0
	error_400_max = 3
	ban_sleep = 3600

	def __init__(self, ID, password,
				tag_list = ['cat', 'car', 'dog'],
				like_speed = 'high',
				likes_per_tag = 5,
				selfie_filter = 'off'):

		self.media_max_like = 200
		self.media_min_like = 5
		self.user_id = ID.lower()
		self.user_password = password
		self.tag_list = tag_list
		self.likes_per_tag = likes_per_tag
		self.media_by_tag = [] #This will be the pool of pictures
		self.s = requests.Session() #Permits to have persistence in connection
		self.like_speed = like_speed

		# Set pseudo random like speed according to 3 standards		
		if self.like_speed == 'high':
			self.like_delay = 3600 / random.randrange(100,110)
		if self.like_speed == 'medium':
			self.like_delay = 3600 / random.randrange(60,80)
		if self.like_speed == 'low':
			self.like_delay = 3600 / random.randrange(30,40)

		# If the selfie filter is activated, we load the model
		if self.selfie_filter == 'on':
			scrap(selfie, 10, "/home/Pictures")
			selfies = get_dir_features('/home/Pictures')
			classifier = create_classifier(selfies)

		print 'INFO: Instamanager starting'
		start_time = datetime.datetime.now()
		self.login()

		signal.signal(signal.SIGTERM, self.exit) #Receive error signal
		atexit.register(self.exit)

	def exit(self):
		if (self.login_status):
			self.logout()

	def login(self):
		print 'Login in with %s...' % (self.user_id)
		self.s.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1',
    							'ig_vw' : '1920', 'csrftoken' : '',
    							's_network' : '', 'ds_user_id' : ''})
		self.login_post = {'username' : self.user_id,
						   'password' : self.user_password}
		self.s.headers.update ({'Accept-Encoding' : 'gzip, deflate',
								'Accept-Language' : self.accept_language,
								'Connection' : 'keep-alive',
								'Content-Length' : '0',
								'Host' : 'www.instagram.com',
								'Origin' : 'https://www.instagram.com',
								'Referer' : 'https://www.instagram.com/',
								'User-Agent' : self.user_agent,
								'X-Instagram-AJAX' : '1',
								'X-Requested-With' : 'XMLHttpRequest'})
		r = self.s.get(self.url['home'])
		self.s.headers.update({'X-CSRFToken' : r.cookies['csrftoken']})
		time.sleep(5 * random.random())
		login = self.s.post(self.url['login'], data=self.login_post, allow_redirects=True)
		self.s.headers.update({'X-CSRFToken' : login.cookies['csrftoken']})
		self.csrftoken = login.cookies['csrftoken']
		time.sleep(5 * random.random())

		if login.status_code == 200:
			r = self.s.get('https://www.instagram.com/')
			finder = r.text.find(self.user_id)
			if finder != -1:
				self.login_status = True
				print 'INFO: Instamanager logged in with %s !' % (self.user_id)
			else:
				self.login_status = False
				print 'ERROR: Impossible to log in! ID error'
		else:
			print 'ERROR: Impossible to log in ! Connection error'

	def logout(self):
		print 'INFO: Instamanager session over: %i likes given ' %(self.like_count)

		try:
			logout_post = {'csrfmiddlewaretoken' : self.csrftoken}
			logout = self.s.post(self.url['logout'], data=logout_post)
			print 'INFO: Logout success'
			self.login_status = False
		except:
			print 'INFO: Logout error!'

	def get_media_by_tag (self, tag):
		if (self.login_status):
			print 'INFO: Instamanager is selecting pictures for the tag: %s' % (tag)
			if self.login_status == 1:
				url_tag = '%s%s%s' % (self.url['tags'], tag, '/')
				try:
					r = self.s.get(url_tag)
					text = r.text

					finder_text_start = ('<script type="text/javascript">'
										'window._sharedData = ')
					finder_text_start_len = len(finder_text_start)-1
					finder_text_end = ';</script>'

					all_data_start = text.find(finder_text_start)
					all_data_end = text.find(finder_text_end, all_data_start + 1)
					json_str = text[(all_data_start + finder_text_start_len + 1) \
									: all_data_end]
					all_data = json.loads(json_str)

					self.media_by_tag = list(all_data['entry_data']['TagPage'][0]\
						['tag']['media']['nodes'])

				except:
					self.media_by_tag = []
					print "INFO: Instamanager cannot find any media! Taking a minute rest"
					time.sleep(60)
			else:
				return 0

	def like_all_media (self, media_size=-1, delay=True):
		if (self.login_status):
			if self.media_by_tag != 0:
				i=0
				for d in self.media_by_tag:
					# Media count by this tag.
					if media_size > 0 or media_size < 0:
						media_size -= 1
						l_c = self.media_by_tag[i]['likes']['count']
						if ((l_c<=self.media_max_like and l_c>=self.media_min_like)or (self.media_max_like==0 and l_c>=self.media_min_like)or (self.media_min_like==0 and l_c<=self.media_max_like)or (self.media_min_like==0 and self.media_max_like==0)):
							print "INFO: liking the media %s" % (self.media_by_tag[i]['id'])
							like = self.like(self.media_by_tag[i]['id'])
							if like != 0:
								if like.status_code == 200:
									# That worked !
									self.error_400 = 0
									self.like_count += 1
								elif like.status_code == 400:
									print "ERROR: cannot like %i" % (like.status_code)
									# Some error. If repeated - can be ban!
									if self.error_400 >= self.error_400_max:
										print "INFO: It seems your account received a ban, Instamanager going to rest for %s s" %(self.ban_sleep_time)
										time.sleep(self.ban_sleep)
									else:
										self.error_400 += 1

								else:
									print "Not liked: %i" % (like.status_code)
									return False
									# Some error.
								i += 1
								if delay:
									time.sleep(self.like_delay*0.9 + self.like_delay*0.2*random.random())
								else:
									return True
							else:
								return False
						else:
							return False
					else:
						return False
			else:
				print "INFO: No media to like!"

	def like(self, media_id):
		""" Send http request to like media by ID """
		if (self.login_status):
			url_likes = self.url['likes'] % (media_id)
			if selfie_filter == 'on': #experimental, needs modification
				feature = get_pic_feature(url_likes)
				if classifier.predict(feature):
					like = 0
					print "INFO: Photo not liked because juged too personnal"
					return like
			try:
				like = self.s.post(url_likes)
				last_liked_media_id = media_id
			except:
				print "INFO: Except on like!"
				like = 0
			return like    

	def auto(self):
		""" Start loop, that get media ID by your tag list, and like it """
		if (self.login_status):
			while True:
				random.shuffle(self.tag_list)
				self.get_media_by_tag(random.choice(self.tag_list))
				self.like_all_media(random.randint \
					(1, self.likes_per_tag))






