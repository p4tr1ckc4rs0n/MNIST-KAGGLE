#!/usr/bin/env python

import caffe
import os
import argparse
import numpy as np
from natsort import natsorted
import csv
import shutil

parser = argparse.ArgumentParser(description='CNN predictions on test digits')

parser.add_argument('-i','--input_digits', dest='test_digits',help='directory for test digits')

args = parser.parse_args()

test_images = args.test_digits
model_path = './lenet.prototxt'
pre_trained = '/tmp/MNIST/snapshot/_iter_500.caffemodel'

caffe.set_mode_cpu()
net = caffe.Classifier(model_path,pre_trained,image_dims=(28,28))

print "###"
print "Feeding test images to CNN for classification"

with open('results.csv', 'wb') as csvfile:

	writer = csv.writer(csvfile)
	writer.writerow(('ImageId','Label'))

	for image_id,image in enumerate(natsorted(os.listdir(test_images))):

		image_name = '/tmp/MNIST/validate_images/'+image

		image_ = caffe.io.load_image(image_name,False)

		prediction = np.argmax(net.predict([image_],oversample=False))

		writer.writerow((str(image_id+1),str(prediction)))

print "CNN test scores saved to 'results.csv' file"
print "###"








