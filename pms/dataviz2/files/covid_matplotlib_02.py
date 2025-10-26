"""
Top 5 States by Deaths - Small Multiples

Shows death trends for the 5 most affected states using small multiples.

Run with: python covid_matplotlib_02.py
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

from covid_data_prep import prepare_full_dataset, TRANSITION_DATE


print("Loading data...")
full_data = prepare_full_dataset()

# Get top 5 states by total deaths
state_totals = full_data[full_data['state'] != 'National'].groupby('state')['deaths'].max().sort_values(ascending=False)
top_5_states = state_totals.head(5).index.tolist()

print("Top 5 states by total deaths:")
for i, state in enumerate(top_5_states, 1):
    print(f"  {i}. {state}: {state_totals[state]:,}")

# Create figure with subplots
fig, axes = plt.subplots(5, 1, figsize=(12, 12), sharex=True)
fig.suptitle('COVID-19 Deaths: Top 5 Most Affected States\n7-Day Moving Average', 
             fontsize=14, fontweight='bold', y=0.995)

for idx, state in enumerate(top_5_states):
    ax = axes[idx]
    
    # Get state data
    state_data = full_data[full_data['state'] == state].sort_values('date').copy()
    
    # Plot 7-day average
    ax.plot(state_data['date'], state_data['deaths_7day'], 
            color='darkred', linewidth=2)
    
    # Add presidential transition line
    ax.axvline(x=TRANSITION_DATE, color='gray', linestyle='--', 
               linewidth=1, alpha=0.5)
    
    # Styling
    total_deaths = state_data['deaths'].max()
    ax.set_ylabel('Daily Deaths', fontsize=10)
    ax.set_title(f'{state} (Total: {total_deaths:,.0f})', 
                 fontsize=11, fontweight='bold', loc='left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)

# Format x-axis only on bottom plot
axes[-1].set_xlabel('Date', fontsize=11)
axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('02_top_states_small_multiples.png', dpi=300, bbox_inches='tight')
print("Saved: 02_top_states_small_multiples.png")
plt.show()
