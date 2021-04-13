# -*- coding: utf-8 -*-
"""Códigos para examen_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t0ChFwBWyop0KNjHEFB2k3JVRZrrHMbS

#Códigos de la Unidad 1, Inteligencia Artificial

###Autor: Miguel Alejandro López Olvera
###Correo: alexander_105@comunidad.unam.mx

##1.Funciones comunes
"""

from matplotlib import pyplot 
import numpy as np

def f_1(x):
  return (1/(1+np.exp(-x)))
def f_2(x):
  return (np.log(1+np.exp(x)))

x_1 = np.linspace(-10,10) 

#pyplot.plot(x_1,[f_1(i) for i in x_1])
pyplot.plot(x_1,[f_2(i) for i in x_1])

"""## 2. Regresión lineal"""

#Step 1: Importing libraries and dataset
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

df = pd.read_csv("https://raw.githubusercontent.com/ulises1229/IA-2021-II/main/data/iris.csv")
    
#df.head()
"""*The formula for our lineal model is:*

$ \hat{y} =  b_0 + b_1 x$

Where the slope can be understood as follows:

$b1 = \frac{\sum x y  - \frac{(\sum x )(\sum y)}{n} }{\sum x^2 - \frac{(\sum x)^2}{n}} = \frac{S_{xy}}{S_{xx}}$
"""
#Step 2:Definition of a class to graph all the functions we want
class Graph:

    def plotGraph(self, title, xlabel,ylabel):
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
    def plotScatter(self, x, y, label):
        plt.scatter(x,y,label = label)
    def plotFunction(self, rangex,func, color, legend):
        plt.plot(rangex,func, color = color, label = legend)
    def showPlot(self):
        plt.show()

"""Step 3: we define a class that contains the following methods:

       1. Constructor: that contains our variables.
    
       2.Linear regression: main function to make our linear model
    
       3. predict: receives a value on the "x" axis and returns a y value that fits the linear model
    
       4. MSE: here we calculate the mean square error
       
       5. gd_method: gradient descent method to optimize the linear regression method
       """
class Regression:
    def __init__(self, x, y,x_t,y_t):
        self.x = x
        self.y = y
        self.x_t = x_t
        self.y_t = y_t
        self.a = symbols('a')

    """ In this method we are doing a linear regression model"""
    def linearRegression(self):
        """We have to calculate the slope of the regression line"""
        #the first step is to calculate the sum of the square of the differences between x_mean and x  -->SSxx 
        x_mean = self.x.mean()
        diffx = x_mean-self.x
        diffx_squared = diffx**2
        SSxx = diffx_squared.sum()
        #The second step is to calculate SSxy
        y_mean = self.y.mean()
        diffy = y_mean-self.y 
        SSxy = (diffx * diffy).sum()
        #once we have SSxx and SSxy we can calculate the slope just diving one by another following our equation
        b1 = SSxy/SSxx
        #finally, solving for the intercept we obtain:
        b0 = y_mean -b1*x_mean
        equation = b1*self.a+b0
        return (equation, b0, b1)
    """Here we use our linear regression model to predict data """
    def predict(self, value):
        objG = Graph()
        equation, b0, b1 = self.linearRegression()
        y = equation.subs(self.a,value)
        y_predict_1 = b1*self.x+b0 #predicted values  
        y_predict_2 = b1*self.x_t+b0 #predicted values with data for testing 
        #Plotting our model
        objG.plotScatter(self.x,self.y,'Training values')
        mse_1 = self.MSE(self.y, y_predict_1) #minimum squared error
        mse_2 = self.MSE(self.y_t, y_predict_2) #minimum squared error with data for testing
        plt.plot(value, y, color= "green", marker ="*", markersize =10,label ='Predicted value')
        print(" Prediction ")
        print("X: ", value)
        print("Y: ", y)
        print("Mean Squared Error with data for training", mse_1)
        print("Mean Squared Error with data for testing", mse_2)
        print("Mean Squared Error with Sklearn", mean_squared_error(self.y_t, y_predict_2, squared=True))
        return y,b0,b1
    """This method is used to calculate the Mean Square Error"""
    def MSE(self, y, y_predict):
        mse = np.mean((y-y_predict)**2)
        return (mse)
     
    """Steps in gradient descent"""
    #1 initialize betas, learnin rate, max_iter
    #2 for loop that will run n times
    #3 save a variable that holdes the error
    #4 predictions using line equation
    #5 calculate the error and append it to a vector so we can plot after
    #6 calculate partial derivatives for both coefficients
    #7 increase the cost of both coefficients
    #8 update values of the coefficients


# 1.Estimate θ, 2. Compute cost, 3.Tweak θ, #Repeat 2 and 3 until you reach convergence.
    def gd_method(self, alpha):
        #initializing parameters
        equation, b0,b1 = self.linearRegression()
        #we are doing this to see the effects in the error plot
        b0 = 0
        b1 = 1
        max_iter = 100
        error = []
        #begin iteration
        for i in range(max_iter):
            error_cost = 0
            cost_b0 = 0
            cost_b1 = 0
            #calculate cost function
            for j in range(len(self.x)):
                #predict value for actual x
                y_predict = (b0+b1*self.x[j])
                #calculate MSE
                #we are iterating in all predicted values, so we can´t just use MSE
                error_cost = error_cost + (self.y[j]-y_predict)**2  
                
                #get the new theta (b_values) 
                for k in range(len(self.x)):
                    partial_wrt_b0 = -2 * (self.y[k] - (b0 + b1*self.x[k]))#partial derivative with respect to b0
                    partial_wrt_b1 = (-2*self.x[k])*(self.y[k]-(b0+b1*self.x[k]))
                    
                    cost_b0 = cost_b0 + partial_wrt_b0
                    cost_b1 = cost_b1 + partial_wrt_b1
                    
                #updating values(intercept and slope)
                b0 = b0 - alpha*cost_b0
                b1 = b1 - alpha*cost_b1
                
            error.append(error_cost)#the error is append to the vector
        y_predict = b0 + b1*self.x#creating a newvector with predicted values
        objG = Graph()
        plt.plot(self.x, y_predict, label = "Predicted line with GD")
        return error 


#Step 4: Our main function in which we call the classes and methods that we previously defined
def main():
    
    #Data definition, 30%=testing, 70%=training
    wSep = df.Sepal_Width[df.Species == 'setosa']
    lSep = df.Sepal_Length[df.Species == 'setosa']
    N_train = (int)((len(wSep))*0.7)#Number of data to train the model
    x_train = wSep[:N_train]
    x_test = wSep[N_train:]
    y_train = lSep[:N_train]
    y_test = lSep[N_train:]
    # Plot data
    objG = Graph()
    objR = Regression(x_train,y_train,x_test, y_test)
    y,b0,b1 = objR.predict(4)
    #Data for plot the linear regression
    objG.plotGraph('Training a model using linear regression', 'Sepal Width','Sepal Length')
    objG.plotScatter(x_test,y_test, 'Testing Values')
    r = np.linspace(np.min(wSep),np.max(wSep),len(wSep))
    objG.plotFunction(r,b1*r+b0, 'red', 'Linear Regression')
    #printing the results
    print("Total number of data: ", len(wSep))
    print("For training: ", len(x_train))
    print("For testing: ", len(x_test))
    error = objR.gd_method(0.001)
    plt.legend()
    #now we can plot the error that we have obtain with GD
    plt.figure(figsize=(11,6))
    plt.plot(np.arange(1,len(error)+1),error,color='blue',linewidth=2)
    plt.title("Iteration vs Error")
    plt.xlabel("Number of Iteration")
    plt.ylabel("Error")
if __name__ == "__main__":
    main()

"""#### K-FOLDS Cross-validation"""

from sklearn.model_selection import KFold # import KFold
X = np.array([[1, 2], [3, 4], [1, 2], [3, 4]]) # create an array
y = np.array([1, 2, 3, 4]) # Create another array
kf = KFold(n_splits=2) # Define the split - into 2 folds 
kf.get_n_splits(X) # returns the number of splitting iterations in the cross-validator
print(kf) 
KFold(n_splits=2, random_state=None, shuffle=False)
for train_index, test_index in kf.split(X):
  print("TRAIN:", train_index, "TEST:", test_index)
  X_train, X_test = X[train_index], X[test_index]
  y_train, y_test = y[train_index], y[test_index]

#Proporciona índices de entrenamiento / prueba para dividir datos en conjuntos de entrenamiento / prueba.

"""## 3. Naive Bayes"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

from sklearn.datasets import make_blobs#it can be used to generate blobs of points with a Gaussian distribution.
from sklearn.naive_bayes import GaussianNB

def main():
    X, y = make_blobs(100, 2, centers=2, random_state=2, cluster_std=1.5)#random_state-->Using an int will produce the same results across different calls
    print("X\n", X)
    print("Y\n",y)
    
    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='RdBu');
    plt.show()
    model = GaussianNB()
    model.fit(X, y);


    rng = np.random.RandomState(0)
    Xnew = [-6, -14] + [14, 18] * rng.rand(2000, 2)
    ynew = model.predict(Xnew)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='RdBu')
    

    lim = plt.axis()
    plt.scatter(Xnew[:, 0], Xnew[:, 1], c=ynew, s=20, cmap='RdBu', alpha=0.1)
    plt.axis(lim);
    
    yprob = model.predict_proba(Xnew)
    yprob[-8:].round(2)
    plt.show()


if __name__ == "__main__":
    main()

"""##4. Support Vector Machine"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from matplotlib import pyplot as plt
# %matplotlib inline
url = 'https://raw.githubusercontent.com/ulises1229/IA-2021-II/main/data/data.csv'
df = pd.read_csv(url)  # Dataset - Breast Cancer Wisconsin Data
df['diagnosis'] = df['diagnosis'].map({
    'M': 1,
    'B': 2
})  # Label values - 1 for Malignant and 2 for Benign
labels = df['diagnosis'].tolist()
df['Class'] = labels  #Cpying values of diagnosis to newly clreated labels column
df = df.drop(['id', 'Unnamed: 32', 'diagnosis'],
             axis=1)  #Dropping unncessary columns
df.head(50)  #Displaying first five rows of the dataset
target_names = ['', 'M', 'B']
df['attack_type'] = df.Class.apply(lambda x: target_names[x])#new column to know what type of cancer it is
print(len(df))
df.head()
df1 = df[df.Class == 1]
df2 = df[df.Class == 2]
plt.xlabel('radius_mean')
plt.ylabel('texture_mean')
plt.scatter(df1['radius_mean'], df1['texture_mean'], color='green', marker='+')
plt.scatter(df2['radius_mean'], df2['texture_mean'], color='blue', marker='.')
X = df.drop(['Class', 'attack_type'], axis='columns')
X.head()

###SVM
y = df.Class
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print(len(X_train))
print(len(X_test))
model = SVC(kernel='linear')
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("SVM Predictions: \n",predictions)
percentage = model.score(X_test, y_test)
from sklearn.metrics import confusion_matrix
res = confusion_matrix(y_test, predictions)
print("Confusion Matrix")
print(res)
print(f"Test Set: {len(X_test)}")
print(f"Accuracy = {percentage*100} %")

"""## 5. Árboles de decisión"""

# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

col_names = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age', 'label']
# load dataset
pima = pd.read_csv("https://raw.githubusercontent.com/ulises1229/IA-2021-II/main/data/diabetes.csv", header=None, names=col_names)

pima.head(50)
#split dataset in features and target variable
feature_cols = ['pregnant', 'insulin', 'bmi', 'age','glucose','bp','pedigree']
X = pima[feature_cols] # Features
y = pima.label # Target variable
# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test
# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = feature_cols,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('diabetes.png')
Image(graph.create_png())
# Create Decision Tree classifer object
clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True, feature_names = feature_cols,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('diabetes.png')
Image(graph.create_png())

"""##### posible código que funciona"""

###https://www.geeksforgeeks.org/decision-tree-implementation-python/#:~:text=Decision%20tree%20implementation%20using%20Python.%20Decision%20Tree%20is,both%20continuous%20as%20well%20as%20categorical%20output%20variables.
# Run this program on your local python
# interpreter, provided you have installed
# the required libraries.
  
# Importing the required packages
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
  
# Function importing Dataset
def importdata():
    balance_data = pd.read_csv(
'https://archive.ics.uci.edu/ml/machine-learning-'+
'databases/balance-scale/balance-scale.data',
    sep= ',', header = None)
      
    # Printing the dataswet shape
    print ("Dataset Length: ", len(balance_data))
    print ("Dataset Shape: ", balance_data.shape)
      
    # Printing the dataset obseravtions
    print ("Dataset: ",balance_data.head())
    return balance_data
  
# Function to split the dataset
def splitdataset(balance_data):
  
    # Separating the target variable
    X = balance_data.values[:, 1:5]
    Y = balance_data.values[:, 0]
  
    # Splitting the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split( 
    X, Y, test_size = 0.3, random_state = 100)
      
    return X, Y, X_train, X_test, y_train, y_test
      
# Function to perform training with giniIndex.
def train_using_gini(X_train, X_test, y_train):
  
    # Creating the classifier object
    clf_gini = DecisionTreeClassifier(criterion = "gini",
            random_state = 100,max_depth=3, min_samples_leaf=5)
  
    # Performing training
    clf_gini.fit(X_train, y_train)
    return clf_gini
      
# Function to perform training with entropy.
def tarin_using_entropy(X_train, X_test, y_train):
  
    # Decision tree with entropy
    clf_entropy = DecisionTreeClassifier(
            criterion = "entropy", random_state = 100,
            max_depth = 3, min_samples_leaf = 5)
  
    # Performing training
    clf_entropy.fit(X_train, y_train)
    return clf_entropy
  
  
# Function to make predictions
def prediction(X_test, clf_object):
  
    # Predicton on test with giniIndex
    y_pred = clf_object.predict(X_test)
    print("Predicted values:")
    print(y_pred)
    return y_pred
      
# Function to calculate accuracy
def cal_accuracy(y_test, y_pred):
      
    print("Confusion Matrix: ",
        confusion_matrix(y_test, y_pred))
      
    print ("Accuracy : ",
    accuracy_score(y_test,y_pred)*100)
      
    print("Report : ",
    classification_report(y_test, y_pred))
  
# Driver code
def main():
      
    # Building Phase
    data = importdata()
    X, Y, X_train, X_test, y_train, y_test = splitdataset(data)
    clf_gini = train_using_gini(X_train, X_test, y_train)
    clf_entropy = tarin_using_entropy(X_train, X_test, y_train)
      
    # Operational Phase
    print("Results Using Gini Index:")
      
    # Prediction using gini
    y_pred_gini = prediction(X_test, clf_gini)
    cal_accuracy(y_test, y_pred_gini)
      
    print("Results Using Entropy:")
    # Prediction using entropy
    y_pred_entropy = prediction(X_test, clf_entropy)
    cal_accuracy(y_test, y_pred_entropy)
      
      
# Calling main function
if __name__=="__main__":
    main()

"""## 6. K-Means"""

#Libraries
import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import math
import pylab as plt
import pandas_datareader as dr  
from scipy.cluster.vq import kmeans, vq
from time import time 

#Import data
prices_df = pd.read_csv('/content/stockPrices.csv')
prices_new = pd.read_csv('/content/stockPrices.csv')
prices_new.pop('Date')



class KMeansAlgo:
  
  #******************************Implementation of the K-Means Algorithm from Scratch***************************************
  #******************************************************************************************************************
  def KMeans_implementation(self,X, column_1, column_2, k):
    start_time = time()
    #################### Step 1, n_clusters,. predefined####################################
    ######################################################################################
    ####################### Step 2, select centroids#############################
    ######################################################################################3
    Centroids = (X.sample(n=k))#random centroids 

    ################### Step 3, each point to the closest centroid##########################
    #######################################################################################
    diff = 1 #variable to store the distance between centroids in the previous and the actual iteration
    j = 0 #label to validate diff in the first iteration
    print("******************************************************************************************")
    print("\n\n\nK-Means Implementation from Scratch")
    print("\nDistance from old centroids to new Centroids")
    while(diff != 0 ): #condition to stop
      X_1 = X #we will modificate X so we have to save another variable with exactly the same value
      i = 1 #centroid position
      for index1,row_1 in Centroids.iterrows(): #saving indexes and values(x and y axis) of Centroids, iterating on each centroid
        cent_dist = [] #here we will save the value of the distances from each point to each centroid so we can compare later
        for index2,row_2 in X_1.iterrows():#now we iterate on each point
          dist_1 = (row_1[column_1] - row_2[column_1])**2 #we have to put the desired column here
          dist_2 = (row_1[column_2]-row_2[column_2])**2#next column
          distance = np.sqrt(dist_1 + dist_2)#pitagoras
          cent_dist.append(distance)#saving the vector of distances
        X[i] = cent_dist  #add a column of distances to each centroid
        i+=1 #change of centroid

      best_cluster = [] 
      for index, row in X.iterrows(): #now we can iterate the distances to each centroid
        min_dist = row[1] #initializing minimum distance 
        pos = 1
        #compare the distances and update
        for i in range(k):
          if(row[i+1] < min_dist):#it's i+1 because the row index is at 1
            min_dist = row[i+1]
            pos = i+1
        best_cluster.append(pos) #here we save the value(number of cluster) with the closest centroid to the point
      X["Cluster"] = best_cluster

      #########################Step 4.	Recompute the centroids of newly formed clusters.#############
      ##############################################################################################
      updated_Centroid = X.groupby(["Cluster"]).mean()[[column_1, column_2]]
      if(j==0):#first iteration
        diff = 1
        j+=1
      else:
        diff = (updated_Centroid[column_1]-Centroids[column_1]).sum()+(updated_Centroid[column_2]-Centroids[column_2]).sum()
        print(diff.sum())
      Centroids = X.groupby("Cluster").mean()[[column_1,column_2]]
    print("\nCentroids: \n", updated_Centroid)
    print("Elapsed Time: \n", time()-start_time)
    return Centroids 

  ####################Plot K-Means Implementation##############################################
  def plot(self, Centroids,k,X, column_1, column_2):
    fig = plt.figure(figsize=(13,8))
    #Centroids = KMeans_implementation()
    color = ['brown','gray','black','cyan','violet','gold']
    for clust in range(k):#iterate in each cluster
      nCluster = X[X["Cluster"] == clust+1]#number of cluster
      plt.scatter(nCluster[column_1],nCluster[column_2],c = color[clust])
    plt.scatter(Centroids[column_1], Centroids[column_2],s=100, c = 'red', marker="*")
    plt.title("K-Means Algorithm From Scratch")
    plt.xlabel(column_1)
    plt.ylabel(column_2)
    plt.show()
    #fig.savefig('img_1.jpg', bbox_inches='tight', dpi=300)
  #******************Plotting the Elbow Curve to Choose The number of Clusters***************************************
  #******************************************************************************************************************
  def elbow_Curve(self):
    #average annual percentage return and volatilities
    ret_vol = prices_new.pct_change().mean()*252 #annual return --> mean= (sum of all values)/(total of values)
                                                 
    print("Original Data Extracted from the Web\n \n", prices_df, "\n\n")
    print("Percentage Change Between the Current and a Prior Element for each Stock\n\n", prices_new.pct_change()*100, "\n\n")
    print("Annual Return")    
    print("There are 253 days of negociation")
    print("So we have 252 data to calculate the Annual Return for each Stock")    
    print(ret_vol, "\n\n")
    ret_vol = pd.DataFrame(ret_vol) #convert to dataframe
    ret_vol.columns = ["Returns"]#set the name of the column 
    #The calculation of historical volatility in the stock market is summarized as the standard deviation of the historical variations in an asset 
    ret_vol['Volatility'] = prices_new.pct_change().std()*math.sqrt(252) #risk=volatility
                                                                        #we can measure the volatility with the standard deviation
    print("Volatility:")    
    print("The calculation of historical volatility in the stock market \nis calculated using the standard deviation of the historical variations of an asset. ")                                                                     
    print("The risk is directly related to the volatility\n")
    print(prices_new.pct_change().std()*math.sqrt(252))
    #convert the data as an array to use it into the KMeans_with_scikitlearn function
    data = np.asarray([np.asarray(ret_vol["Returns"]), np.asarray(ret_vol["Volatility"])]).T #Transpose of the new array containing the 
                                                                                             # Returns and Volatility variables (vector of two columns)
    x = data #(n_samples, n_features)--> 502 x 2 in this case
    SSE = []
    total_clusters = np.arange(2,25)
    for cluster_num in total_clusters:
      k_means = KMeans(n_clusters=cluster_num)
      k_means.fit(x)
      inertia = k_means.inertia_
      SSE.append(inertia)

    fig_1 = plt.figure(figsize=(12,12))
    plt.subplot(2,1,1)
    plt.plot(total_clusters, SSE)
    plt.grid(True)
    plt.title("Elbow Curve")
    plt.xlabel("No. of Clusters")
    plt.ylabel("Sum Squared Error (SSE)")
    print("\n\nWe can see that the optimal number of clusters is between 4 and 6, let's choose 5")
    return data, ret_vol,fig_1
  #********************Implementation of the K-Means Algorithm Using the Scikit Learn Package***************************************
  #******************************************************************************************************************
  def KMeans_with_scikitlearn(self, clusters, dat,fig_1):
    start_time = time()
    centroids, dist = kmeans(dat, clusters)#k-means with  vectors in data and K clusters 
    index, distances= vq(dat, centroids)#returns the index for each observation and the distance between the observation
                            #and its nearest centroid
    print("Elapsed Time: \n", time()-start_time)
    plt.subplot(2,1,2)
    plt.plot(dat[index==0,0], dat[index==0,1], 'ok',
             dat[index==1,0], dat[index==1,1], 'ob',
             dat[index==2,0], dat[index==2,1], 'og',
             dat[index==3,0], dat[index==3,1], 'oy',
             dat[index==4,0], dat[index==4,1], 'oc', markersize = 6)
    plt.plot(centroids[:,0],centroids[:,1],'*r',markersize=8)
    plt.title("K-Means Algorithm Using Scikit-Learn")
    plt.xlabel("Returns")#mean of the percentage change between the current and a prior element*200
    plt.ylabel("Volatility")
    plt.show()
    #fig_1.savefig('img_2.jpg', bbox_inches='tight', dpi=300)
    print("Centroids:\n", centroids)
    print("Data: \n", dat)
    print(len(dat))

def main():
  #class as an object
  km = KMeansAlgo()
  #
  dat,ret_vol,fig_1 = km.elbow_Curve()
  clusters = 5 #we choose 5 as the number of clusters based on the elbow curve method
  km.KMeans_with_scikitlearn(clusters, dat,fig_1)
  X = ret_vol[["Returns", "Volatility"]]
  X = pd.DataFrame(X)
  Centroids = km.KMeans_implementation(X, "Returns", "Volatility", clusters)
  km.plot(Centroids,clusters,X, "Returns", "Volatility")
if __name__=="__main__": 
  main()

"""####Another exampple using a dataset to cluster people by income vs loan amount"""

#Import libraries

import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
#loading dataset
data = pd.read_csv("clustering.csv")
X = data[["LoanAmount", "ApplicantIncome"]]#taking variables from the dataset
# STEP 1: NUMBER OF CLUSTERS
k = 3
#STEP 2: SELECT RANDOM K-POINTS FROM THE DATA AS CENTROIDS
Centroids = (X.sample(n=k))#random centroids from the data
#visualizing datapoints
plt.scatter(X["ApplicantIncome"], X["LoanAmount"], c = 'black')
plt.scatter(Centroids["ApplicantIncome"], Centroids["LoanAmount"], c ='red')
plt.xlabel("Annual Income")
plt.ylabel("Loan Amount")
plt.show()
#STEP 3: ASSIGN ALL THE POINTS TO THE CLOSEST CENTROID
diff = 1
j = 0

while(diff!=0):
    XD = X
    i=1
    for index1,row_c in Centroids.iterrows():
        ED=[]
        for index2,row_d in XD.iterrows():
            d1 = (row_c["ApplicantIncome"]-row_d["ApplicantIncome"])**2#distance between centroid and point (x axis)
            d2 = (row_c["LoanAmount"]-row_d["LoanAmount"])**2  #distance between centroid and point (y axis )
            d = np.sqrt(d1+d2)  #Pitagoras theorem
            ED.append(d)  #vector that contains distances for all points given one centroid
        X[i]=ED #now x will contain also the distances from each points to each centroids
        i+=1
    
    C= [] #vector to store the number of the cluster for each point

    #we have to iterate on each point
    for index,row in X.iterrows():#row will contains the loan amount, aplicant income, and the distances from one point to each centroid
        min_dist = row[1] #initializing minimum distance equal to the first distance
        pos = 1 
        #now we have to compare the distances between one point and each centroid
        for i in range(k): #iterate on each cluster
            if row[i+1] < min_dist:
                min_dist = row[i+1] #updating minimum distance
                pos = i+1 #variable to store the position (cluster) of each point given each centroid
        C.append(pos)
    X["Cluster"] = C #append in X the number or the cluster for each point 
    Centroids_new = X.groupby(["Cluster"]).mean()[["LoanAmount","ApplicantIncome"]]
    if j==0: #if we don't do this we could obtain diff=0 in the first step and end the while loop
        diff=1
        j+=1
    else:
        #diff must be equal to the difference between the centroids in the previous and actual iteration
        diff = (Centroids_new["LoanAmount"] - Centroids["LoanAmount"]).sum()+ (Centroids_new["ApplicantIncome"]-Centroids["ApplicantIncome"]).sum()
        print(diff.sum())
    Centroids = X.groupby(["Cluster"]).mean()[["LoanAmount", "ApplicantIncome"]]#updating centroids


#VISUALIZING THE CLUSTERS
color = ['brown','gray', 'black']
for m in range(k): #we have to iterate in each cluster and save the points here
    data = X[X["Cluster"]==m+1] #saving by number of cluster
    plt.scatter(data["ApplicantIncome"], data["LoanAmount"], c=color[m])
plt.scatter(Centroids["ApplicantIncome"], Centroids["LoanAmount"], c = "red")
plt.xlabel("Income")
plt.ylabel("Loan Amount")
plt.show()  

#DOING THE SAME BUT WITH SCIKIT-LEARN
from sklearn.cluster import KMeans
data = pd.read_csv("clustering.csv")
X = data[["ApplicantIncome", "LoanAmount"]]#taking variables from the dataset
X.describe()
#we can standardizing the data to obtain a less difference of magnitude in std
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled =X
pd.DataFrame(X_scaled).describe()
#function of k-means with k-means++ initialization
kmeans = KMeans(n_clusters=1, init='k-means++')#fitting the k-means algorithm
kmeans.fit(X_scaled)#fitting the k-means algorithm
#We are using k-means++ to obtain better results
#Now lets evaluate the clusters with the inertia value
kmeans.inertia_
#we have only one cluster, so we have a high value of inertia
#lets iterate from 1 to 8 to obtain diferent value of inertia
SSE=[]
for cluster in range(1,20):
    kmeans = KMeans(n_clusters=cluster, init='k-means++')
    kmeans.fit(X_scaled)
    SSE.append(kmeans.inertia_)#append the inertia value for each cluster
frame = pd.DataFrame({'Cluster':range(1,20), 'SSE':SSE})#converting data into a dataframe to plot
plt.figure(figsize=(12,6))
plt.plot(frame['Cluster'], frame['SSE'], marker='o')
plt.xlabel('No. of Clusters')
plt.ylabel('Inertia')
plt.show()
#In this case we can choose from 3 to 5 
#lets choose 4
clusters=4
kmeans = KMeans(n_clusters=clusters, init='k-means++')
kmeans.fit(X_scaled)
pred = kmeans.predict(X_scaled)
X_scaled = pd.DataFrame(X_scaled)
X_scaled["Cluster"] = pred
centroids = kmeans.cluster_centers_
X_scaled.head()
color = ['brown','gray', 'cyan','gold','green']
for m in range(clusters): #we have to iterate in each cluster and save the points here
    data = X_scaled[X_scaled["Cluster"]==m] #saving by number of cluster
    plt.scatter(data["ApplicantIncome"], data["LoanAmount"], c=color[m])
plt.scatter(centroids[:,0], centroids[:,1], c='black')
plt.xlabel("Income")
plt.ylabel("Loan Amount")
plt.show()

"""## 7. Expectation Maximization"""

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
import pandas as pd
import numpy as np 
from sklearn.metrics import accuracy_score

data = datasets.load_iris()
 
x = pd.DataFrame(data.data)
x.columns=["Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width"]

y=pd.DataFrame(data.target)
y.columns = ["Targets"]

#K Means 
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(x)


from scipy.stats import mode
labels = np.zeros_like(clusters)

for i in range(3):
    cat = (clusters == i)
    labels[cat]=mode(data.target[cat])[0]

acc = accuracy_score(data.target, labels)
print("Accuracy = ", acc)

plt.figure(figsize=(10,10))
colormap = np.array(["blue","red","green"])


plt.subplot(2, 2,1)
plt.scatter(x.Petal_Length, x.Petal_Width, c = colormap[labels], s = 40)
plt.title("Real clusters")
plt.xlabel("Petal Length")
plt.ylabel("Petal Width")

plt.subplot(2,2,2)
plt.scatter(x.Petal_Length, x.Petal_Width,c = colormap[labels], s = 40)
plt.title("KMeans Clusters")
plt.xlabel("Petal Length")
plt.ylabel("Petal Width")

"""Now Expectation Maximization"""
from sklearn import preprocessing

scaler = preprocessing.StandardScaler()
scaler.fit(x)

scaled_x = scaler.transform(x)

xs = pd.DataFrame(scaled_x,columns = x.columns)

from sklearn.mixture import GaussianMixture

gmm = GaussianMixture(n_components=3)
gmm_y = gmm.fit_predict(xs)

labels = np.zeros_like(clusters)

for i in range(3):
    cat = (gmm_y == i)
    labels[cat] = mode(data.target[cat])[0]
    
acc = accuracy_score(data.target, labels)
print("Accuracy with GMM ", acc)

plt.subplot(2,2,3)
plt.scatter(x.Petal_Length, x.Petal_Width, c = colormap[gmm_y], s=40)
plt.title("GMM Clusters")
plt.xlabel("Petal Length")
plt.ylabel("Petal Width")

plt.show()
help(scaler.fit)