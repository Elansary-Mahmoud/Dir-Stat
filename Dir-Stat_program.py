#!/usr/bin/env python

import pandas as pd
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np
import os
import sys
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-n", "--num", dest="size",default=10
                  ,help="Check the size of N directories", metavar="FILE")

parser.add_option("-o", "--out", dest="filename",default='TMP_size.txt',
                  help="write report to FILE", metavar="FILE")

parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

if options.verbose:
	print("Program started:")
	print("options:", options)

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))
#size = int(sys.argv[1])

size = int(options.size)
filename = str(options.filename)
os.system('du -sk ./*/ | sort -n >' + filename)
df = pd.read_csv(filename,sep="\t",header=None,names=['size','directory'])
df = df.sort_values('size',ascending=False)

if options.verbose:
	print(df.head())

values = df['size'].apply(lambda x: np.array(x))
labels = df['directory'].apply(lambda x: np.array(x))
new_values = values[0:size].tolist()
new_values.append(df[(size + 1):]['size'].sum())
new_labels = labels[0:size].tolist()
new_labels.append('./others/')
new_labels = [ i.split('/')[1] for i in new_labels ]
new_labels = [ i[:40] + "..." if len(i) > 40 else i  for i in new_labels ]
new_labels = [ new_labels[i] + " (" + str(round(new_values[i] / 1024000,2)) + "G)" for i in range(0,(size + 1))  ]

layout = go.Layout(height = 600,width = 600, autosize = False,title = "Total Directory size " + str(round(df['size'].sum()/1024000,2)) + "G")
trace = go.Pie(labels=new_labels,values=new_values,hoverinfo='label+percent')
fig = go.Figure(data = [trace], layout = layout)

if options.verbose:
	print("file ready for download:")

offline.plot(fig, auto_open=True, image = 'png', image_filename='Directory_size',output_type='file', image_width=800, image_height=600, validate=False)
