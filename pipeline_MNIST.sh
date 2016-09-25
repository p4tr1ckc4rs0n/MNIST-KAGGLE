#!/bin/bash 

# path names
export HOME=$(pwd)
export CAFFE=$(pwd)/deep-learning/caffe
export CAFFE_MODEL=$(pwd)/cnn_model
export CAFFE_TOOLS=/home/pwhc/skycap/deep-learning/caffe/build/tools

# remove last run
rm -rf /tmp/MNIST/*
rmdir /tmp/MNIST*

echo "###"
echo "Starting..."
date
echo "###"

# define locations of temp directories
export ROOT_DIR=/tmp/MNIST
export IMAGES_DIR=$ROOT_DIR/images
export VALIDATE_DIR=$ROOT_DIR/validate_images
export LABELS_DIR=$ROOT_DIR/labels
export SNAPSHOT_DIR=$ROOT_DIR/snapshot

#########################################################################################
# Stage 1: Create directory structure to hold data from each stage in the pipeline
#########################################################################################

# create temporary directories
if [ ! -d "$ROOT_DIR" ]; then
	echo "Creating root directory: $ROOT_DIR"
	mkdir $ROOT_DIR
	# Create inner directories for MNIST classification
    if [ ! -d "$IMAGES_DIR" ]; then
        echo "Creating directory: $IMAGES_DIR"
        mkdir $IMAGES_DIR
    else
        echo "$IMAGES_DIR already exists! Exiting..."
        exit
    fi
    if [ ! -d "$VALIDATE_DIR" ]; then
        echo "Creating directory: $VALIDATE_DIR"
        mkdir $VALIDATE_DIR
    else
        echo "$VALIDATE_DIR already exists! Exiting..."
        exit
    fi
    if [ ! -d "$LABELS_DIR" ]; then
        echo "Creating directory: $LABELS_DIR"
        mkdir $LABELS_DIR
    else
        echo "$LABELS_DIR already exists! Exiting..."
        exit
    fi
    if [ ! -d "$SNAPSHOT_DIR" ]; then
        echo "Creating directory: $SNAPSHOT_DIR"
        mkdir $SNAPSHOT_DIR
    else
        echo "$SNAPSHOT_DIR already exists! Exiting..."
        exit
    fi
fi

#########################################################################################
# Stage 2: Extract digits from csv file 
#########################################################################################

# extract mnist images for trianing
cd $IMAGES_DIR
python $HOME/extract_digits.py -f $HOME/data/train.csv -m /home/pwhc/kaggle/MNIST-KAGGLE/images

# extract mnist images for testing
cd $VALIDATE_DIR
python $HOME/extract_digits.py -f $HOME/data/test.csv -m /home/pwhc/kaggle/MNIST-KAGGLE/validate_images

#########################################################################################
# Stage 3: Split training images into train and test datasets
#########################################################################################

python $HOME/prepare_images.py -i $IMAGES_DIR -l $LABELS_DIR

#########################################################################################
# Stage 4: Convert images to lmdb for caffe
#########################################################################################

echo "Creating caffe database (lmdb)"
echo "###"

$HOME/create_lmdb.sh $CAFFE_TOOLS

#########################################################################################
# Stage 5: Train and test lenet CNN
#########################################################################################

$HOME/train_lenet.sh

#########################################################################################
# Stage 6: Validate lenet CNN: save scores in csv file for kaggle submission
#########################################################################################

cd $HOME 

python ./predict.py -i /tmp/MNIST/validate_images/
