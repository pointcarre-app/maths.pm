"""
Interactive State Explorer (Bokeh)

Bokeh server app for exploring COVID-19 data by state and time period.

Run with: bokeh serve covid_bokeh_10.py
"""

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, Select, RangeSlider, 
                         HoverTool, Span)
from bokeh.plotting import figure
from datetime import timedelta

from covid_data_prep import prepare_full_dataset, TRANSITION_DATE


# Load all data once
print("Loading data for State Explorer...")
full_data = prepare_full_dataset()

# Extract metadata
min_date = full_data['date'].min()
max_date = full_data['date'].max()
total_days = (max_date - min_date).days

# Get initial data (National, full period)
initial_data = full_data[full_data['state'] == 'National'].copy()

# Create data source for display
display_source = ColumnDataSource(data={
    'date': initial_data['date'],
    'deaths_7day': initial_data['deaths_7day'],
    'cases_7day': initial_data['cases_7day'],
    'daily_deaths': initial_data['daily_deaths'],
    'daily_cases': initial_data['daily_cases']
})

# Create figure
p = figure(
    title='COVID-19 Deaths - National',
    x_axis_label='Date',
    y_axis_label='Daily Deaths (7-day average)',
    x_axis_type='datetime',
    width=900,
    height=450,
    tools='pan,wheel_zoom,box_zoom,reset,save'
)

# Add line
line = p.line('date', 'deaths_7day', source=display_source, 
              line_width=3, color='darkred', alpha=0.8)

# Add presidential transition line
transition_line = Span(
    location=TRANSITION_DATE, 
    dimension='height',
    line_color='blue', 
    line_dash='dashed', 
    line_width=2, 
    line_alpha=0.6
)
p.add_layout(transition_line)

# Add hover tool
hover = HoverTool(
    tooltips=[
        ('Date', '@date{%F}'),
        ('Deaths (7-day)', '@deaths_7day{0,0.0}'),
        ('Cases (7-day)', '@cases_7day{0,0.0}'),
    ],
    formatters={'@date': 'datetime'},
    mode='vline'
)
p.add_tools(hover)

# Style
p.title.text_font_size = '14pt'
p.title.align = 'center'
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3

# Create widgets
# State selector
states_list = ['National'] + sorted(
    full_data[full_data['state'] != 'National']['state'].unique().tolist()
)
state_select = Select(
    title='Select State:',
    value='National',
    options=states_list,
    width=300
)

# Time period slider
date_slider = RangeSlider(
    title='Time Period (days since January 2020):',
    start=0,
    end=total_days,
    value=(0, total_days),
    step=1,
    width=600
)

# Python callback function
def update_plot():
    """Filter data and update the plot based on selected state and date range."""
    selected_state = state_select.value
    start_day, end_day = date_slider.value
    
    # Calculate actual dates
    start_date = min_date + timedelta(days=start_day)
    end_date = min_date + timedelta(days=end_day)
    
    # Filter the full dataset
    filtered = full_data[
        (full_data['state'] == selected_state) &
        (full_data['date'] >= start_date) &
        (full_data['date'] <= end_date)
    ].copy()
    
    # Update data source
    display_source.data = {
        'date': filtered['date'],
        'deaths_7day': filtered['deaths_7day'],
        'cases_7day': filtered['cases_7day'],
        'daily_deaths': filtered['daily_deaths'],
        'daily_cases': filtered['daily_cases']
    }
    
    # Update plot title
    p.title.text = f'COVID-19 Deaths - {selected_state}'

# Attach callbacks
state_select.on_change('value', lambda attr, old, new: update_plot())
date_slider.on_change('value', lambda attr, old, new: update_plot())

# Layout
layout = column(
    row(state_select),
    date_slider,
    p
)

# Add to document
curdoc().add_root(layout)
curdoc().title = "COVID-19 State Explorer"

print("State Explorer app ready!")
