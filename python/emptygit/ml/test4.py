from sklearn import datasets
import numpy as np

iris = datasets.load_iris()
np.unique(iris.target)


from sklearn import svm
clf = svm.LinearSVC()
print iris.data
print iris.target
print clf.fit(iris.data , iris.target)