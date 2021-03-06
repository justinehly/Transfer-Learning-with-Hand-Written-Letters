# -*- coding: utf-8 -*-
"""HW4_Ehly.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zr0kts3CP_i9jTjCOPY3KCyz60f3QFW7

# MSDS 7335 Machine Learning II - Wednesday 630p-745p
### HW4 - MNIST and Transfer Learning
#### Justin Ehly
"""

import numpy as np
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential, Model

"""## Import the Dataset

Import the dataset and look at some examples.

The MNIST dataset consists of handwritten digits (0-9).
Pixel values are from 0 to 255.
"""

# import dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

type(x_test)

print(x_train.shape, y_train.shape)

# Look at some random numbers
X_shuffle = shuffle(x_train.copy(), random_state=42)

print('Look at some numbers')
plt.figure(figsize=(12,10))
row, columns = 4, 4
for i in range(16):
  plt.subplot(columns, row, i+1)
  plt.imshow(X_shuffle[i].reshape(28,28), interpolation='nearest', cmap='Greys')

plt.show()

"""## Data Preprocessing

We need to do the following to preprocess the data:

1. Divide the values by the max value (255)
2. Add a color channel (require by the convolutional layer)

By default Keras assumes images are formatted as (number of examples, x-dim, y-dim, number of colors)

An RGB image has 3 color channels, greyscale as 1 color channel

"""

x_train.max()

# divide the color channel
x_train = x_train / 255
x_test = x_test / 255

# add the color channel
x_train = x_train.reshape(x_train.shape + (1,))
x_test = x_test.reshape(x_test.shape + (1,))

print(x_train.shape, x_test.shape)

"""## Setup the Model
This is a very basic convolutional network. There are essentially two sections

1. convolutional feature extraction layers
2. dense (fully-connected) classifier layers
"""

classes = 10
filters = 32
kernel_size = 3
pool_size = 2
dropout = 0.2
input_shape = (28, 28, 1)

model = Sequential([
                    # convolutional feature extraction
                    # ConvNet 1

                    # convolutional part
                    keras.layers.Conv2D(filters, kernel_size, padding = 'valid',
                                        activation = 'relu',
                                        input_shape = input_shape),
                    #pooling part
                    keras.layers.MaxPooling2D(pool_size = pool_size),

                    # ConvNet 2

                    # convolutional part
                    keras.layers.Conv2D(filters, kernel_size, padding = 'valid',
                                        activation = 'relu',
                                        input_shape = input_shape),
                    #pooling part
                    keras.layers.MaxPooling2D(pool_size = pool_size),

                    # classification
                    # retrain from here
                    keras.layers.Flatten(name = 'flatten'),

                    # fully connected layer 1
                    keras.layers.Dropout(dropout),
                    keras.layers.Dense(128, activation='relu'),

                    # fully  connected Layer 2
                    keras.layers.Dropout(dropout, name = 'penult'),
                    keras.layers.Dense(classes, activation='softmax', name='last')
])

# print summary of the model
model.summary()

# print image of each model as check
keras.utils.plot_model(model, show_shapes=True, dpi=48)

es = keras.callbacks.EarlyStopping(min_delta=0.001, patience=2)

"""## Loss Functions
When y labels are sequential use 'sparse_categorical_crossentropy'. When y labels are OHE, use 'categorical_crossentropy'.
"""

model.compile(loss = 'sparse_categorical_crossentropy',
              optimizer = 'adam',
              metrics = ['accuracy'])

history = model.fit(x_train, y_train,
                    validation_split = 0.2,
                    batch_size = 32,
                    epochs = 1000,
                    callbacks = [es])

def plot_training_curves(history, title=None):
  '''plot the training curves for loss and accuracy given a model history'''

  # find the min loss epoch
  minimum = np.min(history.history['val_loss'])
  min_loc = np.where(minimum == history.history['val_loss'])[0]

  # get the vline y-min and y-max
  loss_min, loss_max = (min(history.history['val_loss'] + history.history['loss']),
                        max(history.history['val_loss'] + history.history['loss']))
  acc_min, acc_max = (min(history.history['val_accuracy'] + history.history['accuracy']),
                        max(history.history['val_accuracy'] + history.history['accuracy']))
  
  # create figure
  fig, ax = plt.subplots(ncols = 2, figsize = (15,10))
  fig.suptitle(title)
  idx = np.arange(1, len(history.history['accuracy']) + 1 )

  # plot loss && validation loss
  ax[0].plot(idx, history.history['loss'], label = 'loss')
  ax[0].plot(idx, history.history['val_loss'], label = 'val_loss')
  ax[0].vlines(min_loc + 1, loss_min, loss_max, label = 'min_loss_location')
  ax[0].set_title('Loss')
  ax[0].set_ylabel('Loss')
  ax[0].set_xlabel('Epochs')
  ax[0].legend()

  # plot accuracy && validation accuracy
  ax[1].plot(idx, history.history['accuracy'], label = 'accuracy')
  ax[1].plot(idx, history.history['val_accuracy'], label = 'val_accuracy')
  ax[1].vlines(min_loc + 1, acc_min, acc_max, label = 'min_loss_location')
  ax[1].set_title('Accuracy')
  ax[1].set_ylabel('Accuracy')
  ax[1].set_xlabel('Epochs')
  ax[1].legend()
  plt.show()

plot_training_curves(history)

# predict using the model
preds = model.predict(x_test)

x_test.shape

preds.shape

preds[0]

# classify the test set

# predict using the model
preds = model.predict(x_test)

# argmax along rows to get classification
preds = np.argmax(preds, axis=1).astype('uint8')

accuracy_score(y_test, preds)

preds

"""## Working with my images

"""

!pip install pillow
from PIL import Image

import matplotlib.pyplot as plt
import glob

letters = glob.glob('/content/drive/MyDrive/_SMU/7335 Machine Learning II/HW4/Letters/JPG/*')

# create y_new,
y_new = np.array([letters[i][letters[i].rfind('/')+1] for i, x in enumerate(letters)])

y_new

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
y_new = le.fit_transform(y_new)
y_new

im = Image.open(letters[90])
#im = im.rotate(0)
plt.imshow(im)

# resize images
size = (28,28)
im = im.resize(size)

# convert to grey scale
im = im.convert('L')
plt.imshow(im, cmap='gray')
#plt.imshow(im)

plt.show()

im = np.array(im)
im.max()

print(im.shape)

# load images, convert and combine into a list
size = (28,28)

new_images = [np.array(Image.open(im).convert('L').resize(size)) for im in letters]

# stack the arrays
x_new = np.stack(new_images)
print(x_new.shape)

x_new = x_new / 255

# add the color channel
x_new = x_new.reshape(x_new.shape + (1,))
x_new.shape

"""## Transfer Learning
1. "Lock" the convolutional layers (set to non-trainable)
2. Remove original output layer, add new output layer with 3 neurons
3. Train classifier on new dataset of 5 letters {A, B, C, D, E}
"""

history.history.keys()

# lock the ConvNet Layers
layer_trainable = False

for layer in model.layers:
  layer.trainable = layer_trainable
  if layer.name == 'flatten':
    layer_trainable = True


print(f"{'Layer Name':17} {'Is Trainable?'}")
for layer in model.layers:
  print(f"{layer.name:17} {layer.trainable}")

# get the penultimate layer of the model
penult_layer = model.get_layer(name = 'penult')

# create new output layer
output_layer = keras.layers.Dense(5, activation='softmax')(penult_layer.output)

# create new model with new output layer
new_model = Model(model.input, output_layer)

new_model.summary()

cb = keras.callbacks.EarlyStopping(min_delta=0.001, patience=2)

# split train/ test
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_new, y_new, test_size = 0.3, random_state = 42)
print(x_train.shape, x_test.shape)

new_model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

new_model_hist = new_model.fit(x_train, y_train,
                               validation_data = (x_test, y_test),
                               batch_size = 5,
                               epochs = 1000,
                               callbacks = [cb])

plot_training_curves(new_model_hist)

new_preds = new_model.predict(x_test)

new_preds = np.argmax(new_preds, axis=1).astype('uint8')
accuracy_score(y_test, new_preds)

new_preds.shape


