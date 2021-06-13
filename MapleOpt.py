import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

dataloc = "mapdata.xlsx"
data = pd.ExcelFile(dataloc)
df = pd.read_excel(data,'Map Data')
columns = df.columns

columns = np.array(columns)

#df.isnull().sum()
filter = [0,8,9,10,11,12]
df_purge = df.dropna()
df_purge = df_purge[columns[filter]]
df_purge = df_purge.groupby(list(columns[filter[:4]]),sort=False).sum().reset_index()

df_purge

df_use = df_purge[[columns[8],columns[9]]]

df_use[[columns[8],columns[9]]]

#plt.scatter(df[columns[8]],df[columns[9]])
#plt.show()

model = KMeans(n_clusters=10)
model.fit(df_use)
predictions = model.predict(df_use)
clusters = np.unique(predictions)
for cluster in clusters:
  df_cluster = df_purge[predictions == cluster]
  plt.scatter(df_cluster[columns[8]],df_cluster[columns[9]])
plt.show()

tester = model.predict([[6,7]])
print(tester)
print(df_purge[predictions == tester])

