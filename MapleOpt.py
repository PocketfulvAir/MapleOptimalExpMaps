import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from Clusterer import Clusterer
from EXPModifier import EXPModifier
from Optimizer import Optimizer

if __name__ == "__main__":
    optim = Optimizer(238,8,6,10)
    maps = optim.get_optimal_map()
    print(maps)
