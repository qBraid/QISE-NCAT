import numpy as np
from bokeh.io import output_notebook, show, curdoc
from bokeh.themes import built_in_themes
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_file, show

#global formatting
#curdoc().theme = 'dark_minimal'
output_notebook(hide_banner=True)


wavelength_i=2*np.pi
k_i=2*np.pi/wavelength_i
x = np.linspace(-np.pi*2,np.pi*2, 500)
y = np.cos(k_i*x)

source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(x_range=(-np.pi*2,np.pi*2), y_range=(-3.1,3.1), outer_width=600, outer_height=400)

plot.toolbar.logo=None
plot.toolbar_location=None
plot.toolbar.active_drag = None
plot.toolbar.active_scroll = None
plot.toolbar.active_tap = None

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, line_color='#9A11DA')

amp_slider = Slider(start=0.0, end=3, value=1, step=.1, title="Amplitude")
wavelength_slider = Slider(start=np.pi/4, end=4*np.pi, value=wavelength_i, step=.1, title="Wavelength")
phase_slider = Slider(start=0, end=6.4, value=0, step=np.pi/8, title="Phase Shift")

callback = CustomJS(args=dict(source=source, amp=amp_slider, wave=wavelength_slider, phase=phase_slider),
                    code="""
    const data = source.data;
    const A = amp.value;
    const k = 2*Math.PI/wave.value;
    const phi = phase.value;
    const x = data['x']
    const y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = A*Math.cos(k*x[i]-phi);
    }
    source.change.emit();
""")

amp_slider.js_on_change('value', callback)
wavelength_slider.js_on_change('value', callback)
phase_slider.js_on_change('value', callback)

col = column(amp_slider, wavelength_slider, phase_slider)
layout = row(plot, col)
#plot.sizing_mode='scale_width'
#layout.sizing_mode='scale_width'

#output_file("slider.html", title="slider.py example")
#output_notebook(hide_banner=True)

show(layout,notebook_handle=True)