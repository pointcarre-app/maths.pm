#!/usr/bin/env python
"""
Interactive Presentation App with Bokeh
Run with: bokeh serve 06_interactive_presentation.py
Then open: http://localhost:5006/06_interactive_presentation
"""

from bokeh.plotting import figure, curdoc
from bokeh.models import (
    Div,
    Button,
    Slider,
    Select,
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    ColorBar,
    BasicTicker,
    PrintfTickFormatter,
)
from bokeh.layouts import column, row, layout
from bokeh.palettes import RdYlBu11, Category20
from bokeh.transform import factor_cmap
import numpy as np
import pandas as pd


class InteractivePresentation:
    def __init__(self):
        self.current_slide = 0
        self.total_slides = 6
        self.slides = []
        self.auto_play = False
        self.auto_play_callback = None

        # Create all slides
        self.create_slides()

        # Create navigation
        self.create_navigation()

        # Create main layout
        self.create_layout()

    def create_navigation(self):
        """Create navigation controls"""
        # Navigation buttons
        self.prev_button = Button(label="◀ Previous", button_type="primary", width=100)
        self.next_button = Button(label="Next ▶", button_type="primary", width=100)
        self.home_button = Button(label="🏠 Home", button_type="warning", width=100)

        # Auto-play controls
        self.play_button = Button(label="▶ Auto Play", button_type="success", width=100)
        self.stop_button = Button(label="⏸ Stop", button_type="danger", width=100)

        # Slide selector
        slide_options = [
            (str(i), f"Slide {i + 1}: {self.get_slide_title(i)}") for i in range(self.total_slides)
        ]
        self.slide_select = Select(title="Jump to:", value="0", options=slide_options, width=300)

        # Progress indicator
        self.progress_div = Div(text=self.get_progress_html(), width=200)

        # Attach callbacks
        self.prev_button.on_click(self.prev_slide)
        self.next_button.on_click(self.next_slide)
        self.home_button.on_click(self.go_home)
        self.play_button.on_click(self.start_auto_play)
        self.stop_button.on_click(self.stop_auto_play)
        self.slide_select.on_change("value", self.jump_to_slide)

    def get_slide_title(self, index):
        """Get title for each slide"""
        titles = [
            "Welcome",
            "Data Overview",
            "Interactive Analysis",
            "Time Series Trends",
            "Correlation Explorer",
            "Conclusions",
        ]
        return titles[index] if index < len(titles) else f"Slide {index + 1}"

    def get_progress_html(self):
        """Generate progress bar HTML"""
        progress_pct = ((self.current_slide + 1) / self.total_slides) * 100
        return f"""
        <div style="text-align: center;">
            <b>Slide {self.current_slide + 1} of {self.total_slides}</b><br>
            <div style="width: 100%; background-color: #f0f0f0; border-radius: 5px;">
                <div style="width: {progress_pct}%; background-color: #4CAF50; 
                           height: 20px; border-radius: 5px;"></div>
            </div>
        </div>
        """

    def create_slides(self):
        """Create all presentation slides"""
        self.slides = [
            self.create_slide_1_welcome(),
            self.create_slide_2_overview(),
            self.create_slide_3_interactive(),
            self.create_slide_4_timeseries(),
            self.create_slide_5_correlation(),
            self.create_slide_6_conclusions(),
        ]

    def create_slide_1_welcome(self):
        """Slide 1: Welcome and Introduction"""
        # Title and intro
        title = Div(
            text="""
        <h1 style="text-align: center; color: #2c3e50;">
            📊 Interactive Data Presentation with Bokeh
        </h1>
        """,
            width=800,
            height=80,
        )

        # Animated scatter plot
        n_points = 100
        x = np.random.randn(n_points)
        y = np.random.randn(n_points)
        colors = np.random.choice(["red", "green", "blue", "yellow", "purple"], n_points)
        sizes = np.random.randint(10, 30, n_points)

        source = ColumnDataSource(data=dict(x=x, y=y, colors=colors, sizes=sizes))

        p = figure(width=600, height=400, title="Welcome to Interactive Visualization")
        p.scatter("x", "y", size="sizes", color="colors", alpha=0.6, source=source)

        # Info panels
        features = Div(
            text="""
        <div style="background-color: #ecf0f1; padding: 20px; border-radius: 10px;">
            <h3>🎯 Presentation Features:</h3>
            <ul style="font-size: 14px;">
                <li>📱 <b>Fully Interactive:</b> All plots support zoom, pan, and hover</li>
                <li>🔄 <b>Real-time Updates:</b> Dynamic data visualization</li>
                <li>🎮 <b>User Controls:</b> Sliders, buttons, and selections</li>
                <li>📊 <b>Multiple Chart Types:</b> Line, scatter, bar, heatmap</li>
                <li>🔗 <b>Linked Visualizations:</b> Selections across multiple plots</li>
                <li>⏯️ <b>Auto-play Mode:</b> Automatic slide progression</li>
            </ul>
        </div>
        """,
            width=400,
            height=300,
        )

        instructions = Div(
            text="""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px;">
            <h3>🎮 Navigation:</h3>
            <ul style="font-size: 14px;">
                <li>Use <b>Next/Previous</b> buttons to navigate</li>
                <li>Select specific slides from dropdown</li>
                <li>Click <b>Auto Play</b> for presentation mode</li>
                <li>All visualizations are interactive!</li>
            </ul>
        </div>
        """,
            width=400,
            height=200,
        )

        # Animate button
        animate_btn = Button(label="🎨 Shuffle Data", button_type="success")

        def animate():
            new_x = np.random.randn(n_points)
            new_y = np.random.randn(n_points)
            new_colors = np.random.choice(["red", "green", "blue", "yellow", "purple"], n_points)
            new_sizes = np.random.randint(10, 30, n_points)
            source.data = dict(x=new_x, y=new_y, colors=new_colors, sizes=new_sizes)

        animate_btn.on_click(animate)

        return layout([[title], [column(p, animate_btn), column(features, instructions)]])

    def create_slide_2_overview(self):
        """Slide 2: Data Overview with Multiple Charts"""
        title = Div(
            text="""
        <h2 style="color: #2c3e50;">📈 Data Overview Dashboard</h2>
        <p>Multiple synchronized visualizations showing different aspects of the dataset</p>
        """,
            width=800,
        )

        # Generate sample data
        categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
        years = ["2020", "2021", "2022", "2023", "2024"]

        # Bar chart data
        bar_data = pd.DataFrame(
            {"categories": categories, "values": np.random.randint(50, 200, len(categories))}
        )
        bar_source = ColumnDataSource(bar_data)

        # Line chart data
        line_data = pd.DataFrame({"x": range(50), "y": np.cumsum(np.random.randn(50)) + 100})
        line_source = ColumnDataSource(line_data)

        # Pie chart simulation (using wedge)
        angles = [0, 72, 144, 216, 288]
        colors = Category20[5]
        percentages = np.random.randint(10, 30, 5)
        percentages = percentages / percentages.sum() * 100

        # Create plots
        # 1. Bar chart
        p1 = figure(
            x_range=categories,
            width=400,
            height=300,
            title="Sales by Product",
            toolbar_location="above",
        )
        p1.vbar(
            x="categories",
            top="values",
            width=0.8,
            source=bar_source,
            color=factor_cmap("categories", palette=Category20[5], factors=categories),
        )
        p1.y_range.start = 0

        # 2. Line chart
        p2 = figure(width=400, height=300, title="Trend Analysis")
        p2.line("x", "y", source=line_source, line_width=2, color="navy")
        p2.circle("x", "y", source=line_source, size=5, color="navy", alpha=0.5)

        # 3. Heatmap
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

        heatmap_data = []
        for month in months:
            for day in days:
                heatmap_data.append((month, day, np.random.randint(0, 100)))

        hm_source = ColumnDataSource(
            data=dict(
                months=[x[0] for x in heatmap_data],
                days=[x[1] for x in heatmap_data],
                values=[x[2] for x in heatmap_data],
            )
        )

        p3 = figure(
            x_range=months,
            y_range=days,
            width=400,
            height=300,
            title="Activity Heatmap",
            toolbar_location="above",
        )

        mapper = LinearColorMapper(palette=RdYlBu11[::-1], low=0, high=100)
        p3.rect(
            x="months",
            y="days",
            width=1,
            height=1,
            source=hm_source,
            fill_color={"field": "values", "transform": mapper},
        )

        color_bar = ColorBar(color_mapper=mapper, width=8, location=(0, 0))
        p3.add_layout(color_bar, "right")

        # Statistics panel
        stats = Div(
            text=f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h3>📊 Key Metrics:</h3>
            <table style="width: 100%;">
                <tr><td><b>Total Products:</b></td><td>{len(categories)}</td></tr>
                <tr><td><b>Average Sales:</b></td><td>${bar_data["values"].mean():.2f}</td></tr>
                <tr><td><b>Max Sales:</b></td><td>${bar_data["values"].max()}</td></tr>
                <tr><td><b>Growth Rate:</b></td><td>+{np.random.uniform(5, 15):.1f}%</td></tr>
                <tr><td><b>Data Points:</b></td><td>{len(line_data)}</td></tr>
            </table>
        </div>
        """,
            width=400,
            height=200,
        )

        return layout([[title], [p1, p2], [p3, stats]])

    def create_slide_3_interactive(self):
        """Slide 3: Interactive Analysis with Controls"""
        title = Div(
            text="""
        <h2 style="color: #2c3e50;">🎮 Interactive Data Explorer</h2>
        <p>Adjust parameters to explore different data visualizations</p>
        """,
            width=800,
        )

        # Create data
        self.slide3_source = ColumnDataSource(data=dict(x=[], y=[]))

        # Create plot
        p = figure(width=600, height=400, title="Interactive Function Plotter")
        self.slide3_line = p.line("x", "y", source=self.slide3_source, line_width=2, color="blue")

        # Controls
        self.func_select = Select(
            title="Function:", value="sin", options=["sin", "cos", "exp", "log", "polynomial"]
        )
        self.param_slider = Slider(start=0.1, end=5, value=1, step=0.1, title="Parameter")
        self.points_slider = Slider(start=50, end=500, value=100, step=50, title="Number of Points")
        self.noise_slider = Slider(start=0, end=1, value=0, step=0.05, title="Noise Level")

        # Update function
        def update_slide3():
            func = self.func_select.value
            param = self.param_slider.value
            n_points = int(self.points_slider.value)
            noise = self.noise_slider.value

            x = np.linspace(0, 10, n_points)

            if func == "sin":
                y = np.sin(param * x)
            elif func == "cos":
                y = np.cos(param * x)
            elif func == "exp":
                y = np.exp(-param * x / 5)
            elif func == "log":
                y = np.log(param * x + 1)
            else:  # polynomial
                y = param * x**2 - 2 * x + 1

            # Add noise
            if noise > 0:
                y += np.random.normal(0, noise, len(y))

            self.slide3_source.data = dict(x=x, y=y)

            # Update plot title
            p.title.text = f"{func.upper()} Function (param={param:.1f}, noise={noise:.1f})"

        # Attach callbacks
        self.func_select.on_change("value", lambda a, o, n: update_slide3())
        self.param_slider.on_change("value", lambda a, o, n: update_slide3())
        self.points_slider.on_change("value", lambda a, o, n: update_slide3())
        self.noise_slider.on_change("value", lambda a, o, n: update_slide3())

        # Initial update
        update_slide3()

        # Info panel
        info = Div(
            text="""
        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px;">
            <h3>🎯 Try These:</h3>
            <ul>
                <li>Change function type</li>
                <li>Adjust parameter to modify shape</li>
                <li>Add noise for realistic data</li>
                <li>Change number of points</li>
            </ul>
            <p><b>Tip:</b> Combine different settings to see interesting patterns!</p>
        </div>
        """,
            width=300,
            height=200,
        )

        controls = column(
            self.func_select, self.param_slider, self.points_slider, self.noise_slider, info
        )

        return layout([[title], [p, controls]])

    def create_slide_4_timeseries(self):
        """Slide 4: Time Series Analysis"""
        title = Div(
            text="""
        <h2 style="color: #2c3e50;">📅 Time Series Analysis</h2>
        <p>Exploring temporal patterns and trends</p>
        """,
            width=800,
        )

        # Generate time series data
        dates = pd.date_range("2023-01-01", periods=365, freq="D")
        base_trend = np.linspace(100, 150, 365)
        seasonal = 10 * np.sin(np.arange(365) * 2 * np.pi / 365)
        noise = np.random.randn(365) * 5
        values = base_trend + seasonal + noise

        # Create moving averages
        ma7 = pd.Series(values).rolling(window=7).mean()
        ma30 = pd.Series(values).rolling(window=30).mean()

        source = ColumnDataSource(data=dict(dates=dates, values=values, ma7=ma7, ma30=ma30))

        # Create plot
        p = figure(
            width=800, height=400, x_axis_type="datetime", title="Time Series with Moving Averages"
        )

        p.line(
            "dates",
            "values",
            source=source,
            line_width=1,
            color="lightgray",
            alpha=0.8,
            legend_label="Daily",
        )
        p.line("dates", "ma7", source=source, line_width=2, color="blue", legend_label="7-day MA")
        p.line("dates", "ma30", source=source, line_width=2, color="red", legend_label="30-day MA")

        p.legend.location = "top_left"
        p.legend.click_policy = "hide"

        # Add hover tool
        hover = HoverTool(
            tooltips=[
                ("Date", "@dates{%F}"),
                ("Value", "@values{0.00}"),
                ("7-day MA", "@ma7{0.00}"),
                ("30-day MA", "@ma30{0.00}"),
            ],
            formatters={"@dates": "datetime"},
        )
        p.add_tools(hover)

        # Statistics
        stats = Div(
            text=f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h3>📈 Time Series Statistics:</h3>
            <table>
                <tr><td><b>Period:</b></td><td>{dates[0].strftime("%Y-%m-%d")} to {dates[-1].strftime("%Y-%m-%d")}</td></tr>
                <tr><td><b>Data Points:</b></td><td>{len(dates)}</td></tr>
                <tr><td><b>Mean:</b></td><td>{np.mean(values):.2f}</td></tr>
                <tr><td><b>Std Dev:</b></td><td>{np.std(values):.2f}</td></tr>
                <tr><td><b>Min:</b></td><td>{np.min(values):.2f}</td></tr>
                <tr><td><b>Max:</b></td><td>{np.max(values):.2f}</td></tr>
                <tr><td><b>Trend:</b></td><td>+{(values[-1] - values[0]):.2f}</td></tr>
            </table>
        </div>
        """,
            width=800,
            height=150,
        )

        return layout([[title], [p], [stats]])

    def create_slide_5_correlation(self):
        """Slide 5: Correlation Matrix Explorer"""
        title = Div(
            text="""
        <h2 style="color: #2c3e50;">🔗 Correlation Analysis</h2>
        <p>Exploring relationships between variables</p>
        """,
            width=800,
        )

        # Generate correlated data
        n_vars = 8
        n_samples = 100
        var_names = [f"Var_{i + 1}" for i in range(n_vars)]

        # Create correlation matrix
        data = np.random.randn(n_samples, n_vars)
        # Add some correlations
        data[:, 1] = data[:, 0] * 0.8 + np.random.randn(n_samples) * 0.2
        data[:, 2] = data[:, 0] * -0.6 + np.random.randn(n_samples) * 0.3
        data[:, 4] = data[:, 3] * 0.7 + np.random.randn(n_samples) * 0.3

        corr_matrix = np.corrcoef(data.T)

        # Prepare data for heatmap
        corr_data = []
        for i, var1 in enumerate(var_names):
            for j, var2 in enumerate(var_names):
                corr_data.append((var1, var2, corr_matrix[i, j]))

        source = ColumnDataSource(
            data=dict(
                var1=[x[0] for x in corr_data],
                var2=[x[1] for x in corr_data],
                corr=[x[2] for x in corr_data],
            )
        )

        # Create heatmap
        p = figure(
            x_range=var_names,
            y_range=list(reversed(var_names)),
            width=500,
            height=500,
            title="Correlation Matrix",
            toolbar_location="above",
            tools="hover,save",
        )

        mapper = LinearColorMapper(palette=RdYlBu11[::-1], low=-1, high=1)

        p.rect(
            "var1",
            "var2",
            width=1,
            height=1,
            source=source,
            fill_color={"field": "corr", "transform": mapper},
            line_color="white",
        )

        # Configure hover
        p.hover.tooltips = [("Variables", "@var1 - @var2"), ("Correlation", "@corr{0.00}")]

        # Add color bar
        color_bar = ColorBar(
            color_mapper=mapper,
            width=8,
            location=(0, 0),
            ticker=BasicTicker(desired_num_ticks=10),
            formatter=PrintfTickFormatter(format="%.1f"),
        )
        p.add_layout(color_bar, "right")

        # Interpretation guide
        guide = Div(
            text="""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h3>📊 Interpretation Guide:</h3>
            <ul>
                <li><span style="color: darkblue;">■ Dark Blue:</span> Strong positive correlation (≈1.0)</li>
                <li><span style="color: lightblue;">■ Light Blue:</span> Weak positive correlation</li>
                <li><span style="color: yellow;">■ Yellow:</span> No correlation (≈0.0)</li>
                <li><span style="color: orange;">■ Orange:</span> Weak negative correlation</li>
                <li><span style="color: darkred;">■ Dark Red:</span> Strong negative correlation (≈-1.0)</li>
            </ul>
            <p><b>Hover</b> over cells to see exact correlation values</p>
        </div>
        """,
            width=300,
            height=300,
        )

        return layout([[title], [p, guide]])

    def create_slide_6_conclusions(self):
        """Slide 6: Conclusions and Summary"""
        title = Div(
            text="""
        <h1 style="text-align: center; color: #2c3e50;">
            🎯 Conclusions & Key Takeaways
        </h1>
        """,
            width=800,
            height=80,
        )

        # Summary cards
        card1 = Div(
            text="""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; margin: 10px;">
            <h3>✅ What We've Demonstrated</h3>
            <ul>
                <li>Interactive visualizations with real-time updates</li>
                <li>Multiple chart types and layouts</li>
                <li>User controls and parameter adjustments</li>
                <li>Linked data across multiple plots</li>
                <li>Time series analysis capabilities</li>
                <li>Statistical visualizations</li>
            </ul>
        </div>
        """,
            width=380,
            height=250,
        )

        card2 = Div(
            text="""
        <div style="background-color: #f0f8e8; padding: 20px; border-radius: 10px; margin: 10px;">
            <h3>🚀 Bokeh Server Advantages</h3>
            <ul>
                <li>Python callbacks for complex logic</li>
                <li>Real-time data streaming</li>
                <li>Server-side computation</li>
                <li>Multi-client support</li>
                <li>Stateful interactions</li>
                <li>Production-ready deployment</li>
            </ul>
        </div>
        """,
            width=380,
            height=250,
        )

        card3 = Div(
            text="""
        <div style="background-color: #fff0e8; padding: 20px; border-radius: 10px; margin: 10px;">
            <h3>📚 Use Cases</h3>
            <ul>
                <li>Business intelligence dashboards</li>
                <li>Scientific data exploration</li>
                <li>Real-time monitoring systems</li>
                <li>Interactive reports</li>
                <li>Educational tools</li>
                <li>Data storytelling</li>
            </ul>
        </div>
        """,
            width=380,
            height=250,
        )

        card4 = Div(
            text="""
        <div style="background-color: #f8e8f0; padding: 20px; border-radius: 10px; margin: 10px;">
            <h3>💡 Next Steps</h3>
            <ul>
                <li>Explore the source code</li>
                <li>Customize for your data</li>
                <li>Add more visualizations</li>
                <li>Deploy to production</li>
                <li>Integrate with databases</li>
                <li>Build your own apps!</li>
            </ul>
        </div>
        """,
            width=380,
            height=250,
        )

        # Thank you message
        thanks = Div(
            text="""
        <div style="text-align: center; margin-top: 30px;">
            <h2 style="color: #2c3e50;">Thank You! 🙏</h2>
            <p style="font-size: 16px;">
                This presentation was built entirely with Bokeh Server<br>
                All visualizations are live and interactive<br>
                <br>
                <b>Questions?</b> Explore the code and experiment!
            </p>
        </div>
        """,
            width=800,
            height=150,
        )

        return layout([[title], [card1, card2], [card3, card4], [thanks]])

    def update_slide(self):
        """Update the current slide display"""
        # Update navigation state
        self.prev_button.disabled = self.current_slide == 0
        self.next_button.disabled = self.current_slide == self.total_slides - 1

        # Update progress
        self.progress_div.text = self.get_progress_html()

        # Update selector
        self.slide_select.value = str(self.current_slide)

        # Update main content
        self.main_content.children = [self.slides[self.current_slide]]

        print(f"Showing slide {self.current_slide + 1}: {self.get_slide_title(self.current_slide)}")

    def prev_slide(self):
        """Go to previous slide"""
        if self.current_slide > 0:
            self.current_slide -= 1
            self.update_slide()

    def next_slide(self):
        """Go to next slide"""
        if self.current_slide < self.total_slides - 1:
            self.current_slide += 1
            self.update_slide()
        elif self.auto_play:
            # Loop back to beginning in auto-play mode
            self.current_slide = 0
            self.update_slide()

    def go_home(self):
        """Go to first slide"""
        self.current_slide = 0
        self.update_slide()

    def jump_to_slide(self, attr, old, new):
        """Jump to specific slide"""
        self.current_slide = int(new)
        self.update_slide()

    def start_auto_play(self):
        """Start auto-play mode"""
        if not self.auto_play:
            self.auto_play = True
            self.auto_play_callback = curdoc().add_periodic_callback(
                self.auto_advance,
                5000,  # 5 seconds per slide
            )
            self.play_button.label = "⏸ Pause"
            self.play_button.button_type = "warning"
            print("Auto-play started")

    def stop_auto_play(self):
        """Stop auto-play mode"""
        if self.auto_play:
            self.auto_play = False
            if self.auto_play_callback:
                curdoc().remove_periodic_callback(self.auto_play_callback)
            self.play_button.label = "▶ Auto Play"
            self.play_button.button_type = "success"
            print("Auto-play stopped")

    def auto_advance(self):
        """Automatically advance to next slide"""
        self.next_slide()

    def create_layout(self):
        """Create the main layout"""
        # Navigation bar
        nav_bar = row(
            self.prev_button,
            self.home_button,
            self.next_button,
            self.slide_select,
            self.play_button,
            self.stop_button,
            self.progress_div,
        )

        # Main content area
        self.main_content = column(self.slides[0])

        # Full layout
        self.layout = column(nav_bar, Div(text="<hr>", width=1200, height=10), self.main_content)

        # Initial update
        self.update_slide()


# Create and run the presentation
presentation = InteractivePresentation()
curdoc().add_root(presentation.layout)
curdoc().title = "Interactive Presentation"

print("=" * 50)
print("Interactive Presentation App Started!")
print("=" * 50)
print("Navigate through slides using controls")
print("All visualizations are interactive")
print("Try Auto Play for presentation mode")
print("=" * 50)
