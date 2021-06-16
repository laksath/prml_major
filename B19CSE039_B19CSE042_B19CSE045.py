# -*- coding: utf-8 -*-
"""B19CSE039_B19CSE042_B19CSE045.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C7uth1pTNb4xhoq69w6CntBhS1NHddDO
"""

import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import accuracy_score

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

batches = unpickle("batches.meta")
print(batches)

data_batch_1=unpickle("data_batch_1")
data_batch_2=unpickle("data_batch_2")
data_batch_3=unpickle("data_batch_3")
data_batch_4=unpickle("data_batch_4")
data_batch_5=unpickle("data_batch_5")
#test_batch=unpickle("test_batch")

print(data_batch_1)

len(data_batch_1[b'data'])

data_batch_1[b'data']

x_train=[]
for i in range(len(data_batch_1[b'data'])):
  x_train.append(data_batch_1[b'data'][i].reshape(3,32,32).transpose(1,2,0))
for i in range(len(data_batch_2[b'data'])):
  x_train.append(data_batch_2[b'data'][i].reshape(3,32,32).transpose(1,2,0))
for i in range(len(data_batch_3[b'data'])):
  x_train.append(data_batch_3[b'data'][i].reshape(3,32,32).transpose(1,2,0))
for i in range(len(data_batch_4[b'data'])):
  x_train.append(data_batch_4[b'data'][i].reshape(3,32,32).transpose(1,2,0))
for i in range(len(data_batch_5[b'data'])):
  x_train.append(data_batch_5[b'data'][i].reshape(3,32,32).transpose(1,2,0))

print(data_batch_1[b'filenames'])

print(batches[b'label_names'])

print(data_batch_1[b'labels'])

x_train = np.asarray(x_train)
print(x_train)

y_train = data_batch_1[b'labels']+data_batch_2[b'labels']+data_batch_3[b'labels']+data_batch_4[b'labels']+data_batch_5[b'labels']
print(y_train)
print(len(y_train))

import cv2

from matplotlib import pyplot
from keras.datasets import cifar10
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
print('Train: X=%s, y=%s' % (X_train.shape, y_train.shape))
print('Test: X=%s, y=%s' % (X_test.shape, y_test.shape))

print(y_train)
y_train

print(X_train)

fig = plt.figure(figsize=(10, 10))
for i in range(100):
  fig.add_subplot(10,10, i+1)
  plt.imshow(X_train[i])
  plt.axis('off')

sns.countplot(y_train.flatten())

data_images = X_train.reshape((len(X_train), -1))

data_images

import cv2
X_train_grey=[]
for i in range(len(X_train)):
  X_train_grey.append(cv2.cvtColor(X_train[i], cv2.COLOR_BGR2GRAY))

fig = plt.figure(figsize=(10, 10))
for i in range(100):
  fig.add_subplot(10,10, i+1)
  plt.imshow(X_train_grey[i],cmap='gray')
  plt.axis('off')

from skimage.feature import hog
from skimage.io import imread
from skimage.transform import rescale

fd,hog_img = hog(X_train_grey[1], pixels_per_cell=(8,8),cells_per_block=(2, 2),orientations=5,visualize=True)
fig = plt.figure(figsize=(25, 25))
fig.add_subplot(10,10,1)
plt.imshow(X_train_grey[1], cmap='gray')
fig.add_subplot(10,10,2)
plt.imshow(hog_img, cmap='gray')
plt.show()

hog_img.shape

from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler, Normalizer
import skimage
scalify = StandardScaler()

#CASE 1: 
X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(12,12),cells_per_block=(2, 2),orientations=5) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(12,12),cells_per_block=(2, 2),orientations=5) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)
accuracy_score(y_test, y_pred)

#CASE 2:
X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=1) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=1) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)
accuracy_score(y_test, y_pred)

# CASE 3:
X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(2, 2),orientations=5) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(2, 2),orientations=5) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)

y_test=y_test.flatten()

print(accuracy_score(y_test, y_pred))

#CASE 4:
X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(2, 2),orientations=9) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(2, 2),orientations=9) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)
accuracy_score(y_test, y_pred)

#CASE 5:
X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=9) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=9) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)
accuracy_score(y_test, y_pred)

#CASE 6:

X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=7) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=7) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)
accuracy_score(y_test, y_pred)

#CASE 7:

X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(1, 1),orientations=9) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(1, 1),orientations=9) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)
accuracy_score(y_test, y_pred)

#CASE 8:

X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(6,6),cells_per_block=(2, 2),orientations=5) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(6,6),cells_per_block=(2, 2),orientations=5) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

#CASE 9:

X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(6,6),cells_per_block=(2, 2),orientations=5) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(6,6),cells_per_block=(2, 2),orientations=5) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)

accuracy_score(y_test, y_pred)

#CASE 10:

X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(4,4),cells_per_block=(2, 2),orientations=5) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(4,4),cells_per_block=(2, 2),orientations=5) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)
accuracy_score(y_test, y_pred)

"""BEST:"""

#CASE 5:
X_train_grey = np.array([skimage.color.rgb2gray(img) for img in X_train])
X_train_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=9) for img in X_train_grey])
X_train_prepared = scalify.fit_transform(X_train_hog)
print(X_train_prepared.shape)
X_test_grey = np.array([skimage.color.rgb2gray(img) for img in X_test])
X_test_hog  = np.array([hog(img,pixels_per_cell=(8,8),cells_per_block=(4, 4),orientations=9) for img in X_test_grey])
X_test_prepared = scalify.transform(X_test_hog)

sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
sgd_clf.fit(X_train_prepared, y_train)

y_pred = sgd_clf.predict(X_test_prepared)
print(y_pred)

accuracy_score(y_test, y_pred)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred,average='macro')

from sklearn.metrics import recall_score
recall_score(y_test, y_pred,average='macro')

from sklearn.metrics import precision_score,confusion_matrix
precision_score(y_test, y_pred, average='micro')

from mlxtend.plotting import plot_confusion_matrix
fig, ax = plot_confusion_matrix(conf_mat=confusion_matrix(y_test, y_pred,),figsize=(12, 12),colorbar=True,show_absolute=False,show_normed=True)
plt.show()

#CNN





X_train_prepared[0]

import sys
from matplotlib import pyplot
from keras.datasets import cifar10
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.layers import Dropout
import tensorflow as tf
tf.config.run_functions_eagerly(True)

(X_train, Y_train), (X_test, Y_test) = cifar10.load_data()
trainY = to_categorical(Y_train)
testY = to_categorical(Y_test)

train_norm = X_train.astype('float32')
test_norm = X_test.astype('float32')
trainX = train_norm / 255.0
testX = test_norm / 255.0



model = Sequential()

model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=sgd)

history = model.fit(trainX, trainY, batch_size=32, epochs=10, verbose=2, validation_split=0.2)

# plot Cross Entropy Loss
pyplot.subplot(211)
pyplot.title('Cross Entropy Loss')
pyplot.plot(history.history['loss'], color='blue', label='train')
pyplot.plot(history.history['val_loss'], color='orange', label='test')
# plot accuracy
pyplot.subplot(212)
pyplot.title('Classification Accuracy')
pyplot.plot(history.history['accuracy'], color='blue', label='train')
pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
pyplot.show

_, acc = model.evaluate(testX, testY, verbose=0)
print('> %.3f' % (acc * 100.0))

model = Sequential()

model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# Dropout layer added here
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
# Dropout layer added here
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=sgd)

history = model.fit(trainX, trainY, batch_size=32, epochs=10, verbose=2, validation_split=0.2)
# plot Cross Entropy Loss
pyplot.subplot(211)
pyplot.title('Cross Entropy Loss')
pyplot.plot(history.history['loss'], color='blue', label='train')
pyplot.plot(history.history['val_loss'], color='orange', label='test')
# plot accuracy
pyplot.subplot(212)
pyplot.title('Classification Accuracy')
pyplot.plot(history.history['accuracy'], color='blue', label='train')
pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
pyplot.show
_, acc = model.evaluate(testX, testY, verbose=0)
print('> %.3f' % (acc * 100.0))

from keras.layers.normalization import BatchNormalization
from keras.layers import Activation
model = Sequential()

model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=sgd)

history = model.fit(trainX, trainY, batch_size=32, epochs=10, verbose=2, validation_split=0.2)
# plot Cross Entropy Loss
pyplot.subplot(211)
pyplot.title('Cross Entropy Loss')
pyplot.plot(history.history['loss'], color='blue', label='train')
pyplot.plot(history.history['val_loss'], color='orange', label='test')
# plot accuracy
pyplot.subplot(212)
pyplot.title('Classification Accuracy')
pyplot.plot(history.history['accuracy'], color='blue', label='train')
pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
pyplot.show
_, acc = model.evaluate(testX, testY, verbose=0)
print('> %.3f' % (acc * 100.0))

#MLP



from sklearn.neural_network import MLPClassifier

y_train = to_categorical(y_train, num_classes=10)
y_test = to_categorical(y_test, num_classes=10)


X_train = np.reshape(X_train,(50000,3072))
X_test = np.reshape(X_test,(10000,3072))
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')



X_train /= 255
X_test /= 255

model = Sequential()
model.add(Dense(256, activation='relu', input_dim=3072))
model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(optimizer=sgd,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train,y_train, epochs=20, batch_size=32, verbose=2, validation_split=0.2)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

score = model.evaluate(X_test, y_test, batch_size=128, verbose=0)
score

