# Visual Vocabulary - Financial Times Guide


A comprehensive guide to choosing the right chart for your data story using the *FT Data Visualization Guide*
{: .pm-subtitle}

This work is an adaptation from the [*FT Data Visualization Guide*](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary) from *the Financial Times*. This work is licenced under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).
{: .alert .alert-success .alert-soft}



This ressource has been made available by [The official portal for European data](https://data.europa.eu/apps/data-visualisation-guide/visual-vocabulary), i.e. [data.europa.eu](https://data.europa.eu).
{.alert .alert-info .alert-soft}


[TOC]


## The FT Data Visualization Guide


![Visual Vocabulary - FT Data Visualization Guide](files/visual-vocabulary-ft.png)

License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)



## Deviation
**Emphasize variations (+/-) from a fixed reference point. Often the reference point is zero but it can also be a target or a long-term average. Can also be used to show sentiment (positive/neutral/negative)**

### Example FT uses
Trade surplus/deficit, climate change

### Chart Types

#### **Diverging bar**
- A simple standard bar chart that can handle both negative and positive magnitude values

#### **Diverging stacked bar**
- Perfect for presenting survey results which involve sentiment (eg disagree/neutral/agree)

#### **Spine**
- Splits a single value into 2 contrasting components (eg Male/Female)

#### **Surplus/deficit filled line**
- The shaded area of these charts allows a balance to be shown – either against a baseline or between two series

---

## Correlation
**Show the relationship between two or more variables. Be mindful that, unless you tell them otherwise, many readers will assume the relationships you show them to be causal (i.e. one causes the other)**

### Example FT uses
Inflation & unemployment, income & life expectancy

### Chart Types

#### **Scatterplot**
- The standard way to show the relationship between two continuous variables, each of which has its own axis

#### **Column + line (dual axis)**
- A chart which allows you to look at the relationship between two scaled axis. TAKE CARE: this axis is very easy to manipulate to show nothing or anything

#### **Connected scatterplot**
- Usually used to show how the relationship between 2 variables has changed over time

#### **Bubble**
- Like a scatterplot, but adds additional detail by sizing the circles according to a third variable

#### **XY heatmap**
- A good way of showing the patterns between 2 categories of data, less good at showing fine differences in amounts

---

## Ranking
**Use where an item's position in an ordered list is more important than its absolute or relative value. Don't be afraid to highlight the points of interest**

### Example FT uses
Wealth, deprivation, league tables, constituency election results

### Chart Types

#### **Ordered bar**
- A standard bar chart which orders the bars (longest, shortest, or other)

#### **Ordered column**
- A standard column chart which orders the columns (longest, shortest, or other)

#### **Ordered proportional symbol**
- Use when there are big variations between values and/or seeing fine differences in amounts

#### **Slope**
- Perfect for showing how ranks have changed over time or vary between categories. Use point labels or a combination of the start and end measurements

#### **Lollipop**
- Lollipop charts draw attention to the data value by reducing the excess ink of the bar

#### **Dot strip plot**
- Dot strip plots or dot plot arrays also work well for showing ranking in data where values are more closely grouped

#### **Bump**
- Effective for showing changing ranks through multiple stages

---

## Distribution
**Show values in a dataset and how often they occur. The shape (or 'skew') of a distribution can be a memorable way of highlighting the lack of uniformity or equality in the data**

### Example FT uses
Income distribution, population (age/sex) distribution

### Chart Types

#### **Histogram**
- The standard way to show a statistical distribution - keep the gaps between columns small to highlight the 'shape' of the data

#### **Dot plot**
- A simple way of showing the range (and clustering) of data points

#### **Dot strip plot**
- Good for showing individual values in a distribution, can be a problem when too many dots are in a line

#### **Barcode plot**
- Like dot strip plot - but hides the identity of individual values to focus on the collective pattern

#### **Beeswarm plot**
- A good way of showing all the data points when too many have a single value

#### **Population pyramid**
- A standard way for showing the age and sex breakdown of a population distribution. Used widely to show a population by age and sex

#### **Cumulative curve**
- A good way of showing how unequal a distribution is: y axis is always cumulative frequency, x axis is a measure of what the distribution is showing

#### **Boxplot**
- Summarize multiple distributions by showing the median (center) and the spread of the data

#### **Violin plot**
- Similar to a box plot but more effective with complex distributions (data with two peaks, or multiple humps)

---

## Change over time
**Give emphasis to changing trends. These can be short (intra-day) or long (decade) periods. As time is a dimension variable this is best shown in most cases by using a horizontal axis**

### Example FT uses
Share price changes, temperature changes, economic time series

### Chart Types

#### **Line**
- The standard way to show a changing time series. If data are irregular, consider markers to represent data points

#### **Column**
- Columns work well for showing change over time - but usually best with only one series of data at a time

#### **Column + line timeline**
- A good way of showing the relationship over time between an amount (columns) and a rate (line)

#### **Stock price**
- Usually focused on day-to-day activity, these charts show opening/closing and hi/low points of each day

#### **Slope**
- Good for showing changing data as long as the data can be simply paired

#### **Area chart**
- Use with care - these are good at showing changes to total, but seeing change in components can be very difficult

#### **Fan chart (projections)**
- Use to show the uncertainty in future projections - usually this grows the further forward into the future

#### **Connected scatterplot**
- A good way of showing changing relationship between two variables over time

#### **Calendar heatmap**
- A great way of showing temporal patterns (daily, weekly, monthly) - at the expense of showing precision in quantity

#### **Priestley timeline**
- Great when date and duration are key

#### **Circle timeline**
- Good for showing discrete values of varying size across multiple categories (eg earthquakes by region)

#### **Seismogram**
- Another alternative to the circle timeline for showing series where there are big variations between values

#### **Vertical timeline**
- A simple way of showing the order and timing of events

---

## Magnitude
**Show size comparisons. These can be relative (just being able to see larger/bigger) or absolute (need to see fine differences). Usually these show a 'counted' number (for example, barrels, dollars or people) rather than a calculated rate or percent**

### Example FT uses
Commodity production, market capitalizations

### Chart Types

#### **Column**
- The standard way to compare the size of things. Must have a zero baseline!

#### **Bar**
- See above. Good when the data are not time series and labels have long category names

#### **Proportional stacked bar**
- A multi-set bar chart which includes a gap between each individual series to allow the reader to clearly see the full extent of each series

#### **Paired column**
- As per standard column but allows for multiple series. Can become tricky to read with more than 2 series

#### **Paired bar**
- As per standard bar but allows for multiple series

#### **Proportional symbol**
- Use when there are big variations between values and/or seeing exact amounts is not so important

#### **Isotype (pictogram)**
- Excellent solution in some instances - use only with whole numbers (do not slice off an arm to represent a decimal)

#### **Lollipop**
- Lollipop charts draw attention to the data value by reducing the excess ink of the bar

#### **Radar**
- A space-efficient way of showing magnitude for several categories - but make sure the scales are consistent!

#### **Parallel coordinates**
- An alternative to radar charts - again, ensure the scales are consistent. Usually benefits from highlighting values of interest



#### **Bullet**
- A quick, efficient way of showing actual vs. target values. A good way of showing bars vs. targets without needing too many colors or labels

#### **Grouped symbol**
- An alternative to bar/column charts when showing data that have big variations. Can work well in small multiple format



---

## Part-to-whole
**Show how a single entity can be broken down into its component elements. If the components are too small to see, consider a grouped bar chart instead**

### Example FT uses
Fiscal budgets, company structures, national household spending

### Chart Types

#### **Stacked column**
- A simple way to show part-to-whole relationships but can be difficult to read with more than a few components

#### **Proportional stacked bar**
- A good way of showing the size and proportion of data at the same time - as long as the data are not too complicated

#### **Pie**
- A common way of showing part-to-whole data - but research shows people find it hard to compare the size of segments

#### **Donut**
- Similar to a pie chart - but the center can be a good way of making space to include more information about the data (eg. total)

#### **Treemap**
- Use for hierarchical part-to-whole relationships; can be difficult to read when there are many small segments

#### **Voronoi**
- A way of turning points in space into polygons while showing part to whole. Irregular division of data might be interpreted as meaningful, when it isn't

#### **Arc**
- A hemicircle, often used for showing political data, with the seats orientated as they would be in parliament

#### **Gridplot**
- Good for showing % information, often used when comparing data for two points in time

#### **Venn**
- Generally only used for illustrating simple set logic. Scale can be (but is not always) related to the size of the population

#### **Waterfall**
- Can be useful for showing part-to-whole relationships where some of the components are negative

---

## Spatial
**Used only when precise locations or geographical patterns in data are more important to the reader than anything else**

### Example FT uses
Locator maps, regional/country maps, office locations, natural resource locations, natural disaster locations

### Chart Types

#### **Basic choropleth (rate/ratio)**
- The standard approach for putting data on a map - should always be used for rates rather than totals

#### **Proportional symbol (count/magnitude)**
- Use for totals rather than rates - be wary that small differences in data may be hard to see

#### **Flow map**
- For showing unambiguous movement across a map

#### **Contour map**
- For showing areas of equal value on a map. Can use deviation colour schemes for showing +/- values

#### **Equalised cartogram**
- Converting each unit on a map to a regular and equally-sized shape - good for representing voting regions with equal value

#### **Scaled cartogram (value)**
- Stretching and shrinking a map so that each area is sized according to a particular value

#### **Dot density**
- Used to show the location of individual events/locations - make sure to annotate any patterns the reader should see

#### **Heat map**
- Grid-based data values mapped with an intensity colour scale. As choropleth map - but not snapped to an admin/political unit

---

## Flow
**Show the reader volumes or intensity of movement between two or more states or conditions. These might be logical sequences or geographical locations**

### Example FT uses
Movement of funds, trade, migrants, lawsuits, information, relationships

### Chart Types

#### **Sankey**
- Shows changes in flows from one condition to at least one other; good for tracing the multiple paths through a complex system

#### **Waterfall**
- Designed to show the sequencing of data through a flow process, typically budget. Can include +/- components

#### **Chord**
- A complex but powerful diagram which can illustrate 2-way flows. Needs good labeling

#### **Network**
- Used for showing the strength and inter-connectedness of relationships of varying types
