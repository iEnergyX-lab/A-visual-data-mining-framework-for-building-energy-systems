"""
Created on Sun Jul 26 20:20:41 2020

@author: Chaobo Zhang
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

raw_data = pd.read_csv(open("Test data.csv"))
data_month = {}
data_month["8"] = []
data_month["6,7,9"] = []
data_month["11,12,1,2,3"] = []
data_month["10,4,5"] = []
for i in range(len(raw_data)):
    if raw_data["Month"][i] == "Aug.":
        data_month["8"].append(raw_data["Cooling_load_test"][i])
    if raw_data["Month"][i] == "Jul." or raw_data["Month"][i] == "Jun." or raw_data["Month"][i] == "Sep.":
        data_month["6,7,9"].append(raw_data["Cooling_load_test"][i])
    if raw_data["Month"][i] == "Nov." or raw_data["Month"][i] == "Dec." or raw_data["Month"][i] == "Jan." or raw_data["Month"][i] == "Feb." or raw_data["Month"][i] == "Mar.":
        data_month["11,12,1,2,3"].append(raw_data["Cooling_load_test"][i])    
    if raw_data["Month"][i] == "Oct." or raw_data["Month"][i] == "Apr." or raw_data["Month"][i] == "May":
        data_month["10,4,5"].append(raw_data["Cooling_load_test"][i])    
        
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(211)
plt.tick_params(labelsize=20)  
plt.xticks(fontproperties='Times New Roman',fontsize=20)
plt.yticks(fontproperties='Times New Roman',fontsize=20)
plt.text(46.8, 78, "Month", fontproperties='Times New Roman', color="black", fontsize=24)
plt.text(31.8, 38, "Month", fontproperties='Times New Roman', color="black", fontsize=24)
plt.text(61.8, 38, "Month", fontproperties='Times New Roman', color="black", fontsize=24)

x1 = np.linspace(35, 39, 10)
y1 = (74-48.5)/(47-35)*x1+(48.5-35*(74-48.5)/(47-35))
plt.plot(x1, y1, color="black", linewidth = 1)  
x1 = np.linspace(43, 47, 10)
y1 = (74-48.5)/(47-35)*x1+(48.5-35*(74-48.5)/(47-35))
plt.plot(x1, y1, color="black", linewidth = 1)  
plt.text(35, 58.9, "Jun. to Sep.", fontproperties='Times New Roman', color="black", fontsize=22)

x2 = np.linspace(53, 57, 10)
y2 = (74-48.5)/(53-65)*x2+(48.5-65*(74-48.5)/(53-65))
plt.plot(x2, y2, color="black", linewidth = 1)  
x2 = np.linspace(61, 65, 10)
y2 = (74-48.5)/(53-65)*x2+(48.5-65*(74-48.5)/(53-65))
plt.plot(x2, y2, color="black", linewidth = 1) 
plt.text(50, 58.9, "Jan. to May., Oct. to Dec.", fontproperties='Times New Roman', color="black", fontsize=22)

x3 = np.linspace(7, 18, 10)
y3 = (31.5-0)/(34.5-7)*x3+31.5-34.5*(31.5-0)/(34.5-7)
plt.plot(x3, y3, color="black", linewidth = 1)  
x3 = np.linspace(23.5, 34.5, 10)
y3 = (31.5-0)/(34.5-7)*x3+31.5-34.5*(31.5-0)/(34.5-7)
plt.plot(x3, y3, color="black", linewidth = 1)  
plt.text(19, 14.9, "Aug.", fontproperties='Times New Roman', color="black", fontsize=22)

x4 = np.linspace(34.5, 34.85, 10)
y4 = (31.5-0)/(34.5-35.5)*x4+31.5-34.5*(31.5-0)/(34.5-35.5)
plt.plot(x4, y4, color="black", linewidth = 1)  
x4 = np.linspace(35.13, 35.5, 10)
y4 = (31.5-0)/(34.5-35.5)*x4+31.5-34.5*(31.5-0)/(34.5-35.5)
plt.plot(x4, y4, color="black", linewidth = 1)  
plt.text(28, 14.9, "Jun., Jul., Sep.", fontproperties='Times New Roman', color="black", fontsize=22)

x5 = np.linspace(64, 64.37, 10)
y5 = (31.5-0)/(65-64)*x5+31.5-65*(31.5-0)/(65-64)
plt.plot(x5, y5, color="black", linewidth = 1)  
x5 = np.linspace(64.65, 65, 10)
y5 = (31.5-0)/(65-64)*x5+31.5-65*(31.5-0)/(65-64)
plt.plot(x5, y5, color="black", linewidth = 1)  
plt.text(57, 14.9, "Apr., May, Oct.", fontproperties='Times New Roman', color="black", fontsize=22)

x5 = np.linspace(65, 69.5, 10)
y5 = (31.5-0)/(65-92.5)*x5+31.5-65*(31.5-0)/(65-92.5)
plt.plot(x5, y5, color="black", linewidth = 1)
x5 = np.linspace(82, 92.5, 10)
y5 = (31.5-0)/(65-92.5)*x5+31.5-65*(31.5-0)/(65-92.5)
plt.plot(x5, y5, color="black", linewidth = 1)
plt.text(70, 14.9, "Jan., Feb., Mar.,\n      Nov., Dec.", fontproperties='Times New Roman', color="black", fontsize=22)

ell1 = Ellipse(xy = (50, 80), width = 8.5, height = 17, edgecolor = "black", facecolor= 'white')
ell12 = Ellipse(xy = (35, 40), width = 8.5, height = 17, edgecolor = "black", facecolor= 'white')
ell13 = Ellipse(xy = (65, 40), width = 8.5, height = 17, edgecolor = "black", facecolor= 'white')
ax.add_patch(ell1)
ax.add_patch(ell12)
ax.add_patch(ell13)
plt.ylim(0, 100)
plt.xlim(0, 100)
plt.xticks([]) 
plt.yticks([]) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.tight_layout()

plt.subplot(245)
plt.tick_params(labelsize=20)  
plt.xticks(fontproperties='Times New Roman',fontsize=20)
plt.yticks(fontproperties='Times New Roman',fontsize=20)
plt.ylim(-300, 1800)
sns.violinplot(data = data_month["8"], linewidth = 1, color='navajowhite', inner = None)
plt.xticks([]) 
plt.ylabel("Cooling load (kW)",fontproperties='Times New Roman',fontsize=20)
plt.xlabel("Condition 1",fontproperties='Times New Roman',fontsize=20)
plt.tight_layout()

plt.subplot(246)
plt.tick_params(labelsize=20)  
plt.xticks(fontproperties='Times New Roman',fontsize=20)
plt.yticks(fontproperties='Times New Roman',fontsize=20)
plt.ylim(-300, 1800)
sns.violinplot(data = data_month["6,7,9"], linewidth = 1, color='navajowhite', inner = None)
plt.xticks([]) 
plt.ylabel("Cooling load (kW)",fontproperties='Times New Roman',fontsize=20)
plt.xlabel("Condition 2",fontproperties='Times New Roman',fontsize=20)
plt.tight_layout()

plt.subplot(247)
plt.tick_params(labelsize=20)  
plt.xticks(fontproperties='Times New Roman',fontsize=20)
plt.yticks(fontproperties='Times New Roman',fontsize=20)
plt.ylim(-300, 1800)
sns.violinplot(data = data_month["10,4,5"], linewidth = 1, color='navajowhite', inner = None)
plt.xticks([]) 
plt.ylabel("Cooling load (kW)",fontproperties='Times New Roman',fontsize=20)
plt.xlabel("Condition 3",fontproperties='Times New Roman', weight="bold", fontsize=20)
plt.tight_layout()

plt.subplot(248)
plt.tick_params(labelsize=20)  
plt.xticks(fontproperties='Times New Roman',fontsize=20)
plt.yticks(fontproperties='Times New Roman',fontsize=20)
plt.ylim(-300, 1800)
sns.violinplot(data = data_month["11,12,1,2,3"], linewidth = 1, color='navajowhite', inner = None)
plt.xticks([]) 
plt.ylabel("Cooling load (kW)",fontproperties='Times New Roman',fontsize=20)
plt.xlabel("Condition 4",fontproperties='Times New Roman',fontsize=20)
plt.tight_layout()

plt.subplots_adjust(hspace=0, wspace=1)
plt.savefig('Decision tree.png',dpi=700)
plt.show()