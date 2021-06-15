import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class Clusterer:
    """
    Class for grouping and predicting
    the optimal maps given parameters
    """
    def __init__(self, n_clusters = 8, random_state = None, algo = "full"):
        """
        data will also need to be added as well as data_use
        for useful data purposes
        """
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state,algorithm=algo)


    def check_usability(self):
        try:
            self.data == 0
        except AttributeError:
            print("Data does not exist.")
            return 0
        try:
            self.data_use == 0
        except AttributeError:
            print("Data is in a raw state. Clean/assign it to the data_use var")
            return 0
        print("Class is in a usable state.")
        return 1

    def read_sheet(self, file, sheet): 
        """
        Read and store an xls/xlsx file for a specific sheet
        """
        data = pd.ExcelFile(file)
        self.data = pd.read_excel(data, sheet)

    def maple_clean(self):
        columns = np.array(self.data.columns)
        filter = [0,8,9,10,11,12]
        df_purge = self.data.dropna()
        df_purge = df_purge[columns[filter]]
        self.data_purge = df_purge.groupby(list(columns[filter[:4]]),sort=False).sum().reset_index()
        self.data_use = self.data_purge[[columns[8],columns[9]]]
        

    def fit(self):
        self.model.fit(self.data_use)

    def update_model(self, n_cluster = 8, random_state = None, algo = "full"):
        self.model = KMeans(n_cluster=n_cluster, random_state=random_state,algorithm=algo)

    def update_data(self, data):
        self.data = data

    def data2use(self):
        self.data_use = self.data

    def predict(self, horizontal, vertical):
        predictions = self.model.predict([[horizontal,vertical]])
        return predictions[0]

    def cluster(self):
        predictions = self.model.predict(self.data_use)
        clusters = np.unique(predictions)
        group_clusters = {}
        for cluster in clusters:
            group_clusters[cluster] = self.data_purge[predictions == cluster]
        self.clusters = group_clusters
       
    def within(self, target):
        return self.clusters[target]

if __name__ == "__main__":
    clusterer = Clusterer(n_clusters=10)
    clusterer.read_sheet("mapdata.xlsx", "Map Data")
    clusterer.maple_clean()
    clusterer.check_usability()
    clusterer.fit()
    clusterer.cluster()
    tester = clusterer.predict(7,3)
    print(tester)
    print(clusterer.within(tester))

