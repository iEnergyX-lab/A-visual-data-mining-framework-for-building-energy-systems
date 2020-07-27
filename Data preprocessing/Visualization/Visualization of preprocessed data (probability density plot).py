"""
Created on Sun Jul 26 11:23:09 2020

@author: Chaobo Zhang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.nonparametric.api as smnp

#Draw a probability density plot of a variable

Data_for_density_estimation = pd.read_csv(open('Test data for probability density plot.csv')) #用来估计核密度曲线
fft = "True"
Feature = "Variable 1"
kde = smnp.KDEUnivariate([float(x) for x in Data_for_density_estimation[Feature]])
outlier_ratio = 50 #Scale factor of the outlier threshold
bw = 1 #Bandwidth 
threshold_of_the_number_of_categories = 5 #Threshold of the number of categories
kde.fit("gau", bw, fft)
x, y = kde.support, kde.density
outlier_threshold = max(y)/outlier_ratio #Threshold of the probability density of outliers

plt.figure(figsize=(13, 6))
plt.xticks(fontproperties='Times New Roman',fontsize=24)
plt.yticks(fontproperties='Times New Roman',fontsize=24)
plt.plot(x, y, 'k', linewidth=1.5)
plt.ylim(-0.01, max(y)*1.1)
plt.xlim(min(x), max(x))

outlier_interval = [[-2.0, -1.0], [11.7, 53.0]]
class_interval = [[-1.0, 2.7], [2.7, 6.1], [6.1, 11.7]]

x1 = np.linspace(min(x) , max(x) , 1000)
y1 = []
for i in range(1000):
    y1.append(max(y)*1.1)
y2 = []
for i in range(1000):
    y2.append(outlier_threshold)
y3 = []
for i in range(1000):
    y3.append(-0.01)

for i in range(len(outlier_interval)):
    plt.fill_between(x1, y2, y3, where = (outlier_interval[i][0]<=x1) & (x1<=outlier_interval[i][1]), facecolor='palegreen', edgecolor = 'palegreen', alpha=0.3)
for i in range(len(class_interval)):
    plt.fill_between(x1, y1, y3, where = (class_interval[i][0]<=x1) & (x1<=class_interval[i][1]), facecolor='navajowhite', alpha=0.3)

for i in range(len(class_interval)):
    plt.axvline(x=class_interval[i][0], ls="-.", c="darkgoldenrod", linewidth=1.5)
    plt.axvline(x=class_interval[i][1], ls="-.", c="darkgoldenrod", linewidth=1.5)
plt.axhline(y = outlier_threshold, ls=":", c="green", linewidth=1.5)

plt.xlabel(Feature+" \n(h=%.2f, α=%.2f, δ2=%.2f)" % (bw, outlier_ratio, threshold_of_the_number_of_categories),fontproperties='Times New Roman',fontsize=24)
plt.ylabel("Density",fontproperties='Times New Roman',fontsize=24)
Proportion_of_outliers = 0.67
plt.text(34, 0.24, 'Proportion of outliers: '+str(Proportion_of_outliers)+"%", fontproperties='Times New Roman',fontsize=23)
plt.text(-1.3, 0.24, "Class 1", fontproperties='Times New Roman', color="chocolate", fontsize=22)
plt.text(2.2, 0.22, "Class 2", fontproperties='Times New Roman', color="chocolate", fontsize=22)
plt.text(6.6, 0.24, "Class 3", fontproperties='Times New Roman', color="chocolate", fontsize=22)
plt.text(27.1, 0.01, "Outliers", fontproperties='Times New Roman', color="forestgreen", fontsize=22)
plt.text(-4, 0.01, "Outliers", fontproperties='Times New Roman', color="forestgreen", fontsize=22)
plt.tight_layout()
plt.savefig('Probability density plot.png', dpi=700, bbox_inches='tight')
plt.show()