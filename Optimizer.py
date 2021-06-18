from Clusterer import Clusterer
from EXPModifier import EXPModifier

class Optimizer:

    def __init__(self, level, h, v, n_cluster = 8):
        self.level = level
        self.horizontal = h
        self.vertical = v
        self.maple_cluster(n_cluster)

    def maple_cluster(self, n_cluster):
        self.cluster = Clusterer(n_clusters=n_cluster)
        self.cluster.read_sheet("mapdata.xlsx","Map Data")
        self.cluster.maple_clean()
        self.cluster.fit()
        self.cluster.cluster()
        self.cluster.check_usability()

    def predict(self):
        prediction = self.cluster.predict(self.horizontal, self.vertical)
        self.possibilities = self.cluster.within(prediction)
        self.mod = EXPModifier(self.possibilities)

    def update_parameters(self, h=-1, v=-1, lvl=-1):
        if h > 0:
            self.horizontal = h
        if v > 0:
            self.vertical = v
        if lvl > 0:
            self.level = lvl

    def apply_modifier(self):
        exps = self.mod.calculate()
        self.mod.apply_level_modifier(self.level, exps)
        self.mod.apply_wide_penalty(exps)
        return exps

    def get_optimal_map(self):
        self.predict()
        exps = self.apply_modifier()
        names = self.possibilities['map_name'].tolist()
        mappings = {names[i]: exps[i] for i in range(len(names))}
        maxes = sorted(mappings, key=mappings.get,reverse=True)[:3]
        return maxes