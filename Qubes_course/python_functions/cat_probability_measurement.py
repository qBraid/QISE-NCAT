# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:16:35 2020

@author: Erik
"""

import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets

def cat_probability_measurement(i):
    
    fig=plt.figure(figsize=(10,6))
    x_data=x[0:i]
    y_data=y[0:i]
    plt.scatter(x_data,y_data,color='red')
    plt.ylim(-1,1)
    plt.xlim(-4,4)
    plt.xlabel('# houses away')
    plt.hlines(0,-4,4,color='gray')

x=[np.random.normal(0,1) for _ in range(300)]
y=[np.random.normal(0,0.25) for _ in range(300)]
i=widgets.IntSlider(min=0,max=300,step=1,description='# Observations')
play=widgets.Button(value=False,description='Play')
out=widgets.interactive_output(cat_probability_measurement,{'i':i})
out.layout.height='500px'
output = widgets.Output()
display(play,out,output)
def on_play_click(b):
    with output:
        i.value=0
        for _ in range(300):
            i.value=i.value+1
            
play.on_click(on_play_click)