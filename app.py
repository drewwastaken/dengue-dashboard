import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Dengue Hotspot Heatmap - Metro Manila",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #d62828;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    # Load your CSV file
    df = pd.read_csv('dengue_data.csv')
    
    # Add coordinates for mapping (approximate city centers)
    coords = {
        'Quezon City': {'lat': 14.6760, 'lon': 121.0437},
        'Manila': {'lat': 14.5995, 'lon': 120.9842},
        'Caloocan': {'lat': 14.6508, 'lon': 120.9830},
        'Pasig': {'lat': 14.5764, 'lon': 121.0851},
        'Taguig': {'lat': 14.5176, 'lon': 121.0509},
        'Marikina': {'lat': 14.6507, 'lon': 121.1029},
        'Mandaluyong': {'lat': 14.5794, 'lon': 121.0359},
        'Makati': {'lat': 14.5547, 'lon': 121.0244},
        'Muntinlupa': {'lat': 14.4083, 'lon': 121.0399},
        'Las Piñas': {'lat': 14.4454, 'lon': 120.9830},
        'Parañaque': {'lat': 14.4793, 'lon': 121.0198}
    }
    
    # Clean city names (fix any typos)
    df['City'] = df['City'].str.strip()
    df['City'] = df['City'].replace('Mandaluyondo', 'Mandaluyong')
    
    df['Latitude'] = df['City'].map(lambda x: coords.get(x, {}).get('lat', 14.5995))
    df['Longitude'] = df['City'].map(lambda x: coords.get(x, {}).get('lon', 120.9842))
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B')
    
    return df

df = load_data()

# Header
st.markdown('<p class="main-header">🦟 Dengue Hotspot Heatmap: Metro Manila</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Spatiotemporal Analysis of Dengue Cases to Predict Outbreaks</p>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔍 Dashboard Filters")
st.sidebar.markdown("---")

# Year filter
years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=years,
    default=years
)

# Month filter
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
selected_months = st.sidebar.multiselect(
    "Select Month(s)",
    options=months,
    default=months
)

# City filter
cities = sorted(df['City'].unique())
selected_cities = st.sidebar.multiselect(
    "Select City/Cities",
    options=cities,
    default=cities
)

# Case threshold filter
st.sidebar.markdown("---")
case_threshold = st.sidebar.slider(
    "Minimum Cases to Display",
    min_value=0,
    max_value=int(df['Dengue_Cases'].max()),
    value=0,
    step=50
)

# Filter data
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Month'].isin(selected_months)) &
    (df['City'].isin(selected_cities)) &
    (df['Dengue_Cases'] >= case_threshold)
]

# Key Metrics
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_cases = filtered_df['Dengue_Cases'].sum()
    st.metric("Total Cases", f"{total_cases:,}")

with col2:
    total_deaths = filtered_df['Dengue_Deaths'].sum()
    st.metric("Total Deaths", f"{total_deaths:,}")

with col3:
    avg_cases = filtered_df.groupby('City')['Dengue_Cases'].sum().mean()
    st.metric("Avg Cases per City", f"{avg_cases:,.0f}")

with col4:
    if total_cases > 0:
        mortality_rate = (total_deaths / total_cases) * 100
        st.metric("Case Fatality Rate", f"{mortality_rate:.2f}%")
    else:
        st.metric("Case Fatality Rate", "0.00%")

st.markdown("---")

# Main visualizations
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 🗺️ Dengue Hotspot Map")
    
    # Aggregate data for map
    map_data = filtered_df.groupby(['City', 'Latitude', 'Longitude']).agg({
        'Dengue_Cases': 'sum',
        'Dengue_Deaths': 'sum'
    }).reset_index()
    
    # Create heatmap
    fig_map = px.scatter_mapbox(
        map_data,
        lat='Latitude',
        lon='Longitude',
        size='Dengue_Cases',
        color='Dengue_Cases',
        hover_name='City',
        hover_data={
            'Dengue_Cases': ':,',
            'Dengue_Deaths': ':,',
            'Latitude': False,
            'Longitude': False
        },
        color_continuous_scale='Reds',
        size_max=50,
        zoom=10,
        height=500
    )
    
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

with col_right:
    st.markdown("### 🏙️ Top 5 Affected Cities")
    
    top_cities = filtered_df.groupby('City')['Dengue_Cases'].sum().sort_values(ascending=False).head(5)
    
    fig_top = go.Figure(go.Bar(
        x=top_cities.values,
        y=top_cities.index,
        orientation='h',
        marker=dict(
            color=top_cities.values,
            colorscale='Reds',
            showscale=False
        ),
        text=top_cities.values,
        textposition='auto',
    ))
    
    fig_top.update_layout(
        height=500,
        xaxis_title="Total Cases",
        yaxis_title="City",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_top, use_container_width=True)

# Time series analysis
st.markdown("---")
st.markdown("### 📈 Temporal Trends")

col_ts1, col_ts2 = st.columns(2)

with col_ts1:
    st.markdown("#### Monthly Case Trends by City")
    
    monthly_data = filtered_df.groupby(['Date', 'City'])['Dengue_Cases'].sum().reset_index()
    
    fig_line = px.line(
        monthly_data,
        x='Date',
        y='Dengue_Cases',
        color='City',
        markers=True,
        height=400
    )
    
    fig_line.update_layout(
        xaxis_title="Month",
        yaxis_title="Dengue Cases",
        legend_title="City",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_line, use_container_width=True)

with col_ts2:
    st.markdown("#### Seasonal Pattern Analysis")
    
    seasonal_data = filtered_df.groupby('Month')['Dengue_Cases'].sum().reindex(months).fillna(0)
    
    fig_seasonal = go.Figure(go.Bar(
        x=months,
        y=seasonal_data.values,
        marker=dict(
            color=seasonal_data.values,
            colorscale='RdYlGn_r',
            showscale=False
        ),
        text=seasonal_data.values.astype(int),
        textposition='outside'
    ))
    
    fig_seasonal.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Cases",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_seasonal, use_container_width=True)

# Comparison analysis
st.markdown("---")
st.markdown("### 📊 Comparative Analysis")

col_comp1, col_comp2 = st.columns(2)

with col_comp1:
    st.markdown("#### Cases vs Deaths by City")
    
    comparison_data = filtered_df.groupby('City').agg({
        'Dengue_Cases': 'sum',
        'Dengue_Deaths': 'sum'
    }).reset_index()
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Cases',
        x=comparison_data['City'],
        y=comparison_data['Dengue_Cases'],
        marker_color='indianred'
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='Deaths',
        x=comparison_data['City'],
        y=comparison_data['Dengue_Deaths'],
        marker_color='darkred'
    ))
    
    fig_comparison.update_layout(
        barmode='group',
        xaxis_title="City",
        yaxis_title="Count",
        height=400,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

with col_comp2:
    st.markdown("#### Year-over-Year Comparison")
    
    yearly_data = filtered_df.groupby(['Year', 'Month'])['Dengue_Cases'].sum().reset_index()
    
    fig_yoy = px.bar(
        yearly_data,
        x='Month',
        y='Dengue_Cases',
        color='Year',
        barmode='group',
        height=400,
        category_orders={'Month': months}
    )
    
    fig_yoy.update_layout(
        xaxis_title="Month",
        yaxis_title="Dengue Cases",
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_yoy, use_container_width=True)

# Data table
st.markdown("---")
st.markdown("### 📋 Detailed Data View")

with st.expander("Click to view raw data"):
    st.dataframe(
        filtered_df[['Month', 'Year', 'City', 'Dengue_Cases', 'Dengue_Deaths']].sort_values(
            by=['Year', 'Month', 'Dengue_Cases'], 
            ascending=[False, True, False]
        ),
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>Data Source:</strong> Kaggle - Philippines | 
        <a href='https://www.kaggle.com/datasets/' target='_blank'>https://www.kaggle.com/datasets/</a></p>
        <p>Dashboard created for Health Informatics (ITE3) | Engr. Val Patrick Fabregas, MTA</p>
    </div>
""", unsafe_allow_html=True)
