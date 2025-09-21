### 2.2. Relationships

#### 2.2.1. Relations and dimensionality

- Key in analysis: how components relate, not necessarily their individual meanings, but their differences and connections.
- For every dataset, determining its dimensionality (number/nature of components) directs the choice of graphic strategy.



```yaml
f_type: "codex_"


# TODO excellent example for issues if y-axis doesnt start at 0 (good idea but not always)


<!-- 3D TEMPTATION -->
<!-- https://www.statsmapsnpix.com/2020/11/how-to-make-3d-population-density.html -->
Danger cause of angles : cf squares or other hidden behind because of the position of the observer and the direction he is looking at.

<!-- go back to previous stuff for new tab opening when clicing from 00_plan.md -->


<!-- Nombre premiers lol -->

<!-- Other nice like it for famous math sobject : end of static simple -->


<!-- JUSTIFYING USAGE OF THE DATA FOR COVID-19 IN THE US -->
<!-- Strong statistical aspects -->
<!-- Reliable data -->
<!-- "Panel data???"  --> to see with Etienne, but states yes ?




<!-- Exercice : Tours mais en les rerésetant plus comme des tours -->


- [**Course overview and evaluation criteria (i.e. the file you're currently reading)**](00_plan.md)
- **[Graphic Semiology Fundamentals](01_session_1_h_a.md)**

<!-- - Mostly based on Jacques Bertin's work -->
<!-- - Visual variables: position, size, shape, value, color, orientation, texture
- Mapping data types to visual channels
- Perceptual mathematics: Weber-Fechner law, Stevens' power law -->




<!-- - Mostly based on Jacques Bertin's work -->
<!-- - Visual variables: position, size, shape, value, color, orientation, texture
- Mapping data types to visual channels
- Perceptual mathematics: Weber-Fechner law, Stevens' power law -->



IMPORTANT : 
- Financial Times
- The economist
- Partout où Mike Bostock est passé (citer d3)

Examples de graphes cata (TF1 par exemple)


<!-- - Nominal, ordinal, quantitative data
- Temporal, spatial, hierarchical, network data
- Multivariate and high-dimensional data -->

<!-- **Mathematical Foundations:**
- Coordinate systems (Cartesian, polar, logarithmic)
- Statistical distributions and their visual representations -->

<!-- **Complete Chart Types Taxonomy** *(Ordered easiest to most complex)*

**1. Ranking & Comparison** *(Easiest - Basic aggregations)*
- Bar plots, lollipop charts, line plots, pie charts, doughnut charts
- *Mathematical basis: Basic arithmetic, percentages, sorting*

**2. Distribution Analysis** *(Easy - Statistical foundations)*
- Histograms, box plots, density plots, violin plots, ridgeline plots
- *Mathematical basis: Descriptive statistics, quartile calculations, kernel density estimation*

**3. Correlation & Relationships** *(Moderate - Bivariate analysis)*
- Scatter plots, bubble plots, heatmaps, connected scatter plots, correlograms, 2D density plots
- *Mathematical basis: Correlation coefficients, regression analysis*

**4. Evolution & Time Series** *(Moderate - Temporal complexity)*
- Area charts, stacked area charts, stream graphs
- *Mathematical basis: Time series analysis, smoothing algorithms*

**5. Part-of-Whole Relationships** *(Moderate-Advanced - Hierarchical structures)*
- Treemaps, circular packing, dendrograms
- *Mathematical basis: Hierarchical clustering, tree algorithms*

**6. Advanced Comparison & Multi-dimensional** *(Advanced - Complex encodings)*
- Spider/radar charts, parallel coordinates, circular bar plots, word clouds
- *Mathematical basis: Normalization techniques, dimensionality reduction*

**7. Spatial & Geographic** *(Advanced - Coordinate systems)*
- Geographic scatter, choropleth maps, hexbin maps, cartograms
- *Mathematical basis: Map projections, spatial statistics*

**8. Connections & Networks** *(Most Complex - Graph theory)*
- Flow diagrams, network graphs, arc diagrams, bubble maps, chord diagrams, Sankey diagrams, edge bundling
- *Mathematical basis: Graph theory, network analysis algorithms, force-directed layouts*

**Homework:** Review provided datasets, individual reflection on preferred dataset -->















#### **Hour 1: Group Formation & Project Launch**
- **🎯 GROUP FORMATION** (3-4 students per group)
- Project requirements explanation
- Dataset selection by groups  
- Initial project planning (scope, objectives, deliverables)

#### **Hour 2: Matplotlib Foundations & Basic Charts**
**Statistical Graphics Principles** *(Following Tufte's principles)*
- Data-ink ratio optimization
- Chart junk elimination
- Small multiples principle

**Practice - Level 1 (Easiest Charts):**
- **Ranking & Comparison implementation**
  - Bar plots, line plots, pie charts, lollipop charts
  - **Code:** `02a_basic_charts.py`

#### **Hour 3: Distribution Analysis with Matplotlib**
**Practice - Level 2:**
- **Distribution visualization implementation**
  - Histograms, box plots, density plots, violin plots
  - Statistical foundations in practice
  - **Code:** `02b_distributions.py`

**Group Work:**
- Groups begin initial data exploration
- Apply basic charts and distributions to chosen dataset










### **Session 3: Correlations & First Presentations (3 hours)**

#### **Hours 1-2: Correlation & Relationship Analysis**
**Practice - Level 3 (Moderate complexity):**
- **Bivariate analysis implementation**
  - Scatter plots, bubble plots, heatmaps, correlation matrices
  - Connected scatter plots for temporal relationships
  - 2D density plots, correlograms
  - **Code:** `02c_correlations.py`

**Advanced Theory:**
- Correlation coefficients and statistical significance
- Regression analysis visualization
- Multi-dimensional relationship encoding

**Group Workshop:**
- Groups apply correlation analysis to their datasets
- Instructor consultations on visualization strategy

#### **Hour 3: First Group Presentations (1 hour)**
**🎤 GROUP PRESENTATIONS Round 1**
- **5 minutes per group**
- **Required Content:**
  - Chosen dataset description and context
  - Initial insights discovered through basic charts
  - Correlation analysis findings
  - Planned interactive visualization approach for final project
  - Technical challenges identified

**Evaluation Focus:** Data understanding, appropriate chart selection, visualization strategy

---



La session 4 contient les PYthon idioms pcq c pas l'objet du cours



GeoData ? 
Sankey ? 

































# Hour 1: Course Introduction & Visual Variables

## Course Overview and Evaluation Criteria

This course focuses on the fundamental principles of data visualization, combining theoretical foundations with practical applications. Students will learn to create effective visual representations of data by understanding the relationship between human perception and graphic design principles.

### Learning Objectives
- Master the theoretical foundations of graphic semiology
- Understand visual variables and their perceptual properties
- Apply perceptual mathematics to visualization design
- Create effective mappings between data types and visual channels

### Evaluation Components
- Theoretical understanding of visual perception principles
- Practical application of visual variables in data representation
- Critical analysis of existing visualizations
- Design and implementation of data visualizations

## Graphic Semiology Fundamentals

### Jacques Bertin's Framework
Jacques Bertin (1918-2010) revolutionized data visualization through his systematic approach to graphic representation. His seminal work "Semiology of Graphics" (1967) established the theoretical foundation for modern data visualization.

**Key Principles:**
- **Graphic**: Visual representation that uses position on a plane to express relationships
- **Sign**: Basic unit of graphic communication consisting of location and marking
- **Variable**: Perceptual dimension that can be systematically varied to encode information

### The Communication Model
Bertin's framework treats visualization as a communication system:
```
Data → Encoding → Graphic → Decoding → Information
```

### Levels of Reading
1. **Elementary Level**: Individual marks and their immediate properties
2. **Intermediate Level**: Groups and patterns within the visualization
3. **Overall Level**: Global structure and main message

## Visual Variables

Bertin identified seven fundamental visual variables that can be used to encode information:

### 1. Position
**Definition**: Location of marks in 2D space (x, y coordinates)

**Properties:**
- **Selective**: Easily distinguishable categories
- **Associative**: Can group similar elements
- **Quantitative**: Supports ordered and ratio comparisons
- **Length**: No practical limit to variations

**Applications:**
- Scatterplots (x, y position for two quantitative variables)
- Maps (geographic positioning)
- Time series (temporal positioning)

### 2. Size
**Definition**: Variation in the physical dimensions of marks

**Properties:**
- **Selective**: Good for a limited number of categories (≤7)
- **Associative**: Moderate grouping ability
- **Quantitative**: Strong support for ordered comparisons
- **Length**: Limited by visual resolution and display constraints

**Applications:**
- Bubble charts (circle area for quantitative data)
- Proportional symbol maps
- Bar chart heights

### 3. Shape
**Definition**: Geometric form or symbol type

**Properties:**
- **Selective**: Excellent for categorical distinctions
- **Associative**: Can create visual groups through similar shapes
- **Quantitative**: No inherent order
- **Length**: Limited by recognition capacity (~12 distinct shapes)

**Applications:**
- Scatter plot point types for categories
- Icon-based visualizations
- Network node types

### 4. Value (Lightness)
**Definition**: Variation from light to dark (grayscale intensity)

**Properties:**
- **Selective**: Limited discrimination (3-5 levels reliably)
- **Associative**: Creates natural groupings
- **Quantitative**: Strong ordered perception
- **Length**: Continuous but perceptually limited

**Applications:**
- Choropleth maps
- Heatmaps
- Grayscale encodings for ordinal data

### 5. Color (Hue)
**Definition**: Spectral wavelength variation (red, blue, green, etc.)

**Properties:**
- **Selective**: Excellent for categories (≤10 distinct hues)
- **Associative**: Moderate grouping through color families
- **Quantitative**: No natural order (except through cultural conventions)
- **Length**: Limited by color discrimination abilities

**Applications:**
- Categorical color coding
- Multi-class visualizations
- Qualitative differentiation

### 6. Orientation
**Definition**: Angular rotation or directional alignment

**Properties:**
- **Selective**: Good for limited categories (4-8 orientations)
- **Associative**: Can group through similar angles
- **Quantitative**: Natural circular ordering
- **Length**: Limited by angular resolution

**Applications:**
- Wind direction visualization
- Flow charts with directional arrows
- Glyph-based representations

### 7. Texture
**Definition**: Surface pattern or visual texture variation

**Properties:**
- **Selective**: Moderate categorical distinction
- **Associative**: Creates pattern-based groupings
- **Quantitative**: Limited ordered perception
- **Length**: Constrained by pattern recognition

**Applications:**
- Pattern fills in maps
- Accessible alternatives to color
- Layered information encoding

## Mapping Data Types to Visual Channels

### Data Types Classification

**Nominal (Categorical)**
- No inherent order
- Examples: Country names, product categories, species
- Best visual variables: Shape, Color (hue), Position (separate groups)

**Ordinal**
- Natural ordering without meaningful intervals
- Examples: Education levels, satisfaction ratings, size categories
- Best visual variables: Value, Size, Position (ordered arrangement)

**Interval**
- Equal intervals, no true zero
- Examples: Temperature in Celsius, calendar dates
- Best visual variables: Position, Size (with care for zero point)

**Ratio**
- Equal intervals with meaningful zero point
- Examples: Height, weight, count, income
- Best visual variables: Position, Size, Value

### Effectiveness Ranking

**For Quantitative Data (Ordered):**
1. Position along common scale
2. Position along non-aligned scale
3. Length
4. Angle/Slope
5. Area
6. Volume
7. Color saturation/value

**For Categorical Data:**
1. Position (spatial separation)
2. Color hue
3. Shape
4. Texture/Pattern
5. Orientation

## Perceptual Mathematics

### Weber-Fechner Law

**Statement**: The perceived intensity of a stimulus is proportional to the logarithm of the physical intensity.

**Mathematical Expression:**
```
P = k × log(S/S₀)
```
Where:
- P = Perceived intensity
- S = Physical stimulus intensity
- S₀ = Threshold stimulus intensity
- k = Constant

**Implications for Visualization:**
- Linear increases in data may not be perceived linearly
- Logarithmic scales may better represent perception
- Small differences at low values are more noticeable than at high values

**Applications:**
- Audio visualization (decibel scales)
- Financial data (log scales for stock prices)
- Scientific data spanning multiple orders of magnitude

### Stevens' Power Law

**Statement**: Perceived magnitude is proportional to the physical intensity raised to a power.

**Mathematical Expression:**
```
P = k × Sⁿ
```
Where:
- P = Perceived magnitude
- S = Physical stimulus intensity
- k = Scaling constant
- n = Perceptual exponent (varies by stimulus type)

**Common Exponents:**
- **Brightness**: n ≈ 0.33 (sublinear - perceived brightness increases slower than physical intensity)
- **Length**: n ≈ 1.0 (linear - accurate perception)
- **Area**: n ≈ 0.7 (sublinear - areas appear smaller than they are)
- **Volume**: n ≈ 0.57 (sublinear - volumes significantly underestimated)

**Design Implications:**

**For Area Encodings:**
- Bubble chart areas are systematically underestimated
- Consider using radius instead of area for magnitude encoding
- Apply perceptual correction: use √(data) for radius to encode data in area

**For Brightness/Value:**
- Exponential data scaling may be needed for linear perception
- Consider gamma correction in color encodings

**For Length:**
- Most reliable visual variable for quantitative data
- Linear relationship between data and perception
- Foundation for bar charts and position encodings

### Practical Applications

**Scale Selection:**
- Use linear scales for data following normal distributions
- Apply logarithmic scales for data spanning multiple orders of magnitude
- Consider square root transformations for count data with extreme values

**Visual Variable Choice:**
- Prefer position and length for precise quantitative comparisons
- Use area encodings cautiously, with perceptual corrections
- Avoid volume encodings for precise quantitative tasks

**Accessibility Considerations:**
- Provide multiple encodings for critical information
- Consider perceptual variations across populations
- Test visualizations with representative users

## Summary and Next Steps

This foundational hour establishes the theoretical framework for effective data visualization. Key takeaways:

1. **Bertin's semiology provides systematic approach** to graphic design
2. **Seven visual variables** offer different perceptual properties
3. **Data type determines appropriate visual encoding** strategies
4. **Human perception is non-linear** and must be considered in design
5. **Effectiveness hierarchies guide** optimal visual variable selection

**Preparation for Hour 2:**
- Review visual variable examples in existing visualizations
- Identify data types in provided datasets
- Practice mapping data attributes to visual channels
- Consider perceptual limitations in current visualization tools

**Recommended Reading:**
- Bertin, J. (1983). Semiology of Graphics: Diagrams, Networks, Maps
- Cleveland, W. S. (1985). The Elements of Graphing Data
- Ware, C. (2012). Information Visualization: Perception for Design