'''
We use the covid-chestxray-dataset repository uploaded by Dr. Joseph Cohen from University of Montreal. 
Link to repository : https://github.com/ieee8023/covid-chestxray-dataset

This code finds all the X-ray images of a person infected by a virus and for a certain view (specified at the start of the code). The images are copied to the outputDir also specified at the start. 
+ The code iterates through the metadata.csv file and retrieves the image file names. 
+ The image files are copied from the images folder to the outputDir folder. 
'''
#import required libraries
import pandas as pd
import shutil 
import os

#selecting the disease
virus = "COVID-19"
#selecting the X-ray view required
X_ray_view = "PA"

metadata_csv = "./covid-chestxray-dataset/metadata.csv"     # Meta info
imageDir = "./covid-chestxray-dataset/images"               # Directory of images
outputDir = "./dataset/covid"       # Output directory to store selected images

if not os.path.exists(outputDir):   #check if directory exists and create one if not
    os.makedirs(outputDir)

#converting csv file to readable format
metadata = pd.read_csv(metadata_csv)

#iterating through rows of metadata dataframe
for index, row in metadata.iterrows():
    if row['finding'] == virus and row['view'] == X_ray_view:
        fileName = row['filename'].split(os.path.sep)[-1]   #get only the filename if the filename contains full path
        filePath = os.path.sep.join([imageDir,fileName])    #get the full path to the file present in the images directory 
        shutil.copy2(filePath, outputDir)                   #copy file to outputDir