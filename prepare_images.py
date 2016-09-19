#!/usr/bin/python

from sklearn.cross_validation import train_test_split
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Process some inputs.')

parser.add_argument('-i','--input', dest='imagesDir',help='training images directory')

parser.add_argument('-l','--label_directory',dest='labelsDir',help='directory for labels list files')

args = parser.parse_args()

# switch to correct directory
imagesDir = str(args.imagesDir)
os.chdir(imagesDir)

# list containing all training images
imagelist = [ image for image in os.listdir(imagesDir)]

# split radargram images into lists for entry into train/test directories (75/25% train/test split)
train, test = train_test_split(imagelist, test_size=0.25)

# create directories for train and test data
os.chdir(imagesDir)
os.makedirs("train")
os.makedirs("test")

def archive_data(directory_name,imagelist):

	# move files to appropriate directories
    for image_file in imagelist:
        shutil.move(imagesDir+"/"+image_file, imagesDir+"/"+directory_name)

def gen_labels(imagesDir,labelsDir):

	# create list files
	ftest = open(labelsDir+"/"+"test.txt","w+")
	ftrain = open(labelsDir+"/"+"train.txt","w+")

    # write to list files
	for filename in os.listdir(imagesDir+"/"+"train"):
		label = filename.split(".")[0][-1]
		ftrain.write("/"+filename+" "+str(label)+"\n")

	for filename in os.listdir(imagesDir+"/"+"test"):
		label = filename.split(".")[0][-1]
		ftest.write("/"+filename+" "+str(label)+"\n")

	# close files
	ftest.close()
	ftrain.close()

def main():
    archive_data("train",train)
    archive_data("test",test)
    gen_labels(args.imagesDir,args.labelsDir)

    print "###"
    print "Train test split and list generation completed"
    print "###"

if __name__ == "__main__":
    main()

