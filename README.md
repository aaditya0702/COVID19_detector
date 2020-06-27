# coronavirus_detector

The aim is to create a deep learning model using Keras and Tensorflow to predict whether a person is infected by the Coronavirus. Since large scale testing of coronavirus is very difficult and an x-ray machine is present in most places around the world, this might be an effective way to detect the virus. 

The proposed model is developed to provide accurate diagnostics for binary classification (COVID vs Healthy) and multi-class classification (COVID vs Healthy and Pneumonia). The VGG16 model provided an accuracy of *98.5%* and *97.33%* respectively. 

We spent a lot of time reading different scientific papers and blogs to understand how to create models for medical data such as x-rays. 

Our dataset consisted of 447 Covid19 infected x-rays, 1211 pneumonia infected x rays and 1348 healthy xrays. 
First, we trained the CNNs on a dataset consisting of only covid and healthy x rays. We tried several models like VGG16, VGG19, Resnet50, Resnet101 and a basic CNN model of our own. 


    Basic Model: Accuracy: 93.5% F1 Score: 0.93

    ResNet50: Accuracy: 86% F1 Score: 0.84

    VGG16: Accuracy: 98.5% F1 Score: 0.985

    ResNet101: Accuracy: 90.5% F1 Score: 0.895

    VGG19: Accuracy: 97.5% F1 Score: 0.974

Next, we grouped the pneumonia and normal pictures to simulate realistic situations. 


    Basic Model:   Accuracy: 90.33%
                   F1 Score: 0.83
    ResNet50:      Accuracy: 81.67%
                   F1 Score: 0.62
    VGG16:         Accuracy: 97.33%
                   F1 Score: 0.96
    ResNet101:     Accuracy: 90%
                   F1 Score: 0.83
    VGG19:         Accuracy: 94.67%
                   F1 Score: 0.91
                   
Initially, our model was giving generalizing most of the xrays to give a negative result due to the less number of COVID xrays. Therefore, we changed the distribution of our validation and test set to have a larger proportion of covid infected xrays. We used F1 score as our metric as it accounts for the generalizing. 

Clearly, the VGG16 convolutional neural network has the best results. 

The VGG-16 produced the following activations for COVID X-rays:
![alt text](https://github.com/aaditya0702/coronavirus_detector/blob/master/sample/COVID1.png?raw=true)
![alt text](https://github.com/aaditya0702/coronavirus_detector/blob/master/sample/COVID2.png?raw=true)
![alt text](https://github.com/aaditya0702/coronavirus_detector/blob/master/sample/COVID3.png?raw=true)

It produced the following activations for pneumonia X-rays: 
![alt text](https://github.com/aaditya0702/coronavirus_detector/blob/master/sample/PNEUMONIA1.png?raw=true)

It produced the following activations for normal X-rays:
![alt text](https://github.com/aaditya0702/coronavirus_detector/blob/master/sample/NORMAL1.png?raw=true)
![alt text](https://github.com/aaditya0702/coronavirus_detector/blob/master/sample/NORMAL2.png?raw=true)

This entire project is done based on a tutorial posted by Adrian RoseBrock on his blog. 
Link: https://www.pyimagesearch.com/2020/03/16/detecting-covid-19-in-x-ray-images-with-keras-tensorflow-and-deep-learning/

The aim of the project is to enable automatic detection of Coronavirus based on the X-ray of the lungs, which is more easily available than the current testing methods. 

## How can COVID-19 be detected in X-ray images?
Since COVID-19 attacks the epithelial cells that line the respiratory tract, we can use X-rays to analyze the health of patient's lungs. Since X-ray analysis takes time, developing an automated analysis is required to save time. 

## Source of COVID-19 X-rays
The COVID-19 X-ray image dataset is curated by Dr. Joseph Cohen from the University of Montreal. 
Link: https://github.com/ieee8023/covid-chestxray-dataset
## Source of healthy X-rays
We used Kaggle's Chest X-ray images (Pneumonia) dataset to get a set of healthy X-rays. 
Link: https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia

### Authors
Manas Minnoor 
Aaditya Singh

