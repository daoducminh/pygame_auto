import pandas as pd


class SpeedDeduction:
    def __init__(self, filename):
        self.rules = pd.read_csv(filename).to_dict(orient='records')

    def get_args(self, light, distance):
        pass

    def deduce(self, light, distance):
        pass
