"""
Created on Sun Jul 26 11:23:09 2020

@author: Chaobo Zhang
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from numpy import array
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.patches import Ellipse
from matplotlib.pyplot import MultipleLocator
from matplotlib import colors

plt.figure(figsize=(15, 10))

########################Visualize the maximal frequent subgraph########################
gs = gridspec.GridSpec(20, 3)
ax = plt.subplot(gs[:, 0:2])
Support = 22.03 #Support of the maximal frequent subgraph
#Nodes of the maximal frequent subgraph
node = {0: 'CH1-8', 1: 'COWP1-10', 2: 'CT1-20', 3: 'PCHWP1-10', 4: 'WDH', 5: 'A zone', 6: 'B zone', 7: 'C zone', 8: 'D zone', 9: 'WCH', 
        11: 'N${_\\mathregular{COWP}}$:\n2', 12: 'N${_\\mathregular{PCHWP}}$:\n1', 13: 'N${_\\mathregular{CH}}$:\n2', 
        21: 'P${_\\mathregular{CH}}$:\n348.1-1269.4kW', 22: 'P${_\\mathregular{COWP}}$:\n110.9-181.8kW', 23: 'P${_\\mathregular{PCHWP}}$:\n6.7-40.7kW'}
#Position of nodes of the maximal frequent subgraph
pos_node = {'A zone': array([ 0.3, -0.3]), 'B zone': array([ 0.5, -0.3]), 'C zone': array([ 0.7, -0.3]), 'CH1-8': array([-0.3,  0. ]), 'COWP1-10': array([-0.75, -0.25]),
            'CT1-20': array([-0.75,  0.25]), 'D zone': array([ 0.9, -0.3]), 'N${_\\mathregular{CH}}$:\n2': array([-0.6,  0. ]), 'N${_\\mathregular{COWP}}$:\n2': array([-1.05, -0.25]), 
            'N${_\\mathregular{PCHWP}}$:\n1': array([-0.15,  0.25]), 'P${_\\mathregular{CH}}$:\n348.1-1269.4kW': array([0., 0.]), 'P${_\\mathregular{COWP}}$:\n110.9-181.8kW': array([-0.75, -0.55]),
            'P${_\\mathregular{PCHWP}}$:\n6.7-40.7kW': array([0.15, 0.55]), 'PCHWP1-10': array([0.15, 0.25]), 'WCH': array([ 0.6, -0.6]), 'WDH': array([0.6, 0. ])}
#Color of nodes of the maximal frequent subgraph
node_color_ = ['bisque', 'bisque', 'bisque', 'bisque', 'bisque', 'bisque', 'bisque', 'bisque', 'bisque', 'bisque', 
               'paleturquoise', 'paleturquoise', 'paleturquoise', 'paleturquoise', 'paleturquoise', 'paleturquoise']
#Edges of the maximal frequent subgraph
edge = {(0, 1): ('CH1-8', 'COWP1-10'), (0, 2): ('CH1-8', 'CT1-20'), (0, 3): ('CH1-8', 'PCHWP1-10'), (0, 9): ('CH1-8', 'WCH'), (0, 13): ('CH1-8', 'N${_\\mathregular{CH}}$:\n2'),
        (0, 21): ('CH1-8', 'P${_\\mathregular{CH}}$:\n348.1-1269.4kW'), (1, 0): ('COWP1-10', 'CH1-8'), (1, 2): ('COWP1-10', 'CT1-20'), (1, 11): ('COWP1-10', 'N${_\\mathregular{COWP}}$:\n2'),
        (1, 22): ('COWP1-10', 'P${_\\mathregular{COWP}}$:\n110.9-181.8kW'), (2, 0): ('CT1-20', 'CH1-8'), (2, 1): ('CT1-20', 'COWP1-10'), (3, 0): ('PCHWP1-10', 'CH1-8'),
        (3, 4): ('PCHWP1-10', 'WDH'), (3, 12): ('PCHWP1-10', 'N${_\\mathregular{PCHWP}}$:\n1'), (3, 23): ('PCHWP1-10', 'P${_\\mathregular{PCHWP}}$:\n6.7-40.7kW'),
        (4, 3): ('WDH', 'PCHWP1-10'), (4, 5): ('WDH', 'A zone'), (4, 6): ('WDH', 'B zone'), (4, 7): ('WDH', 'C zone'), (4, 8): ('WDH', 'D zone'), (5, 4): ('A zone', 'WDH'),
        (5, 9): ('A zone', 'WCH'), (6, 4): ('B zone', 'WDH'), (6, 9): ('B zone', 'WCH'), (7, 4): ('C zone', 'WDH'), (7, 9): ('C zone', 'WCH'), (8, 4): ('D zone', 'WDH'),
        (8, 9): ('D zone', 'WCH'), (9, 0): ('WCH', 'CH1-8'), (9, 5): ('WCH', 'A zone'), (9, 6): ('WCH', 'B zone'), (9, 7): ('WCH', 'C zone'), (9, 8): ('WCH', 'D zone')}

#Draw the maximal frequent subgraph
G=nx.DiGraph()
G.add_nodes_from(list(node.values()))
G.add_edges_from(list(edge.values()))
nx.draw_networkx(G, pos = pos_node, with_labels=True, edge_color='black', alpha=1, font_size=14, node_size=2000, node_color=node_color_, font_family='Times New Roman')

#Legends of the maximal frequent subgraph
cir1 = Ellipse(xy = (-1, 0.6), width = 0.1, height = 0.058, color='bisque')
ax.add_patch(cir1)
cir2 = Ellipse(xy = (-1, 0.5), width = 0.1, height = 0.058, color='paleturquoise')
ax.add_patch(cir2)
plt.text(-0.9, 0.59, "A device", fontproperties='Times New Roman', color="black", fontsize=16)
plt.text(-0.9, 0.49, "A measured variable", fontproperties='Times New Roman', color="black", fontsize=16)
plt.text(0.5, 0.5, "Support: "+str(Support)+"%", fontproperties='Times New Roman', color="black", fontsize=16)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.tight_layout() 

########################Visualize the temporal distribution of the maximal frequent subgraph########################
Month = {1: 367, 2: 353, 3: 626, 11: 0, 12: 0}
Hour = {0: 234, 1: 230, 2: 220, 3: 212, 4: 186, 5: 135, 6: 16, 7: 0, 20: 0, 21: 0, 22: 0, 23: 113}
Day_type = {1: 181, 2: 209, 3: 255, 4: 351, 5: 350}

ax = plt.subplot(gs[0:5,2])
plt.bar(np.arange(len(list(Month.keys()))), Month.values(), width = 0.5, color="gold")
plt.xlabel("Month",fontproperties='Times New Roman',fontsize=16)
plt.ylabel("Frequency",fontproperties='Times New Roman',fontsize=16)  
plt.xticks(np.arange(len(list(Month.keys()))), [1,2,3,11,12], fontproperties='Times New Roman',fontsize=16)
plt.yticks(fontproperties='Times New Roman',fontsize=16)

ax = plt.subplot(gs[5:10,2])
plt.bar(Day_type.keys(), Day_type.values(), width = 0.5, color="limegreen")
plt.xlabel("Day type",fontproperties='Times New Roman',fontsize=16)
plt.ylabel("Frequency",fontproperties='Times New Roman',fontsize=16)  
plt.xticks(fontproperties='Times New Roman',fontsize=16)
plt.yticks(fontproperties='Times New Roman',fontsize=16)
ax=plt.gca()
x_major_locator=MultipleLocator(1)
ax.xaxis.set_major_locator(x_major_locator)  

ax = plt.subplot(gs[10:15,2])
plt.bar(np.arange(len(list(Hour.keys()))), Hour.values(), width = 0.5, color="c")
plt.xlabel("Hour",fontproperties='Times New Roman',fontsize=16)
plt.ylabel("Frequency",fontproperties='Times New Roman',fontsize=16)  
plt.xticks(np.arange(len(list(Hour.keys()))), [0, 1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23], fontproperties='Times New Roman',fontsize=16)
plt.yticks(fontproperties='Times New Roman',fontsize=16)

########################Visualize the typical days of the maximal frequent subgraph########################
ax = plt.subplot(gs[15:19,2])
Top_three_days = ['2/23', '3/30', '3/7']
cmap = colors.ListedColormap(["lightgrey",'grey'])
bounds=[-0.5, 0.5, 1.5]
heatmap_ = {0: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
 1: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
 2: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1]}
heatmap_data = []
non_ = [np.nan]*78
heatmap_data.append(heatmap_[2])
heatmap_data.append(non_)
heatmap_data.append(heatmap_[1])
heatmap_data.append(non_)
heatmap_data.append(heatmap_[0])

norm = colors.BoundaryNorm(bounds, cmap.N)
heatmap = plt.pcolor(np.array(heatmap_data), cmap=cmap, norm=norm)
xticks = [0, 12, 24, 36, 54, 66]
xlabels = ['0:00', '2:00', '4:00', '6:00', '20:00', '22:00']
plt.xticks(xticks, xlabels, fontproperties='Times New Roman',fontsize=16)
plt.text(-8, 4.2, Top_three_days[0], fontproperties='Times New Roman', color="black", fontsize=16)
plt.text(-8, 2.2, Top_three_days[1], fontproperties='Times New Roman', color="black", fontsize=16)
plt.text(-8, 0.2, Top_three_days[2], fontproperties='Times New Roman', color="black", fontsize=16)
plt.yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax = plt.subplot(gs[19:20,2])
cmap = colors.ListedColormap(["lightgrey",'grey'])
bounds=[-0.5, 0.5, 1.5]
heatmap_data = []
heatmap_data.append([1]*8+[np.nan]*28+[0]*8+[np.nan]*28)
norm = colors.BoundaryNorm(bounds, cmap.N)
heatmap = plt.pcolor(np.array(heatmap_data), cmap=cmap, norm=norm)
plt.text(8.5, 0.7, "The graph occurs", fontproperties='Times New Roman', color="black", fontsize=16)
plt.text(45, 1.25, "The graph doesn't\noccur", fontproperties='Times New Roman', color="black", fontsize=16)
plt.xticks([])
plt.yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.tight_layout()
plt.savefig('A maximal frequent subgraph.png', dpi=700, bbox_inches='tight')
plt.show()