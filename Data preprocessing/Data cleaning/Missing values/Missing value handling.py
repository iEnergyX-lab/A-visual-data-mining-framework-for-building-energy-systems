"""
Created on Sun Jul 26 20:20:41 2020

@author: Chaobo Zhang
"""

import math
import datetime
import pandas as pd

#Fill in missing values using the linear interpolation if they last for a short time. Otherwise, they are deleted.

def MissingValueCleaning(Raw_data, Interpolation_interval, Time_name, Time_series_format):
    """
    Inputs:
    Raw_data: Raw data stored in a DataFrame
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
    Raw_Data = pd.read_csv(open("Test data.csv"))
    Data_without_missing_value = MissingValueCleaning(Raw_Data, 1, "Time", "%Y/%m/%d %H:%M") #Data without missing values
    Data_without_missing_value.to_csv("Data without missing values.csv", index = 0)