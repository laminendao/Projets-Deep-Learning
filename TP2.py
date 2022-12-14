# -*- coding: utf-8 -*-
"""Emma-TP2 - Deep Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zkekueoxxZmI6XcuKJBfGUnE7OJrhGS4
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.14

import tensorflow
print(tensorflow.__version__)

import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Activation

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

"""**Exercice 1**"""

model = Sequential() #  initialisation du model
model.add(Dense(10,  input_dim=784, name='fc1')) #ajout d'une couche de projection linéaire de taille 10
model.add(Activation('softmax'))

model.summary()

"""Modèle reconnu ?

Avec Keras, on va compiler le modèle en lui passant un loss (ici l” entropie croisée), une méthode d’optimisation (ici uns descente de gradient stochastique, stochatic gradient descent, sgd), et une métrique d’évaluation (ici le taux de bonne prédiction des catégories, accuracy):
"""

from keras.optimizers import SGD
learning_rate = 0.1
sgd = SGD(learning_rate)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

"""l’apprentissage du modèle sur des données d’apprentissage est mis en place avec la méthode fit"""

from keras.utils import np_utils
batch_size = 100
nb_epoch = 200
# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)
model.fit(X_train, Y_train,batch_size=batch_size, epochs=nb_epoch,verbose=1)

scores = model.evaluate(X_test, Y_test, verbose=0)
print("%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

"""On a implémenté l’apprentissage du modèle sur la base de train de la base MNIST.
On remarque que les performances du réseau sur la base de test sont les mêmes que celles obtenues lors de la ré-implémentation manuelle (92.13%)

# **Exercice2**

On va maintenant enrichir le modèle de régression logistique en créant une couche de neurones cachée complètement connectée supplémentaire, suivie d’une fonction d’activation non linéaire de type sigmoïde. On va ainsi obtenir un réseau de neurones à une couche cachée, le Perceptron

**Mise en place du perceptron**
"""

model = Sequential() #  initialisation du model
model.add(Dense(100,  input_dim=784, name='fc1')) #ajout à un réseau séquentiel vide une première couche cachée
model.add(Activation('sigmoid')) #non linéarité de type sigmoïde
model.add(Dense(10, name='fc2'))#ajout d'une couche de projection linéaire de taille 10
model.add(Activation('softmax'))

"""(besoin que de la dimension d'entrée avec Keras)"""

model.summary()

"""Le modèle possède 784*100 + 100 + 100X10 + 10 = 79510 paramètres"""

from keras.optimizers import SGD
learning_rate = 1
sgd = SGD(learning_rate)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

from keras.utils import np_utils
batch_size = 100
nb_epoch = 100
# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)
model.fit(X_train, Y_train,batch_size=batch_size, epochs=nb_epoch,verbose=1)

scores = model.evaluate(X_test, Y_test, verbose=0)
print("%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

"""Évaluer les performances du réseau sur la base de test et les comparer à celles obtenues lors de la séance précédente. Conclure On est censé retrouvé les même performances que pour l'exo 2 du TP 1

**sauvegarde du modèle appris**
"""

from keras.models import model_from_yaml
def saveModel(model, savename):
  # serialize model to YAML
  model_yaml = model.to_yaml()
  with open(savename+".yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
    print("Yaml Model ",savename,".yaml saved to disk")
  # serialize weights to HDF5
  model.save_weights(savename+".h5")
  print("Weights ",savename,".h5 saved to disk")

saveModel(model,"MLP")

"""# **Exercice 3 : Réseaux de neurones convolutifs avec Keras**"""

X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)

from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D

model = Sequential([
                    Conv2D(16,kernel_size=(5, 5),activation='relu',input_shape=(28, 28, 1),padding='valid'),
                    MaxPooling2D(pool_size=(2, 2)),
                    Conv2D(32,kernel_size=(5, 5),activation='relu',input_shape=(28, 28, 1),padding='valid'),
                    MaxPooling2D(pool_size=(2, 2)),
                    Flatten(),
                    Dense(100),
                    Activation('sigmoid'),
                    Dense(10),
                    Activation('softmax'),               
])

model.summary()

from keras.optimizers import SGD
learning_rate = 0.5
sgd = SGD(learning_rate)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

"""Quelle est le temps d’une époque avec ce modèle convolutif ?28sec"""

from keras.utils import np_utils
batch_size = 100
nb_epoch = 20
# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)
model.fit(X_train, Y_train,batch_size=batch_size, epochs=nb_epoch,verbose=1)

scores = model.evaluate(X_test, Y_test, verbose=0)
print("%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

"""Quelle est le maintenant temps d’une époque avec ce modèle convolutif sur GPU ? 2s 3ms
Quel est le taux d’accélération ? D’où vient ce gain ? plus de 10 fois plus rapide, cela vien de l'utilisation du hardware GPU, le calcul du foreward est beaucoup plus rapide, parallélisation interne qui rend les calculs rapides.
"""

from keras.models import model_from_yaml
def saveModel(model, savename):
  # serialize model to YAML
  model_yaml = model.to_yaml()
  with open(savename+".yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
    print("Yaml Model ",savename,".yaml saved to disk")
  # serialize weights to HDF5
  model.save_weights(savename+".h5")
  print("Weights ",savename,".h5 saved to disk")

saveModel(model,"CNN")

"""# **Exercice 4 : Visualisation avec t-SNE**

L’objectif va être d’effectuer une réduction de dimension en 2D des données de la base de test de MNIST en utilisant la méthode t-SNE
"""

import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
from scipy.spatial import ConvexHull
from sklearn.mixture import GaussianMixture
from scipy import linalg
from sklearn.neighbors import NearestNeighbors

def convexHulls(points, labels):
  # computing convex hulls for a set of points with asscoiated labels
  convex_hulls = []
  for i in range(10):
    convex_hulls.append(ConvexHull(points[labels==i,:]))
  return convex_hulls
# Function Call

def best_ellipses(points, labels):
  # computing best fiiting ellipse for a set of points with asscoiated labels
  gaussians = []
  for i in range(10):
    gaussians.append(GaussianMixture(n_components=1, covariance_type='full').fit(points[labels==i, :]))
  return gaussians
# Function Call

def neighboring_hit(points, labels):
  k = 6
  nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='ball_tree').fit(points)
  distances, indices = nbrs.kneighbors(points)

  txs = 0.0
  txsc = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  nppts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

  for i in range(len(points)):
    tx = 0.0
    for j in range(1,k+1):
      if (labels[indices[i,j]]== labels[i]):
        tx += 1
    tx /= k
    txsc[labels[i]] += tx
    nppts[labels[i]] += 1
    txs += tx

  for i in range(10):
    txsc[i] /= nppts[i]

  return txs / len(points)

def visualization(points2D, labels, convex_hulls, ellipses ,projname, nh):
  points2D_c= []
  for i in range(10):
      points2D_c.append(points2D[labels==i, :])
  # Data Visualization
  cmap =cm.tab10

  plt.figure(figsize=(3.841, 7.195), dpi=100)
  plt.set_cmap(cmap)
  plt.subplots_adjust(hspace=0.4 )
  plt.subplot(311)
  plt.scatter(points2D[:,0], points2D[:,1], c=labels,  s=3,edgecolors='none', cmap=cmap, alpha=1.0)
  plt.colorbar(ticks=range(10))

  plt.title("2D "+projname+" - NH="+str(nh*100.0))

  vals = [ i/10.0 for i in range(10)]
  sp2 = plt.subplot(312)
  for i in range(10):
      ch = np.append(convex_hulls[i].vertices,convex_hulls[i].vertices[0])
      sp2.plot(points2D_c[i][ch, 0], points2D_c[i][ch, 1], '-',label='$%i$'%i, color=cmap(vals[i]))
  plt.colorbar(ticks=range(10))
  plt.title(projname+" Convex Hulls")

  def plot_results(X, Y_, means, covariances, index, title, color):
      splot = plt.subplot(3, 1, 3)
      for i, (mean, covar) in enumerate(zip(means, covariances)):
          v, w = linalg.eigh(covar)
          v = 2. * np.sqrt(2.) * np.sqrt(v)
          u = w[0] / linalg.norm(w[0])
          # as the DP will not use every component it has access to
          # unless it needs it, we shouldn't plot the redundant
          # components.
          if not np.any(Y_ == i):
              continue
          plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color, alpha = 0.2)

          # Plot an ellipse to show the Gaussian component
          angle = np.arctan(u[1] / u[0])
          angle = 180. * angle / np.pi  # convert to degrees
          ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
          ell.set_clip_box(splot.bbox)
          ell.set_alpha(0.6)
          splot.add_artist(ell)

      plt.title(title)
  plt.subplot(313)

  for i in range(10):
      plot_results(points2D[labels==i, :], ellipses[i].predict(points2D[labels==i, :]), ellipses[i].means_,
      ellipses[i].covariances_, 0,projname+" fitting ellipses", cmap(vals[i]))

  plt.savefig(projname+".png", dpi=100)
  plt.show()

from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, init='pca', verbose=2)

X_test_projected = tsne.fit_transform(X_test)

convex_hulls= convexHulls(X_test_projected, y_test)
ellipses = best_ellipses(X_test_projected, y_test)
NH = neighboring_hit(X_test_projected, y_test)

visualization(X_test_projected, y_test, convex_hulls, ellipses, 't-SNE', NH)



"""Pour PCA"""

from sklearn.decomposition import PCA

pca = PCA(n_components=2)

X_test_pca = pca.fit_transform(X_test)

convex_hulls= convexHulls(X_test_pca, y_test)
ellipses = best_ellipses(X_test_pca, y_test)
NH = neighboring_hit(X_test_pca, y_test)

visualization(X_test_pca, y_test, convex_hulls, ellipses, 'pca', NH)



"""# **Exercice 5 : Visualisation des représentations internes des réseaux de neurones**"""

from keras.models import model_from_yaml
def loadModel(savename):
  with open(savename+".yaml", "r") as yaml_file:
    model = model_from_yaml(yaml_file.read())
  print("Yaml Model ",savename,".yaml loaded ")
  model.load_weights(savename+".h5")
  print("Weights ",savename,".h5 loaded ")
  return model

MLP = loadModel('MLP')

CNN = loadModel('CNN')

CNN.pop()

CNN.pop()

CNN.summary()

"""On récupère bien le vecteur de taille 100 souhaité en retirant 2 couches."""

MLP.pop()

MLP.pop()

MLP.summary

hidden_CNN = CNN.predict(X_test)

X_test = X_test.reshape(10000, 784)

hidden_MLP = MLP.predict(X_test)

#print(hidden_CNN.shape)
print(hidden_MLP.shape)

from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, init='pca', verbose=2)

hidden_MLP_tsne = tsne.fit_transform(hidden_MLP)

convex_hulls_MLP= convexHulls(hidden_MLP_tsne, y_test)
ellipses_MLP = best_ellipses(hidden_MLP_tsne, y_test)
NH_MLP = neighboring_hit(hidden_MLP_tsne, y_test)

hidden_CNN_tsne = tsne.fit_transform(hidden_CNN)

convex_hulls_CNN= convexHulls(hidden_CNN_tsne, y_test)
ellipses_CNN = best_ellipses(hidden_CNN_tsne, y_test)
NH_CNN = neighboring_hit(hidden_CNN_tsne, y_test)

visualization(hidden_MLP_tsne, y_test, convex_hulls_MLP, ellipses_MLP, 't-SNE', NH_MLP)

visualization(hidden_CNN_tsne, y_test, convex_hulls_CNN, ellipses_CNN, 't-SNE', NH_CNN)