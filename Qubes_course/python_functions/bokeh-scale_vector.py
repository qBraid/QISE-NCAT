import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Segment, Patch, Label
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


p = figure(x_range=(-7.1,7.1), y_range=(-7.1,7.1), outer_width=400, outer_height=400)
plot_settings(p)

#create data
def create_vector(p,xi,yi,color):
    
    length=np.sqrt(xi**2 + yi**2)
    x_hat=xi/length
    y_hat=yi/length
    w=0.2
    h=0.5
    
    source_stem= ColumnDataSource(data=dict(x0=[0],x1=[xi - x_hat*w],y0=[0],y1=[yi-y_hat*w]))
    source_head = ColumnDataSource(data=dict(x=[xi,
                                        xi - h*x_hat + w*y_hat,
                                        xi - h*x_hat - w*y_hat],
                                     y=[yi,
                                        yi - h*y_hat - w*x_hat,
                                        yi - h*y_hat + w*x_hat]))
    sources=[source_stem,source_head]
    
    vector = Segment(x0="x0", y0="y0", x1="x1", y1="y1", line_width=3, line_color=color)
    head = Patch(x='x',y='y', line_color=color, fill_color=color)
    p.add_glyph(source_stem , vector)
    p.add_glyph(source_head, head)

    return sources

sources=create_vector(p,2,2,'#9A11DA')

theta = Slider(start=0, end=360, value=45, step=5, title="\u03b8")
scale = Slider(start=-6, end=6, value=2*np.sqrt(2), step=0.1, title="scale")

vector_update_code="""
    
    //input parameters
    const x_value = scale.value*Math.cos(theta.value*Math.PI/180)
    const y_value = scale.value*Math.sin(theta.value*Math.PI/180)
    const r = Math.sqrt(x_value**2 + y_value**2)
    
    //stem
    const data = sources[0].data;
    const x1 = data['x1'];
    const y1 = data['y1'];
    x1[0] = x_value;
    y1[0]=  y_value;
    
    //head
    const length = Math.sqrt(x1[0]**2 + y1[0]**2);
    var xi = x1[0];
    var yi = y1[0];
    const x_hat = x1[0]/length;
    const y_hat = y1[0]/length;
    
    const data2= sources[1].data;
    var x = data2['x'];
    var y = data2['y'];
    const h = 0.5;
    const w = 0.2;

    x[0]=x1[0] ;
    x[1]=xi - h*x_hat + w*y_hat;
    x[2]=xi - h*x_hat - w*y_hat;
    y[0]=y1[0];
    y[1]=yi - h*y_hat - w*x_hat;
    y[2]=yi - h*y_hat + w*x_hat;
    
    //adjust stem
    x1[0] -= x_hat*w;
    y1[0] -= y_hat*w;
    
    sources[0].change.emit();
    sources[1].change.emit();
"""

callback = CustomJS(args=dict(sources=sources, theta = theta,scale=scale),code=vector_update_code)

theta.js_on_change('value',callback)
scale.js_on_change('value',callback)

#semantics
p.line([0,0],[0,0])
p.xaxis.fixed_location= 0
p.yaxis.fixed_location= 0

layout = row( p ,column(theta,scale) )
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'
    
#output_file("double_wave.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)