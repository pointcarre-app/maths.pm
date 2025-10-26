# Technical documentation


[TOC]

Tree view of the Data Visualization 2 course, files list and developer notes.
{: .pm-subtitle}



> As of October 26, 2025


## Tree view


```bash
dataviz2/
├── 01_plan_cards.md
├── 02_covid_us_stats_analysis.md
├── 03_technical_doc.md
├── 99_sandbox.md
├── 99_sandbox_bokeh.md
├── session_0.md
├── session_1_a.md
├── session_1_a0_shannon.md
├── session_1_a1_visual.md
├── session_1_b.md
├── session_1_c.md
├── session_1_d.md
├── session_1_e.md
├── session_1_f.md
├── session_2_a.md
├── session_2_b.md
├── session_2_c.md
├── session_2_c0correction.md
├── session_3_a.md
├── session_3_b.md
└── files/
    ├── 99_test_consistency_codex_jupyter_local.ipynb
    ├── bertin-livre-couverture-cc-wikipedia.png
    ├── covid-2timeseries-us-presidency.jpg
    ├── covid-graphs-correction.ipynb
    ├── covid-graphs-statement.ipynb
    ├── covid-maps-correction.ipynb
    ├── covid-maps-statement.ipynb
    ├── covid19-states-analysis.png
    ├── covid_bokeh_10.py
    ├── covid_bokeh_11.py
    ├── covid_data_prep.py
    ├── covid_matplotlib_01.py
    ├── covid_matplotlib_02.py
    ├── covid_matplotlib_03.py
    ├── covid_matplotlib_04.py
    ├── covid_matplotlib_12.py
    ├── gdp.csv
    ├── gdp_exclude_not_country.ipynb
    ├── language_bits_per_second-original.jpeg
    ├── language_bits_per_second.webp
    ├── s1f_a.png
    ├── s1f_b.png
    ├── s1f_c.png
    ├── s1f_d.png
    ├── session_1_f.ipynb
    ├── session_1_f.py
    ├── us-states.csv
    └── bokeh_server_apps/
        ├── 01_simple_slider.py
        ├── 03_real_time_streaming.py
        ├── 05_linked_plots.py
        ├── 06_interactive_presentation.py
        ├── README.md
        ├── run_all.sh
        ├── run_presentation.sh
        ├── test_import.py
        └── visual-vocabulary-ft.png
```


## Accessing all files

- 01_plan_cards.md — [**Plan Cards**](01_plan_cards.md)
- 02_covid_us_stats_analysis.md — [**COVID-19 US Stats Analysis**](02_covid_us_stats_analysis.md)
- 03_technical_doc.md — [**Technical Documentation**](03_technical_doc.md)
- 99_sandbox.md — [**Sandbox**](99_sandbox.md)
- 99_sandbox_bokeh.md — [**Sandbox Bokeh**](99_sandbox_bokeh.md)
- session_0.md — [**Session 0**](session_0.md)
- session_1_a.md — [**Session 1a**](session_1_a.md)
- session_1_a0_shannon.md — [**Session 1a0: Shannon**](session_1_a0_shannon.md)
- session_1_a1_visual.md — [**Session 1a1: Visual**](session_1_a1_visual.md)
- session_1_b.md — [**Session 1b**](session_1_b.md)
- session_1_c.md — [**Session 1c**](session_1_c.md)
- session_1_d.md — [**Session 1d**](session_1_d.md)
- session_1_e.md — [**Session 1e**](session_1_e.md)
- session_1_f.md — [**Session 1f**](session_1_f.md)
- session_2_a.md — [**Session 2a**](session_2_a.md)
- session_2_b.md — [**Session 2b**](session_2_b.md)
- session_2_c.md — [**Session 2c**](session_2_c.md)
- session_2_c0correction.md — [**Session 2c0: Correction**](session_2_c0correction.md)
- session_3_a.md — [**Session 3a**](session_3_a.md)
- session_3_b.md — [**Session 3b**](session_3_b.md)
- **files/**
    - Download: <a href="/pm/dataviz2/files/99_test_consistency_codex_jupyter_local.ipynb" download>99_test_consistency_codex_jupyter_local.ipynb</a>
    - Download: <a href="/pm/dataviz2/files/bertin-livre-couverture-cc-wikipedia.png" download>bertin-livre-couverture-cc-wikipedia.png</a>
    - Download: <a href="/pm/dataviz2/files/covid-2timeseries-us-presidency.jpg" download>covid-2timeseries-us-presidency.jpg</a>
    - Download: <a href="/pm/dataviz2/files/covid-graphs-correction.ipynb" download>covid-graphs-correction.ipynb</a>
    - Download: <a href="/pm/dataviz2/files/covid-graphs-statement.ipynb" download>covid-graphs-statement.ipynb</a>
    - Download: <a href="/pm/dataviz2/files/covid-maps-correction.ipynb" download>covid-maps-correction.ipynb</a>
    - Download: <a href="/pm/dataviz2/files/covid-maps-statement.ipynb" download>covid-maps-statement.ipynb</a>
    - Download: <a href="/pm/dataviz2/files/covid19-states-analysis.png" download>covid19-states-analysis.png</a>
    - Download: <a href="/pm/dataviz2/files/covid_bokeh_10.py" download>covid_bokeh_10.py</a>
    - Download: <a href="/pm/dataviz2/files/covid_bokeh_11.py" download>covid_bokeh_11.py</a>
    - Download: <a href="/pm/dataviz2/files/covid_data_prep.py" download>covid_data_prep.py</a>
    - Download: <a href="/pm/dataviz2/files/covid_matplotlib_01.py" download>covid_matplotlib_01.py</a>
    - Download: <a href="/pm/dataviz2/files/covid_matplotlib_02.py" download>covid_matplotlib_02.py</a>
    - Download: <a href="/pm/dataviz2/files/covid_matplotlib_03.py" download>covid_matplotlib_03.py</a>
    - Download: <a href="/pm/dataviz2/files/covid_matplotlib_04.py" download>covid_matplotlib_04.py</a>
    - Download: <a href="/pm/dataviz2/files/covid_matplotlib_12.py" download>covid_matplotlib_12.py</a>
    - Download: <a href="/pm/dataviz2/files/gdp.csv" download>gdp.csv</a>
    - Download: <a href="/pm/dataviz2/files/gdp_exclude_not_country.ipynb" download>gdp_exclude_not_country.ipynb</a>
    - Download: <a href="/pm/dataviz2/files/language_bits_per_second-original.jpeg" download>language_bits_per_second-original.jpeg</a>
    - Download: <a href="/pm/dataviz2/files/language_bits_per_second.webp" download>language_bits_per_second.webp</a>
    - Download: <a href="/pm/dataviz2/files/s1f_a.png" download>s1f_a.png</a>
    - Download: <a href="/pm/dataviz2/files/s1f_b.png" download>s1f_b.png</a>
    - Download: <a href="/pm/dataviz2/files/s1f_c.png" download>s1f_c.png</a>
    - Download: <a href="/pm/dataviz2/files/s1f_d.png" download>s1f_d.png</a>
    - Download: <a href="/pm/dataviz2/files/session_1_f.ipynb" download>session_1_f.ipynb</a>
    - Download: <a href="/pm/dataviz2/files/session_1_f.py" download>session_1_f.py</a>
    - Download: <a href="/pm/dataviz2/files/us-states.csv" download>us-states.csv</a>
    - **bokeh_server_apps/**
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/01_simple_slider.py" download>01_simple_slider.py</a>
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/03_real_time_streaming.py" download>03_real_time_streaming.py</a>
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/05_linked_plots.py" download>05_linked_plots.py</a>
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/06_interactive_presentation.py" download>06_interactive_presentation.py</a>
        - README.md — [**README**](files/bokeh_server_apps/README.md)
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/run_all.sh" download>run_all.sh</a>
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/run_presentation.sh" download>run_presentation.sh</a>
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/test_import.py" download>test_import.py</a>
        - Download: <a href="/pm/dataviz2/files/bokeh_server_apps/visual-vocabulary-ft.png" download>visual-vocabulary-ft.png</a>







## Developer notes

### Frontend Dependencies

This product (`dataviz2`) loads the following external dependencies in the HTML `<head>`:

#### 1. Fonts

- **Google Fonts** (multiple families):
    - Comfortaa (300-700)
    - Cormorant Garamond (300-700, italic variants)
    - Dancing Script (400-700)
    - EB Garamond (400-800, italic variants)
    - Inter (100-900, variable font)
    - JetBrains Mono (100-800, italic variants)
    - Lora (400-700, italic variants)
    - Playfair Display (400-900, italic variants)
    - Source Serif 4 (200-900, variable font, italic variants)
    - Spectral (200-800, italic variants)
    - Lexend (100-900)
- **Open Dyslexic** v1.0.3 (accessibility font)

#### 2. CSS Frameworks

- **Tailwind CSS** v4.1.16 (browser version via CDN)
- **DaisyUI** v5 (component library)

#### 3. Custom Stylesheets

- `/static/css/root.css` (domain-level root styles)
- `/static/css/styles.css` (domain-level styles)
- `/static/css/styles-alt.css` (domain-level alternative styles)
- `/static/products/dataviz2/css/pm.css` (product-specific styles)
- `/static/products/dataviz2/css/toc.css` (table of contents styles)
- `/static/products/dataviz2/css/dataviz2.css` (product-specific styles)

#### 4. JavaScript Libraries

**Accessibility:**

- `/static/js/accessibility-manager.js` (custom accessibility manager)

**Math Rendering:**

- **KaTeX** v0.16.9 (CSS + JS + auto-render extension)
- **MathLive** v0.105.2 (interactive LaTeX editor)

**Code Editor:**

- **CodeMirror** v5.65.16 (CSS + JS + Python mode)

**Product-specific:**

- `/static/products/dataviz2/js/bokeh-detector.js` (Bokeh plot detection)
- `/static/products/dataviz2/js/main.js` (product main script)

#### 5. Configuration Notes

- Tailwind is configured with typography plugin
- KaTeX delimiters: `$$...$$` (display), `$...$` (inline)
- Math rendering can be delayed and triggered via `render-math-now` event
- Metadata includes SEO, OpenGraph, and Twitter card properties

#### 6. Page-Specific Dependencies (Dynamic Loading)

Some markdown files include frontmatter that triggers additional JavaScript dependencies to be loaded dynamically. Example from `session_3_a.md`:

```yaml
---
js_dependencies:
  - "https://cdn.bokeh.org/bokeh/release/bokeh-3.6.2.min.js"
  - "https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.6.2.min.js"
  - "https://cdn.bokeh.org/bokeh/release/bokeh-tables-3.6.2.min.js"
---
```

These dependencies are loaded only when the specific page is rendered, allowing for:

- **Conditional loading** of heavy libraries (like Bokeh)
- **Performance optimization** by avoiding global loading of page-specific dependencies
- **Flexibility** for different pages to require different JavaScript libraries
