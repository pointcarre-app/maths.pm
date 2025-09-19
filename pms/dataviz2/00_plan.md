# Data Visualization - Detailed Syllabus
**ENSAI Master for Smart Data Science - UE-MSD04**  
**ECTS Credits:** 1  
**Duration:** 15 hours lectures/tutorials + 10 hours personal work  
**Teaching Language:** English  
**Software & Packages:** Python (Matplotlib, Bokeh)

## Course Description
Data visualization is a fundamental ingredient of data science as it "forces us to notice what we never expected to see" in a given dataset. Dataviz is also a tool for communication and, as such, is a visual language. All along the courses, we will focus on methods and strategies to represent datasets, using dynamic and interactive tools.

**📖 Course Materials:**
- **[Introduction & Interactive Notebooks](01_introduction.md)** - Getting started with Jupyter environments and code fragments
- **[Jupyter Launcher](jupyter_launcher.md)** - Direct access to interactive Python environments

---

## Learning Outcomes
By the end of this course, students will be able to:
- Apply graphic semiology principles to choose relevant visualizations
- Create interactive diagrams, cartographic or otherwise, to represent datasets in Python
- Build web-based interactive dashboards using Bokeh
- Understand the mathematical foundations underlying different visualization types
- Critically evaluate visualization effectiveness for communication

---

## Prerequisites
- Basics on Python
- Fundamental statistics and mathematics
- Understanding of data structures (arrays, DataFrames)

---

## Course Structure & Detailed Syllabus

### **Module 1: Foundations & Graph Types Theory (4 hours)**

#### **Theory: Graphic Semiology & Data Types (2 hours)**
- **Visual Variables** *(Based on Jacques Bertin's work - Public Domain)*
  - Position, size, shape, value, color, orientation, texture
  - Mapping data types to visual channels

- **Data Types Classification**
  - Nominal, ordinal, quantitative data
  - Temporal, spatial, hierarchical, network data
  - Multivariate and high-dimensional data

- **Mathematical Foundations**
  - Coordinate systems (Cartesian, polar, logarithmic)
  - Statistical distributions and their visual representations
  - Perceptual mathematics: Weber-Fechner law, Stevens' power law

#### **Theory: Comprehensive Chart Types by Data Purpose (2 hours)**
*Ordered from easiest to most complex*

**1. Ranking & Comparison** *(Easiest - Basic aggregations)*
- **Bar plots** - Categorical comparisons
- **Lollipop charts** - Alternative to bar charts
- **Line plots** - Simple temporal trends
- **Pie charts** - Simple proportional relationships
- **Doughnut charts** - Circular part-to-whole with center space

*Mathematical basis: Basic arithmetic, percentages, sorting*

**2. Distribution Analysis** *(Easy - Statistical foundations)*
- **Histograms** - Frequency distributions for continuous data
- **Box plots** - Five-number summary visualization
- **Density plots** - Continuous probability distributions
- **Violin plots** - Probability density + box plot combination
- **Ridgeline plots** - Multiple density distributions stacked

*Mathematical basis: Descriptive statistics, quartile calculations, kernel density estimation*

**3. Correlation & Relationships** *(Moderate - Bivariate analysis)*
- **Scatter plots** - Bivariate relationships
- **Bubble plots** - Three-dimensional scatter plots
- **Heatmaps** - Matrix data visualization
- **Connected scatter plots** - Temporal relationships
- **Correlograms** - Correlation matrix visualization
- **2D Density plots** - Bivariate density estimation

*Mathematical basis: Correlation coefficients, regression analysis*

**4. Evolution & Time Series** *(Moderate - Temporal complexity)*
- **Area charts** - Cumulative quantities over time
- **Stacked area charts** - Multiple series evolution
- **Stream graphs** - Flowing temporal patterns

*Mathematical basis: Time series analysis, smoothing algorithms*

**5. Part-of-Whole Relationships** *(Moderate-Advanced - Hierarchical structures)*
- **Treemaps** - Hierarchical data with size encoding
- **Circular packing** - Nested circular representations
- **Dendrograms** - Hierarchical clustering visualization

*Mathematical basis: Hierarchical clustering, tree algorithms*

**6. Advanced Comparison & Multi-dimensional** *(Advanced - Complex encodings)*
- **Spider/Radar charts** - Multivariate comparison
- **Parallel coordinates** - High-dimensional data exploration
- **Circular bar plots** - Radial bar representations
- **Word clouds** - Frequency-based text visualization

*Mathematical basis: Normalization techniques, dimensionality reduction*

**7. Spatial & Geographic** *(Advanced - Coordinate systems)*
- **Geographic scatter** - Point data on maps
- **Choropleth maps** - Statistical data on geographic regions
- **Hexbin maps** - Spatial density with hexagonal binning
- **Cartograms** - Distorted geography by statistical values

*Mathematical basis: Map projections, spatial statistics*

**8. Connections & Networks** *(Most Complex - Graph theory)*
- **Flow diagrams** - Directional relationships
- **Network graphs** - Node-link diagrams
- **Arc diagrams** - Linear node arrangement with curved links
- **Bubble maps** - Geographic relationships with size encoding
- **Chord diagrams** - Circular network relationships
- **Sankey diagrams** - Flow quantities between nodes
- **Edge bundling** - Simplified network visualization

*Mathematical basis: Graph theory, network analysis algorithms, force-directed layouts*

### **Module 2: Static Visualizations with Matplotlib (4 hours)**

#### **Theory (1 hour)**
- **Statistical Graphics Principles** *(Following Tufte's principles - Fair Use)*
  - Data-ink ratio optimization
  - Chart junk elimination
  - Small multiples principle
- **📚 [See Interactive Examples & Code Fragments](01_introduction.md)** for hands-on practice

#### **Practice (3 hours)**
*Following the complexity progression*

- **Basic Charts** *(Start here - easiest)*
  - Bar plots, line plots, pie charts, lollipop charts
  - **Code:** `02a_basic_charts.py`

- **Distribution Analysis**
  - Histograms, box plots, density plots, violin plots
  - **Code:** `02b_distributions.py`

- **Correlation & Relationships**
  - Scatter plots, bubble plots, heatmaps, correlation matrices
  - **Code:** `02c_correlations.py`

- **Advanced Charts** *(Most complex)*
  - Time series, geographic basics, simple network diagrams
  - **Code:** `02d_advanced_charts.py`

### **Module 3: Interactive Visualizations with Bokeh (6 hours)**

#### **Theory (1 hour)**
- **Interaction Design Principles** *(Based on Shneiderman's work - Academic Use)*
  - Overview first, zoom and filter, details on demand
  - Direct manipulation principles
  - Real-time data streaming concepts
- **🚀 [Access Interactive Jupyter Environments](01_introduction.md#interactive-jupyter-notebooks)** for live coding practice

#### **Practice (5 hours)**
- **Interactive Distribution Analysis**
  - Dynamic histograms, interactive box plots
  - Linked brushing for exploratory analysis
  - **Code:** `03a_interactive_distributions.py`

- **Advanced Correlation Tools**
  - Interactive scatter plots with regression lines
  - Dynamic correlation matrices
  - Multi-dimensional bubble charts
  - **Code:** `03b_interactive_correlations.py`

- **Time Series Dashboards**
  - Interactive line plots with zoom/pan
  - Real-time streaming data visualization
  - **Code:** `03c_timeseries_dashboard.py`

- **Geographic Visualizations**
  - Interactive choropleth maps
  - Geographic scatter with hover details
  - **Code:** `03d_interactive_maps.py`

- **Network & Flow Visualizations**
  - Interactive network diagrams
  - Sankey diagram implementations
  - **Code:** `03e_network_flows.py`

### **Module 4: Advanced Topics & Project Preparation (1 hour)**

#### **Theory & Practice (1 hour)**
- **Web Deployment Strategies**
  - Bokeh server applications
  - Static HTML generation
  - Embedding in web applications

- **Performance Optimization**
  - Large dataset handling
  - Efficient rendering techniques
  - Memory management

- **Project Planning Session**
  - Dataset selection guidance
  - Visualization strategy planning
  - **Code:** Project template setup

---

## Mathematical Concepts Integrated

### **Statistics & Probability**
- Kernel density estimation for smooth distributions
- Correlation coefficients and significance testing
- Regression analysis and confidence intervals
- Time series decomposition and trend analysis

### **Linear Algebra**
- Matrix operations for correlation matrices
- Principal component analysis for dimensionality reduction
- Transformation matrices for coordinate systems

### **Graph Theory**
- Network centrality measures
- Shortest path algorithms for network visualization
- Hierarchical clustering algorithms

### **Computational Geometry**
- Voronoi diagrams for spatial analysis
- Convex hulls for scatter plot analysis
- Spatial indexing for geographic data

---

## Assessment

### **Final Project: Interactive Web Visualization (100%)**
**Requirement:** Build a comprehensive interactive data visualization website using Bokeh

**Project Components:**
1. **Data Exploration & Analysis** (25%)
   - Dataset cleaning and preprocessing
   - Statistical analysis and insights discovery
   - Documentation of data exploration process

2. **Visualization Design & Implementation** (40%)
   - Application of appropriate chart types from course taxonomy
   - Interactive features implementation
   - User experience design
   - Technical execution quality

3. **Mathematical Accuracy** (20%)
   - Correct statistical representations
   - Appropriate mathematical transformations
   - Accurate geographic projections (if applicable)

4. **Communication & Presentation** (15%)
   - Clear storytelling through visualization
   - Effective use of graphic semiology principles
   - Web deployment functionality

**Deliverables:**
- Functional Bokeh web application
- Source code with documentation
- Project report explaining design decisions
- Brief presentation of findings

---

## Resources & Bibliography

### **Primary References**
1. **Official Python Documentation** - https://docs.python.org/
2. **Matplotlib Documentation** - https://matplotlib.org/ *(BSD License)*
3. **Bokeh Documentation** - https://docs.bokeh.org/en/latest/ *(BSD License)*

### **Academic Sources (Freely Available)**
1. **Stanford CS448B - Data Visualization** *(Creative Commons)*
   - Theoretical foundations and best practices
2. **MIT OpenCourseWare - Data Visualization**
   - Mathematical approaches to visualization
3. **UC Berkeley - Principles of Data Visualization**
   - Perceptual and cognitive aspects

### **Theoretical Foundations**
1. **Bertin, J.** - "Semiology of Graphics" *(Public Domain)*
2. **Tufte, E.R.** - Visual design principles *(Fair Use Educational)*
3. **Shneiderman, B.** - Information visualization taxonomy
4. **Cleveland, W.S.** - Statistical graphics theory

### **Open Datasets**
- World Bank Open Data (CC BY 4.0)
- UCI Machine Learning Repository
- Government open data portals
- Kaggle public datasets

---

## File Structure

```
course_materials/
├── lectures/
│   ├── 01_foundations_chart_types.md
│   ├── 02_matplotlib_implementation.md
│   ├── 03_bokeh_interactive.md
│   └── 04_advanced_deployment.md
├── code/
│   ├── 02a_distributions.py
│   ├── 02b_correlations.py
│   ├── 02c_rankings.py
│   ├── 02d_temporal_spatial.py
│   ├── 03a_interactive_distributions.py
│   ├── 03b_interactive_correlations.py
│   ├── 03c_timeseries_dashboard.py
│   ├── 03d_interactive_maps.py
│   └── 03e_network_flows.py
├── data/
│   └── [sample datasets for each chart type]
└── project/
    ├── templates/
    └── examples/
```

---

## Note on Future Extensions
While this course focuses on Python-based visualization tools (Matplotlib and Bokeh), the comprehensive chart type taxonomy covered in the theory sections provides a foundation for future exploration of other visualization libraries and frameworks, including web-based solutions that may be covered in advanced courses.