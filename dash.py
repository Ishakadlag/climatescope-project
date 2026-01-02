import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="ClimateScope Dashboard",
    layout="wide"
)

# =====================================================
# LOAD & PREPARE DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_weather.csv")

    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
    df = df.dropna(subset=['last_updated'])

    df['year'] = df['last_updated'].dt.year
    df['month'] = df['last_updated'].dt.month
    df['month_name'] = df['last_updated'].dt.strftime('%b')
    df['year_month'] = df['last_updated'].dt.to_period('M').astype(str)

    return df

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.title("🌍 ClimateScope Filters")

# -------- COUNTRY FILTER WITH ALL OPTION --------
all_countries = sorted(df['country'].unique())
country_options = ["All Countries"] + all_countries

selected_countries = st.sidebar.multiselect(
    "Select Country",
    options=country_options,
    default=["All Countries"]
)

countries = all_countries if "All Countries" in selected_countries else selected_countries

# -------- DATE FILTER --------
date_range = st.sidebar.date_input(
    "Date Range",
    [df['last_updated'].min(), df['last_updated'].max()]
)

# -------- METRIC FILTER --------
metric = st.sidebar.selectbox(
    "Select Metric",
    ["temperature_celsius", "humidity", "precip_mm", "wind_kph"]
)

# -------- EXTREME THRESHOLD --------
threshold = st.sidebar.slider(
    "Extreme Threshold",
    float(df[metric].min()),
    float(df[metric].max()),
    float(df[metric].quantile(0.95))
)

# -------- PAGE NAVIGATION --------
page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Statistical Analysis",
        "Climate Trends",
        "Extreme Events",
        "Help"
    ]
)

# =====================================================
# APPLY FILTERS
# =====================================================
filtered = df[
    (df['country'].isin(countries)) &
    (df['last_updated'].between(
        pd.to_datetime(date_range[0]),
        pd.to_datetime(date_range[1])
    ))
]

if filtered.empty:
    st.warning("⚠️ No data available for selected filters.")
    st.stop()

# =====================================================
# DATA VALIDATION SUMMARY
# =====================================================
st.sidebar.markdown("### 🧪 Data Validation Summary")

total_records = len(filtered)
missing_pct = (filtered.isnull().sum().sum() / filtered.size) * 100
duplicate_rows = filtered.duplicated().sum()

st.sidebar.write(f"**Records:** {total_records}")
st.sidebar.write(f"**Missing %:** {missing_pct:.2f}%")
st.sidebar.write(f"**Duplicate Rows:** {duplicate_rows}")
st.sidebar.write(f"**Countries:** {filtered['country'].nunique()}")
st.sidebar.write(
    f"**Date Range:** {filtered['last_updated'].min().date()} → {filtered['last_updated'].max().date()}"
)

# =====================================================
# OUTLIER DETECTION (IQR METHOD)
# =====================================================
Q1 = filtered[metric].quantile(0.25)
Q3 = filtered[metric].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = filtered[
    (filtered[metric] < lower_bound) |
    (filtered[metric] > upper_bound)
]

# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================
if page == "Executive Dashboard":
    st.title("🌎 ClimateScope – Executive Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average", round(filtered[metric].mean(), 2))
    c2.metric("Maximum", round(filtered[metric].max(), 2))
    c3.metric("Minimum", round(filtered[metric].min(), 2))
    c4.metric("Records", len(filtered))

    st.subheader("📌 Latest Weather Snapshot")
    latest = filtered.sort_values("last_updated").iloc[-1]

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Temp (°C)", round(latest["temperature_celsius"], 2))
    s2.metric("Humidity (%)", round(latest["humidity"], 2))
    s3.metric("Rain (mm)", round(latest["precip_mm"], 2))
    s4.metric("Wind (kph)", round(latest["wind_kph"], 2))

    st.subheader("🗺️ Global Weather Map")
    fig_map = px.scatter_geo(
        filtered,
        lat="latitude",
        lon="longitude",
        color=metric,
        hover_name="country",
        animation_frame="year",
        projection="natural earth"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("📈 Time-Series Trend")
    ts = filtered.groupby("last_updated")[metric].mean().reset_index()
    fig_ts = px.line(ts, x="last_updated", y=metric)
    st.plotly_chart(fig_ts, use_container_width=True)

# =====================================================
# STATISTICAL ANALYSIS
# =====================================================
elif page == "Statistical Analysis":
    st.title("📊 Statistical Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig_scatter = px.scatter(
            filtered,
            x="humidity",
            y="temperature_celsius",
            color="country",
            title="Temperature vs Humidity"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        corr = filtered[
            ["temperature_celsius", "humidity", "precip_mm", "wind_kph"]
        ].dropna().corr()
        fig_heat = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
        st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("📋 Descriptive Statistics")
    st.dataframe(filtered.describe())

    st.subheader("🧪 Missing Values Check")
    st.dataframe(
        filtered.isnull().sum().reset_index()
        .rename(columns={"index": "Column", 0: "Missing Values"})
    )

    st.subheader("🚨 Outlier Detection (IQR Method)")
    st.write(f"**Outliers detected:** {len(outliers)}")
    st.dataframe(outliers[["country", "last_updated", metric]].head(10))

    fig_outlier = px.box(
        filtered,
        y=metric,
        points="outliers",
        title="Outlier Visualization (Box Plot)"
    )
    st.plotly_chart(fig_outlier, use_container_width=True)

# =====================================================
# CLIMATE TRENDS
# =====================================================
elif page == "Climate Trends":
    st.title("🌡️ Climate Trends")

    monthly = filtered.groupby("year_month")[metric].mean().reset_index()

    fig_line = px.line(
        monthly,
        x="year_month",
        y=metric,
        title="Monthly Climate Trend Over Time"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    fig_box_country = px.box(
        filtered,
        x="country",
        y=metric,
        title="Metric Distribution by Country"
    )
    st.plotly_chart(fig_box_country, use_container_width=True)

# =====================================================
# EXTREME EVENTS
# =====================================================
elif page == "Extreme Events":
    st.title("🚨 Extreme Climate Events")

    extreme = filtered[filtered[metric] >= threshold]

    if extreme.empty:
        st.warning("No extreme events detected for selected threshold.")
    else:
        freq = extreme.groupby("country")[metric].count().reset_index()
        fig_freq = px.bar(freq, x="country", y=metric)
        st.plotly_chart(fig_freq, use_container_width=True)

        st.subheader("🏆 Top 5 Extreme Events")
        st.dataframe(
            extreme.sort_values(metric, ascending=False)
            .head(5)[["country", "last_updated", metric]]
        )

# =====================================================
# HELP PAGE
# =====================================================
else:
    st.title("❓ Help & User Guide")
    st.markdown("""
    **ClimateScope Dashboard**

    - Supports global and country-wise analysis  
    - Includes data validation and outlier detection  
    - Uses IQR method for statistical outlier identification  
    - Suitable for academic and analytical use  
    """)

# =====================================================
# DOWNLOAD DATA
# =====================================================
st.sidebar.download_button(
    "⬇️ Download Filtered Data",
    filtered.to_csv(index=False),
    file_name="filtered_climate_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("🌍 ClimateScope Dashboard | Data Science Project")
