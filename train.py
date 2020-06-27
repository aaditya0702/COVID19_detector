# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15D-Dt40bzKc4NY21pJdVkHsGGdBycO_x

Instructions:
1. Clone the repository. 
2. Run the cells for data preprocessing.
2. For all pre-trained models, run the code cell corresponding to the one you wish to train.
3. Create a data augmentation object.
4. Compile the model.
5. Train the network.
6. Evaluate the model's metrics.
7. For the basic CNN, all code required to train is within the block (except for the data augmentation object.)
"""

#Clone a private Github repository.

import os
from getpass import getpass
import urllib

user = input('User name: ')
password = getpass('Password: ')
password = urllib.parse.quote(password) 
repo_name = input('Repo name: ')

cmd_string = 'git clone https://{0}:{1}@github.com/{0}/{2}.git'.format(user, password, repo_name)

os.system(cmd_string)
cmd_string, password = "", ""

#Import the necessary libraries.
import tensorflow as tf
from tensorflow import keras 
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from sklearn.metrics import confusion_matrix
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import ResNet101
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import VGG19
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

"""**Data Preprocessing**"""

#Define the categories of x-rays. 
class_names = ['covid', 'normal', 'pneumonia']

#Path of the directories where the pictures are stored.
covidDir = "/content/coronavirus_detector/dataset/covid"
pneumoniaDir = "/content/coronavirus_detector/dataset/pneumonia"
normalDir = "/content/coronavirus_detector/dataset/normal"

#Function to load and resize the pictures and return them along with labels.
def load_images_from_folder(folder):
  images = []
  labels = []
  for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder, filename))                
    img = cv2.resize(img, (144, 144))                                 #Resize to 144 x 144
    images.append(img)
    label = (os.path.join(folder, filename)).split(os.path.sep)[-2]
    if label=='covid':
      labels.append(1)                                                #Covid-19 positive x-rays labelled 1
    else:
      labels.append(0)                                                #Healthy and non-Covid pneumonia x-rays labelled 0
  return images, labels

#Load the images from the respective directories.

images_covid, labels_covid = load_images_from_folder(covidDir)
images_normal, labels_normal = load_images_from_folder(normalDir)
images_pneu, labels_pneu = load_images_from_folder(pneumoniaDir)


#Display the number of x-rays from each category.

print(len(labels_covid))
print(len(labels_normal))
print(len(labels_pneu))

#Create the test dataset with 100 x-rays from each category to ensure balance.

test_images = images_covid[:100]
test_labels = labels_covid[:100]
test_images.extend(images_normal[:100])
test_labels.extend(labels_normal[:100])
test_images.extend(images_pneu[:100])
test_labels.extend(labels_pneu[:100])

#Create the validation dataset in the same manner as test dataset.

valid_images = images_covid[-100:]
valid_labels = labels_covid[-100:]
valid_images.extend(images_normal[-100:])
valid_labels.extend(labels_normal[-100:])
valid_images.extend(images_pneu[-100:])
valid_labels.extend(labels_pneu[-100:])

#Create the training dataset with the remaining x-rays.

train_images = images_covid[100:-100]
train_labels = labels_covid[100:-100]
train_images.extend(images_normal[100:-100])
train_labels.extend(labels_normal[100:-100])
train_images.extend(images_pneu[100:-100])
train_labels.extend(labels_pneu[100:-100])

#Convert the datasets to numpy arrays.
X_test = np.array(test_images)
y_test = np.array(test_labels)

X_train = np.array(train_images)
y_train = np.array(train_labels)

X_valid = np.array(valid_images)
y_valid = np.array(valid_labels)


#Normalize the images.
X_test = X_test / 255.0
X_train = X_train / 255.0
X_valid = X_valid / 255.0

#Display the number of Covid-19 positive x-rays in each dataset.

print(np.count_nonzero(y_train == 1))
print(len(y_train))
print(np.count_nonzero(y_test == 1))
print(len(y_test))
print(np.count_nonzero(y_valid == 1))
print(len(y_valid))

"""**Model Definitions and Training**"""

#Define a basic CNN model.

def getModel(optimizer):
  model = Sequential()
  model.add(Convolution2D(32, (3, 3), activation = 'relu', kernel_initializer = 'he_uniform', padding = 'same', input_shape = (144, 144, 3)))
  model.add(MaxPooling2D((2, 2)))
  model.add(Flatten())
  model.add(Dense(128, activation = 'relu', kernel_initializer = 'he_uniform'))
  model.add(Dense(1, activation = 'sigmoid'))
  return model

#Define the optimizer.
opt = keras.optimizers.SGD(lr = 0.001, momentum = 0.9)
model = getModel(opt)

#Compile the model
model.compile(optimizer = opt, loss = 'binary_crossentropy', metrics = ['accuracy'])

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

#Train the model along with cross-validation.
model.fit(
trainAug.flow(X_train, y_train, batch_size=BS),
steps_per_epoch=len(X_train) // BS,
validation_data=(X_valid, y_valid),
validation_steps=len(X_valid) // BS,
epochs=EPOCHS)

#Use ResNet-50 with ImageNet weights.

baseModel = ResNet50(weights = "imagenet", include_top = False, input_tensor = Input(shape = (144, 144, 3)))
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
headModel = Flatten()(headModel)
headModel = Dense(64, activation = 'relu')(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(1, activation = 'sigmoid')(headModel)
for layer in baseModel.layers:
  layer.trainable = False
model = Model(inputs = baseModel.input, outputs = headModel)

#Use VGG-16.

baseModel = VGG16(weights = "imagenet", include_top = False, input_tensor = Input(shape = (144, 144, 3)))
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
headModel = Flatten()(headModel)
headModel = Dense(64, activation = 'relu')(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(1, activation = 'sigmoid')(headModel)
for layer in baseModel.layers:
  layer.trainable = False
model = Model(inputs = baseModel.input, outputs = headModel)

#Use ResNet-101.

baseModel = ResNet101(weights = "imagenet", include_top = False, input_tensor = Input(shape = (144, 144, 3)))
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
headModel = Flatten()(headModel)
headModel = Dense(64, activation = 'relu')(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(1, activation = 'sigmoid')(headModel)
for layer in baseModel.layers:
  layer.trainable = False
model = Model(inputs = baseModel.input, outputs = headModel)

#Use VGG-19.

baseModel = VGG19(weights = "imagenet", include_top = False, input_tensor = Input(shape = (144, 144, 3)))
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
headModel = Flatten()(headModel)
headModel = Dense(64, activation = 'relu')(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(1, activation = 'sigmoid')(headModel)
for layer in baseModel.layers:
  layer.trainable = False
model = Model(inputs = baseModel.input, outputs = headModel)

#Define parameters.

INIT_LR = 1e-3
EPOCHS = 25
BS = 8

#Create a data augmentation object.

trainAug = ImageDataGenerator(
	rotation_range=15,
	fill_mode="nearest")

#Compile the chosen model.
opt = tf.keras.optimizers.Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

#Train the model.

print("Training model.")
model.fit(
trainAug.flow(X_train, y_train, batch_size=BS),
steps_per_epoch=len(X_train) // BS,
validation_data=(X_valid, y_valid),
validation_steps=len(X_valid) // BS,
epochs=EPOCHS)

"""**Evaluation Metrics**"""

#Evaluate the model on the Test dataset.

model.evaluate(X_test, y_test, verbose = 2)

#Evaluate other metrics of the model.

y_pred = model.predict(X_test)
y_pred = y_pred[:,0]                        #Creating a single array of predictions

for i in range(len(y_pred)):
  if(y_pred[i] > 0.5):                      #Threshold value of 0.5
    y_pred[i] = 1
  else:
    y_pred[i] = 0

#print(y_pred)                              #Uncomment line to print predictions 
print("Accuracy Score - ", accuracy_score(y_test, y_pred)) 
print("Precision Score - ", precision_score(y_test, y_pred))
print("Recall Score - ", recall_score(y_test, y_pred))         #F1 Score
print("F1 Score - ",f1_score(y_test, y_pred))                 
print("Cohen Kappa Score - ",cohen_kappa_score(y_test, y_pred))
print("ROC AUC Score - ",roc_auc_score(y_test, y_pred))
print("Confusion Matrix - ",confusion_matrix(y_test, y_pred))     #Confusion Matrix

"""1. Basic Model:

  Accuracy: 90.33%

  F1 Score: 0.83

2. ResNet50:

  Accuracy: 81.67%

  F1 Score: 0.62

3. VGG16:
  
  Accuracy: 97.33%
  
  F1 Score: 0.96

4. ResNet101:
  
  Accuracy: 90%
  
  F1 Score: 0.83

5. VGG19:
  
  Accuracy: 94.67%
  
  F1 Score: 0.91
"""