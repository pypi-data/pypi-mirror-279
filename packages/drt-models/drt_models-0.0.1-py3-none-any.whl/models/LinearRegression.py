import numpy as np
import pickle
import src


class LinearRegression:
    def __init__(self, X=None, y=None):
        self.coefficients = None
        self.mse = None
        self.mae = None
        self.mape = None
        self.smape = None
        self.X = X
        if self.X is not None:
            self.newX = self.X.copy()
        self.y = y

    def fit(self):
        # Добавляем столбец с единицами для учёта коэффициента b0
        self.newX = np.concatenate((np.ones((self.X.shape[0], 1)), self.X), axis=1)
        # Находим значения коэффициентов b с помощью метода наименьших квадратов
        self.coefficients = np.linalg.inv(self.newX.T @ self.newX) @ self.newX.T @ self.y

    def predict(self, features):
        features = np.concatenate((np.ones((features.shape[0], 1)), features), axis=1)
        return features @ self.coefficients

    def calc_metrics(self):
        y_pred = []
        for item in self.X:
            y_pred.append(self.predict(np.array([item])))

        y_pred = np.array(y_pred)
        metrics = src.Metrics.Metrics(self.y, y_pred)
        mse = metrics.calc_MSE()
        print("mse = ", mse)
        mae = metrics.calc_MAE()
        print("mae = ", mae)
        mape = metrics.calc_MAPE()
        print("mape = ", mape)
        smape = metrics.calc_SMAPE()
        print("smape = ", smape)
        return mse, mae, mape, smape

    def save_coeffs_to_pickle(self):
        with open("coeffs.pickle", 'xb') as file:
            pickle.dump(self.coefficients, file)

    def load_coeffs_from_pickle(self):
        with open("coeffs.pickle", 'rb') as file:
            tmp = pickle.load(file)
            self.coefficients = np.array(tmp)

