'''
We used Kaggle's Chest X-ray images (Pneumonia) dataset to get a set of healthy X-rays. 
Link to dataset: https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia

This code obtains X-ray images of a healthy person. The images are copied to the location specified as a command-line argument. 
+ The code creates a list of all healthy x-rays and chooses a random subset of required size (again specified as an argument.) 
+ The image files are copied from the NORMAL folder to the outputpath. 

Usage: python kaggle_xrays.py --normalpath chest_xray --outputpath dataset/normal

'''

# Import necessary libraries
from imutils import paths
import random
import os
import argparse
import shutil


# Parsing CLI arguments 
argp = argparse.ArgumentParser()
argp.add_argument("-n","--normalpath", required=True, help="Path to retrieve healthy xray images")
argp.add_argument("-o","--outputpath",required=True, help="Path to store healthy images in dataset")
argp.add_argument("-s","--samplesize",default=50, type=int, help="number of samples to retrieve")
args = vars(argp.parse_args())


# Obtain the image paths of all normal x-rays from Kaggle dataset
basePath = os.path.sep.join([args["normalpath"],"train","NORMAL"])
imagePaths = list(paths.list_images(basePath))

# Shuffling dataset and picking a random subset of preferred size
random.seed(42)
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["samplesize"]]

# Iterating through selected image paths
for (i, imagePath) in enumerate(imagePaths):
    filename = imagePath.split(os.path.sep)[-1]
    outputImg = os.path.sep.join([args["outputpath"],filename])       #constructing output file path

    shutil.copy2(imagePath, outputImg)                              #copying the image to output directory
