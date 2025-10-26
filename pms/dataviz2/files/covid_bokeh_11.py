"""
Trend Decomposition Dashboard (Bokeh)

Bokeh server app for decomposing COVID-19 death trends into components.

Run with: bokeh serve covid_bokeh_11.py
"""

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, CheckboxGroup, HoverTool, 
                         Span, Label)
from bokeh.plotting import figure
from statsmodels.tsa.seasonal import STL

from covid_data_prep import (prepare_full_dataset, MAJOR_EVENTS, 
                              TRUMP_START, TRANSITION_DATE)


print("Loading data for Decomposition Dashboard...")
full_data = prepare_full_dataset()

# Filter to national data in analysis period
national = full_data[
    (full_data['state'] == 'National') &
    (full_data['date'] >= TRUMP_START) & 
    (full_data['daily_deaths'].notna())
].copy()

# Set date as index for STL
decomp_data = national.set_index('date')

# Perform two-stage STL decomposition on raw daily deaths
print("Performing STL decomposition...")

# Stage 1: Extract weekly seasonality
stl_weekly = STL(
    decomp_data['daily_deaths'],
    seasonal=7,
    period=7,
    trend=None
)
result_weekly = stl_weekly.fit()
weekly_seasonal = result_weekly.seasonal
detrended_weekly = decomp_data['daily_deaths'] - weekly_seasonal

# Stage 2: Extract annual seasonality with moderate trend
stl_annual = STL(
    detrended_weekly,
    seasonal=53,
    period=7,
    trend=91
)
result_annual = stl_annual.fit()

annual_seasonal = result_annual.seasonal
trend = result_annual.trend
residual = result_annual.resid

# Total seasonal component
total_seasonal = weekly_seasonal + annual_seasonal

# Verify reconstruction
reconstructed = trend + total_seasonal + residual
print(f"Max reconstruction error: {abs(decomp_data['daily_deaths'] - reconstructed).max():.2f}")

# Create data sources for each component
source_original = ColumnDataSource(data={
    'date': decomp_data.index,
    'value': decomp_data['daily_deaths'].values
})

source_trend = ColumnDataSource(data={
    'date': decomp_data.index,
    'value': trend.values
})

source_weekly = ColumnDataSource(data={
    'date': decomp_data.index,
    'value': weekly_seasonal.values
})

source_annual = ColumnDataSource(data={
    'date': decomp_data.index,
    'value': annual_seasonal.values
})

source_total_seasonal = ColumnDataSource(data={
    'date': decomp_data.index,
    'value': total_seasonal.values
})

source_residual = ColumnDataSource(data={
    'date': decomp_data.index,
    'value': residual.values
})

# Create figure
p = figure(
    title='RAW Daily Deaths Decomposition with Health & Political Events',
    x_axis_type='datetime',
    width=1100,
    height=550,
    tools='pan,wheel_zoom,box_zoom,reset,save'
)

# Plot all components (store references for visibility control)
line_original = p.line('date', 'value', source=source_original, 
                       line_width=1.5, color='#2c3e50', alpha=0.7, 
                       legend_label='Raw Daily Deaths', visible=True)

line_trend = p.line('date', 'value', source=source_trend, 
                    line_width=3, color='#e74c3c', alpha=0.9, 
                    legend_label='Trend (90 days)', visible=True)

line_weekly = p.line('date', 'value', source=source_weekly, 
                     line_width=1.5, color='#3498db', alpha=0.8,
                     legend_label='Weekly Pattern', visible=True)

line_annual = p.line('date', 'value', source=source_annual, 
                     line_width=2, color='#27ae60', alpha=0.8,
                     legend_label='Annual (Winter/Summer)', visible=False)

line_total_seasonal = p.line('date', 'value', source=source_total_seasonal,
                             line_width=2, color='#16a085', alpha=0.7, line_dash='dashed',
                             legend_label='Total Seasonal', visible=False)

line_residual = p.line('date', 'value', source=source_residual, 
                       line_width=1.5, color='#9b59b6', alpha=0.8,
                       legend_label='Residual', visible=True)

# Store line references for callback
lines = [line_original, line_trend, line_weekly, line_annual, line_total_seasonal, line_residual]

# Add event markers and labels
for event in MAJOR_EVENTS:
    # Style based on event type
    if event['type'] == 'political':
        line_dash = 'dotted'
        line_width = 2
    elif event['type'] == 'transition':
        line_dash = 'dashed'
        line_width = 3
    else:
        line_dash = 'dotted'
        line_width = 1.5
    
    span = Span(
        location=event['date'],
        dimension='height',
        line_color=event['color'],
        line_dash=line_dash,
        line_width=line_width,
        line_alpha=0.7
    )
    p.add_layout(span)
    
    # Add label
    label = Label(
        x=event['date'],
        y=4500,
        text=event['label'],
        text_font_size='8pt',
        text_color=event['color'],
        text_alpha=0.9,
        angle=90,
        angle_units='deg',
        text_baseline='bottom',
        text_align='left'
    )
    p.add_layout(label)

# Add zero reference line
zero_span = Span(location=0, dimension='width', line_color='gray', 
                 line_dash='solid', line_width=1, line_alpha=0.3)
p.add_layout(zero_span)

# Style the plot
p.yaxis.axis_label = 'Daily Deaths (RAW, not smoothed)'
p.xaxis.axis_label = 'Date'
p.title.text_font_size = '12pt'
p.title.align = 'center'
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3

# Configure legend
p.legend.location = "top_left"
p.legend.click_policy = "hide"
p.legend.background_fill_alpha = 0.95

# Add hover tool
hover = HoverTool(
    tooltips=[
        ('Date', '@date{%F}'),
        ('Deaths', '@value{0,0}')
    ],
    formatters={'@date': 'datetime'},
    mode='vline'
)
p.add_tools(hover)

# Create checkbox widget for toggling visibility
checkbox = CheckboxGroup(
    labels=['Raw Deaths', 'Trend', 'Weekly', 'Annual', 'Total Seasonal', 'Residual'],
    active=[0, 1, 2, 5],
    width=600
)

# Python callback for visibility control
def update_visibility(attr, old, new):
    """Toggle line visibility based on checkbox selection."""
    for i, line in enumerate(lines):
        line.visible = i in checkbox.active

checkbox.on_change('active', update_visibility)

# Print residual statistics
trump_residuals = residual[residual.index < TRANSITION_DATE]
biden_residuals = residual[residual.index >= TRANSITION_DATE]

print("\n=== RESIDUAL STATISTICS ===")
print(f"Trump period: mean={trump_residuals.mean():.1f}, std={trump_residuals.std():.1f}")
print(f"Biden period: mean={biden_residuals.mean():.1f}, std={biden_residuals.std():.1f}")

# Layout
layout = column(
    p,
    row(column(checkbox, width=600))
)

# Add to document
curdoc().add_root(layout)
curdoc().title = "COVID-19 Decomposition"

print("Decomposition Dashboard ready!")