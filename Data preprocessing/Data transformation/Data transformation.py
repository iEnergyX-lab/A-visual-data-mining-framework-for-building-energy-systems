# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:10:29 2020

@author: Chaobo Zhang
"""

import numpy as np
import statsmodels.nonparametric.api as smnp #A Python module that provides classes and functions for the estimation of many different statistical model:  http://www.statsmodels.org/devel/generated/statsmodels.nonparametric.kde.KDEUnivariate.html
import pandas as pd
import copy

#Transform numerical data into categorical data

def DataTransformation(Numerical_data, Time_name, Outlier_ratio = 50, bw = 1, kernel = "gau", threshold_of_the_number_of_categories = 5):
    """
    Inputs:
    Numerical_data: Numerical data stored in a DataFrame.
    Time_name: Name of the time variable in the numerical data.
    Outlier_ratio: Scale factor of the outlier threshold.
    bw: Bandwidth.
    kernel: Kernel function.
    threshold_of_the_number_of_categories: Threshold of the number of categories.
    
    Outputs:
    Categorical_data: Categorical data.
    """
    
    Features = list(Numerical_data.keys())
    Features.remove(Time_name)
    Categorical_data = copy.deepcopy(Numerical_data)
    for feature in Features:
#####################Kernel density estimation#####################
        fft = "True"
        kde = smnp.KDEUnivariate([float(x) for x in Numerical_data[feature]])
        kde.fit(kernel, bw, fft)
        x, y = kde.support, kde.density

#####################Initial data classification#####################
        outlier_threshold = max(y)/Outlier_ratio #Threshold of the probability density of outliers
        
        #Obtain valley values
        valley_values = []
        for i in range(len(y)):
            if i == 0:
                if y[i] >= outlier_threshold and y[i] < y[i+1]:
                    valley_values.append(i)
            elif i == len(y)-1:
                if y[i] >= outlier_threshold and y[i] < y[i-1]:
                    valley_values.append(i)
            else:
                if y[i] >= outlier_threshold and y[i] < y[i-1] and y[i] < y[i+1]:
                    valley_values.append(i)
                if y[i] >= outlier_threshold and y[i] < y[i-1] and y[i+1] < outlier_threshold:
                    valley_values.append(i)
                if y[i] >= outlier_threshold and y[i] < y[i+1] and y[i-1] < outlier_threshold:
                    valley_values.append(i)
        
        #Obtain valley values
        peak_values = []
        for i in range(len(y)):
            if i == 0:
                if y[i] >= outlier_threshold and y[i] > y[i+1]:
                    peak_values.append(i)
            elif i == len(y)-1:
                if y[i] >= outlier_threshold and y[i] > y[i-1]:
                    peak_values.append(i)
            else:
                if y[i] >= outlier_threshold and y[i] > y[i-1] and y[i] > y[i+1]:
                    peak_values.append(i)
        
        #Obtain intervals of categories
        Intervals_of_categories = []
        for i in peak_values:
            if i == 0:
                valley = [x for x in valley_values if x > i]
                Intervals_of_categories.append([i, i, valley[0]])
            elif i == len(y)-1:
                valley = [x for x in valley_values if x < i]
                Intervals_of_categories.append([valley[-1], i, i])
            else:
                left_valley = [x for x in valley_values if x < i]
                right_valley = [x for x in valley_values if x > i]
                Intervals_of_categories.append([left_valley[-1], i, right_valley[0]])

#####################Merge categories if it is necessary#####################
        while(len(Intervals_of_categories) > threshold_of_the_number_of_categories):
            number_of_categories_old = len(Intervals_of_categories)
            minimum_interval_size = np.inf
            for i in range(len(Intervals_of_categories)):
                if x[Intervals_of_categories[i][2]]-x[Intervals_of_categories[i][0]] < minimum_interval_size:
                    if i == 0 and Intervals_of_categories[i][2] == Intervals_of_categories[i+1][0]:
                        minimum_interval_size = x[Intervals_of_categories[i][2]]-x[Intervals_of_categories[i][0]]
                        category_to_be_merged = i
                    if i == len(Intervals_of_categories)-1 and Intervals_of_categories[i-1][2] == Intervals_of_categories[i][0]:
                        minimum_interval_size = x[Intervals_of_categories[i][2]]-x[Intervals_of_categories[i][0]]
                        category_to_be_merged = i
                    if i != 0 and i != len(Intervals_of_categories)-1:
                        if Intervals_of_categories[i-1][2] == Intervals_of_categories[i][0] or Intervals_of_categories[i][2] == Intervals_of_categories[i+1][0]:
                            minimum_interval_size = x[Intervals_of_categories[i][2]]-x[Intervals_of_categories[i][0]]
                            category_to_be_merged = i
            
            if category_to_be_merged == 0:
                if y[Intervals_of_categories[category_to_be_merged][1]] > y[Intervals_of_categories[category_to_be_merged+1][1]]:
                    Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged][0], Intervals_of_categories[category_to_be_merged][1], Intervals_of_categories[category_to_be_merged+1][2]]
                else:
                    Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged][0], Intervals_of_categories[category_to_be_merged+1][1], Intervals_of_categories[category_to_be_merged+1][2]]
                del Intervals_of_categories[category_to_be_merged+1]
            elif category_to_be_merged == len(Intervals_of_categories)-1:
                if y[Intervals_of_categories[category_to_be_merged][1]] > y[Intervals_of_categories[category_to_be_merged-1][1]]:
                    Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged-1][0], Intervals_of_categories[category_to_be_merged][1], Intervals_of_categories[category_to_be_merged][2]]
                else:
                    Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged-1][0], Intervals_of_categories[category_to_be_merged-1][1], Intervals_of_categories[category_to_be_merged][2]]
                del Intervals_of_categories[category_to_be_merged-1]     
            else:
                left_consistency_index = y[Intervals_of_categories[category_to_be_merged][1]] - y[Intervals_of_categories[category_to_be_merged][0]]
                right_consistency_index = y[Intervals_of_categories[category_to_be_merged][2]] - y[Intervals_of_categories[category_to_be_merged][1]]
                if left_consistency_index < right_consistency_index:
                    if y[Intervals_of_categories[category_to_be_merged][1]] > y[Intervals_of_categories[category_to_be_merged-1][1]]:
                        Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged-1][0], Intervals_of_categories[category_to_be_merged][1], Intervals_of_categories[category_to_be_merged][2]]
                    else:
                        Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged-1][0], Intervals_of_categories[category_to_be_merged-1][1], Intervals_of_categories[category_to_be_merged][2]]
                    del Intervals_of_categories[category_to_be_merged-1]  
                if left_consistency_index > right_consistency_index:
                    if y[Intervals_of_categories[category_to_be_merged][1]] > y[Intervals_of_categories[category_to_be_merged+1][1]]:
                        Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged][0], Intervals_of_categories[category_to_be_merged][1], Intervals_of_categories[category_to_be_merged+1][2]]
                    else:
                        Intervals_of_categories[category_to_be_merged] = [Intervals_of_categories[category_to_be_merged][0], Intervals_of_categories[category_to_be_merged+1][1], Intervals_of_categories[category_to_be_merged+1][2]]
                    del Intervals_of_categories[category_to_be_merged+1]         
            
            if len(Intervals_of_categories) == number_of_categories_old:
                print("Error: This variable cannot be merged")
        
#####################Data transformation according to categories#####################
        Variable_ = []
        for i in range(len(Numerical_data[feature])):
            flag = 0
            for j in range(len(Intervals_of_categories)):
                if x[Intervals_of_categories[j][0]] <= Numerical_data[feature][i] and x[Intervals_of_categories[j][2]] >= Numerical_data[feature][i]:
                    Variable_.append(feature + ": " + str(round(x[Intervals_of_categories[j][0]],2))+ "-" + str(round(x[Intervals_of_categories[j][2]],2)))
                    flag = 1
                    break
            if flag == 0:
                Variable_.append(np.nan)
        Categorical_data[feature] = Variable_
    
    return Categorical_data

if __name__ == '__main__':
    Raw_data = pd.read_csv(open("Test data.csv"))
    Time_name = "Time"
    Outlier_ratio = 50
    bw = 1
    kernel = "gau"
    threshold_of_the_number_of_categories = 5
    Categorical_data = DataTransformation(Raw_data, Time_name, Outlier_ratio, bw, kernel, threshold_of_the_number_of_categories)
    Categorical_data.to_csv("Categorical data.csv", index = 0)