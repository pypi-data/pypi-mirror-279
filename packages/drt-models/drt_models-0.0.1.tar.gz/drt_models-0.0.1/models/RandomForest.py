import numpy as np
import pickle

# Define the Decision Tree Regressor class
class DecisionTreeRegressor:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.X = X
        self.y = y

    def predict(self, X):
        predictions = []
        for x in X:
            # Simple mean prediction for demonstration purposes
            predictions.append(np.mean(self.y))
        return np.array(predictions)


# Define the Random Forest Regressor class
class RandomForestRegressor:
    def __init__(self, n_estimators=100, max_depth=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.trees = [DecisionTreeRegressor(max_depth=self.max_depth) for _ in range(n_estimators)]

    def fit(self, X, y):
        for tree in self.trees:
            indices = np.random.choice(X.shape[0], X.shape[0], replace=True)
            tree.fit(X[indices], y[indices])

    def predict(self, X):
        predictions = np.zeros((X.shape[0], len(self.trees)))
        for i, tree in enumerate(self.trees):
            predictions[:, i] = tree.predict(X)
        return np.mean(predictions, axis=1)

    def load_coefficents_from_pickle(self):
        with open("forest.pickle") as file:
            rf = pickle.load(file)
            return rf
