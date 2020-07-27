"""
Created on Sun Jul 26 20:20:41 2020

@author: Chaobo Zhang
"""

import pandas as pd
import numpy as np
import statsmodels.nonparametric.api as smnp #A Python module that provides classes and functions for the estimation of many different statistical model:  http://www.statsmodels.org/devel/generated/statsmodels.nonparametric.kde.KDEUnivariate.html
import math
import datetime

#Identify outliers and handle outliers.

def kernel_density_estimation(univariate_dataset, k = "gau", bw = 1):
    kernel = k
    bandwidth = bw
    fft = kernel == "gau"
    kde = smnp.KDEUnivariate(univariate_dataset)
    kde.fit(kernel, bandwidth, fft)
    x, y = kde.support, kde.density
    return x, y

def MissingValueCleaning(Raw_data, Interpolation_interval, Time_name, Time_series_format):
    """
    Inputs:
    Raw_data: Raw data stored in a DataFrame.
    Interpolation_interval: If the interval of a missing value is less than the Interpolation_interval, it would be filled in. Its unit is hour.
    Time_name: Name of the time variable in the raw data.
    Time_series_format: Storage format of time series in the raw data, such as "%Y/%m/%d %H:%M".
    
    Outputs:
    Data: Data without missing values.
    """
    
    Data = Raw_data.copy()
    Features = list(Data.columns)
    Features.remove(Time_name)
    Interpolation(Data, Interpolation_interval, Time_name, Time_series_format) 
    Data.dropna(axis=0, how='any', inplace=True)
    Data.index=range(len(Data.index))
    return Data

def Interpolation(Data, Interpolation_interval, Time_name, Time_series_format):
    Features = list(Data.columns)
    Features.remove(Time_name)
    for i in range(len(Features)):
        for j in range(len(Data[Features[i]])):
            if math.isnan(float(Data[Features[i]][j])):  
                flag = 1
                count = 0
                while(1):
                    if math.isnan(float(Data[Features[i]][j-flag])):
                        flag = flag+1
                        continue
                    else:
                        T_before = datetime.datetime.strptime(Data[Time_name][j-flag], Time_series_format)
                        label_before = j-flag
                        count = count+1
                        break
                flag = 1
                while(1):
                    if j+flag > len(Data[Features[i]])-1:
                        break
                    if math.isnan(float(Data[Features[i]][j+flag])):
                        flag = flag+1
                        continue
                    else:
                        T_after = datetime.datetime.strptime(Data[Time_name][j+flag], Time_series_format)
                        label_after = j+flag
                        count = count+1
                        break
                if count == 2 and T_after-T_before < datetime.timedelta(hours = Interpolation_interval):
                    T_now = datetime.datetime.strptime(Data[Time_name][j], Time_series_format)
                    k = (T_now-T_before)/(T_after-T_before)
                    Data[Features[i]][j] = k*(float(Data[Features[i]][label_after])-float(Data[Features[i]][label_before]))+float(Data[Features[i]][label_before])
                    
if __name__ == '__main__':
    Raw_data = pd.read_csv(open("Test data.csv"))
    Features = list(Raw_data.columns)
    Features.remove("Time")
    Data_with_outliers_ = Raw_data.copy()
    
    for i in Features:
        outlier_ratio = 50 #Scale factor of the outlier threshold
        bw = 1 #Bandwidth 
        kernel = "gau" #Gaussian kernel function
        x, y = kernel_density_estimation(Raw_data[i], bw = bw, k = kernel) #Kernel density estimation
        outlier_threshold = max(y)/outlier_ratio #Threshold of the probability density of outliers
    
        outlier_point = []
        flag = 0
        for j in range(len(y)):
            if j == 0 and y[j] <= outlier_threshold:
                if y[j+1] > outlier_threshold:
                    outlier_point.append([x[j],0,1])
                if y[j+1] < outlier_threshold:
                    outlier_point.append([x[j],0,0])
            if j == len(y)-1 and y[j] <= outlier_threshold:
                if y[j-1] > outlier_threshold:
                    outlier_point.append([x[j],1,0])
                if y[j-1] < outlier_threshold:
                    outlier_point.append([x[j],0,0])  
            if j != 0 and j != len(y)-1 and y[j] <= outlier_threshold:
                if y[j-1] <= outlier_threshold and y[j+1] > outlier_threshold:
                    outlier_point.append([x[j],0,1])   
                if y[j-1] > outlier_threshold and y[j+1] <= outlier_threshold:
                    outlier_point.append([x[j],1,0])
        
        outlier_interval = []
        for j in range(len(outlier_point)-1):
            if outlier_point[j][2] == 0 and outlier_point[j+1][1] == 0:
                outlier_interval.append([outlier_point[j][0], outlier_point[j+1][0]])
        
        for j in range(len(Raw_data[i])):
            for k in range(len(outlier_interval)):
                if outlier_interval[k][0] <= Raw_data[i][j] and Raw_data[i][j] <= outlier_interval[k][1]:
                    Data_with_outliers_[i][j] = np.nan
    
    Data_with_outliers = MissingValueCleaning(Data_with_outliers_, 1, "Time", "%Y/%m/%d %H:%M") #Data without outliers
    Data_with_outliers.to_csv("Data without outliers.csv", index = 0)