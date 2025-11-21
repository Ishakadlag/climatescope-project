🌍 ClimateScope – Global Weather Trends & Extreme Events Visualization

A data-driven climate analytics platform

📌 Overview

ClimateScope is a data analysis and visualization project focused on understanding global weather patterns, anomalies, and climate behavior using the Global Weather Repository Dataset from Kaggle.

This project processes worldwide daily weather observations to uncover:

Seasonal temperature trends

Regional climatic differences

Extreme weather events

Air quality indicators

Climate anomalies across the globe

The project is divided into 4 milestones, starting from data acquisition to dashboard development.

🚀 Features

✔ Large-scale global weather dataset
✔ Automated cleaning and preprocessing
✔ Missing value & anomaly detection
✔ Daily → Monthly aggregation
✔ Normalized metrics for analysis
✔ Ready for statistical analysis and visualization (Milestone-2)
✔ Fully reproducible pipeline

🧱 Tech Stack
Component	Tools Used
Language	Python 3
Libraries	Pandas, NumPy, Matplotlib/Plotly (later), Seaborn
Storage	CSV 
Dataset Source	Kaggle Global Weather Repository
📂 Dataset Source

Dataset Used: Global Weather Repository – Kaggle
Link: https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository

Contains fields like:

temperature_celsius, humidity, wind_kph, precip_mm

Air quality metrics

Weather conditions

Timestamps (last_updated)

Geo-coordinates

Visibility, pressure, UV index, sunrise, sunset, etc.

🧩 Milestones
🟦 Milestone 1 – Data Preparation & Initial Analysis (Completed)

Tasks completed:

✔ Download & load dataset
✔ Inspect dataset structure, schema, and data types
✔ Identify missing values, anomalies, outliers
✔ Handle missing & inconsistent entries

Removed invalid temperature rows

Filled humidity with median

Filled remaining numeric missing values

Converted timestamp into datetime

Removed invalid precipitation & wind values

✔ Convert & normalize units

Used temperature_celsius and wind_kph as primary fields

✔ Aggregate daily → monthly averages

Extracted year and month

Created grouped monthly dataset

✔ Save cleaned data

Output file:
data/cleaned/monthly_weather.csv

✔ Summary document created

File: Milestone1_Summary.pdf
