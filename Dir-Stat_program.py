#!/usr/bin/env python

import pandas as pd
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np
import os
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

size = int(sys.argv[1])
os.system('du -sk ./*/ | sort -n > tmp_size.txt')
df = pd.read_csv("tmp_size.txt",sep="\t",header=None,names=['size','directory'])
df = df.sort_values('size',ascending=False)
values = df['size'].apply(lambda x: np.array(x))
labels = df['directory'].apply(lambda x: np.array(x))
new_values = values[0:size].tolist()
new_values.append(df[(size+1):]['size'].sum())
new_labels = labels[0:size].tolist()
new_labels.append('./others/')
new_labels = [ i.split('/')[1] for i in new_labels ]
new_labels = [ i[:40] + "..." if len(i) > 40 else i  for i in new_labels ]
new_labels = [ new_labels[i] + " (" + str(round(new_values[i] / 1024000,2)) + "G)" for i in range(0,(size+1))  ]

layout = go.Layout(height = 600,width = 600, autosize = False,title = "Total Directory size " + str(round(df['size'].sum()/1024000,2)) + "G")
trace = go.Pie(labels=new_labels,values=new_values,hoverinfo='label+percent')
fig = go.Figure(data = [trace], layout = layout)
offline.plot(fig, auto_open=True, image = 'png', image_filename='Directory_size',output_type='file', image_width=800, image_height=600, validate=False)

