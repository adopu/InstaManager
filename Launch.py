''' This is the file to run the program, you can configure the parameters here'''

import Instamanager

parameters = {
	'ID' : 'YOUR@ID',
	'password' : 'YOUR_PWD',
	'like_speed' : '1000',
	'likes_per_tag' : '5',
	'tags' : ['bike', 'caferacer'],
	'selfie_filter' : 'off'
}

manager = InstaManager(**parameters)

manager.auto()
