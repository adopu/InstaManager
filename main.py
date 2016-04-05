import json

from time import sleep
from instagram.client import InstagramAPI

class InstaManager:

    def __init__(self, config_file, tags_file):
        # Loading the configuration file, it has the access_token, user_id and others configs
        self.config = json.load(config.json)

        self.api = InstagramAPI (access_token= self.config["access_token"],
			client_ips= self.config["my_ip"],
			client_secret= self.config["client_secret"])
     


    def run(self):
     	while True:
     	    recent_media, url= self.api.tag_recent_media(tag_name="iphonephotography", count =2)
            for media in recent_media:
	            id_ = media.id
	            users = [user.username for user in media.likes]
	            if "re.mi.to" in users:
		            print ("IN PHOTO")
	            else:
	            	print("LIKING PICTURE")
		            api.like_media(media_id=id_)

	        sleep(self.config["sleep_timer"])

if __name__ == '__main__':
    bot = Bot(open("config_bot.json", "r"), open("tags.json", "r"))
    bot.run(