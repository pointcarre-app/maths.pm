


# Graphic Semiology Fundamentals

## Matplotlib Configuration Best Practices

When working with matplotlib in this environment, it's recommended to configure fonts and warnings at the beginning of your code to ensure clean output:

```yaml
f_type: "codex_"
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  import warnings
  import matplotlib
  
  # Configure matplotlib for clean output
  warnings.filterwarnings('ignore', message='findfont: Generic family')
  matplotlib.rcParams['font.family'] = 'DejaVu Sans'  # Use reliable fallback font
  matplotlib.rcParams['font.size'] = 10
  matplotlib.rcParams['axes.labelsize'] = 12
  matplotlib.rcParams['axes.titlesize'] = 14
  
  # Example plot demonstrating clean configuration
  fig, ax = plt.subplots(figsize=(8, 6))
  
  # Sample data
  categories = ['Category A', 'Category B', 'Category C', 'Category D']
  values = [23, 45, 56, 78]
  
  # Create bar plot
  bars = ax.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
  
  # Customize appearance
  ax.set_title('Sample Data Visualization', fontweight='bold')
  ax.set_ylabel('Values')
  ax.grid(axis='y', alpha=0.3)
  
  # Add value labels on bars
  for bar, value in zip(bars, values):
      ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
              str(value), ha='center', va='bottom')
  
  plt.tight_layout()
  plt.show()
  
  print("✅ Plot generated with clean configuration!")
```

## Key Configuration Elements

- **Font warnings suppression**: `warnings.filterwarnings('ignore', message='findfont: Generic family')`
- **Reliable font family**: `matplotlib.rcParams['font.family'] = 'DejaVu Sans'`
- **Consistent sizing**: Set font sizes for different elements
- **Clean styling**: Use grids, colors, and spacing effectively






Write this file while trying to be precise, but also pretty exhaustive