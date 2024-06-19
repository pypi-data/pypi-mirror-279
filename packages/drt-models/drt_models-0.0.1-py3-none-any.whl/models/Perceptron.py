import numpy as np
from src import Metrics, XLSXHelper
import pickle


class Perceptron:

    def __init__(self, learning_rate=0.00001, epochs=1):
        self.weights = None
        self.bias = None
        self.learning_rate = learning_rate
        self.epochs = epochs

    def activation(self, x):
        # return np.exp(-x)
        # return 1.0 / np.log(1 + np.exp(x))
        return -x
        # return 1.0 / (1.0 + np.exp(-x))
        # return np.log1p(np.exp(-np.abs(x))) + np.maximum(x, 0)


    def fit(self, X, y):
        n_features = X.shape[1]

        # Initializing weights and bias
        self.weights = np.zeros((n_features))
        self.bias = 0

        # Iterating until the number of epochs
        for epoch in range(self.epochs):

            # Traversing through the entire training set
            for i in range(len(X)):
                # y_pred = self.predict(X[i])
                # print(y_pred)
                print('Xi', X[i])
                print('w', self.weights)
                z = np.dot(X[i], self.weights) + self.bias
                # y_pred = self.predict(z)
                print('z' ,z)
                y_pred = self.predict(X[i])
                print('pred', y_pred)
                print('yi', y[i])
                # Updating weights and bias
                self.weights = self.weights + self.learning_rate * (y[i] - y_pred) * X[i]
                self.bias = self.bias + self.learning_rate * (y[i] - y_pred)

        return self.weights, self.bias

    def predict(self, X):
        z = np.dot(X, self.weights) + self.bias
        return z

    def save_coeffs_to_pickle(self):
        with open("perceptron.pickle", 'xb') as file:
            w = self.weights.tolist()
            b = self.bias.tolist()
            w.append(b[0])
            pickle.dump(w, file)

    def load_coeffs_from_pickle(self):
        with open("perceptron.pickle", 'rb') as file:
            tmp = pickle.load(file)
            self.bias = np.array(tmp[-1])
            tmp = tmp[:-1]
            self.weights = np.array(tmp)

    def calc_metrics(self, y_true, y_pred):
        m = Metrics.Metrics(y_true, y_pred)
        mse = m.calc_MSE()
        mae = m.calc_MAE()
        mape = m.calc_MAPE()
        smape = m.calc_SMAPE()
        print(mse, mae, mape, smape)


def prepare_data():
    data = XLSXHelper.read_excel("../dataset.xlsx")
    X = data.copy()
    X.drop(X.columns[9], axis=1, inplace=True)
    X = X.to_numpy(dtype=float)
    Y = data.copy()
    cols = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    Y.drop(Y.columns[cols], axis=1, inplace=True)
    Y = Y.to_numpy(dtype=float)
    return X, Y

X, y = prepare_data()

model = Perceptron()
model.fit(X, y)

y_pred = []
for item in X:
    t = model.predict(item)
    t = t.squeeze()

    y_pred.append([t])

# print(np.array(y_pred))
# print(y)
#
# print(model.weights)
# print(model.bias)
#
# model.calc_metrics(y, np.array(y_pred))
#
#
# x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#
# for i in range(len(x)):
#     f = np.array([100, 10, 10, 15, 7, 15, 20, 0.2, x[i]])
#     r = model.predict(f)
#     print(x[i], r)





