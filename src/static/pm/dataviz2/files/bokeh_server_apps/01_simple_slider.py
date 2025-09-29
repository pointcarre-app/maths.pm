#!/usr/bin/env python
"""
Simple Bokeh Server App with Slider
Run with: bokeh serve 01_simple_slider.py
Then open: http://localhost:5006/01_simple_slider
"""

from bokeh.plotting import figure, curdoc
from bokeh.models import Slider
from bokeh.layouts import column
import numpy as np

# Create data
x = np.linspace(0, 4 * np.pi, 100)

# Create figure
p = figure(
    title="Interactive Sine Wave with Amplitude Control",
    width=800,
    height=400,
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Initial plot
y = np.sin(x)
line = p.line(x, y, line_width=2, color="navy", alpha=0.8)

# Create slider
amplitude_slider = Slider(start=0.1, end=3.0, value=1.0, step=0.1, title="Amplitude")


# Define callback
def update_amplitude(attr, old, new):
    """Update the plot when slider changes"""
    y = amplitude_slider.value * np.sin(x)
    line.data_source.data = {"x": x, "y": y}
    print(f"Amplitude changed from {old} to {new}")


# Attach callback to slider
amplitude_slider.on_change("value", update_amplitude)

# Create layout
layout = column(amplitude_slider, p)

# Add to document
curdoc().add_root(layout)
curdoc().title = "Simple Slider Demo"

print("Bokeh server app started - Simple Slider Demo")
