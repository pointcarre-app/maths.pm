#!/usr/bin/env python
"""
Bokeh Server App with Linked Plots
Run with: bokeh serve 05_linked_plots.py
Then open: http://localhost:5006/05_linked_plots
"""

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.layouts import column, gridplot
import numpy as np
import pandas as pd

# Generate sample data
n = 500
np.random.seed(42)

# Create correlated data
x = np.random.randn(n)
y = 2 * x + np.random.randn(n) * 0.5
z = x + y + np.random.randn(n) * 0.3
w = np.sin(x) + np.random.randn(n) * 0.2

df = pd.DataFrame({"x": x, "y": y, "z": z, "w": w, "index": range(n)})

# Create shared data source
source = ColumnDataSource(df)

# Common tools
TOOLS = "pan,wheel_zoom,box_select,lasso_select,reset,save"

# Create plots
p1 = figure(title="X vs Y", width=400, height=400, tools=TOOLS, toolbar_location="above")
p1.scatter(
    "x",
    "y",
    source=source,
    size=5,
    alpha=0.6,
    selection_color="red",
    selection_alpha=1.0,
    nonselection_alpha=0.2,
)

p2 = figure(title="X vs Z", width=400, height=400, tools=TOOLS, toolbar_location="above")
p2.scatter(
    "x",
    "z",
    source=source,
    size=5,
    alpha=0.6,
    color="green",
    selection_color="red",
    selection_alpha=1.0,
    nonselection_alpha=0.2,
)

p3 = figure(title="Y vs Z", width=400, height=400, tools=TOOLS, toolbar_location="above")
p3.scatter(
    "y",
    "z",
    source=source,
    size=5,
    alpha=0.6,
    color="blue",
    selection_color="red",
    selection_alpha=1.0,
    nonselection_alpha=0.2,
)

p4 = figure(
    title="X vs W (sin relationship)", width=400, height=400, tools=TOOLS, toolbar_location="above"
)
p4.scatter(
    "x",
    "w",
    source=source,
    size=5,
    alpha=0.6,
    color="purple",
    selection_color="red",
    selection_alpha=1.0,
    nonselection_alpha=0.2,
)

# Add hover tools
hover1 = HoverTool(tooltips=[("Index", "@index"), ("X", "@x{0.00}"), ("Y", "@y{0.00}")])
hover2 = HoverTool(tooltips=[("Index", "@index"), ("X", "@x{0.00}"), ("Z", "@z{0.00}")])
hover3 = HoverTool(tooltips=[("Index", "@index"), ("Y", "@y{0.00}"), ("Z", "@z{0.00}")])
hover4 = HoverTool(tooltips=[("Index", "@index"), ("X", "@x{0.00}"), ("W", "@w{0.00}")])

p1.add_tools(hover1)
p2.add_tools(hover2)
p3.add_tools(hover3)
p4.add_tools(hover4)

# Create histogram for selected data
hist_fig = figure(
    title="Distribution of Selected Points", width=800, height=200, toolbar_location="above"
)

# Initial histogram (empty)
hist_source = ColumnDataSource(data=dict(top=[], left=[], right=[]))
hist_fig.quad(
    top="top",
    bottom=0,
    left="left",
    right="right",
    source=hist_source,
    fill_color="navy",
    alpha=0.5,
)

# Statistics display
stats_div = Div(text="<b>Selection Statistics:</b> No points selected", width=800)

# Instructions
instructions = Div(
    text="""
    <h3>Instructions:</h3>
    <ul>
        <li><b>Box Select:</b> Click and drag to select rectangular region</li>
        <li><b>Lasso Select:</b> Click and draw freeform selection</li>
        <li><b>Pan:</b> Click and drag with pan tool</li>
        <li><b>Zoom:</b> Scroll to zoom</li>
        <li><b>Reset:</b> Click reset to clear selection and reset view</li>
    </ul>
    <p>Selection is <b>linked across all plots</b> - selecting in one plot highlights the same points in all plots!</p>
    """,
    width=800,
)


def update_histogram_and_stats(attr, old, new):
    """Update histogram and statistics based on selection"""
    selected = source.selected.indices

    if selected:
        # Get selected data
        selected_data = df.iloc[selected]

        # Update histogram for X values
        hist, edges = np.histogram(selected_data["x"], bins=30)
        hist_source.data = dict(top=hist, left=edges[:-1], right=edges[1:])

        # Update statistics
        stats_text = f"""
        <h3>Selection Statistics ({len(selected)} points):</h3>
        <table style="width:100%">
        <tr>
            <th>Variable</th>
            <th>Mean</th>
            <th>Std</th>
            <th>Min</th>
            <th>Max</th>
        </tr>
        <tr>
            <td><b>X</b></td>
            <td>{selected_data["x"].mean():.3f}</td>
            <td>{selected_data["x"].std():.3f}</td>
            <td>{selected_data["x"].min():.3f}</td>
            <td>{selected_data["x"].max():.3f}</td>
        </tr>
        <tr>
            <td><b>Y</b></td>
            <td>{selected_data["y"].mean():.3f}</td>
            <td>{selected_data["y"].std():.3f}</td>
            <td>{selected_data["y"].min():.3f}</td>
            <td>{selected_data["y"].max():.3f}</td>
        </tr>
        <tr>
            <td><b>Z</b></td>
            <td>{selected_data["z"].mean():.3f}</td>
            <td>{selected_data["z"].std():.3f}</td>
            <td>{selected_data["z"].min():.3f}</td>
            <td>{selected_data["z"].max():.3f}</td>
        </tr>
        <tr>
            <td><b>W</b></td>
            <td>{selected_data["w"].mean():.3f}</td>
            <td>{selected_data["w"].std():.3f}</td>
            <td>{selected_data["w"].min():.3f}</td>
            <td>{selected_data["w"].max():.3f}</td>
        </tr>
        </table>
        """
        stats_div.text = stats_text
        hist_fig.title.text = f"Distribution of X for {len(selected)} Selected Points"

        print(f"Selected {len(selected)} points")
    else:
        # Clear histogram and stats
        hist_source.data = dict(top=[], left=[], right=[])
        stats_div.text = "<b>Selection Statistics:</b> No points selected"
        hist_fig.title.text = "Distribution of Selected Points"
        print("Selection cleared")


# Attach selection callback
source.selected.on_change("indices", update_histogram_and_stats)

# Create layout
plots = gridplot([[p1, p2], [p3, p4]], toolbar_location="above")
layout = column(instructions, plots, hist_fig, stats_div)

# Add to document
curdoc().add_root(layout)
curdoc().title = "Linked Plots Demo"

print("Bokeh server app started - Linked Plots Demo")
