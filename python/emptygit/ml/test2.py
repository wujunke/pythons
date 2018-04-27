#coding=utf8
import numpy as np
import urllib
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
# url with dataset

url = "http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"

# download the file

raw_data = urllib.urlopen(url)

# load the CSV file as a numpy matrix

dataset = np.loadtxt(raw_data, delimiter=",")

# separate the data from the target attributes

X = dataset[:,0:7]
y = dataset[:,8]

# print X
# print y
model = ExtraTreesClassifier()
model.fit(X,y)
print(model.feature_importances_)


alphas = np.array([1, 0.1, 0.01, 0.001, 0.0001, 0])
model = Ridge()
grid = GridSearchCV(estimator=model,param_grid=dict(alpha=alphas))
grid.fit(X,y)
print(grid)
print(grid.best_score_)
print(grid.best_estimator_.alpha)


# from sklearn.model_selection import RandomizedSearchCV
# from scipy.stats import uniform as sp_rand
# # prepare a uniform distribution to sample for the alpha parameter
#
# param_grid = {'alpha': sp_rand()}
#
# # create and fit a ridge regression model, testing random alpha values
#
# model = Ridge()
#
# rsearch = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=100)
#
# rsearch.fit(X, y)
#
# print(rsearch)
#
# # summarize the results of the random parameter search
#
# print(rsearch.best_score_)
#
# print(rsearch.best_estimator_.alpha)

