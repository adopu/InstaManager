from __future__ import division
from PIL import Image
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm
from sklearn import grid_search


def get_pic_feature(picture):
	if not picture.mode == 'RGB':
		return None
	feature = [0] * 4 * 4 * 4
	pixel_count = 0
	for pixel in picture.getdata():
		red_idx = int(pixel[0]/(256/4))
		green_idx = int(pixel[1]/(256/4))
		blue_idx = int(pixel[2]/(256/4))
		idx = red_idx + green_idx * 4 + blue_idx * 4 * 4
		feature[idx] += 1
		pixel_count += 1
		feature_vect=[x/pixel_count for x in feature]
	return feature_vect


def get_dir_features(dir_path):
	dir_features = []
	for pic in os.listdir(dir_path):
		if os.path.isfile(os.path.join(dir_path,pic)) and 'selfie' in pic:
			picture = Image.open(os.path.join(dir_path,pic))
			pic_feature = get_pic_feature(picture)
			if pic_feature:
				dir_features.append(pic_feature)
	return dir_features


def create_classifier(training_data):
	classifier = svm.OneClassSVM()
	classifier.fit(training_data)
	return classifier


if __name__=='__main__':
	dir_path = '/home/remi/Pictures'
	selfies = get_dir_features(dir_path)
	classifier = create_classifier(selfies)
	while True:
		print 'Input the path to picture'
		pic_path = raw_input('-->')
		picture = Image.open(pic_path)
		feature = get_pic_feature(picture)
		print(classifier.predict(feature))
