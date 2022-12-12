import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Button
from bokeh.plotting import ColumnDataSource, figure, output_file, show


outer_width = 500
outer_height = 400

n=2
x = np.linspace(0,1,100)
y = np.sqrt(2)*np.sin(n*np.pi*x) 
y2 = [i**2 for i in y]

source = ColumnDataSource(data = dict(x=x,y=y,y2=y2))


p = figure(x_range=(0,1), y_range = (-2.5,2.5), outer_width=outer_width, outer_height=outer_height)

a = p.line(x='x',y='y', source = source, color ='#9A11DA', line_width = 3, line_alpha = 0.6,muted_alpha = 0, legend_label = '\u03a8\u2099(x)')
b = p.line(x='x',y='y2', source = source, color ='#D30982', line_width = 3, line_alpha = 0.6, muted_alpha = 0,legend_label = 'p(x) = (\u03a8\u2099(x))\u00b2')
b.muted = True

p.legend.location = "bottom_left"
p.legend.click_policy="mute"

#adjust plot settings
def plot_settings(p):
    p.toolbar.logo=None
    p.toolbar_location=None
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None
plot_settings(p)

slider = Slider(title = "n", start = 1, end = 10, value = 1,step  = 1,max_width = 200)

callback = CustomJS(args=dict(source = source, slider = slider),
                     code = """
     const n = slider.value;
     const x = source.data['x'];
     const y = [];
     const y2 = [];
     for (var i of x){
         var q = Math.sqrt(2)*Math.sin(n*3.14*i)
         y.push(q)
         y2.push(q*q)
     }
     source.data['y'] = y;
     source.data['y2'] = y2;
     source.change.emit();
                     """)

slider.js_on_change('value', callback)

#output_file("slider.html", title="slider.py example")
output_notebook(hide_banner=True)

layout = column(slider,p)

show(layout,notebook_handle=True)