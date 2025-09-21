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