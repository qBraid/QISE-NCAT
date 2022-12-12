import numpy as np
from math import pi
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_file, show

def plot_settings(p):
    p.toolbar.logo=None
    p.toolbar_location=None
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None

height=200
plot1 = figure(x_range=(-3,3), y_range=(-2.1,2.1), outer_width=600, outer_height=height)
plot_settings(plot1)


#create data
phi=0.5
x = np.linspace(-3,3, 500)
y1 = np.cos(x*pi)
y2 = np.cos(x*pi+phi*pi)

source1 = ColumnDataSource(data=dict(x=x, y=y1))
source2 = ColumnDataSource(data=dict(x=x,y=y2))
sources=[source1,source2]

plot1.line('x', 'y', source=source1, line_width=3, line_alpha=0.6, line_color='#00FFFF')
plot1.line('x', 'y', source=source2, line_width=3, line_alpha=0.6, line_color='#FF0000')

phase_1 = Slider(start=0.5, end=2, value=0.5, step=0.5, title="\u03d5")

callback_code="""
    //first wave
    const data1 = sources[0].data;
    const x1 = data1['x']
    const y1 = data1['y']
    for (var i = 0; i < x1.length; i++) {
        y1[i] = Math.cos(x1[i]*Math.PI);
    }
    
    //second wave
    const data2 = sources[1].data;
    const phi_1 = phase_1.value;
    const x2 = data2['x']
    const y2 = data2['y']
    for (var i = 0; i < x2.length; i++) {
        y2[i] = Math.cos(x2[i]*Math.PI-phi_1*Math.PI);
    }
    
    sources[0].change.emit();
    sources[1].change.emit();
"""

callback = CustomJS(args=dict(sources=sources, phase_1=phase_1),code=callback_code)

phase_1.js_on_change('value', callback)

layout = row( column(plot1), column(phase_1) )
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("double_wave.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)