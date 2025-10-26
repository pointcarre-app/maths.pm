"""
Cumulative Deaths by Presidential Administration

Static matplotlib visualization comparing COVID-19 deaths
during Trump and Biden administrations.

Run with: python covid_matplotlib_01.py
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

from covid_data_prep import prepare_full_dataset, TRANSITION_DATE


print("Loading data...")
full_data = prepare_full_dataset()

# Filter to national data
national = full_data[full_data['state'] == 'National'].copy().sort_values('date')

# Calculate cumulative deaths from daily deaths
national['cumulative_deaths'] = national['daily_deaths'].cumsum()

# Define analysis periods
trump_start = datetime(2020, 3, 1)
biden_analysis_end = datetime(2022, 5, 11)

# Filter to analysis period
chart_data = national[
    (national['date'] >= trump_start) & 
    (national['date'] <= biden_analysis_end)
].copy()

# Split by administration
trump_data = chart_data[chart_data['date'] < TRANSITION_DATE]
biden_data = chart_data[chart_data['date'] >= TRANSITION_DATE]

# Create figure
fig, ax = plt.subplots(figsize=(14, 8))

# Colors
trump_color = '#E74C3C'
biden_color = '#3498DB'

# Plot cumulative deaths
ax.plot(trump_data['date'], trump_data['cumulative_deaths'], 
        color=trump_color, linewidth=3, label='Trump Administration')

ax.plot(biden_data['date'], biden_data['cumulative_deaths'], 
        color=biden_color, linewidth=3, label='Biden Administration')

# Presidential transition line
ax.axvline(x=TRANSITION_DATE, color='black', linestyle='-', 
           linewidth=2, alpha=0.8)

# Calculate statistics
trump_final_deaths = trump_data['cumulative_deaths'].iloc[-1]
biden_final_deaths = biden_data['cumulative_deaths'].iloc[-1]
biden_period_deaths = biden_final_deaths - trump_final_deaths

# Annotations
ax.annotate(f'Trump era:\n{trump_final_deaths:,.0f} deaths\n(327 days)', 
            xy=(datetime(2020, 8, 1), (trump_final_deaths + biden_final_deaths)/3),
            fontsize=11, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=trump_color, alpha=0.1))

ax.annotate(f'Biden era:\n{biden_period_deaths:,.0f} additional deaths\n({(biden_analysis_end - TRANSITION_DATE).days} days)', 
            xy=(datetime(2021, 8, 1), (trump_final_deaths + biden_final_deaths)/3),
            fontsize=11, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=biden_color, alpha=0.1))

ax.annotate('Presidential\nTransition\nJan 20, 2021', 
            xy=(TRANSITION_DATE, trump_final_deaths),
            xytext=(datetime(2021, 3, 1), trump_final_deaths - 50000),
            arrowprops=dict(arrowstyle='->', color='black', alpha=0.7),
            fontsize=10, ha='center')

# Styling
ax.set_title('COVID-19 Deaths in the United States\nCumulative Deaths by Presidential Administration', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Cumulative Deaths', fontsize=12, fontweight='bold')

# Format axes
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))

# Grid and styling
ax.grid(True, alpha=0.2, linestyle='-')
ax.set_facecolor('#FAFAFA')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.legend(loc='upper left', fontsize=11, frameon=False)

plt.tight_layout()
plt.savefig('01_cumulative_deaths.png', dpi=300, bbox_inches='tight')
print("Saved: 01_cumulative_deaths.png")
plt.show()
