import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from sklearn import decomposition
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class HimdexKMeans:
    '''
    Python class for generating the k-Means clustering model
    '''

    def __init__(self, data):
        '''
        Purpose: creates a new k-Means clustering model

        INPUT:
        data - pandas dataframe of data to use
        '''
        self.data = data
    
    def generate_labels(self, clusters, max_iter, random_state):
        '''
        Purpose: generates a new K-mean model

        INPUTS:
        clusters - int number of desired clusters
        max_iter - int max iteration used for the k-Means model
        random_state - int random state for replicability

        OUTPUT:
        labels - list of clustering labels
        '''

        # define standard scaler
        scaler = StandardScaler()
        
        # transform data
        data = scaler.fit_transform(self.data)
        self.scaled_data = data

        # perform clustering to get training labels
        k = 2
        KM = KMeans(
            n_clusters = clusters, 
            max_iter = max_iter, 
            random_state = random_state
        )
        KM.fit(data)
        self.model = KM
        self.labels = KM.labels_

        return self.labels
    
    def visualize_features(self):
        '''
        Purpose: visualize the difference in features for each class
        '''
        data = self.scaled_data
        labels = self.labels
        features = self.data.columns

        # loop through each feature
        for i in range(data.shape[1]):
            # plot the class conditional density
            pd.DataFrame(data[labels == 1,i]).plot.kde(title = f'{features[i]} for 1')
            pd.DataFrame(data[labels == 0,i]).plot.kde(title = f'{features[i]} for 0')
            # print the class conditional mean
            print(data[labels == 1,i].mean())
            print(data[labels == 0,i].mean())
            print()
    
    def generate_pca(self, components):
        '''
        Purpose: performs principal component analysis on the data

        INPUT:
        components - int number of desired components

        OUTPUT:
        pca_components - array of the PCA components
        '''

        self.pca = decomposition.PCA(n_components = components)
        self.pca_points = self.pca.fit_transform(self.scaled_data)

        return self.pca.components_

    def visualize_3d_pca(self, colors, alpha):
        '''
        Purpose: plot a graph of the PCA in a 3D space

        INPUT:
        colors - list of string for the desired colors of the graph
        alpha - float value between 0 and 1 to determine opacity of plot
        '''

        points = self.pca_points

        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(projection = '3d')

        # 3d projection
        ax.scatter(
            points[:, 0], 
            points[:, 1], 
            points[:, 2], 
            c = self.labels, 
            cmap = matplotlib.colors.ListedColormap(colors), 
            alpha = alpha
        )

        plt.show()
    
    def visualize_2d_pca(self, colors, alpha):
        '''
        Purpose: plot a graph of the PCA in a 2D space

        INPUT:
        colors - list of string for the desired colors of the graph
        alpha - float value between 0 and 1 to determine opacity of plot
        '''

        points = self.pca_points

        # 2d projection of the plot
        plt.scatter(
            points[:, 0], 
            points[:, 1], 
            c = self.labels, 
            cmap = matplotlib.colors.ListedColormap(colors), 
            alpha = alpha
        )
        
        plt.show()