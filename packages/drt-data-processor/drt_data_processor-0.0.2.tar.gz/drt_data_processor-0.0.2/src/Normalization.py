import pandas as pd


class DataNormalization:
    def __init__(self, data):
        self.df = data

    def normalize(self):
        result = self.df.copy()  
        for feature_name in self.df.columns:
            if feature_name == 'nш':
                continue
            # if feature_name == 'Qe' or feature_name == 'Qst' or feature_name == 'Vst' or feature_name == 'Se' or feature_name == 'H' or feature_name == 'nш' or feature_name == 'y':
            #     continue
            # else:
            max_value = self.df[feature_name].max()
            min_value = self.df[feature_name].min()
            result[feature_name] = (self.df[feature_name] - min_value) / (max_value - min_value)
        return result
