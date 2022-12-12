import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Patch, Rect, Label,Toggle, Button, Div, RadioButtonGroup
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.embed import components

#global formatting
#curdoc().theme = 'dark_minimal'

#establish plot
plot = figure(x_range=(0,6), y_range=(0,5), outer_width=600, outer_height=500)
def plot_settings(p, qbook = False):
    p.toolbar.logo=None
    p.toolbar_location=None
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.grid.visible = False
    if qbook:
        p.background_fill_alpha = .5
        p.border_fill_alpha = .25
        p.axis.axis_line_color = 'white'
        p.axis.axis_label_text_color = 'white'
        p.axis.major_tick_line_color = 'white'
        p.axis.minor_tick_line_color = 'white'
        p.axis.minor_tick_line_color = 'white'
        p.axis.major_label_text_color = 'white'
        p.xgrid.grid_line_color = 'gray'
        p.ygrid.grid_line_color = 'gray'
        p.xaxis.level = 'underlay'
        p.yaxis.level = 'underlay'

plot_settings(plot, True)

#lines for photon paths
base = plot.line(x=[1,2],y=[1,1],line_width = 3, line_alpha = 1, line_color = '#9A11DA')
upper_line = plot.line(x=[2,2,4],y=[1,3,3],line_width = 3, line_alpha = 0.5, line_color = '#9A11DA')
lower_line = plot.line(x=[2,3],y=[1,1],line_width = 3, line_alpha = 0.5, line_color = '#9A11DA')
lower_line2 = plot.line(x=[3,4,4],y=[1,1,3],line_width = 3, line_alpha = 0.5, line_color = '#9A11DA')
detector_a_line = plot.line(x=[4,4],y=[3,4],line_width = 3, line_alpha = 0.5, line_color = '#9A11DA')
detector_b_line = plot.line(x=[4,5],y=[3,3],line_width = 3, line_alpha = 0.5, line_color = '#9A11DA')
#sliders to track line alphas
upper_alpha = Slider(start = 0, end = 1, step =0.1 , value = 0.5)
lower_alpha = Slider(start = 0, end = 1, step =0.1 , value = 0.5)
lower_alpha2 = Slider(start = 0, end = 1, step =0.1 , value = 0.5)
detector_a_alpha = Slider(start = 0, end = 1, step =0.1 , value = 0.5)
detector_b_alpha = Slider(start = 0, end = 1, step =0.1 , value = 0.5)
#link sliders to line glyphs
upper_alpha.js_link('value',upper_line.glyph,'line_alpha')
lower_alpha.js_link('value',lower_line.glyph,'line_alpha')
lower_alpha2.js_link('value',lower_line2.glyph,'line_alpha')
detector_a_alpha.js_link('value',detector_a_line.glyph,'line_alpha')
detector_b_alpha.js_link('value',detector_b_line.glyph,'line_alpha')

#build hardware
plot.rect(x=1,y=1, width = 0.6, height = 0.3)
plot.rect(x=[2,4],y=[1,3], width = 0.1, height = 0.5, color='gray',line_color='dimgrey', line_width = 3,angle = -np.pi/4)
plot.rect(x=[2,4],y=[3,1], width = 0.1, height = 0.5, color='lightsteelblue', line_color ='steelblue', line_width =3, angle = -np.pi/4)
plot.rect(x =3, y = 1, width = 0.8, height = 0.8, color='gainsboro')
plot.ellipse(x=[4,5],y=[4,3],width = [0.5,0.2],height = [0.2,0.5], fill_color ='sienna',fill_alpha = 0.8, line_color = 'chocolate',line_width = 3)

#notations
plot.add_layout(Label(text = "Detector A", x = 4, y =4.2,x_offset = 0, y_offset = 0,text_align = 'center',text_font_size = '15px'))
plot.add_layout(Label(text = "Detector B", x = 5, y =3.4,x_offset = 0, y_offset = 0,text_align = 'center',text_font_size = '15px'))

#outcome circles signals
explosion = plot.circle(x=3, y= 1, size = 50, color = 'red')
no_explosion = plot.circle(x=3, y=1, size = 20, color='black')
detector_a = plot.circle(x=4,y=3.9, size = 25, color = '#9A11DA',fill_alpha = 1)
detector_b = plot.circle(x=4.9,y=3, size = 25, color = '#9A11DA',fill_alpha = 1)
explosion.visible = False
no_explosion.visible = False
detector_a.visible = False
detector_b.visible = False
#buttons to track outcome signals
tog_exp = Toggle(button_type = "success")
tog_no_exp = Toggle(button_type = 'success')
tog_a = Toggle(button_type = "success")
tog_b = Toggle(button_type = "success")
#link buttons to circles
tog_exp.js_link('active',explosion,'visible')
tog_no_exp.js_link('active', no_explosion,'visible')
tog_a.js_link('active',detector_a,'visible')
tog_b.js_link('active',detector_b,'visible')

#user sliders
splitter_1 = Slider(value=50, start=0, end=100, step=10)
splitter_2 = Slider(value=50, start=0, end=100, step=10)
firework_present = RadioButtonGroup(labels=['No Firework Present', 'Firework Present'],active=0)

#data for case 2 messages
source = ColumnDataSource(data = dict(messages = []))
message = Div(text = "")

#callbacks
run = Button(label = "Run Experiment", width=100)
reset = Button(label = "Reset", width =100)
callback = CustomJS(args = dict(upper_alpha = upper_alpha,
                                 lower_alpha = lower_alpha,
                                 lower_alpha2 = lower_alpha2,
                                 detector_a_alpha = detector_a_alpha ,
                                 detector_b_alpha = detector_b_alpha,
                                 tog_a = tog_a,
                                 tog_b = tog_b,
                                 tog_exp = tog_exp,
                                 tog_no_exp = tog_no_exp,
                                 source = source,
                                 splitter_1 = splitter_1,
                                 splitter_2 = splitter_2,
                                 firework_present = firework_present),code ="""
const alpha1 = Math.sqrt(splitter_1.value/100) //upper path 
const beta1 = Math.sqrt(1-splitter_1.value/100) // lower path
const alpha2 = Math.sqrt(splitter_2.value/100) //detector a path
const beta2 = Math.sqrt(1-splitter_2.value/100) //detector b path

tog_exp.active = false
tog_a.active = false
tog_b.active = false
                                 
//case: no firework
if (firework_present.active === 0) {
    
    tog_no_exp.active= false
    
    //after splitter 1
    upper_alpha.value = alpha1**2;
    lower_alpha.value = beta1**2;
    lower_alpha2.value = beta1**2;
    
    //after splitter 2
    detector_a_alpha.value = (alpha2*alpha1 + beta1*beta2)**2
    detector_b_alpha.value = (alpha1*beta2 - beta1*alpha2)**2
    
} else {

    tog_no_exp.active = true

    //after splitter 1
    upper_alpha.value = alpha1**2;
    lower_alpha.value = beta1**2;
    lower_alpha2.value = 0;
    
    //after splitter 2
    detector_a_alpha.value = (alpha1*alpha2)**2
    detector_b_alpha.value = (alpha1*beta2)**2
}
                                 """ )

callback_run = CustomJS(args = dict(upper_alpha = upper_alpha,
                                 lower_alpha = lower_alpha,
                                 lower_alpha2 = lower_alpha2,
                                 detector_a_alpha = detector_a_alpha ,
                                 detector_b_alpha = detector_b_alpha,
                                 tog_a = tog_a,
                                 tog_b = tog_b,
                                 tog_exp = tog_exp,
                                 tog_no_exp = tog_no_exp,
                                 source = source,
                                 splitter_1 = splitter_1,
                                 splitter_2 = splitter_2,
                                 firework_present = firework_present),code ="""

const alpha1 = Math.sqrt(splitter_1.value/100) //upper path 
const beta1 = Math.sqrt(1-splitter_1.value/100) // lower path
const alpha2 = Math.sqrt(splitter_2.value/100) //detector a path
const beta2 = Math.sqrt(1-splitter_2.value/100) //detector b path

//case: no firework
if (firework_present.active === 0) {
    
    
    tog_exp.active=false
    tog_no_exp.active= false
    
    //visual line alphas are also probabilities
    if (Math.random() < detector_a_alpha.value) {
        
        //measured a
        tog_a.active = true
        tog_b.active = false
        source.data['messages'].push('Photon measured at Detector A');
        
    } else {
    
        //measured b
        tog_a.active = false
        tog_b.active = true
        source.data['messages'].push('Photon measured at Detector B');
    }
    
} else {

    if (Math.random() < lower_alpha.value) {
        //firework explodes
        tog_a.active = false
        tog_b.active = false
        tog_exp.active=true
        tog_no_exp.active=false
        source.data['messages'].push('Firework went off!');
        
    } else {
        
        tog_exp.active = false
        tog_no_exp.active = true
        
        if (Math.random() < alpha2**2) {
            //land detector a
            tog_a.active = true
            tog_b.active = false
            source.data['messages'].push('Photon measured at Detector A');
            
        } else {
            tog_b.active = true
            tog_a.active = false
            source.data['messages'].push('Photon measured at Detector B');
        }
        
    }
}
""")

callback_reset = CustomJS(args = dict(tog_a = tog_a,
                                 tog_b = tog_b,
                                 tog_exp = tog_exp,
                                 tog_no_exp = tog_no_exp,
                                 firework_present = firework_present),code ="""
tog_a.active= false
tog_b.active = false
tog_exp.active = false

if (firework_present.active === 0) {
    tog_no_exp.active = false
} else {
    tog_no_exp.active = true
}
""")

callback_message = CustomJS( args = dict(source = source,
                                   message = message), code = """
var message_list = source.data['messages'];
if (message_list.length > 15){
    message_list.shift();
}
var text = ''
for (var m of message_list) {
    text += m + '<br>'
}
message.text = text;
                                   """)

run.js_on_click(callback_run)
run.js_on_click(callback_message)
reset.js_on_click(callback_reset)
firework_present.js_on_click(callback)
splitter_1.js_on_change('value',callback)
splitter_2.js_on_change('value',callback)
#case_a.js_on_click(callback_message)
#case_b.js_on_click(callback_b)
#case_b.js_on_click(callback_message)

hidden = column(upper_alpha,lower_alpha,detector_a_alpha,detector_b_alpha,tog_exp,tog_a,tog_b)
sidebar = column(firework_present,row(run,reset),message)
layout = row(sidebar,plot)

#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("slider.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)

script, div = components(layout)