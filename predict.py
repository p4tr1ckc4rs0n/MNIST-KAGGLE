#!/usr/bin/env python

import caffe
import os
import argparse
import numpy as np
from natsort import natsorted
import csv


def predict_images(images, model_definition, model_path):
    test_images = images
    caffe.set_mode_cpu()
    net = caffe.Classifier(model_path, model_defintion, image_dims=(28, 28))

    with open('results.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('ImageId', 'Label'))

        for image_id, image in enumerate(natsorted(os.listdir(test_images))):
            image_name = '/tmp/MNIST/validate_images/' + image
            image_ = caffe.io.load_image(image_name, False)
            prediction = np.argmax(net.predict([image_], oversample=False))
            writer.writerow((str(image_id + 1), str(prediction)))


def main():
    parser = argparse.ArgumentParser(description='CNN predictions on test digits')
    parser.add_argument('-i', '--images', help='path to images directory')
    parser.add_argument('-p', '--model_path', help='path to cnn model definition')
    parser.add_argument('-m', '--model', help='path to trained model')
    args = parser.parse_args()

    print "###"
    print "Feeding test images to CNN for classification"

    predict_images(args.test_digits, args.model_definiton, args.model_path)

    print "CNN test scores saved to './results.csv'"
    print "###"

if __name__ == "__main__":
    main()