import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Patch, Rect, Label
from bokeh.plotting import ColumnDataSource, figure, output_file, show

#global formatting
#curdoc().theme = 'dark_minimal'

#set initial values
wavelength_i = 1
a_i = 1
ref_i = 0
k_i=2*np.pi/wavelength_i
n=25



TOOLTIPS = [("\u0394 d", "@delta_d"),
           ("\u0394 d/\u03BB", "@delta_d_wave")]

#establish plot
plot = figure(x_range=(0,6), y_range=(-3,3), tooltips=TOOLTIPS, outer_width=600, outer_height=400)
plot.toolbar.logo=None
plot.toolbar_location=None
plot.toolbar.active_drag = None
plot.toolbar.active_scroll = None
plot.toolbar.active_tap = None



#plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, line_color='#9A11DA')
line_sources= [ColumnDataSource(data=dict(x=[0,5], y=[a_i/2,0])),
              ColumnDataSource(data=dict(x=[0,5], y=[-a_i/2,0]))]
plot.line(x='x',y='y',source=line_sources[0], line_width=2, line_color='#9A11DA')
plot.line(x='x',y='y',source=line_sources[1], line_width=2, line_color='#9A11DA')

#set data for glyphs and plot glyphs
sources=[]
for i in range(n):
    x=np.linspace(5,wavelength_i+5,100)
    y=0.1*np.cos(k_i*x)
    baseline=6*i/n-3
    y += baseline
    y[0]=baseline
    y[-1]=baseline
    sources.append(ColumnDataSource(data=dict(x=x, y=y)))
for i in range(n):
    glyph = Patch(x='x',y='y',fill_color="#D30982", fill_alpha=0.6, line_alpha = 0)
    plot.add_glyph(sources[n-1-i],glyph)

#set data for labels
x_label = [5.5 for _ in range(n)]
y_label = [6*i/n-3 for i in range(n)]
delta_d = []
delta_d_wave = []
for i in range(n):
    d1 = np.sqrt((y[i]-a_i)**2 + 5**2)
    d2 = np.sqrt((y[i]+a_i)**2 + 5**2)
    delta_d.append(abs(d1-d2))
    delta_d_wave.append(abs(d1-d2)/wavelength_i)

#hover description
description_source = ColumnDataSource(data=dict(x=x_label,y=y_label,delta_d=delta_d, delta_d_wave=delta_d_wave))

#plot labels
plot.rect('x','y',1,0.2,source = description_source, fill_alpha=0, line_alpha=0)
    
#build slit rectangles
top_height= 3-a_i/2 - 0.1
middle_height= a_i-0.2
bottom_height= top_height
rect_sources=[ColumnDataSource(data=dict(x=[0],y=[3-top_height/2],width=[0.2],height=[top_height])),
              ColumnDataSource(data=dict(x=[0],y=[0],width=[0.2],height=[middle_height])),
              ColumnDataSource(data=dict(x=[0],y=[-3 + bottom_height/2],width=[0.2],height=[bottom_height]))]

rects = [Rect(x='x', y='y', width='width', height='height') for _ in range(3)]
for i in range(3):
    plot.add_glyph(rect_sources[i],rects[i])
    
#build sliders
reference_point = Slider(start=-3, end=3, value=0, step=.1, title="Reference Point")
wavelength_slider = Slider(start=0.1, end=2, value=wavelength_i, step=.1, title="Wavelength (\u03BB)")
a_slider = Slider(start=0, end=3, value=1, step=0.1,title="a")

#update function
callback = CustomJS(args=dict(sources=sources, description_source=description_source,
                              wave=wavelength_slider, a_s=a_slider),
                    code="""
                    
    function f(d1,d2,k,shift) {
        return Math.cos(k*(d1+shift))+Math.cos(k*(d2+shift));
    } 
    
    var description_data = description_source.data;
    var delta_d = description_data['delta_d'];
    var delta_d_wave = description_data['delta_d_wave']
    
    for (var i=0;i<sources.length;i++) {
        
        const baseline = 6*i/sources.length-3;
        const data = sources[i].data;
        const a = a_s.value/2;
        const wavelength = wave.value;
        const k = 2*Math.PI/wave.value;
    
        var d1 = Math.sqrt(5**2 + (baseline+a)**2);
        var d2 = Math.sqrt(5**2 + (baseline-a)**2);
        delta_d[i]=Math.abs(d1-d2).toFixed(2);
        delta_d_wave[i]=(Math.abs(d1-d2)/wavelength).toFixed(2);
        
        const y = data['y'];
        var shift=0;
    
        for (var j=0; j< y.length;j++) {
            shift = (j/y.length); 
            y[j]=0.1*f(d1,d2,k,shift) + baseline;
        }
        
        y[0]=baseline;
        y[y.length-1]=baseline;
        sources[i].change.emit();
    }
    description_source.change.emit();

                    """)

callback2 = CustomJS(args=dict(sources=rect_sources, a_s = a_slider),
                     code = """
                     
     const a=a_s.value;
     var data0 = sources[0].data;
     var data1 = sources[1].data;
     var data2 = sources[2].data;
     
     var height_top = data0['height']
     height_top[0] = 3 - a/2 - 0.1;
     var pos_top = data0['y']
     pos_top[0] = 3 - height_top/2
     
     var height_middle = data1['height']
     height_middle[0] = a - 0.2
     
     var height_bottom = data2['height']
     height_bottom[0] = 3 - a/2 - 0.1;
     var pos_bottom = data2['y']
     pos_bottom[0] = -3 + height_bottom/2;
     
     sources[0].change.emit();
     sources[1].change.emit();
     sources[2].change.emit();
                     """)

callback3 = CustomJS(args=dict(sources=line_sources, a_s = a_slider, y_s = reference_point),
                     code = """
     const a = a_s.value;
     const y = y_s.value;
     
     var data0 = sources[0].data;
     var data1 = sources[1].data;
     
     var y0 = data0['y'];
     var y1 = data1['y'];
     
     y0[0] = a/2;
     y0[1] = y;
     y1[0] = -a/2;
     y1[1] = y;
     
     sources[0].change.emit();
     sources[1].change.emit();
                     """)

a_slider.js_on_change('value', callback, callback2, callback3)
wavelength_slider.js_on_change('value', callback)
reference_point.js_on_change('value', callback3)

col = column(a_slider, wavelength_slider, reference_point)
layout = row(plot, col)
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("slider.html", title="slider.py example")
output_notebook(hide_banner=True)

show(layout,notebook_handle=True)