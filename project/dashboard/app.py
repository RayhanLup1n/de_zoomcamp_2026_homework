"""
Indonesia Weather Analytics Dashboard

Streamlit dashboard for visualizing Indonesian weather patterns
across 5 major cities using data from Open-Meteo API.

Supports dual-mode:
  - Local: DuckDB (default)
  - Cloud: BigQuery (when GCP_PROJECT_ID is set)
"""

import os
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Optional: BigQuery support for cloud mode
try:
    from google.cloud import bigquery
    from google.oauth2 import service_account

    HAS_BIGQUERY = True
except ImportError:
    HAS_BIGQUERY = False

# Page configuration
st.set_page_config(
    page_title="Indonesia Weather Analytics",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────
# Database Connection Logic
# ──────────────────────────────────────────────────────


def get_duckdb_path():
    """Get DuckDB database path from environment."""
    return os.environ.get("DUCKDB_PATH", "./data/capstone.duckdb")


def is_cloud_mode() -> bool:
    """Check if BigQuery (Cloud Mode) should be used."""
    if not HAS_BIGQUERY:
        return False
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        return False
    # On Cloud Run, ADC is available automatically
    if os.environ.get("K_SERVICE"):
        return True
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return bool(creds_path and os.path.exists(creds_path))


@st.cache_resource
def get_bigquery_client():
    """Initialize and cache BigQuery client."""
    if not is_cloud_mode():
        return None
    project_id = os.environ.get("GCP_PROJECT_ID")
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if os.environ.get("K_SERVICE") or not creds_path or not os.path.exists(creds_path):
        return bigquery.Client(project=project_id)
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    return bigquery.Client(credentials=credentials, project=project_id)


def check_database_exists() -> tuple:
    """Check if any database (BigQuery or DuckDB) is accessible."""
    if is_cloud_mode():
        try:
            client = get_bigquery_client()
            list(client.list_datasets(max_results=1))
            return True, "Connected to BigQuery"
        except Exception as e:
            return False, f"BigQuery error: {e}"
    else:
        db_path = get_duckdb_path()
        if os.path.exists(db_path):
            try:
                con = duckdb.connect(db_path, read_only=True)
                con.close()
                return True, "Connected to DuckDB"
            except Exception as e:
                return False, f"DuckDB error: {e}"
        return False, "Database not found. Run `make setup` first."


@st.cache_data(ttl=600)
def query_data(query: str) -> pd.DataFrame:
    """Execute query on BigQuery or DuckDB based on mode."""
    if is_cloud_mode():
        try:
            client = get_bigquery_client()
            return client.query(query).to_dataframe()
        except Exception as e:
            st.error(f"BigQuery query error: {e}")
            return pd.DataFrame()
    else:
        try:
            db_path = get_duckdb_path()
            con = duckdb.connect(db_path, read_only=True)
            df = con.execute(query).df()
            con.close()
            return df
        except Exception as e:
            st.error(f"DuckDB query error: {e}")
            return pd.DataFrame()


# ──────────────────────────────────────────────────────
# Data Fetching Functions
# ──────────────────────────────────────────────────────


@st.cache_data(ttl=300, show_spinner="Loading available years...")
def get_available_years() -> list:
    """Get available years from the fact table."""
    query = """
        SELECT DISTINCT observation_year
        FROM analytics.fct_weather
        ORDER BY observation_year DESC
    """
    df = query_data(query)
    return df["observation_year"].tolist() if not df.empty else []


@st.cache_data(ttl=300, show_spinner="Loading metrics...")
def get_key_metrics(year: int, city: str) -> dict:
    """Get summary metrics for the selected year and city."""
    city_filter = "" if city == "All" else f"AND city_name = '{city}'"
    query = f"""
        SELECT
            COUNT(*) AS total_observations,
            ROUND(AVG(temperature_mean_c), 1) AS avg_temperature,
            ROUND(SUM(precipitation_mm), 1) AS total_precipitation,
            ROUND(AVG(wind_speed_max_kmh), 1) AS avg_wind_speed,
            ROUND(AVG(sunshine_hours), 1) AS avg_sunshine,
            SUM(CASE WHEN is_rainy_day THEN 1 ELSE 0 END) AS rain_days
        FROM analytics.fct_weather
        WHERE observation_year = {year}
            {city_filter}
    """
    df = query_data(query)
    if df.empty:
        return {
            "total_observations": 0,
            "avg_temperature": 0.0,
            "total_precipitation": 0.0,
            "avg_wind_speed": 0.0,
            "avg_sunshine": 0.0,
            "rain_days": 0,
        }
    return df.iloc[0].to_dict()


# ──────────────────────────────────────────────────────
# Visualization Functions
# ──────────────────────────────────────────────────────


def plot_temperature_by_city(year: int) -> go.Figure:
    """Tile 1: Average Temperature by City (Categorical Distribution).

    Shows how temperature patterns differ across Indonesian cities
    for the selected year. Includes min/max markers for range.
    """
    query = f"""
        SELECT
            city_name,
            avg_temperature_c,
            min_temperature_c,
            max_temperature_c,
            rainy_days,
            avg_sunshine_hours
        FROM analytics.weather_by_city
        WHERE observation_year = {year}
        ORDER BY avg_temperature_c DESC
    """
    df = query_data(query)

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"Temperature by City ({year})",
            annotations=[
                {
                    "text": "No data available",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                }
            ],
        )
        return fig

    fig = go.Figure()

    # Bar for average temperature
    fig.add_trace(
        go.Bar(
            x=df["city_name"],
            y=df["avg_temperature_c"],
            name="Avg Temp (°C)",
            marker_color="#ff7f0e",
            text=df["avg_temperature_c"].apply(lambda x: f"{x}°C"),
            textposition="outside",
        )
    )

    # Max temperature markers
    fig.add_trace(
        go.Scatter(
            x=df["city_name"],
            y=df["max_temperature_c"],
            mode="markers",
            name="Max Temp",
            marker=dict(color="#d62728", size=12, symbol="triangle-up"),
        )
    )

    # Min temperature markers
    fig.add_trace(
        go.Scatter(
            x=df["city_name"],
            y=df["min_temperature_c"],
            mode="markers",
            name="Min Temp",
            marker=dict(color="#1f77b4", size=12, symbol="triangle-down"),
        )
    )

    fig.update_layout(
        title=f"Temperature Comparison by City ({year})",
        xaxis_title="City",
        yaxis_title="Temperature (°C)",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )

    return fig


def plot_monthly_precipitation(year: int, city: str) -> go.Figure:
    """Tile 2: Monthly Precipitation Trends (Temporal Distribution).

    Shows how precipitation patterns change across months
    for the selected year and city.
    """
    city_filter = "" if city == "All" else f"AND city_name = '{city}'"
    query = f"""
        SELECT
            observation_month,
            city_name,
            total_precipitation_mm,
            avg_temperature_c,
            rainy_days
        FROM analytics.weather_monthly_trends
        WHERE observation_year = {year}
            {city_filter}
        ORDER BY city_name, observation_month
    """
    df = query_data(query)

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"Monthly Precipitation ({year})",
            annotations=[
                {
                    "text": "No data available",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                }
            ],
        )
        return fig

    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
    }
    df["month_name"] = df["observation_month"].map(month_names)

    fig = px.line(
        df,
        x="month_name",
        y="total_precipitation_mm",
        color="city_name",
        title=f"Monthly Precipitation Trends ({year})",
        labels={
            "month_name": "Month",
            "total_precipitation_mm": "Total Precipitation (mm)",
            "city_name": "City",
        },
        markers=True,
        category_orders={
            "month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        },
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Precipitation (mm)",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )

    return fig


# ──────────────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────────────


def main():
    """Main dashboard application."""
    # Header
    st.markdown(
        '<div class="main-header">🌤️ Indonesia Weather Analytics Dashboard</div>',
        unsafe_allow_html=True,
    )

    # ── Sidebar ──
    with st.sidebar:
        st.header("⚙️ Configuration")

        db_exists, db_status = check_database_exists()

        if db_exists:
            st.success(f"✅ {db_status}")
        else:
            st.error(f"❌ {db_status}")
            st.info("Please run the pipeline first:\n```\nmake setup\n```")
            return

        st.divider()

        # Year selector
        available_years = get_available_years()
        if not available_years:
            st.warning("No data available. Run ingestion + dbt first.")
            return

        selected_year = st.selectbox("Select Year", options=available_years, index=0)

        # City selector
        cities = ["All", "Jakarta", "Surabaya", "Denpasar", "Medan", "Makassar"]
        selected_city = st.selectbox("Select City", options=cities, index=0)

        st.divider()

        st.info(
            f"""
        **Dashboard Info**
        - Year: {selected_year}
        - City: {selected_city}
        - Mode: {"☁️ BigQuery" if is_cloud_mode() else "🏠 DuckDB"}
        """
        )

        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()

    # ── Key Metrics Row ──
    st.subheader("📊 Key Metrics")
    metrics = get_key_metrics(selected_year, selected_city)

    cols = st.columns(5)
    with cols[0]:
        st.metric("🌡️ Avg Temperature", f"{metrics['avg_temperature']}°C")
    with cols[1]:
        st.metric("🌧️ Total Precipitation", f"{metrics['total_precipitation']:,.0f} mm")
    with cols[2]:
        st.metric("💨 Avg Wind Speed", f"{metrics['avg_wind_speed']} km/h")
    with cols[3]:
        st.metric("☀️ Avg Sunshine", f"{metrics['avg_sunshine']} hrs")
    with cols[4]:
        st.metric("🌧️ Rain Days", f"{int(metrics['rain_days'])}")

    st.divider()

    # ── Two Dashboard Tiles ──
    col1, col2 = st.columns(2)

    # Tile 1: Temperature by City (Categorical Distribution)
    with col1:
        st.subheader("🌡️ Temperature by City")
        fig1 = plot_temperature_by_city(selected_year)
        st.plotly_chart(fig1, use_container_width=True)

        with st.expander("View Data"):
            query = f"""
                SELECT city_name, avg_temperature_c, min_temperature_c,
                       max_temperature_c, total_precipitation_mm, rainy_days,
                       avg_sunshine_hours
                FROM analytics.weather_by_city
                WHERE observation_year = {selected_year}
                ORDER BY avg_temperature_c DESC
            """
            st.dataframe(query_data(query), hide_index=True)

    # Tile 2: Monthly Precipitation Trends (Temporal Distribution)
    with col2:
        st.subheader("🌧️ Monthly Precipitation Trends")
        fig2 = plot_monthly_precipitation(selected_year, selected_city)
        st.plotly_chart(fig2, use_container_width=True)

        with st.expander("View Data"):
            city_filter = (
                "" if selected_city == "All" else f"AND city_name = '{selected_city}'"
            )
            query = f"""
                SELECT city_name, observation_month, total_precipitation_mm,
                       avg_temperature_c, rainy_days
                FROM analytics.weather_monthly_trends
                WHERE observation_year = {selected_year}
                    {city_filter}
                ORDER BY city_name, observation_month
            """
            st.dataframe(query_data(query), hide_index=True)

    st.divider()

    # Footer
    st.caption(
        """
    Indonesia Weather Analytics Dashboard - Data Engineering Capstone Project 2026
    Data Source: Open-Meteo Historical Weather API (free, no authentication required)
    Built with Streamlit, DuckDB/BigQuery, dbt, and Plotly
    """
    )


if __name__ == "__main__":
    main()
