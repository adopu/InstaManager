from time import sleep
from instagram.client import InstagramAPI

access_token = "(u'2678886743.a62ec61.63ee3298b59145b8b667bae42e22d561', {u'username': u're.mi.to', u'bio': u'Smartphone photography devotee & aspiring data scientist.', u'website': u'', u'profile_picture': u'https://scontent.cdninstagram.com/t51.2885-19/s150x150/12677708_973837385996671_1966088584_a.jpg', u'full_name': u'R\xe9mi Canard', u'id': u'2678886743'})"
api = InstagramAPI (access_token=access_token,
					client_ips="10.0.0.17",
					client_secret="6b27e40e8c4a44a882ec2de50660b2af")
recent_media, url= api.tag_recent_media(tag_name="iphonephotography", count =2)

for media in recent_media:
	id_ = media.id
	users = [user.username for user in media.likes]
	if "re.mi.to" in users:
		print ("IN PHOTO")
	else:
		print("LIKING PICTURE")
		api.like_media(media_id=id_)

	sleep(2)

	