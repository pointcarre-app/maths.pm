# Data Visualization 


[TOC]

Organizational aspects and syllabus
{: .pm-subtitle}


<!-- <hr class="my-5 border-base-200"> -->


## An first example from Reuters


![COVID-19 Mortality in the US](files/covid-2timeseries-us-presidency.jpg)

> Can we make bold statements about the time-series of COVID-19 of numbers of deaths in the US ? Do we need more data ?


The complete article from **Reuters** is available [here](https://www.reuters.com/world/us/biden-marks-1-million-americans-dead-covid-2022-05-12/).
To better understand this chart and the conclusion we can draw more, details are provided [here](80_covid_us_stats_analysis.md).


## About this course



### 📝 Organizational details

**Teaching Language:** English  
**ECTS Credits:** 1  
**Duration:** 

- 15 hours lectures and tutorials (i.e. $3\\times 5h= 15h$)
- 10 hours personal work  

**Teaching material: *(more details below)***

- *"Slides"*
- Exercises



### ✅ Prerequisites

- Basics on Python
- (secondary) Fundamental statistics and mathematics
- (secondary) Understanding of data structures (mostly `numpy.arrays`, `pandas.DataFrames`)

**Those two secondary aspects will be presented in the course, but not covered in depth.**



### 🛠️ Technologies used in this course


**Software:** Python 

**Focus on the libraries:**

- Matplotlib
- Bokeh


### 📊 Learning Outcomes

- Notions in graphic semiology to be able to choose the relevant vizualisation. 
- Creation of interactive diagrams, cartographic or otherwise, to represent datasets, in Python.



### 🎯 Subjects Covered

> Data visualization is a fundamental ingredient of data science as it “forces us to notice what we never expected to see” in a given dataset. Dataviz is also a tool for communication and, as such, is a visual language. All along the courses, we will focus on methods and strategies to represent datasets, using dynamic and interactive tools.






<!-- 
**📖 Course Materials:**
- **[Introduction & Interactive Notebooks](01_introduction.md)** - Getting started with Jupyter environments and code fragments
- **[Jupyter Launcher](jupyter_launcher.md)** - Direct access to interactive Python environments -->

### 📝 Evaluation
The evaluation consists on a data vizualisation project. The students will have *to build a web site* based on Bokeh library. As this course doesn't include any web development concepts and tools, the student will have will have the right to use a `Jupyter Notebook`. Hence, bokeh interactivity will be avalaible



## Detailed plan and organization of the course

### 1️⃣ Session 1: Foundations & Graphic Semiology (3 hours)

#### Hour 1: Course Introduction & Visual Variables

- [**Course overview and evaluation criteria**](00_plan.md) *(i.e. the file you're currently reading)*
- [**Graphic Semiology Fundamentals**](session_1_a.md)
- <span class="text-base-content/60"> [Optional] [**Installing Python, the clean way**](01_installing_python.md) </span>


#### Hours 2 & 3: Data types & first graphs

- [**Data Types Classification and introduction to `matplotlib`**](session_1_h_23.md)
- [**Groups consitution and project data requirements**](01_session_1_b.md)
- [**Practical work with `matplotlib`**](01_session_1_c.md)


### 2️⃣ Session 2: Static data vizualisation panorama


#### Hour 1 & 2: Static graphical representation panorama

- [**`matplotlib` as the Python reference**](01_session_2_a.md)
- [**Practical work with `matplotlib`**](01_session_2_b.md)
<!-- Proposer en groupe -->



#### Hours 3: Group work: project setup

- [**Data selection & project planning**](01_session_2_c.md)

<!-- Precise deilverable -->



### 3️⃣ Session 3: Advanced data vizualisation


Any issue related to the proper execution of code on machine must be solved during this session. **Feel free to ask for help.**
{: .alert .alert-error .alert-soft}

Each group must have selected a dataset and a project scope during hour 3.
{: .alert .alert-warning .alert-soft}

It's good practice to think about the story you want to tell with your data. Combined with the characteristics of your data, **this will help you to choose the relevant graph types.** 
{: .alert .alert-success .alert-soft}

Even though data modeling is not the scope of this course, prelaminary knowledge of the correlations and or causations and *"forces at play"* can help a lot to build story statistically defended.
{: .alert .alert-success .alert-soft}



#### Hour 1: Advanced static data vizualisation 

- [**Advanced static data vizualisation**](01_session_3_a.md)
<!-- Include geojson here -->

#### Hour 2: Interactive data vizualisation

- [**Bokeh presentation and basic usage**](01_session_3_b.md)


#### Hour 3: Group work: data validation

- [**Practical work per group: data refinement & first graphs**](01_session_3_c.md)


### 4️⃣ Session 4: Practical Work

#### Hours 1 & 2: Practical work

- [**Practical work: COVID 19 in the US**](01_session_4_a.md)

- [**Practical work: COVID 19 in the US: cartographic representation**](01_session_4_b.md)



#### Hour 3: Group work: advanced data vizualisation

- [**Practical work per group: advanced data vizualisation**](01_session_4_c.md)



### 5️⃣ Session 5: Finale session & project presentations



#### Hour 1: Some other Python libraries

- [**`networkx` and `seaborn`**](01_session_5_a.md)

<!-- ?? To see if seaborn is viable -->

#### Hour 2: Group work: final project polishing

- [**Practical work per group: final project**](01_session_5_a.md)


#### Hour 2: Group work: final project

- [**Practical work per group: final project**](01_session_5_b.md)