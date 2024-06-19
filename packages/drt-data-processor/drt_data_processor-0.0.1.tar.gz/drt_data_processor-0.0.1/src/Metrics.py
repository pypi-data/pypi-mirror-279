import math


class Metrics:
    def __init__(self, y_true, y_pred):
        self.y_karaushev = y_true.squeeze()
        self.y_model = y_pred.squeeze()

    def calc_MSE(self):
        mse = 0.0
        for i in range(len(self.y_karaushev)):
            mse += math.pow(self.y_karaushev[i] - self.y_model[i], 2)
        mse = mse / len(self.y_karaushev)
        return mse

    def calc_MAE(self):
        mae = 0.0
        mae_dict = dict(zip(self.y_karaushev, self.y_model))
        for key, value in mae_dict.items():
            mae += math.fabs(key - value)
        mae = mae / len(mae_dict)
        return mae

    def calc_MAPE(self):
        mape = 0.0
        for i in range(len(self.y_karaushev)):
            mape += math.fabs(self.y_karaushev[i] - self.y_model[i]) / math.fabs(self.y_karaushev[i])
        mape = mape / len(self.y_karaushev)
        return mape

    def calc_SMAPE(self):
        smape = 0.0
        smape_dict = dict(zip(self.y_karaushev, self.y_model))
        for key, value in smape_dict.items():
            smape += (2 * math.fabs(key - value)) / (key + value)
        smape = smape / len(smape_dict)
        return smape