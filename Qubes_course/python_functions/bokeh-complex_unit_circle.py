import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Segment, Patch, Label, Div, LabelSet
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

width=1.5
height=1.5
p = figure(x_range=(-width,width), y_range=(-height,height), outer_width=500, outer_height=500)
plot_settings(p)

#add reference point circle
p.ellipse(0,0,width = 2,height = 2, line_color = 'black', fill_alpha=0)

#create data
def create_vector(p,xi,yi,color='#9A11DA',xi_start=0,yi_start=0):
    
    length=np.sqrt(xi**2 + yi**2)
    x_hat=xi/length
    y_hat=yi/length
    w=0.05
    h=0.1
    
    source_stem= ColumnDataSource(data=dict(x0=[xi_start],
                                            x1=[xi - x_hat*w + xi_start],
                                            y0=[yi_start],
                                            y1=[yi-y_hat*w + yi_start]))
    source_head = ColumnDataSource(data=dict(x=[xi + xi_start,
                                        xi - h*x_hat + w*y_hat + xi_start,
                                        xi - h*x_hat - w*y_hat + xi_start],
                                     y=[yi + yi_start,
                                        yi - h*y_hat - w*x_hat + yi_start,
                                        yi - h*y_hat + w*x_hat + yi_start]))
    sources=[source_stem,source_head]
    
    vector = Segment(x0="x0", y0="y0", x1="x1", y1="y1", line_width=3, line_color=color)
    head = Patch(x='x',y='y', line_color=color, fill_color=color)
    p.add_glyph(source_stem , vector)
    p.add_glyph(source_head, head)

    return sources

source1 = create_vector(p,1,0,color='#9A11DA')
source2 = create_vector(p,0,1,color='#D30982')

theta_1 = Slider(start=0, end=2*np.pi, value=np.pi/4, step=np.pi/32, title="Phase 1 (\u03c6\u2081)")
theta_2 = Slider(start=0, end=2*np.pi, value=0, step=np.pi/32, title="Phase 2 (\u03c6\u2082)")
message = Div(text = "Phase Difference =  0.25 \u03c0 ")

code = """
function update_vector(x_value,y_value,x_start_value,y_start_value,sources) {

    //input variables
    const delta_x = x_start_value;
    const delta_y = y_start_value;
    
    //desired vector
    const new_x = x_value;
    const new_y = y_value;
    
    //stem
    const data = sources[0].data;
    const x0 = data['x0'];
    const y0 = data['y0'];
    const x1 = data['x1'];
    const y1 = data['y1'];
    x0[0] = delta_x;
    y0[0] = delta_y;
    x1[0] = delta_x + new_x;
    y1[0] = delta_y + new_y;
    
    //head
    const length = Math.sqrt(new_x**2 + new_y**2);
    const x_hat = new_x/length;
    const y_hat = new_y/length;
    
    const data2 = sources[1].data;
    var x = data2['x'];
    var y = data2['y'];
    const h = 0.1;
    const w = 0.05;

    x[0]=new_x + delta_x;
    x[1]=new_x - h*x_hat + w*y_hat + delta_x;
    x[2]=new_x - h*x_hat - w*y_hat + delta_x;
    y[0]=new_y + delta_y;
    y[1]=new_y - h*y_hat - w*x_hat + delta_y;
    y[2]=new_y - h*y_hat + w*x_hat + delta_y;
    
    //adjust stem
    x1[0] -= x_hat*w;
    y1[0] -= y_hat*w;
    
    sources[0].change.emit();
    sources[1].change.emit();

}

const x1 = Math.cos(theta_1.value)
const y1 = Math.sin(theta_1.value)
const x2 = Math.cos(theta_2.value)
const y2 = Math.sin(theta_2.value)

update_vector(x1,y1,0,0,source1)
update_vector(x2,y2,0,0,source2)
"""

callback = CustomJS(args=dict(source1 = source1, source2 = source2, theta_1  = theta_1, theta_2 = theta_2),code=code)     
callback2 = CustomJS(args=dict(theta_1  = theta_1, theta_2 = theta_2, message = message),code="""
var diff = theta_2.value - theta_1.value
if (diff<0)
    {diff += 2*Math.PI}
if ((diff>Math.PI) ||(diff <0))
    {diff = 2*Math.PI - diff;}

const num = diff/Math.PI
message.text = `Phase Difference:  ${num.toFixed(2)} \u03c0`
""")     
theta_1.js_on_change('value',callback)
theta_2.js_on_change('value',callback)
theta_1.js_on_change('value',callback2)
theta_2.js_on_change('value',callback2)


#semantics
p.line([0,0],[0,0])
p.xaxis.fixed_location= 0
p.yaxis.fixed_location= 0

#ticks off
p.xaxis.major_tick_line_color=None
p.xaxis.minor_tick_line_color=None
p.yaxis.major_tick_line_color=None
p.yaxis.minor_tick_line_color=None
p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels

#labels
source = ColumnDataSource(data = dict(x=[1,0,-1,0],y=[0,1,0,-1],label=['1','i','-1','-i']))
p.scatter(source = source, x = 'x',y='y',color='black')
p.add_layout(LabelSet(source = source,x='x',y='y',text='label',x_offset = 5, y_offset = 5,render_mode='canvas',text_font_size='20px'))

layout = row( column(theta_1, theta_2,message),p  )
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("double_wave.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)