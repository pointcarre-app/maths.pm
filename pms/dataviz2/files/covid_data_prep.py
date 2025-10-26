"""
COVID-19 Data Preparation Module

Handles all data loading and preprocessing.
Returns a single comprehensive dataset that apps can filter as needed.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Constants
DATA_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/refs/heads/master/us-states.csv"
TRANSITION_DATE = datetime(2021, 1, 20)
TRUMP_START = datetime(2020, 3, 1)

# Key dates and events for annotations
MAJOR_EVENTS = [
    {'date': datetime(2020, 3, 11), 'label': 'WHO Pandemic', 'color': '#e74c3c', 'type': 'health'},
    {'date': datetime(2020, 3, 27), 'label': 'CARES Act', 'color': '#8e44ad', 'type': 'political'},
    {'date': datetime(2020, 11, 3), 'label': 'Election Day', 'color': '#8e44ad', 'type': 'political'},
    {'date': datetime(2020, 12, 14), 'label': 'First Vaccine', 'color': '#27ae60', 'type': 'health'},
    {'date': TRANSITION_DATE, 'label': 'Transition', 'color': '#3498db', 'type': 'transition'},
    {'date': datetime(2021, 3, 11), 'label': 'Stimulus Bill', 'color': '#8e44ad', 'type': 'political'},
    {'date': datetime(2021, 7, 1), 'label': 'Delta Wave', 'color': '#e67e22', 'type': 'health'},
    {'date': datetime(2021, 12, 1), 'label': 'Omicron', 'color': '#9b59b6', 'type': 'health'},
]


def prepare_full_dataset(filepath=None):
    """
    Load and prepare the complete COVID-19 dataset.
    
    This single function handles all data preparation:
    - Loads raw data
    - Aggregates to state and national levels
    - Calculates daily metrics from cumulative data
    - Computes 7-day moving averages
    - Returns everything in one DataFrame
    
    Parameters:
    -----------
    filepath : str, optional
        Local path to CSV file. If None, downloads from NYT GitHub.
    
    Returns:
    --------
    pd.DataFrame
        Combined dataset with columns:
        - date: datetime
        - state: string ('National' or state name)
        - cases: cumulative cases
        - deaths: cumulative deaths
        - daily_cases: daily new cases
        - daily_deaths: daily new deaths
        - cases_7day: 7-day moving average of daily cases
        - deaths_7day: 7-day moving average of daily deaths
        - days_since_start: integer days since first date (for sliders)
    """
    print("Loading COVID-19 data...")
    
    # Load raw data
    if filepath:
        df = pd.read_csv(filepath, parse_dates=["date"])
    else:
        df = pd.read_csv(DATA_URL, parse_dates=["date"])
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Prepare state-level data
    print("Processing state-level data...")
    state_data = df.groupby(['state', 'date']).agg({
        'cases': 'sum',
        'deaths': 'sum'
    }).reset_index().sort_values(['state', 'date'])
    
    # Calculate daily metrics for states (data is cumulative!)
    state_data['daily_cases'] = state_data.groupby('state')['cases'].diff().fillna(0).clip(lower=0)
    state_data['daily_deaths'] = state_data.groupby('state')['deaths'].diff().fillna(0).clip(lower=0)
    
    # Calculate 7-day moving averages for states
    state_data['cases_7day'] = state_data.groupby('state')['daily_cases'].transform(
        lambda x: x.rolling(7, center=True, min_periods=1).mean()
    )
    state_data['deaths_7day'] = state_data.groupby('state')['daily_deaths'].transform(
        lambda x: x.rolling(7, center=True, min_periods=1).mean()
    )
    
    # Prepare national-level data
    print("Processing national-level data...")
    national_data = df.groupby('date').agg({
        'cases': 'sum',
        'deaths': 'sum'
    }).reset_index().sort_values('date')
    
    national_data['state'] = 'National'
    
    # Calculate daily metrics for national (data is cumulative!)
    national_data['daily_cases'] = national_data['cases'].diff().fillna(0).clip(lower=0)
    national_data['daily_deaths'] = national_data['deaths'].diff().fillna(0).clip(lower=0)
    
    # Calculate 7-day moving averages for national
    national_data['cases_7day'] = national_data['daily_cases'].rolling(
        7, center=True, min_periods=1
    ).mean()
    national_data['deaths_7day'] = national_data['daily_deaths'].rolling(
        7, center=True, min_periods=1
    ).mean()
    
    # Combine state and national data
    print("Combining datasets...")
    full_data = pd.concat([state_data, national_data], ignore_index=True)
    
    # Add helper column for date sliders
    min_date = full_data['date'].min()
    full_data['days_since_start'] = (full_data['date'] - min_date).dt.days
    
    print(f"Data preparation complete!")
    print(f"  Date range: {full_data['date'].min().date()} to {full_data['date'].max().date()}")
    print(f"  States: {full_data[full_data['state'] != 'National']['state'].nunique()}")
    print(f"  Total rows: {len(full_data):,}")
    
    return full_data


if __name__ == '__main__':
    # Test the module
    data = prepare_full_dataset()
    
    print("\n=== DATASET SAMPLE ===")
    print("\nNational data (first 10 rows):")
    print(data[data['state'] == 'National'].head(10)[
        ['date', 'state', 'daily_deaths', 'deaths_7day']
    ])
    
    print("\nCalifornia data (first 10 rows):")
    print(data[data['state'] == 'California'].head(10)[
        ['date', 'state', 'daily_deaths', 'deaths_7day']
    ])
    
    print("\n=== TOP 5 STATES BY TOTAL DEATHS ===")
    state_totals = data[data['state'] != 'National'].groupby('state')['deaths'].max().sort_values(ascending=False)
    for i, (state, total) in enumerate(state_totals.head(5).items(), 1):
        print(f"  {i}. {state}: {total:,}")
