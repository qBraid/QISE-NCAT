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

width=8
height=8
p = figure(x_range=(-width,width), y_range=(-height,height), outer_width=500, outer_height=500)
plot_settings(p)

#add reference point circle
p.circle([-3],[7],size = 5, color = 'black', alpha=0.8)

#create data
def create_vector(p,xi,yi,color='#9A11DA',xi_start=0,yi_start=0):
    
    length=np.sqrt(xi**2 + yi**2)
    x_hat=xi/length
    y_hat=yi/length
    w=0.2
    h=0.5
    
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

i_ = 2
j_ = 2

sources1 = create_vector(p,i_,0,color='#9A11DA')
sources2 = create_vector(p,0,j_,color='#D30982',xi_start = i_)
sources3 = create_vector(p,i_,j_,color='green')

i = Slider(start=-width, end=width, value=2, step=0.5, title="i")
j = Slider(start=-height, end=height, value=4, step=0.5, title="j")

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
    const h = 0.5;
    const w = 0.2;

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

const source1 = source_list[0];
const source2 = source_list[1];
const source3 = source_list[2];

update_vector(i.value,0,0,0,source1)
update_vector(0,j.value,i.value,0,source2)
update_vector(i.value,j.value,0,0,source3)
"""

callback = CustomJS(args=dict(source_list=[sources1,sources2,sources3], i=i,j=j),code=code)               
i.js_on_change('value',callback)
j.js_on_change('value',callback)

#semantics
p.line([0,0],[0,0])
p.xaxis.fixed_location= 0
p.yaxis.fixed_location= 0

layout = row( column(i,j),p  )
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("double_wave.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)