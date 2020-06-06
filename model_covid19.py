#import the necessary libraries
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from tensorflow import keras 
from cv2 import imread
from cv2 import resize
from os import listdir
from os import path
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import SGD
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

#name of directories where pictures are stored 
infectedDir = "./dataset/covid"
normalDir = "./dataset/normal"

#function to resize the pictures and return them along with labels
def load_images_from_folder(folder):
  images = []
  labels = []
  for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder, filename))
    img = cv2.resize(img, (224, 224))
    images.append(img)

    label = (os.path.join(folder, filename)).split(os.path.sep)[-2]
    if label=='covid':
      labels.append(1)
    else:
      labels.append(0)
  return images, labels


#load the images from the respective directories
images_covid, labels_covid = load_images_from_folder(infectedDir)
images_normal, labels_normal = load_images_from_folder(normalDir)

#join the pictures and labels
images_covid.extend(images_normal)
data_images = images_covid
labels_covid.extend(labels_normal)
data_labels = labels_covid

#convert to numpy array for easy manipulation
X = np.array(data_images)
y = np.array(data_labels)

#normalize the data
X = X / 255.0

#separates data into 70% train and 30% test set after shuffling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, shuffle = True, random_state = 42)

#define our model with the specific optimizer
def getModel(optimizer):
  model = Sequential()
  model.add(Convolution2D(32, (3, 3), activation = 'relu', kernel_initializer = 'he_uniform', padding = 'same', input_shape = (224, 224, 3)))
  model.add(MaxPooling2D((2, 2)))
  model.add(Flatten())
  model.add(Dense(128, activation = 'relu', kernel_initializer = 'he_uniform'))
  model.add(Dense(1, activation = 'sigmoid'))
  return model

#define the optimizer
opt = optimizers.SGD(lr = 0.001, momentum = 0.9)
model = getModel(opt)

#compile the model
model.compile(optimizer = opt, loss = 'binary_crossentropy', metrics = ['accuracy'])

#train the model on the entire set while checking with cross validation
model.fit(X, y, validation_split=0.3, epochs=150, batch_size=10)

#test the model 
model.evaluate(X_test, y_test, verbose = 2)