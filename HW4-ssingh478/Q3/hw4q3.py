## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect seizure

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the paramater 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.30,shuffle=True, random_state=random_state)

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
regr = LinearRegression()
regr.fit(x_train, y_train)
y_predict_train=regr.predict(x_train)
y_predict_test =regr.predict(x_test)
y_predict_train=[0 if i<=0.5 else 1 for i in y_predict_train]
y_predict_test=[0 if i<=0.5 else 1 for i in y_predict_test]
train_accuracy_regr=accuracy_score(y_train,y_predict_train)
test_accuracy_regr=accuracy_score(y_test,y_predict_test)
print("Train accuracy for Linear regression: "+str(100*round(train_accuracy_regr,3)))
print("Test accuracy for Linear regression:  "+str(100*round(test_accuracy_regr,3)))
# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Use y_predict.round() to get 1 or 0 as the output.
# XXX



# ############################################### Multi Layer Perceptron #################################################
# XXX
# TODO: Create an MLPClassifier and train it.
# XXX
mpcr = MLPClassifier()
mpcr.fit(x_train, y_train)
y_predict_train_mpcr=mpcr.predict(x_train)
y_predict_test_mpcr = mpcr.predict(x_test)
train_accuracy_mpcr=accuracy_score(y_train,y_predict_train_mpcr.round())
test_accuracy_mpcr=accuracy_score(y_test,y_predict_test_mpcr.round())
print("Train accuracy for Multi Layer Perceptron: "+str(100*round(train_accuracy_mpcr,3)))
print("Train accuracy for Multi Layer Perceptron: "+str(100*round(test_accuracy_mpcr,3)))

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX





# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
rfcr=RandomForestClassifier(random_state=100)
rfcr.fit(x_train, y_train)
# XXX

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
y_predict_train_rfcr=rfcr.predict(x_train)
y_predict_test_rfcr = rfcr.predict(x_test)
train_accuracy_rfcr=accuracy_score(y_train,y_predict_train_rfcr.round())
test_accuracy_rfcr=accuracy_score(y_test,y_predict_test_rfcr.round())
print("Training accuracy for Random Forest before tuning: "+str(100*round(train_accuracy_rfcr,3)))
print("Testing accuracy for Random Forest before tuning: "+str(100*round(test_accuracy_rfcr,3)))

# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX


# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
parameters = {'n_estimators':[5,10,50], 'max_depth':[10, 15, 50]}
clf = GridSearchCV(rfcr, parameters, cv=10, refit=True,scoring='accuracy')
clf.fit(x_train, y_train)
print(clf.best_params_)
print("Best score for random forest in grid search: "+str(100*round(clf.best_score_,3)))


maxaccrfc=RandomForestClassifier(n_estimators=50,max_depth=50).fit(x_train,y_train)
max_accuracy_RF=accuracy_score(maxaccrfc.predict(x_test),y_test)
print("Testing accuracy for random forest after tuning: "+str(100*round(max_accuracy_RF,3)))

# XXX


# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# normalizer = Normalizer().fit(x_train)
# x_data=normalize(x_data)
# x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.30,shuffle=True, random_state=1)
# TODO: Create a SVC classifier and train it.
# XXX
x_train=normalize(x_train)
x_test=normalize(x_test)
svcr=SVC(gamma=0.001) 
svcr.fit(x_train, y_train)
y_predict_train_svcr=np.round(svcr.predict(x_train))
y_predict_test_svcr = np.round(svcr.predict(x_test))
train_accuracy_svcr=accuracy_score(y_train,y_predict_train_svcr)
test_accuracy_svcr=accuracy_score(y_test,y_predict_test_svcr)
print("Train accuracy of SVM before tuning "+str(round(100*train_accuracy_svcr,3)))
print("Test accuracy of SVM before tuning "+str(round(100*test_accuracy_svcr,3)))

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX

# XXX
parameters = {'kernel':['rbf','linear'], 'C':[0.0000001,0.0001, 0.01]}
clfs = GridSearchCV(SVC(), parameters, cv=10, return_train_score=True)
clfs.fit(x_train, y_train)
print(clfs.best_params_)
print(clfs.best_score_)


max_index=clfs.cv_results_["params"].index(clfs.best_params_)
print("Mean Test Score: "+str(round(clfs.cv_results_["mean_test_score"][max_index],3)))
print("Mean Train Score: "+str(round(clfs.cv_results_["mean_train_score"][max_index],3)))
print("Mean fit time: "+str(round(clfs.cv_results_["mean_fit_time"][max_index],3)))

maxaccsvm=SVC(C=1e-7,kernel='linear').fit(x_train,y_train)
max_accuracy=accuracy_score(maxaccsvm.predict(x_test),y_test)

print("Test accuracy of SVM after tuning: "+str(100*round(max_accuracy,3)))
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX


