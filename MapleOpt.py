import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from Clusterer import Clusterer
from EXPModifier import EXPModifier

if __name__ == "__main__":
    clusterer = Clusterer(n_clusters=10)
    clusterer.read_sheet("mapdata.xlsx", "Map Data")
    clusterer.maple_clean()
    clusterer.check_usability()
    clusterer.fit()
    clusterer.cluster()
    tester = clusterer.predict(7,3)
    print(tester)
    #print(clusterer.within(tester))

    mod = EXPModifier(clusterer.within(tester))
    print(mod.data)
#    print(mod.data.columns)
    calcs = mod.calculate()
    print(calcs)
    mod.apply_wide_penalty(calcs)
    print(calcs)