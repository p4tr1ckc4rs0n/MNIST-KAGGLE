#!/usr/bin/env python

import os
import numpy as np
import Image
import argparse
import csv
import uuid
import shutil

parser = argparse.ArgumentParser(description='extract digits from csv file')

parser.add_argument('-f','--csv_file',dest='csv_file', help='MNIST csv file')

parser.add_argument('-m','--train_or_test',dest='dataDir', help='name of directory to store extracted MNIST images')

args = parser.parse_args()

def extract_digits(csv_file,data_dir):

	print "###"
	print "Extracting and saving digits from "+str(csv_file.split("/")[-1])

	dataset_tag = str(csv_file)

	# open csv file
	with open(csv_file,'rb') as csvfile:

		# read contents of file
		contents = csv.reader(csvfile)
		# skip header
		next(contents)
		# extract and save test images
		count = 0
		if "validate" in data_dir:
			for row in contents:
				digit = np.array(row).reshape((28,28)).astype(np.uint8)
				digit_out = Image.fromarray(digit)
				digit_out.save(str(count)+'.png')
				count += 1
		else:
			# extract and save training images
			for row in contents:
				unique_filename = uuid.uuid4()
				pixels = row[1:]
				digit = np.array(pixels).reshape((28,28)).astype(np.uint8)
				digit_out = Image.fromarray(digit)
				digit_out.save(str(unique_filename)+str(row[0])+'.png')

		print "Done."

		# close file
		csvfile.close()

def main():
	# input csv file
	csv_file = args.csv_file
	# extract images from csv file and save
	extract_digits(csv_file,args.dataDir)

if __name__ == "__main__":
	main()


