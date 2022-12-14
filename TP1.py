# -*- coding: utf-8 -*-
"""TP1_Emma.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EPwh55d2S0U3lNj6DhtXTIihV1LW__mk

**Algorithme de rétro-propagation de l’erreur**
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.14

import tensorflow
print(tensorflow.__version__)

"""**Chargement des données** **texte en gras**"""

import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from keras.datasets import mnist

# the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

"""**VISUALISATION**"""

mpl.use('TKAgg')
plt.figure(figsize=(7.195, 3.841), dpi=100)
for i in range(200):
  plt.subplot(10,20,i+1)
  plt.imshow(X_train[i,:].reshape([28,28]), cmap='gray')
  plt.axis('off')
plt.show()

"""s=x.W+b  s(1,10) x(1,784=28*28) W(784,1) b(1,10)

**Regression Logistique**

Le modèle possède 784*10 + 10 = 7850 paramètres

La fonction de coût est bien convexe par rapports aux paramètres W,b du modèle, on peut assurer ici la convergence vers un minimum global de la solution. En effet son gradient sera la somme d'une fonction linéaire et d'une fonction convexe ce qui donne donc une fonction convexe. Cette linéarité est perdu en ajoutant une couche cachée, on verra cela plus tard, l'initialisation sera alors importante, on évitera d'initialiser à 0.
"""

from keras.utils import np_utils
K=10
# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, K)
Y_test = np_utils.to_categorical(y_test, K)

def softmax(X):
 # Input matrix X of size Nbxd - Output matrix of same size
 E = np.exp(X)
 return (E.T / np.sum(E,axis=1)).T

def forward(batch, W, b):
  s = np.dot(batch, W)+b
  return softmax(s)

def cross_entropy(predictions, targets, epsilon=1e-12):
  """
  computes cross entropy between targets (encoded as one-hot vectors) and predictions
  Input : predictions (N,k) ndarray
          targets (N,k) ndarray
  Returns: scalar
  """
  predictions = np.clip(predictions,epsilon, 1.-epsilon)
  N=predictions.shape[0]
  ce = -np.sum(targets*np.log(predictions+1e-9))/N
  return ce

N = X_train.shape[0]
d = X_train.shape[1]
W = np.zeros((d,K))
b = np.zeros((1,K))
numEp = 20 # Number of epochs for gradient descent
eta = 1e-1 # Learning rate
batch_size = 100
nb_batches = int(float(N) / batch_size)
gradW = np.zeros((d,K))
gradb = np.zeros((1,K))

for epoch in range(numEp):
  loss = 0
  for ex in range(nb_batches):
     # FORWARD PASS : compute prediction with current params for examples in batch
     batch = X_train[ex*batch_size:(ex+1)*batch_size]
     true_y = Y_train[ex*batch_size:(ex+1)*batch_size]
     pred_y = forward(batch, W, b)
     #print(Y.shape)
     dy = pred_y - true_y
     # BACKWARD PASS :
     # 1) compute gradients for W and b
     dW = (1/len(batch))* np.dot(batch.T, dy)
     db = (1/len(batch))* dy.sum()
     # 2) update W and b parameters with gradient descent
     W = W - eta *dW
     b = b -eta *db
     loss += cross_entropy( pred_y, true_y)
  loss/= len(batch)
  print("Epoc {} : {}".format(epoch, loss))

print(batch.shape)
print(true_y.shape)
print(pred_y.shape)
print(dy.shape)
print(dW.shape)
print(W.shape)
print(b.shape)
print(db.shape)

def accuracy(W, b, images, labels):
  pred = forward(images, W,b )
  return np.where( pred.argmax(axis=1) != labels.argmax(axis=1) , 0.,1.).mean()*100.0

print(accuracy(W, b, X_test, Y_test))

"""**Exercice 2**"""

from keras.utils import np_utils
K=10
# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, K)
Y_test = np_utils.to_categorical(y_test, K)

def softmax(X):
 # Input matrix X of size Nbxd - Output matrix of same size
 E = np.exp(X)
 return (E.T / np.sum(E,axis=1)).T

def sigmoid(X):
  E = np.exp(-X)
  return (1 / (1 + E))

def forward(batch, Wh, bh, Wy, by):
  u = np.dot(batch, Wh)+bh
  h = sigmoid(u)
  v = np.dot(h, Wy)+by
  return softmax(v), h

def cross_entropy(predictions, targets, epsilon=1e-12):
  """
  computes cross entropy between targets (encoded as one-hot vectors) and predictions
  Input : predictions (N,k) ndarray
          targets (N,k) ndarray
  Returns: scalar
  """
  predictions = np.clip(predictions,epsilon, 1.-epsilon)
  N=predictions.shape[0]
  ce = -np.sum(targets*np.log(predictions+1e-9))/N
  return ce

N = X_train.shape[0]
d = X_train.shape[1]
L = 100
Wh = np.random.normal(loc=0, scale= 0.1, size=(d,L))
#Wh = np.random.randn(d,L)*np.sqrt(1/d)
#Wh = np.zeros((d,L))
bh = np.zeros((1,L))
Wy = np.random.normal(loc=0, scale= 0.1, size=(L,K))
#Wy = np.random.randn(L,K)*np.sqrt(1/L)
#Wy = np.zeros((L,K))
by = np.zeros((1,K))
numEp = 100 # Number of epochs for gradient descent
eta = 1 # Learning rate
batch_size = 100
nb_batches = int(float(N) / batch_size)
losses = []

for epoch in range(numEp):
  loss = 0
  for ex in range(nb_batches):
     batch = X_train[ex*batch_size:(ex+1)*batch_size]
     true_y = Y_train[ex*batch_size:(ex+1)*batch_size]
     # FORWARD PASS : compute prediction with current params for examples in batch
     pred_y, h = forward(batch, Wh, bh, Wy, by)
     #gradient error
     dy = pred_y - true_y
     dh = np.dot(dy, Wy.T) * (h*(1-h))
     # BACKWARD PASS :
     # 1) compute gradients for W and b
     dWy = (1/len(batch))* np.dot(h.T, dy)
     dby = (1/len(batch))* dy.sum(axis=0)
     dWh = (1/len(batch))* np.dot(batch.T, dh)
     dbh = (1/len(batch))* dh.sum(axis=0)
     # 2) update W and b parameters with gradient descent
     Wy = Wy - eta *dWy
     by = by -eta *dby
     Wh = Wh - eta *dWh
     bh = bh -eta *dbh
     loss += cross_entropy( pred_y, true_y)
  loss/= len(batch)
  losses.append(loss)
  print("Epoc {} : {}".format(epoch, loss))

def accuracy(Wy, by, Wh, bh, images, labels):
  pred, _ = forward(images, Wh, bh, Wy, by)
  return np.where( pred.argmax(axis=1) != labels.argmax(axis=1) , 0.,1.).mean()*100.0

print(accuracy(Wy, by, Wh, bh, X_test, Y_test))

plt.plot(range(1, len(losses)+1), losses)
plt.show