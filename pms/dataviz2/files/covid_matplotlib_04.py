"""
Death Rate Distributions by Administration

Violin plots and CDFs comparing death rate distributions between administrations.

Run with: python covid_matplotlib_04.py
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from covid_data_prep import prepare_full_dataset, TRUMP_START, TRANSITION_DATE


print("Loading data...")
full_data = prepare_full_dataset()

# Filter to national data
national = full_data[full_data['state'] == 'National'].sort_values('date').copy()

# Split by administration
trump_data = national[
    (national['date'] >= TRUMP_START) & 
    (national['date'] < TRANSITION_DATE)
].copy()

biden_data = national[national['date'] >= TRANSITION_DATE].copy()

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Colors
colors = ['#E74C3C', '#3498DB']

# Panel 1: Violin plots
ax1 = axes[0]
box_data = [
    trump_data['deaths_7day'].dropna(),
    biden_data['deaths_7day'].dropna()
]

positions = [1, 2]
parts = ax1.violinplot(box_data, positions=positions, showmeans=True, showmedians=True)

for pc, color in zip(parts['bodies'], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.6)

ax1.set_xticks(positions)
ax1.set_xticklabels(['Trump', 'Biden'])
ax1.set_ylabel('Daily Deaths (7-day average)', fontsize=11, fontweight='bold')
ax1.set_title('Distribution Comparison\n(Violin Plot)', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Panel 2: Cumulative distribution functions
ax2 = axes[1]
trump_sorted = np.sort(trump_data['deaths_7day'].dropna())
biden_sorted = np.sort(biden_data['deaths_7day'].dropna())

trump_cdf = np.arange(1, len(trump_sorted) + 1) / len(trump_sorted)
biden_cdf = np.arange(1, len(biden_sorted) + 1) / len(biden_sorted)

ax2.plot(trump_sorted, trump_cdf, color=colors[0], linewidth=2.5, label='Trump')
ax2.plot(biden_sorted, biden_cdf, color=colors[1], linewidth=2.5, label='Biden')

ax2.set_xlabel('Daily Deaths (7-day average)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Cumulative Probability', fontsize=11, fontweight='bold')
ax2.set_title('Cumulative Distribution Functions', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('04_death_rate_distributions.png', dpi=300, bbox_inches='tight')
print("Saved: 04_death_rate_distributions.png")

# Print summary statistics
print("\n=== SUMMARY STATISTICS ===")
print(f"\nTrump Administration:")
print(f"  Mean: {trump_data['deaths_7day'].mean():.0f}")
print(f"  Median: {trump_data['deaths_7day'].median():.0f}")
print(f"  Std: {trump_data['deaths_7day'].std():.0f}")

print(f"\nBiden Administration:")
print(f"  Mean: {biden_data['deaths_7day'].mean():.0f}")
print(f"  Median: {biden_data['deaths_7day'].median():.0f}")
print(f"  Std: {biden_data['deaths_7day'].std():.0f}")

plt.show()
