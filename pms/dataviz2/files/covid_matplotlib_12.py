"""
Time-Lagged Correlation Analysis

Shows correlation between cases and deaths at different time lags,
and displays aligned time series at optimal lag.

Run with: python 05_time_lagged_correlation.py
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

from covid_data_prep import prepare_full_dataset, TRANSITION_DATE


print("Loading data...")
full_data = prepare_full_dataset()

# Filter to national data
national = full_data[
    (full_data['state'] == 'National') &
    (full_data['cases_7day'].notna()) & 
    (full_data['deaths_7day'].notna())
].copy()

# Calculate correlations for different lags
max_lag = 35
lags = range(0, max_lag + 1)
correlations = []

print("Calculating correlations...")
for lag in lags:
    deaths_shifted = national['deaths_7day'].shift(-lag)
    valid_mask = deaths_shifted.notna()
    
    if valid_mask.sum() > 30:
        corr = national.loc[valid_mask, 'cases_7day'].corr(deaths_shifted[valid_mask])
        correlations.append(corr)
    else:
        correlations.append(np.nan)

# Find optimal lag
optimal_lag = int(np.nanargmax(correlations))
max_corr = np.nanmax(correlations)

print(f"Optimal lag: {optimal_lag} days (correlation: {max_corr:.3f})")

# Create figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Panel 1: Correlation function
ax1.plot(lags, correlations, 'o-', color='purple', linewidth=2, markersize=6)
ax1.axvline(x=optimal_lag, color='red', linestyle='--', 
            linewidth=2, alpha=0.7,
            label=f'Maximum correlation at {optimal_lag} days')
ax1.axhline(y=max_corr, color='red', linestyle=':', 
            linewidth=1, alpha=0.5)

ax1.set_xlabel('Lag (days)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Correlation Coefficient', fontsize=11, fontweight='bold')
ax1.set_title(f'Correlation: Cases vs Deaths\nMaximum Correlation = {max_corr:.3f} at {optimal_lag} days', 
              fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, max_lag)

# Panel 2: Time series with optimal lag
deaths_shifted_optimal = national['deaths_7day'].shift(-optimal_lag)

ax2.plot(national['date'], national['cases_7day'] / 100,  # Scale for visualization
         color='steelblue', linewidth=2, label='Daily Cases (÷100)', alpha=0.8)

ax2.plot(national['date'], deaths_shifted_optimal,
         color='darkred', linewidth=2, label=f'Daily Deaths (shifted {optimal_lag} days earlier)', 
         alpha=0.8)

ax2.axvline(x=TRANSITION_DATE, color='gray', linestyle='--', 
            linewidth=1.5, alpha=0.5, label='Presidential Transition')

ax2.set_ylabel('Count', fontsize=11, fontweight='bold')
ax2.set_xlabel('Date', fontsize=11, fontweight='bold')
ax2.set_title(f'Cases vs Deaths with Optimal Lag = {optimal_lag} days\n(Deaths shifted backward to align with cases)', 
              fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)

# Format x-axis
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('05_time_lagged_correlation.png', dpi=300, bbox_inches='tight')
print("Saved: 05_time_lagged_correlation.png")
plt.show()
