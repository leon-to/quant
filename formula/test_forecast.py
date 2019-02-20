import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import forecast
import datetime


from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC, SVC
#create lag series of S&P500
snpret = forecast.create_lagged_series(
        '^GSPC',
        datetime.datetime(2001,1,10),
        datetime.datetime(2005,12,31))

#use prior 2 days of return as predictor values,
#with direction as response
X = snpret[['Lag1', 'Lag2']]
y = snpret['Direction']

#test data is split into 2 parts: before & after 2005,1,1
start_test = datetime.datetime(2005,1,1)

#create training & data set
X_train = X[X.index < start_test]
X_test = X[X.index >= start_test]
y_train = y[y.index < start_test]
y_test = y[y.index >= start_test]

#create parametrised models
models = [('LR', LogisticRegression()),
          ('LDA', LDA()),
          ('QDA', QDA()),
          ('LSVC', LinearSVC()),
          ('RSVM', SVC(
                  C=1000000.0, cache_size=200, class_weight=None,
                  coef0=0.0, degree=3, gamma=0.0001, kernel='rbf',
                  max_iter=-1, probability=False, random_state=None,
                  shrinking=True, tol=0.001, verbose=False)),
          ('RF', RandomForestClassifier(
                  n_estimators=1000, criterion='gini', 
                  max_depth=None, min_samples_split=2,
                  min_samples_leaf=1, max_features='auto',
                  bootstrap=True, oob_score=False, n_jobs=1,
                  random_state=None, verbose=0))
          ]

result = {}
result['Hit Rate'] = {}
result['Confusion Matrix'] = {}
#iterate through models
for m in models:
    #train each model on training set
    m[1].fit(X_train, y_train)
    
    #make an array of predictions on test set
    pred = m[1].predict(X_test)
    
    #output hit rate & confusion matrix
    result['Hit Rate'][m[0]] = m[1].score(X_test, y_test)
    result['Confusion Matrix'][m[0]] = confusion_matrix(pred, y_test)