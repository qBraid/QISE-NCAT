import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Segment, Patch, Label,Button, Div, Markup
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

width=10
height=10
p = figure(x_range=(-width,width), y_range=(-height,height), outer_width=500, outer_height=500)
plot_settings(p)

#create data
def create_vector(p,xi,yi,color='#9A11DA',xi_start=0,yi_start=0):
    
    length=np.sqrt(xi**2 + yi**2)
    x_hat=xi/length
    y_hat=yi/length
    w=0.001
    h=0.001
    
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

sources_main = create_vector(p,0.01,0.01,color='green')
sources_x_neg = [create_vector(p,-0.01,0,xi_start = 0-i,color = '#9A11DA') for i in range(width)]
sources_x_pos = [create_vector(p, 0.01,0,xi_start = i,color = '#9A11DA') for i in range(width)]
sources_y_neg = [create_vector(p,0,-0.01,yi_start = 0-j,color = '#D30982') for j in range(width)]
sources_y_pos = [create_vector(p,0, 0.01,yi_start = j,color = '#D30982') for j in range(width)]

code = """
function update_vector_head_only(x_value,y_value,sources) {

    //desired vector
    const new_x = x_value;
    const new_y = y_value;
    
    //stem
    const data = sources[0].data;
    const x0 = data['x0'];
    const y0 = data['y0'];
    const x1 = data['x1'];
    const y1 = data['y1'];
    const delta_x = x0[0] ;
    const delta_y = y0[0] ;
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

function zero_all(sources) {
    for (var source of sources) {
        update_vector_head_only(0,0,source)
    }
}

function zero_some(sources,index, xy, sign) {
    
    let x = 0;
    let y = 0;
    
    if (xy == 'x'){x = 1} 
    else { y = 1 }
    
    for (var i = 0;i<sources.length;i++) {
        if (i < index) {
            update_vector_head_only(sign*x,sign*y,sources[i])
        } else {
            update_vector_head_only(0,0,sources[i])
        }
    }
}

//const x = data.data['x'][0];
//const y = data.data['y'][0];
const x = x_slider.value;
const y = y_slider.value;


//update x 
if (x == 0) {
    zero_all(sources_x_neg);
    zero_all(sources_x_pos);
} else if (x>0) {
    zero_all(sources_x_neg)
    zero_some(sources_x_pos,x,'x',1)
} else {
    zero_all(sources_x_pos)
    zero_some(sources_x_neg,-x,'x',-1)
}

//update y
if (y == 0) {
    zero_all(sources_y_neg);
    zero_all(sources_y_pos);
} else if (y>0) {
    zero_all(sources_y_neg)
    zero_some(sources_y_pos,y,'y',1)
} else {
    zero_all(sources_y_pos)
    zero_some(sources_y_neg,-y,'y',-1)
}

"""

code2 = """
function update_vector_head_only(x_value,y_value,sources) {

    //desired vector
    const new_x = x_value;
    const new_y = y_value;
    
    //stem
    const data = sources[0].data;
    const x0 = data['x0'];
    const y0 = data['y0'];
    const x1 = data['x1'];
    const y1 = data['y1'];
    const delta_x = x0[0] ;
    const delta_y = y0[0] ;
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

update_vector_head_only(x.value,y.value,source)
"""

data = ColumnDataSource(data = dict(x=[1],y=[1]))

#define buttons and message divs
#x
button_width = 40
x_minus = Button(label = "-", max_width = button_width)
x_div = Div(text = "0")
x_plus = Button(label = "+", max_width = button_width)
#y
y_minus = Button(label = "-", max_width = button_width)
y_div = Div(text = "0")
y_plus = Button(label = "+", max_width = button_width)
#invisible sliders
x = Slider(start = -width, end = width, value = 0 , step = 1)
y = Slider(start = -width, end = width, value = 0, step = 1)
message = Div(text = """Arrows Used: <br>Arrows Left: <br>Vector Length:""", width = 230)

#define callbacks
callback = CustomJS(args=dict(sources_x_neg = sources_x_neg, sources_x_pos = sources_x_pos, 
                              sources_y_neg = sources_y_neg, sources_y_pos = sources_y_pos, x_slider = x,y_slider = y ),code=code)
callback_message = CustomJS(args = dict(x=x,y=y, message = message),code = """
const arrows_used = Math.abs(x.value) + Math.abs(y.value);
var arrows_left = 10 - arrows_used;
if (arrows_left < 0) {
    arrows_left = `Used ${Math.abs(arrows_left)} too many arrows!`
}
const vector_length = Math.sqrt(x.value**2 + y.value**2)

message.text = `Arrows Used: ${arrows_used}<br>Arrows Left: ${arrows_left}<br>Vector Length: ${vector_length.toFixed(2)}`
console.log(message.text)
""")
callback_main = CustomJS(args = dict(x=x,y=y,source = sources_main),code = code2)
#x
callback_xm = CustomJS(args = dict(x = x),code = """x.value -=1;""")
callback_xp = CustomJS(args = dict(x = x),code = """x.value +=1;""")
callback_x = CustomJS(args = dict(x_div = x_div, x = x), code = "x_div.text = x.value.toString();")
x_minus.js_on_click(callback_xm)
x_minus.js_on_click(callback_x)
x_minus.js_on_click(callback)
x_minus.js_on_click(callback_message)
x_minus.js_on_click(callback_main)
x_plus.js_on_click(callback_xp)
x_plus.js_on_click(callback_x)
x_plus.js_on_click(callback)
x_plus.js_on_click(callback_message)
x_plus.js_on_click(callback_main)

#y
callback_ym = CustomJS(args = dict(y = y),code = """y.value -=1;""")
callback_yp = CustomJS(args = dict(y = y),code = """y.value +=1;""")
callback_y = CustomJS(args = dict(y_div = y_div, y = y), code = "y_div.text = y.value.toString();")
y_minus.js_on_click(callback_ym)
y_minus.js_on_click(callback_y)
y_minus.js_on_click(callback)
y_minus.js_on_click(callback_message)
y_minus.js_on_click(callback_main)
y_plus.js_on_click(callback_yp)
y_plus.js_on_click(callback_y)
y_plus.js_on_click(callback)
y_plus.js_on_click(callback_message)
y_plus.js_on_click(callback_main)

#axis location center
p.line([0,0],[0,0])
p.xaxis.fixed_location= 0
p.yaxis.fixed_location= 0

side_bar = column(row(x_minus,x_div,x_plus), row(y_minus,y_div,y_plus),message)
layout = row(side_bar,p )
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'
#output_file("double_wave.html", title="slider.py example")


output_notebook(hide_banner=True)

show(layout,notebook_handle=True)