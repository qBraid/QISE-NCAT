import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Div
from bokeh.plotting import ColumnDataSource, figure, output_file, show

#global formatting
#curdoc().theme = 'dark_minimal'
#output_notebook(hide_banner=True)

#establish plot
def plot_settings(p):
    p.toolbar.logo=None
    p.toolbar_location=None
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None

height=200
plot1 = figure(x_range=(-np.pi*2,np.pi*2), y_range=(-2.1,2.1), outer_width=600, outer_height=height)
plot2 = figure(x_range=(-np.pi*2,np.pi*2), y_range=(-2.1,2.1), outer_width=600, outer_height=height)
plot_settings(plot1)
plot_settings(plot2)


#create data
phi=np.pi/4
x = np.linspace(-np.pi*2,np.pi*2, 500)
y1 = np.cos(x)
y2 = np.cos(x+phi)
y3= y1 + y2

source1 = ColumnDataSource(data=dict(x=x, y=y1))
source2 = ColumnDataSource(data=dict(x=x,y=y2))
source3 = ColumnDataSource(data=dict(x=x,y=y3))
sources=[source1,source2,source3]

plot1.line('x', 'y', source=source1, line_width=3, line_alpha=0.6, line_color='#9A11DA')
plot1.line('x', 'y', source=source2, line_width=3, line_alpha=0.6, line_color='#9A11DA')
plot2.line('x', 'y', source=source3, line_width=3, line_alpha=0.6, line_color='#D30982')

phase_1 = Slider(start=0, end=6.4, value=0, step=np.pi/16, title="Phase 1")
phase_2 = Slider(start=0, end=6.4, value=0+phi, step=np.pi/16, title="Phase 2")
message = Div(text = "Phase Difference =  0.25 \u03c0 ")

callback_code="""
    //first wave
    const data1 = sources[0].data;
    const phi_1 = phase_1.value;
    const x1 = data1['x']
    const y1 = data1['y']
    for (var i = 0; i < x1.length; i++) {
        y1[i] = Math.cos(x1[i]-phi_1);
    }
    
    //second wave
    const data2 = sources[1].data;
    const phi_2 = phase_2.value;
    const x2 = data2['x']
    const y2 = data2['y']
    for (var i = 0; i < x2.length; i++) {
        y2[i] = Math.cos(x2[i]-phi_2);
    }
    
    //superpositions
    const data3 = sources[2].data;
    const x3 = data3['x']
    const y3 = data3['y']
    for (var i = 0;i < x3.length; i++) {
        y3[i] = y1[i] + y2[i];
    }
    
    sources[0].change.emit();
    sources[1].change.emit();
    sources[2].change.emit();
"""

callback = CustomJS(args=dict(sources=sources, phase_1=phase_1,phase_2=phase_2),code=callback_code)
callback2 = CustomJS(args=dict(theta_1  = phase_1, theta_2 = phase_2, message = message),code="""
var diff = theta_2.value - theta_1.value
if (diff<0)
    {diff += 2*Math.PI}
if ((diff>Math.PI) ||(diff <0))
    {diff = 2*Math.PI - diff;}

const num = diff/Math.PI
message.text = `Phase Difference:  ${num.toFixed(2)} \u03c0`
""")

phase_1.js_on_change('value', callback)
phase_2.js_on_change('value', callback)
phase_1.js_on_change('value', callback2)
phase_2.js_on_change('value', callback2)

layout = row( column(plot1,plot2), column(phase_1,phase_2,message) )
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("double_wave.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)