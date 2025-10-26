"""
Cases vs Deaths Scatter Analysis

Scatter plot showing relationship between total cases and deaths by state.

Run with: python covid_matplotlib_03.py
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from covid_data_prep import prepare_full_dataset


print("Loading data...")
full_data = prepare_full_dataset()

# Calculate state-level totals
state_summary = full_data[full_data['state'] != 'National'].groupby('state').agg({
    'cases': 'max',
    'deaths': 'max'
}).reset_index()

# Calculate case fatality rate
state_summary['cfr'] = (state_summary['deaths'] / state_summary['cases'] * 100)

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Main scatter plot
scatter = ax.scatter(state_summary['cases'], state_summary['deaths'], 
                     s=100, alpha=0.6, edgecolors='black', linewidth=0.5,
                     color='steelblue')

# Add linear regression line
slope, intercept, r_value, p_value, std_err = linregress(
    state_summary['cases'], state_summary['deaths']
)
x_line = np.array([state_summary['cases'].min(), state_summary['cases'].max()])
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, 'b--', linewidth=2, alpha=0.7,
        label=f'Linear fit (R² = {r_value**2:.3f})')

# Label some interesting states
top_deaths = state_summary.nlargest(5, 'deaths')
for _, row in top_deaths.iterrows():
    ax.annotate(row['state'], 
                xy=(row['cases'], row['deaths']),
                xytext=(10, 10), textcoords='offset points',
                fontsize=9, alpha=0.7)

# Styling
ax.set_xlabel('Total Cases', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Deaths', fontsize=12, fontweight='bold')
ax.set_title('COVID-19 Cases vs Deaths by State', 
             fontsize=14, fontweight='bold', pad=20)

# Format axes
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))

ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='upper left')

plt.tight_layout()
plt.savefig('03_cases_vs_deaths_scatter.png', dpi=300, bbox_inches='tight')
print("Saved: 03_cases_vs_deaths_scatter.png")
print(f"\nCorrelation: R² = {r_value**2:.3f}")
plt.show()
