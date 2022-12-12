import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Segment, Patch, Label, MultiLine
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.embed import components

#global formatting
#curdoc().theme = 'dark_minimal'
#output_notebook(hide_banner=True)

#establish plot
def plot_settings(p, qbook = False):
    p.toolbar.logo=None
    p.toolbar_location=None
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    if qbook:
        p.background_fill_alpha = 0
        p.border_fill_alpha = 0
        p.axis.axis_line_color = 'white'
        p.axis.axis_label_text_color = 'white'
        p.axis.major_tick_line_color = 'white'
        p.axis.minor_tick_line_color = 'white'
        p.axis.minor_tick_line_color = 'white'
        p.axis.major_label_text_color = 'white'
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

width=8
height=8
p = figure(x_range=(-width,width), y_range=(-height,height), outer_width=500, outer_height=500, max_width = 600, sizing_mode = 'scale_width')
plot_settings(p, False)

#create grid _________________________________________________________________
ax = 1
ay = 0
bx = 0
by = 1

x , y = [], []
w = 20
for i in range(-w,w):
    for j in range(-w,w):
        x.append( i*ax/2 + j*bx/2 )
        y.append( i*ay/2 + j*by/2 )
        
xpts = np.array([ax, 0, -ax, 0,  bx,0,-bx,0])
ypts = np.array([ay,  0, -ay, 0, by,0,-by,0])

source = ColumnDataSource(dict(
        xs=[xpts+xx for i, xx in enumerate(x)],
        ys=[ypts+yy for i, yy in enumerate(y)],
    )
)
glyph = MultiLine(xs="xs", ys="ys", line_color="lightgray", line_width=1)
p.add_glyph(source, glyph)

#create vectors _______________________________________________________________

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

sources_a = create_vector(p,1,0,color='#9A11DA')
sources_b = create_vector(p,0,1,color='#D30982')

sources_result_a = create_vector(p,1,0,color='#9A11DA')
sources_result_b = create_vector(p,0,1,color='#D30982')
sources_result = create_vector(p,1,1,color='green')

#create sliders__________________________________________________________________________

a_x = Slider(start=-3, end=3, value=1, step=0.5, title="a_x", sizing_mode = 'stretch_both')
a_y = Slider(start=-3, end=3, value=0, step=0.5, title="a_y", sizing_mode = 'stretch_both')
b_x = Slider(start=-3, end=3, value=0, step=0.5, title="b_x", sizing_mode = 'stretch_both')
b_y = Slider(start=-3, end=3, value=1, step=0.5, title="b_y", sizing_mode = 'stretch_both')
alpha = Slider(start=-10, end=10, value=0, step=0.5, title="alpha", sizing_mode = 'stretch_both')
beta = Slider(start=-10, end=10, value=0, step=0.5, title="beta", sizing_mode = 'stretch_both')

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

const source_a = source_list[0];
const source_b = source_list[1];
const source_result_a = source_list[2];
const source_result_b = source_list[3];
const source_result = source_list[4];

const ax = a_x.value
const ay = a_y.value
const bx = b_x.value
const by = b_y.value

const ax_result = alpha.value*a_x.value
const ay_result = alpha.value*a_y.value
const bx_result = beta.value*b_x.value
const by_result = beta.value*b_y.value
const result_x = ax_result + bx_result
const result_y = ay_result + by_result

update_vector(ax,ay,0,0,source_a)
update_vector(bx,by,0,0,source_b)
update_vector(ax_result,ay_result,0,0,source_result_a)
update_vector(bx_result,by_result, ax_result,ay_result,source_result_b)
update_vector(result_x,result_y, 0,0, source_result)
"""

code_grid = """

//update source for multiline
const ax = a_x.value
const ay = a_y.value
const bx = b_x.value
const by = b_y.value

var x = [];
var y = [];

const d = 40

for (var i=-d;i<d;i++){
    for (var j=-d;j<d;j++){
        x.push(i*ax + j*bx)
        y.push(i*ay + j*by)
    }
}

const xpts = [ax,0,-ax,0,bx,0,-bx,0]
const ypts = [ay,  0, -ay, 0, by,0,-by,0]

var xs = x.map((i) => {
    return xpts.map(q => q+i)
})
var ys = y.map((i) => {
    return ypts.map(q => q+i)
})

source.data['xs'] = xs;
source.data['ys'] = ys
source.change.emit();
"""

callback_vectors = CustomJS(args=dict(source_list=[sources_a,sources_b,sources_result_a, sources_result_b, sources_result], 
                                      a_x = a_x,
                                      a_y = a_y,
                                      b_x = b_x,
                                      b_y = b_y,
                                      alpha = alpha,
                                      beta = beta),code=code)
callback_grid = CustomJS(args=dict(source = source, 
                                      a_x = a_x,
                                      a_y = a_y,
                                      b_x = b_x,
                                      b_y = b_y),code=code_grid)    
a_x.js_on_change('value',callback_vectors,callback_grid)
a_y.js_on_change('value',callback_vectors,callback_grid)
b_x.js_on_change('value',callback_vectors,callback_grid)
b_y.js_on_change('value',callback_vectors,callback_grid)
alpha.js_on_change('value',callback_vectors)
beta.js_on_change('value',callback_vectors)




#semantics
p.line([0,0],[0,0])
p.xaxis.fixed_location= 0
p.yaxis.fixed_location= 0

layout = row( column(a_x,a_y,b_x,b_y,alpha,beta , sizing_mode = 'fixed', height = 100, width = 150),p , sizing_mode = 'stretch_width' )
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("double_wave.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)

#script, div = components(layout)