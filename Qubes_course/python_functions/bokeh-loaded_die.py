import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Button
from bokeh.plotting import ColumnDataSource, figure, output_file, show


outer_width = 400
outer_height = 500

source1 = ColumnDataSource(data = dict(x=[1,2,3,4,5,6], top = [0,0,0,0,0,0]))
source2 = ColumnDataSource(data = dict(x=[1,2,3,4,5,6], top = [0,0,0,0,0,0]))

plot1 = figure(x_range=(0.3,6.8), outer_width=outer_width, outer_height=outer_height)
plot2 = figure(x_range=(0.3,6.8), y_range=(0,1), outer_width=outer_width, outer_height=outer_height)

plot1.vbar(x='x', top ='top', source = source1,width = 0.5, bottom = 0, color ='#9A11DA')
plot2.vbar(x='x', top ='top', source = source2,width = 0.5, bottom = 0, color ='#D30982')

#adjust plot settings
def plot_settings(p):
    p.toolbar.logo=None
    p.toolbar_location=None
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None
plot_settings(plot1)
plot_settings(plot2)

roll_once = Button(label = "Roll Once")
roll_ten = Button(label = "Roll Ten Times")
roll_hundred = Button(label = "Roll Hundred Times")


code="""
const weights = [7,10,7,4,2,1];
const sum_weights = weights.reduce((a,b) => a+b, 0);
var unit_weights = [];
for (var i = 0; i<weights.length;i++){
    var temp =0;
    for (var j = 0;j<i+1;j++){
        temp += weights[j]
    }
    unit_weights.push(temp/sum_weights)
}

var roll_counts = source1.data['top']
for (var i = 0; i<times;i++) {
    var r = Math.random()
    for (var j =0;j<weights.length;j++) {
        if (r < unit_weights[j]) { 
            roll_counts[j] += 1;
            break;
        }
    }
}

var probs = []
var sum = 0
for (var x of roll_counts){sum +=x};
for (var x of roll_counts){
    probs.push(x/sum)
}

source2.data['top'] = probs;
console.log(probs);
source1.change.emit();
source2.change.emit();

"""

callback_once = CustomJS(args=dict(times=1, source1 = source1, source2 = source2),code = code) 
callback_ten = CustomJS(args=dict(times=10, source1 = source1, source2 = source2),code = code) 
callback_hundred = CustomJS(args=dict(times=100, source1 = source1, source2 = source2),code = code) 
roll_once.js_on_click(callback_once)
roll_ten.js_on_click(callback_ten)
roll_hundred.js_on_click(callback_hundred)

#output_file("slider.html", title="slider.py example")
output_notebook(hide_banner=True)

layout = row(column(roll_once,roll_ten,roll_hundred),plot1,plot2)

show(layout,notebook_handle=True)