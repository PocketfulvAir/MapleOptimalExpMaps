import pandas as pd
import math
# spawn notes:
# current respawn time of 7s according to kms

class EXPModifier:
    """
    The class used to apply exp/level additions/penalties
    to further estimate the optimal map for exp.
    """
    global spawn_time
    spawn_time = 7

    def __init__(self, data = None):
        """
        Input data should be the post-clustered dataframe
        """
        self.data = data


    def run_30_min(self, initialxp, spawnxp):
        """
        Ran to try to minimize the difference between the initial spawn size
        vs the overall max summons that can occur
        """
        executions = math.floor(60 * 30 / spawn_time)
        return round((initialxp + (spawnxp * executions)) / (executions + 1))


    def level_bonus(self, char_lvl, mon_lvl):
        """
        Returns an integer value of the percentage to be used
        for level difference penalty/bonus
        """
        difference = char_lvl - mon_lvl
        adiff = abs(difference)
        # Above and below 10 levels are the same
        if adiff < 2:
            return 20
        elif adiff < 5:
            return 10
        elif adiff < 10:
            return 5
        elif adiff == 10:
            return 0
        # -1% for every 2 level above 
        if difference > 10 and difference < 21:
            return -math.ceil((difference - 10) / 2)
        # base -10%, -1% per level down to -30% 
        elif difference > 20: 
            return max(-(10 + (difference - 20)), -30)
        # -1% for every 1 level below
        elif difference < -10 and difference > -21: 
            return difference + 10
        # base -30%, -4% per level down to -90%
        elif difference < -20:
            return max(-(30 - ((difference + 20) * 4)),-90)

    def wide_penalty(self, wide):
        """
        This simulates the inability to kill every mob
        on the map due to not reaching it.
        Currently scaled from 1-10 for future narrowing
        but currently, only 5-10 matter for a general estimate
        """
        # A 10 indicates inability to reach half the map
        # thus attainable exp reduced by half
        return (wide - 5) * 10

    def wild_totem_bonus(self):
        self.run_30_min(1,1)

    def calculate(self):
        initexp = self.data["total_exp_init"].tolist()
        spawnexp = self.data["total_exp_spawn"].tolist()
        size = len(initexp)
        adjustedexp = []
        for i in range(size):
            adjustedexp.append(self.run_30_min(initexp[i],spawnexp[i]))
        return adjustedexp

    def apply_wide_penalty(self, exps):
        widths = self.data["wideness"].tolist()
        size = len(widths)
        for i in range(size):
            exps[i] = round(exps[i] * (1 - (self.wide_penalty(widths[i]) / 100)))

    def apply_level_modifier(self, char_lvl, exps):
        lvls = self.data['mob_level'].tolist()
        size = len(lvls)
        for i in range(size):
            exps[i] = round(exps[i] * (1 + (self.level_bonus(char_lvl, lvls[i]) / 100)))
        
if __name__ == "__main__":
    a = EXPModifier()
    for i in range(1,40):
       b = a.level_bonus(i, 50)
       print(b)