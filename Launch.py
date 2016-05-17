''' This is the file to run the program, you can configure the parameters here'''

import Instamanager

parameters = {
	'ID' : 're.mi.to',
	'password' : 'Remi2adeza!im',
	'like_speed' : '1000',
	'likes_per_tag' : '5',
	'tags' : ['bike', 'caferacer'],
	'selfie_filter' : 'off'
}

manager = InstaManager(**parameters)

manager.auto()
