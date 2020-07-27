# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 23:33:36 2020

@author: Admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib import colors

#Draw a temporal heat map of the preprocessed data

data = pd.read_csv(open('Test data for temporal heat map.csv'))
heat_map = pd.DataFrame(np.random.rand(12, int(31*24*60/10)))

#Obtain all possible timestamps
T_0 = datetime.datetime.strptime(data["Timestamp_raw"][0], '%Y/%m/%d %H:%M')
T_old = T_0
Time_template = []
Time_template_ = []
for i in range(12):
    Time_month = [T_old]
    Time_month_ = [T_old.strftime('%Y/%m/%d %H:%M')]
    while(T_old.month == i+1):
        T_next = T_old+datetime.timedelta(minutes = 10)
        Time_month.append(T_next)
        Time_month_.append(T_next.strftime('%Y/%m/%d %H:%M'))
        T_old = T_next
    del(Time_month[-1])
    del(Time_month_[-1])
    Time_template.append(Time_month)
    Time_template_.append(Time_month_)

#Obtain timestamps of missing values
Missing_value_with_long_time = [] #Timestamps of missing values with long time
Missing_value_with_short_time = [] #Timestamps of missing values with short time
Time_template_list = []

for i in range(len(Time_template)):
    for j in range(len(Time_template[i])):
        t = Time_template[i][j].strftime('%Y/%m/%d %H:%M')
        Time_template_list.append(t)
t1 = [x for x in list(data["Timestamp_after_deleting_and_filling_in_missing_values"]) if type(x) == str]
t2 = [x for x in list(data["Timestamp_after_deleting_missing_values"]) if type(x) == str]

for i in t1:
    if i not in t2:
        Missing_value_with_short_time.append(i)

t1_ = []
for i in t1:
    t_1 = datetime.datetime.strptime(i, '%Y/%m/%d %H:%M')
    t_2 = t_1.strftime('%Y/%m/%d %H:%M')
    t1_.append(t_2)
for i in Time_template_list:
    if i not in t1_:
        Missing_value_with_long_time.append(i)

Missing_value_with_long_time_transformed = []
Missing_value_with_short_time_transformed = []
for i in Missing_value_with_long_time:
    t_1 = datetime.datetime.strptime(i, '%Y/%m/%d %H:%M')
    t_2 = t_1.strftime('%Y/%m/%d %H:%M')
    Missing_value_with_long_time_transformed.append(t_2)
for i in Missing_value_with_short_time:
    t_1 = datetime.datetime.strptime(i, '%Y/%m/%d %H:%M')
    t_2 = t_1.strftime('%Y/%m/%d %H:%M')
    Missing_value_with_short_time_transformed.append(t_2)

#Obtain timestamps of outliers
Outlier_with_long_time = [] #Timestamps of outliers with long time
Outlier_with_short_time = [] #Timestamps of outliers with short time
t3 = [x for x in list(data["Timestamp_after_deleting_and_filling_in_missing_values_and_deleting_and_fill_in_outliers"]) if type(x) == str] #异常值填充后的日期
t4 = [x for x in list(data["Timestamp_after_deleting_and_filling_in_missing_values_and_deleting_outliers"]) if type(x) == str] #异常值不填充后的日期
for i in t3:
    if i not in t4:
        Outlier_with_short_time.append(i)
for i in t1:
    if i not in t3:
        Outlier_with_long_time.append(i)
        
Outlier_with_long_time_transformed = []
Outlier_with_short_time_transformed = []
for i in Outlier_with_long_time:
    t_1 = datetime.datetime.strptime(i, '%Y/%m/%d %H:%M')
    t_2 = t_1.strftime('%Y/%m/%d %H:%M')
    Outlier_with_long_time_transformed.append(t_2)
for i in Outlier_with_short_time:
    t_1 = datetime.datetime.strptime(i, '%Y/%m/%d %H:%M')
    t_2 = t_1.strftime('%Y/%m/%d %H:%M')
    Outlier_with_short_time_transformed.append(t_2)
    
temporal_matrix = {}
n = 1
for i in range(len(Time_template_)):
    matrix_month = []
    for j in range(len(Time_template_[i])):
        if Time_template_[i][j] in Missing_value_with_short_time_transformed:
            matrix_month.append(4)
        elif Time_template_[i][j] in Missing_value_with_long_time_transformed:
            matrix_month.append(3)
        elif Time_template_[i][j] in Outlier_with_short_time_transformed:
            matrix_month.append(2)
        elif Time_template_[i][j] in Outlier_with_long_time_transformed:
            matrix_month.append(1) 
        else:
            matrix_month.append(0)
    temporal_matrix[n] = matrix_month
    n = n+1

data_quality_map = []
for i in [12,11,10,9,8,7,6,5,4,3,2,1]:
    data_quality_month = []
    for j in range(len(temporal_matrix[i])):
        data_quality_month.append(temporal_matrix[i][j])
    while(len(data_quality_month)<4464):
        data_quality_month.append(np.nan)
    data_quality_map.append(data_quality_month)

plt.figure(figsize=(20, 20*0.5))

plt.text(4960, 1, "Normal values", fontproperties='Times New Roman', color="black", fontsize=24)
plt.text(4960, 3.1, "Outliers\n(Deleted)", fontproperties='Times New Roman', color="black", fontsize=24)
plt.text(4960, 5.5, "Outliers\n(Replaced)", fontproperties='Times New Roman', color="black", fontsize=24)
plt.text(4960, 7.9, "Missing values\n(Deleted)", fontproperties='Times New Roman', color="black", fontsize=24)
plt.text(4960, 10.3, "Missing values\n(Filled in)", fontproperties='Times New Roman', color="black", fontsize=24)

plt.axhline(y=1, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=2, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=3, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=4, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=5, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=6, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=7, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=8, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=9, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=10, ls="-", c="lightgray", linewidth=1)
plt.axhline(y=11, ls="-", c="lightgray", linewidth=1)
for i in range(30):
    plt.axvline(x=(i+1)*144, ls="-", c="lightgray", linewidth=1)

cmap = colors.ListedColormap(['papayawhip',"orchid",'limegreen','orange','cornflowerblue'])
bounds=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
norm = colors.BoundaryNorm(bounds, cmap.N)
heatmap = plt.pcolor(np.array(data_quality_map), cmap=cmap, norm=norm)
plt.colorbar(heatmap, ticks=[])

yticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
ylabels = ["Jan.","Feb.","Mar.","Apr.","May","Jun.","Jul.","Aug.","Sep.","Oct.","Nov.","Dec."]
ylabels.reverse()
plt.yticks(yticks, ylabels, fontproperties='Times New Roman',fontsize=26)
xticks = [144/2+x*2*144 for x in range(16)]
xlabels = ["1st", "3rd", "5th", "7th", "9th", "11th", "13th", "15th", "17th", "19th", "21th", "23th", "25th", "27th", "29th", "31th"]
plt.xticks(xticks, xlabels, fontproperties='Times New Roman',fontsize=26)
plt.xlabel('Date', fontproperties='Times New Roman', fontweight='bold', fontsize=27)
plt.ylabel('Month', fontproperties='Times New Roman', fontweight='bold', fontsize=27)
plt.savefig('Temporal heat map.png', dpi=700, bbox_inches='tight')
plt.show()