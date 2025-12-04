🌍 ClimateScope — Milestone 2
Core Analysis & Interactive Dashboard Development

This document summarizes all work completed in Milestone 2, including statistical analysis, exploratory insights, visualization planning, and the development of an interactive dashboard using Plotly Dash.

✅ 1. Objective of Milestone 2

The goal of Milestone 2 was to perform core climate data analysis, identify important patterns (extreme events, regional differences, trends), and design an interactive dashboard that can visualize insights across countries.

📊 2. Work Completed
2.1 Statistical Analysis

Performed detailed analysis on the cleaned dataset generated in Milestone 1:

✔️ Distribution analysis of temperature, humidity, wind speed

✔️ Correlation analysis to find relationships between variables

Example: temperature vs humidity, wind_speed vs pressure

✔️ Seasonal trends based on timestamps

✔️ Country-wise comparative analysis

✔️ Detection of extreme weather values

High/low temperature

Very high humidity

Sudden variations in wind speed

🌦️ 3. Key Insights Derived
Temperature Trends

Countries with large climate variation were identified.

Times of sudden temperature drops/spikes were detected.

Humidity & Wind Patterns

Some regions show consistently high humidity.

Correlation revealed that wind speed spikes are often linked with lower pressure.

Extreme Events

Temperature > 45°C (heatwave range)

Sudden drops below 0°C (cold extremes)

Wind speeds > 40 km/h (storm conditions)

These events were summarized using group-by, filtering, and statistical summaries.

📍 4. Visualization Planning

The following chart types were selected for the dashboard:

Insight	Chart Type
Temperature trends	Line chart
Country-wise comparison	Bar chart / Choropleth
Global temperature distribution	World map
Humidity / wind comparison	Scatterplot
Extreme events	Heatmap / table
🖥️ 5. Interactive Dashboard (Plotly Dash)

A fully functional web-based dashboard was created using:

Dash (Plotly)

Plotly Express

Pandas

Python

✔️ Dashboard Features

Dropdown to select country

Trend line showing temperature over time

Global choropleth map showing average temperature by country

Automatic browser launch at:
http://127.0.0.1:8050/
