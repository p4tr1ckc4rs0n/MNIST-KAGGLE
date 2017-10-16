#!/usr/bin/python

from sklearn.cross_validation import train_test_split
import os
import shutil
import argparse


def setup(image_dir, train_name, test_name):
    # create directories for train and test data
    os.chdir(image_dir)
    os.makedirs(train_name)
    os.makedirs(test_name)

    # training images
    images = [image for image in os.listdir(image_dir)]

    # train test split (80/20)
    train_images, test_images = train_test_split(images, test_size=0.2)

    return train_images, test_images


def archive_data(images_dir, directory_name, imagelist):
    # move files to appropriate directories
    for image_file in imagelist:
        shutil.move(images_dir + "/" + image_file, images_dir + "/" + directory_name)


def gen_labels(images_dir, labels_dir):
    # write to list files
    with open(labels_dir + "/" + "test.txt", 'wb') as writer:
        for filename in os.listdir(images_dir + "/" + "train"):
            label = filename.split(".")[0][-1]
            writer.writerow("/" + filename + " " + str(label) + "\n")

    with open(labels_dir + "/" + "train.txt", 'wb') as writer:
        for filename in os.listdir(images_dir + "/" + "test"):
            label = filename.split(".")[0][-1]
            writer.writerow("/" + filename + " " + str(label) + "\n")


def main():
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('-i', '--input', dest='images_dir', help='training images directory')
    parser.add_argument('-l', '--label_directory', dest='labels_dir', help='directory for labels list files')
    args = parser.parse_args()

    train_images, test_images = setup(args.images_dir, "train", "test")

    archive_data(args.imagesDir, "train", train_images)
    archive_data(args.imagesDir, "test", test_images)

    gen_labels(args.images_dir, args.labels_dir)

    print "###"
    print "Train test split and list generation completed"
    print "###"


if __name__ == "__main__":
    main()
