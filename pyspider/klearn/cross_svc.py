#coding=utf-8
from sklearn.svm import SVC  
from sklearn import grid_search  
import numpy as np   
from sklearn import cross_validation as cs  
from sklearn.externals import joblib  
import warnings  
import time  
import os  
  
def load_data():  
    dataset = np.loadtxt(os.path.join(os.getcwd(), 'pyspider/klearn/traindata/train_data.txt'), delimiter=',')  
    return dataset  
      
  
# 交叉验证  
def cross_validation():  
    dataset = load_data()  
    row,col = dataset.shape  
    X = dataset[:,:col-1]  
    Y = dataset[:,-1]  
    #X表示train_data  训练数据
    #Y表示train_target  训练结果
    #clf为分类器 kernel表示核函数
    clf = SVC(kernel='rbf',C=1000)  
    #对结果进行训练
    clf.fit(X,Y)  
    #对训练结果进行交叉验证
    scores = cs.cross_val_score(clf,X,Y,cv=5)  
    print "Accuracy: %0.2f (+- %0.2f)" % (scores.mean(),scores.std())  
      
    return clf  
  
def searchBestParameter():  
    parameters = {'kernel':('linear','poly','rbf','sigmoid'),'C':[1,100]}  
      
    dataset = load_data()  
    row,col = dataset.shape  
    X = dataset[:,:col-1]  
    Y = dataset[:,-1]  
    svr = SVC()  
    clf = grid_search.GridSearchCV(svr,parameters)  
    clf.fit(X,Y)  
      
    print clf.best_params_  
