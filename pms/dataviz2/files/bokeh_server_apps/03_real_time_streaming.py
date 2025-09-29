#!/usr/bin/env python
"""
Bokeh Server App with Real-time Data Streaming
Run with: bokeh serve 03_real_time_streaming.py
Then open: http://localhost:5006/03_real_time_streaming
"""

from bokeh.plotting import figure, curdoc
from bokeh.models import Button, Slider, Div
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
import numpy as np
from datetime import datetime

# Global state
streaming_active = False
callback_id = None

# Create data source
source = ColumnDataSource(data=dict(x=[], y=[]))

# Create figure
p = figure(
    title="Real-time Data Streaming",
    width=800,
    height=400,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    x_axis_type="datetime",
)

# Add line
p.line("x", "y", source=source, line_width=2, color="blue", alpha=0.8)
p.circle("x", "y", source=source, size=4, color="red", alpha=0.5)

# Controls
start_button = Button(label="Start Streaming", button_type="success")
stop_button = Button(label="Stop Streaming", button_type="danger")
clear_button = Button(label="Clear Data", button_type="warning")

update_rate = Slider(start=100, end=2000, value=500, step=100, title="Update Rate (ms)")

window_size = Slider(start=50, end=500, value=200, step=50, title="Window Size (points)")

# Info display
info_div = Div(text="<b>Status:</b> Ready to stream")
stats_div = Div(text="<b>Data Points:</b> 0")


# Streaming function
def stream_data():
    """Generate and stream new data point"""
    global source

    # Generate new data
    new_x = datetime.now()
    new_y = np.random.randn() + 10 * np.sin(len(source.data["x"]) * 0.1)

    # Get current data
    x_data = list(source.data["x"])
    y_data = list(source.data["y"])

    # Add new point
    x_data.append(new_x)
    y_data.append(new_y)

    # Maintain window size
    max_points = int(window_size.value)
    if len(x_data) > max_points:
        x_data = x_data[-max_points:]
        y_data = y_data[-max_points:]

    # Update source
    source.data = dict(x=x_data, y=y_data)

    # Update stats
    stats_div.text = f"""
    <b>Data Points:</b> {len(x_data)}<br>
    <b>Latest Value:</b> {new_y:.3f}<br>
    <b>Mean:</b> {np.mean(y_data):.3f}<br>
    <b>Std:</b> {np.std(y_data):.3f}
    """

    print(f"Streamed point {len(x_data)}: {new_y:.3f}")


# Button callbacks
def start_streaming():
    """Start the data streaming"""
    global streaming_active, callback_id

    if not streaming_active:
        streaming_active = True
        callback_id = curdoc().add_periodic_callback(stream_data, int(update_rate.value))
        info_div.text = "<b>Status:</b> <span style='color:green'>Streaming...</span>"
        print("Started streaming")


def stop_streaming():
    """Stop the data streaming"""
    global streaming_active, callback_id

    if streaming_active:
        streaming_active = False
        if callback_id:
            curdoc().remove_periodic_callback(callback_id)
        info_div.text = "<b>Status:</b> <span style='color:red'>Stopped</span>"
        print("Stopped streaming")


def clear_data():
    """Clear all data"""
    global source
    source.data = dict(x=[], y=[])
    stats_div.text = "<b>Data Points:</b> 0"
    info_div.text = "<b>Status:</b> Data cleared"
    print("Cleared data")


def update_rate_change(attr, old, new):
    """Update streaming rate"""
    global callback_id, streaming_active

    if streaming_active:
        # Restart with new rate
        stop_streaming()
        start_streaming()
        print(f"Update rate changed to {new}ms")


# Attach callbacks
start_button.on_click(start_streaming)
stop_button.on_click(stop_streaming)
clear_button.on_click(clear_data)
update_rate.on_change("value", update_rate_change)

# Create layout
controls = column(
    start_button, stop_button, clear_button, update_rate, window_size, info_div, stats_div
)

layout = row(controls, p)

# Add to document
curdoc().add_root(layout)
curdoc().title = "Real-time Streaming Demo"

print("Bokeh server app started - Real-time Streaming Demo")
