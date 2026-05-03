"""
Indonesia Weather Analytics Dashboard
Tropical Meteorological Observatory

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
    page_icon="\U0001F30A",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────
# Design System
# ──────────────────────────────────────────────────────

CITY_COLORS = {
    "Jakarta": "#5DF8D8",
    "Surabaya": "#6FD1D7",
    "Denpasar": "#3B7597",
    "Medan": "#48B8A0",
    "Makassar": "#093C5D",
}

# Lighter version for text/labels on dark backgrounds
CITY_COLORS_LIGHT = {
    "Jakarta": "#5DF8D8",
    "Surabaya": "#6FD1D7",
    "Denpasar": "#6FA8C7",
    "Medan": "#48B8A0",
    "Makassar": "#4A7A9A",
}

MONTH_NAMES = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}

YEAR_COLORS = {
    2020: "#093C5D",
    2021: "#3B7597",
    2022: "#4ab8a1",
    2023: "#6FD1D7",
    2024: "#5DF8D8",
    2025: "#5DF8D8",
}


def hex_to_rgba(hex_color, alpha=0.1):
    """Convert hex color to rgba string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Global ── */
    .stApp {
        background: linear-gradient(170deg, #0a1628 0%, #0d1f3c 40%, #0f1a2e 100%);
        color: #e8eaf6;
    }

    /* ── Top Header Bar (force dark) ── */
    header[data-testid="stHeader"] {
        background: #0a1628 !important;
        color: #b0bec5 !important;
    }
    header[data-testid="stHeader"] button {
        color: #b0bec5 !important;
    }
    div[data-testid="stDecoration"] {
        background: none !important;
    }
    div[data-testid="stToolbar"] {
        background: transparent !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b30 0%, #111d35 100%);
        border-right: 1px solid rgba(79, 195, 247, 0.1);
    }
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #b0bec5 !important;
    }

    /* ── Sidebar Button Fix ── */
    section[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: rgba(93, 248, 216, 0.15) !important;
        color: #5DF8D8 !important;
        border: 1px solid rgba(93, 248, 216, 0.3) !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: rgba(93, 248, 216, 0.25) !important;
        border-color: #5DF8D8 !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"] p {
        color: #5DF8D8 !important;
    }

    /* ── Header ── */
    .observatory-header {
        background: linear-gradient(135deg, rgba(15, 25, 50, 0.9), rgba(20, 35, 65, 0.9));
        border: 1px solid rgba(79, 195, 247, 0.12);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .observatory-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #093C5D, #3B7597, #6FD1D7, #5DF8D8);
    }
    .observatory-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e8eaf6, #5DF8D8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.02em;
    }
    .observatory-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: #78909c;
        margin: 0;
        letter-spacing: 0.03em;
    }

    /* ── Streamlit Metric Cards ── */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(22, 32, 64, 0.8), rgba(15, 25, 50, 0.9)) !important;
        border: 1px solid rgba(79, 195, 247, 0.15) !important;
        border-radius: 12px !important;
        padding: 1.2rem 1rem !important;
    }
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] [data-testid="stMetricLabel"],
    [data-testid="stMetric"] [data-testid="stMetricLabel"] * {
        color: #b0bec5 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.82rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        justify-content: center !important;
        text-align: center !important;
        display: flex !important;
        width: 100% !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stMetric"] [data-testid="stMetricValue"] * {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        justify-content: center !important;
        text-align: center !important;
        display: flex !important;
        width: 100% !important;
    }

    /* ── Chart Containers ── */
    .chart-container {
        background: linear-gradient(145deg, rgba(22, 32, 64, 0.6), rgba(15, 25, 50, 0.7));
        border: 1px solid rgba(79, 195, 247, 0.08);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .chart-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.45rem;
        font-weight: 600;
        color: #b0bec5 !important;
        margin: 0.3rem 0 0.5rem 0;
    }
    .chart-desc {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: #607d8b;
        margin: 0 0 1rem 0;
        line-height: 1.5;
    }
    .tile-badge {
        display: inline-block;
        background: rgba(93, 248, 216, 0.12);
        color: #5DF8D8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        margin-right: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Expander (View Raw Data) ── */
    div[data-testid="stExpander"] {
        border: 1px solid rgba(93, 248, 216, 0.25) !important;
        border-radius: 10px !important;
        background: rgba(22, 32, 64, 0.5) !important;
        margin-top: 0.5rem !important;
    }
    div[data-testid="stExpander"]:hover {
        border-color: rgba(93, 248, 216, 0.5) !important;
        background: rgba(22, 32, 64, 0.7) !important;
    }
    div[data-testid="stExpander"] summary {
        padding: 0.7rem 1rem !important;
    }
    div[data-testid="stExpander"] summary p,
    .streamlit-expanderHeader p {
        color: #5DF8D8 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    div[data-testid="stExpander"] summary svg {
        color: #5DF8D8 !important;
    }

    /* ── Footer ── */
    .observatory-footer {
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(79, 195, 247, 0.06);
        color: #546e7a;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
    }
    .observatory-footer a { color: #5DF8D8; text-decoration: none; }

    /* ── General ── */
    div[data-testid="stMetricValue"] { color: #ffffff !important; }
    .stDivider { border-color: rgba(79, 195, 247, 0.08) !important; }
    h1, h2, h3 { color: #b0bec5 !important; }
    .stMarkdown p, .stMarkdown span { color: #b0bec5; }
    .stAlert p { color: inherit; }

    /* ── Main block background ── */
    .stMainBlockContainer, .block-container {
        color: #e8eaf6;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# Plotly Theme
# ──────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#90a4ae", size=12),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b0bec5", size=11),
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5,
    ),
    xaxis=dict(
        gridcolor="rgba(79, 195, 247, 0.06)",
        zerolinecolor="rgba(79, 195, 247, 0.1)",
        tickfont=dict(color="#78909c"),
    ),
    yaxis=dict(
        gridcolor="rgba(79, 195, 247, 0.06)",
        zerolinecolor="rgba(79, 195, 247, 0.1)",
        tickfont=dict(color="#78909c"),
    ),
    margin=dict(l=50, r=30, t=60, b=80),
    hoverlabel=dict(
        bgcolor="#162040",
        bordercolor="#4fc3f7",
        font=dict(color="#e8eaf6", family="DM Sans"),
    ),
)


# ──────────────────────────────────────────────────────
# Database Connection
# ──────────────────────────────────────────────────────

def get_duckdb_path():
    return os.environ.get("DUCKDB_PATH", "./data/capstone.duckdb")


def is_cloud_mode() -> bool:
    if not HAS_BIGQUERY:
        return False
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        return False
    if os.environ.get("K_SERVICE"):
        return True
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return bool(creds_path and os.path.exists(creds_path))


@st.cache_resource
def get_bigquery_client():
    if not is_cloud_mode():
        return None
    project_id = os.environ.get("GCP_PROJECT_ID")
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if os.environ.get("K_SERVICE") or not creds_path or not os.path.exists(creds_path):
        return bigquery.Client(project=project_id)
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    return bigquery.Client(credentials=credentials, project=project_id)


def check_database_exists() -> tuple:
    if is_cloud_mode():
        try:
            client = get_bigquery_client()
            list(client.list_datasets(max_results=1))
            return True, "BigQuery"
        except Exception as e:
            return False, f"BigQuery error: {e}"
    else:
        db_path = get_duckdb_path()
        if os.path.exists(db_path):
            try:
                con = duckdb.connect(db_path, read_only=True)
                con.close()
                return True, "DuckDB"
            except Exception as e:
                return False, f"DuckDB error: {e}"
        return False, "Database not found. Run `make setup` first."


@st.cache_data(ttl=600)
def query_data(query: str) -> pd.DataFrame:
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
# Data Functions
# ──────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_available_years() -> list:
    df = query_data("""
        SELECT DISTINCT observation_year
        FROM analytics.fct_weather
        ORDER BY observation_year DESC
    """)
    return df["observation_year"].tolist() if not df.empty else []


def sql_list(values):
    """Convert list to SQL IN clause string."""
    return ", ".join(str(v) if isinstance(v, (int, float)) else f"'{v}'" for v in values)


@st.cache_data(ttl=300)
def get_key_metrics(years: tuple, cities: tuple) -> dict:
    year_filter = f"observation_year IN ({sql_list(years)})"
    city_filter = f"AND city_name IN ({sql_list(cities)})" if cities else ""
    query = f"""
        SELECT
            COUNT(*) AS total_observations,
            ROUND(AVG(temperature_mean_c), 1) AS avg_temperature,
            ROUND(SUM(precipitation_mm), 1) AS total_precipitation,
            ROUND(AVG(wind_speed_max_kmh), 1) AS avg_wind_speed,
            ROUND(AVG(sunshine_hours), 1) AS avg_sunshine,
            SUM(CASE WHEN is_rainy_day THEN 1 ELSE 0 END) AS rain_days
        FROM analytics.fct_weather
        WHERE {year_filter} {city_filter}
    """
    df = query_data(query)
    if df.empty:
        return dict(total_observations=0, avg_temperature=0.0,
                    total_precipitation=0.0, avg_wind_speed=0.0,
                    avg_sunshine=0.0, rain_days=0)
    return df.iloc[0].to_dict()


# ──────────────────────────────────────────────────────
# Chart Functions
# ──────────────────────────────────────────────────────

def plot_temperature_by_city(years: tuple, cities: tuple) -> go.Figure:
    """Tile 1: Temperature comparison across cities (Categorical)."""
    year_filter = f"observation_year IN ({sql_list(years)})"
    city_filter = f"AND city_name IN ({sql_list(cities)})" if cities else ""
    query = f"""
        SELECT city_name, observation_year, avg_temperature_c,
               min_temperature_c, max_temperature_c
        FROM analytics.weather_by_city
        WHERE {year_filter} {city_filter}
        ORDER BY city_name, observation_year
    """
    df = query_data(query)

    fig = go.Figure()
    if df.empty:
        fig.update_layout(**PLOTLY_LAYOUT, height=440)
        return fig

    BAR_OUTLINE = dict(width=1.5, color="rgba(255,255,255,0.25)")

    if len(years) == 1:
        # Single year: one bar per city with city colors
        df = df.sort_values("avg_temperature_c", ascending=False)
        colors = [CITY_COLORS.get(c, "#6FD1D7") for c in df["city_name"]]
        fig.add_trace(go.Bar(
            x=df["city_name"], y=df["avg_temperature_c"],
            marker=dict(color=colors, opacity=0.9, line=BAR_OUTLINE),
            error_y=dict(
                type="data", symmetric=False,
                array=df["max_temperature_c"] - df["avg_temperature_c"],
                arrayminus=df["avg_temperature_c"] - df["min_temperature_c"],
                color="rgba(255,255,255,0.3)", thickness=2, width=6,
            ),
            text=[f"{t:.1f}°C" for t in df["avg_temperature_c"]],
            textposition="outside",
            textfont=dict(color="#e8eaf6", size=13, family="JetBrains Mono"),
            hovertemplate="<b>%{x}</b><br>Avg: %{y:.1f}°C<extra></extra>",
            showlegend=False,
        ))
        title = f"Average Temperature by City ({years[0]})"
    else:
        # Multi-year: one group per city, bars colored by city
        sorted_cities = sorted(df["city_name"].unique())
        for city_name in sorted_cities:
            city_df = df[df["city_name"] == city_name].sort_values("observation_year")
            color = CITY_COLORS.get(city_name, "#6FD1D7")
            fig.add_trace(go.Bar(
                x=[str(yr) for yr in city_df["observation_year"]],
                y=city_df["avg_temperature_c"],
                name=city_name,
                marker=dict(color=color, opacity=0.9, line=BAR_OUTLINE),
                text=[f"{t:.1f}" for t in city_df["avg_temperature_c"]],
                textposition="outside",
                textfont=dict(color="#e8eaf6", size=10, family="JetBrains Mono"),
                hovertemplate=f"<b>{city_name}</b><br>%{{x}}: %{{y:.1f}}°C<extra></extra>",
            ))
        fig.update_layout(barmode="group")
        title = f"Average Temperature by City ({min(years)}-{max(years)})"

    layout = {**PLOTLY_LAYOUT}
    layout["yaxis"] = {**PLOTLY_LAYOUT["yaxis"],
                       "range": [20, df["max_temperature_c"].max() + 4]}
    fig.update_layout(
        **layout, height=440,
        title=dict(text=title, font=dict(color="#b0bec5", size=15)),
        yaxis_title="Temperature (°C)",
    )
    return fig


def plot_monthly_precipitation(years: tuple, cities: tuple) -> go.Figure:
    """Tile 2: Monthly precipitation trends (Temporal)."""
    year_filter = f"observation_year IN ({sql_list(years)})"
    city_filter = f"AND city_name IN ({sql_list(cities)})" if cities else ""
    query = f"""
        SELECT observation_month, observation_year, city_name,
               total_precipitation_mm, rainy_days
        FROM analytics.weather_monthly_trends
        WHERE {year_filter} {city_filter}
        ORDER BY city_name, observation_year, observation_month
    """
    df = query_data(query)

    fig = go.Figure()
    if df.empty:
        fig.update_layout(**PLOTLY_LAYOUT, height=440)
        return fig

    df["month_name"] = df["observation_month"].map(MONTH_NAMES)
    month_order = list(MONTH_NAMES.values())
    BAR_OUTLINE = dict(width=1.5, color="rgba(255,255,255,0.25)")

    multi_year = len(years) > 1
    multi_city = len(cities) > 1

    if multi_year and multi_city:
        # BOTH multi → grouped bar (avg across years), one bar per city
        agg = df.groupby(["city_name", "observation_month", "month_name"], as_index=False).agg(
            avg_precip=("total_precipitation_mm", "mean")
        ).sort_values(["city_name", "observation_month"])

        for city_name in sorted(agg["city_name"].unique()):
            city_df = agg[agg["city_name"] == city_name]
            color = CITY_COLORS.get(city_name, "#6FD1D7")
            fig.add_trace(go.Bar(
                x=city_df["month_name"], y=city_df["avg_precip"],
                name=city_name,
                marker=dict(color=color, opacity=0.85, line=BAR_OUTLINE),
                hovertemplate=f"<b>{city_name}</b><br>%{{x}}: %{{y:.0f}} mm (avg)<extra></extra>",
            ))
        fig.update_layout(barmode="group")
        title = f"Avg Monthly Precipitation by City ({min(years)}-{max(years)})"

    elif multi_year and not multi_city:
        # Multi year, single city: one line per year with city color shades
        city_color = CITY_COLORS.get(cities[0], "#6FD1D7")
        opacities = [0.3, 0.4, 0.5, 0.65, 0.8, 1.0]
        sorted_years = sorted(years)
        for i, yr in enumerate(sorted_years):
            yr_df = df[df["observation_year"] == yr].sort_values("observation_month")
            op = opacities[min(i, len(opacities) - 1)]
            w = 3 if yr == max(years) else 1.5
            fig.add_trace(go.Scatter(
                x=yr_df["month_name"], y=yr_df["total_precipitation_mm"],
                name=str(yr), mode="lines+markers",
                line=dict(color=city_color, width=w, shape="spline"),
                marker=dict(size=6 if yr == max(years) else 3, color=city_color),
                opacity=op,
                hovertemplate=f"<b>{yr}</b><br>%{{x}}: %{{y:.0f}} mm<extra></extra>",
            ))
        title = f"Monthly Precipitation — {cities[0]} ({min(years)}-{max(years)})"

    else:
        # Single year (or single city): line per city with city colors
        for city_name in sorted(df["city_name"].unique()):
            city_df = df[df["city_name"] == city_name].sort_values("observation_month")
            color = CITY_COLORS.get(city_name, "#6FD1D7")
            fig.add_trace(go.Scatter(
                x=city_df["month_name"], y=city_df["total_precipitation_mm"],
                name=city_name, mode="lines+markers",
                line=dict(color=color, width=2.5, shape="spline"),
                marker=dict(size=6, color=color,
                            line=dict(width=1, color="rgba(255,255,255,0.3)")),
                hovertemplate=f"<b>{city_name}</b><br>%{{x}}: %{{y:.0f}} mm<extra></extra>",
            ))
        title = f"Monthly Precipitation by City ({years[0]})"

    layout = {**PLOTLY_LAYOUT}
    layout["xaxis"] = {**PLOTLY_LAYOUT["xaxis"],
                       "categoryorder": "array", "categoryarray": month_order}
    fig.update_layout(
        **layout, height=440,
        title=dict(text=title, font=dict(color="#b0bec5", size=15)),
        yaxis_title="Precipitation (mm)",
    )
    return fig


def plot_weather_distribution(years: tuple, cities: tuple) -> go.Figure:
    """Bonus: Weather condition distribution."""
    year_filter = f"observation_year IN ({sql_list(years)})"
    city_filter = f"AND city_name IN ({sql_list(cities)})" if cities else ""
    query = f"""
        SELECT city_name, weather_category, COUNT(*) as days
        FROM analytics.fct_weather
        WHERE {year_filter} {city_filter}
        GROUP BY city_name, weather_category
        ORDER BY city_name, days DESC
    """
    df = query_data(query)

    fig = go.Figure()
    if df.empty:
        fig.update_layout(**PLOTLY_LAYOUT, height=350)
        return fig

    cat_colors = {
        "Clear": "#5DF8D8", "Cloudy": "#90a4ae", "Rain": "#3B7597",
        "Rain Showers": "#6FD1D7", "Drizzle": "#4ab8a1",
        "Thunderstorm": "#093C5D", "Fog": "#b0bec5", "Unknown": "#546e7a",
    }

    for cat in df["weather_category"].unique():
        cat_df = df[df["weather_category"] == cat]
        fig.add_trace(go.Bar(
            x=cat_df["city_name"], y=cat_df["days"],
            name=cat,
            marker=dict(
                color=cat_colors.get(cat, "#546e7a"),
                line=dict(width=1, color="rgba(255,255,255,0.2)"),
            ),
            opacity=0.85,
            hovertemplate=f"<b>{cat}</b><br>%{{x}}: %{{y}} days<extra></extra>",
        ))

    yr_label = f"{min(years)}-{max(years)}" if len(years) > 1 else str(years[0])
    layout_no_legend = {k: v for k, v in PLOTLY_LAYOUT.items() if k != "legend"}
    fig.update_layout(
        **layout_no_legend, height=350, barmode="stack",
        title=dict(text=f"Weather Condition Distribution ({yr_label})",
                   font=dict(color="#b0bec5", size=15)),
        yaxis_title="Days",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#b0bec5", size=10),
            orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5,
        ),
    )
    return fig


# ──────────────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────────────

def main():
    # ── Sidebar ──
    with st.sidebar:
        st.markdown("### Observatory Controls")
        st.markdown("---")

        db_exists, db_status = check_database_exists()
        if db_exists:
            mode_icon = "Cloud" if db_status == "BigQuery" else "Local"
            st.success(f"Connected: {db_status} ({mode_icon})")
        else:
            st.error(f"{db_status}")
            st.info("Run the pipeline first:\n```\nmake setup\n```")
            return

        available_years = get_available_years()
        if not available_years:
            st.warning("No data available.")
            return

        selected_years = st.multiselect(
            "Select Year(s)",
            options=available_years,
            default=[available_years[0]],
        )
        if not selected_years:
            st.warning("Please select at least one year.")
            return

        all_cities = ["Jakarta", "Surabaya", "Denpasar", "Medan", "Makassar"]
        selected_cities = st.multiselect(
            "Select City(s)",
            options=all_cities,
            default=all_cities,
        )
        if not selected_cities:
            st.warning("Please select at least one city.")
            return

        st.markdown("---")
        st.markdown(
            f"""**Filters active:**  \n"""
            f"""Years: {', '.join(str(y) for y in sorted(selected_years))}  \n"""
            f"""Cities: {', '.join(selected_cities)}"""
        )

        st.markdown("---")
        if st.button("Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Convert to tuples for caching
    years_tuple = tuple(sorted(selected_years))
    cities_tuple = tuple(selected_cities)

    # ── Header ──
    st.markdown(
        """
        <div class="observatory-header">
            <p class="observatory-title">Indonesia Weather Observatory</p>
            <p class="observatory-subtitle">
                Historical weather analysis across 5 major Indonesian cities
                &bull; Daily data from 2020&ndash;2025 &bull; Powered by Open-Meteo API
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Key Metrics ──
    metrics = get_key_metrics(years_tuple, cities_tuple)

    m1, m2, m3, m4, m5 = st.columns(5, gap="small")
    with m1:
        st.metric(label="AVG TEMPERATURE", value=f"{metrics['avg_temperature']}°C")
    with m2:
        st.metric(label="TOTAL RAINFALL", value=f"{metrics['total_precipitation']:,.0f} mm")
    with m3:
        st.metric(label="AVG WIND SPEED", value=f"{metrics['avg_wind_speed']} km/h")
    with m4:
        st.metric(label="AVG SUNSHINE", value=f"{metrics['avg_sunshine']} hrs")
    with m5:
        st.metric(label="RAIN DAYS", value=f"{int(metrics['rain_days'])}")

    st.markdown("")

    # ── Two Main Tiles ──
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown(
            """
            <div class="chart-container">
                <span class="tile-badge">Tile 1 &bull; Categorical</span>
                <h3 class="chart-title">Temperature by City</h3>
                <p class="chart-desc">
                    Average temperature comparison across Indonesian cities.
                    Error bars show min&ndash;max daily range.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig1 = plot_temperature_by_city(years_tuple, cities_tuple)
        st.plotly_chart(fig1, use_container_width=True, key="tile1")

        with st.expander("View Raw Data"):
            year_f = f"observation_year IN ({sql_list(years_tuple)})"
            city_f = f"AND city_name IN ({sql_list(cities_tuple)})"
            q = f"""
                SELECT city_name AS City, observation_year AS Year,
                       avg_temperature_c AS "Avg (C)", min_temperature_c AS "Min (C)",
                       max_temperature_c AS "Max (C)", total_precipitation_mm AS "Rain (mm)"
                FROM analytics.weather_by_city
                WHERE {year_f} {city_f}
                ORDER BY observation_year DESC, avg_temperature_c DESC
            """
            st.dataframe(query_data(q), hide_index=True, use_container_width=True)

    with col2:
        st.markdown(
            """
            <div class="chart-container">
                <span class="tile-badge">Tile 2 &bull; Temporal</span>
                <h3 class="chart-title">Monthly Precipitation Trends</h3>
                <p class="chart-desc">
                    Precipitation patterns across months.
                    Reveals wet/dry season shifts per city.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig2 = plot_monthly_precipitation(years_tuple, cities_tuple)
        st.plotly_chart(fig2, use_container_width=True, key="tile2")

        with st.expander("View Raw Data"):
            q = f"""
                SELECT city_name AS City, observation_year AS Year,
                       observation_month AS Month,
                       total_precipitation_mm AS "Rain (mm)", rainy_days AS "Rain Days"
                FROM analytics.weather_monthly_trends
                WHERE {year_f} {city_f}
                ORDER BY city_name, observation_year, observation_month
            """
            st.dataframe(query_data(q), hide_index=True, use_container_width=True)

    # ── Bonus: Weather Distribution ──
    st.markdown(
        """
        <div class="chart-container" style="margin-top:0.5rem">
            <span class="tile-badge">Bonus &bull; Distribution</span>
            <h3 class="chart-title">Weather Condition Distribution</h3>
            <p class="chart-desc">
                Breakdown of weather conditions (Clear, Cloudy, Rain, Thunderstorm)
                across cities. Stacked bars show total days per condition.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    fig3 = plot_weather_distribution(years_tuple, cities_tuple)
    st.plotly_chart(fig3, use_container_width=True, key="weather_dist")

    # ── Footer ──
    st.markdown(
        """
        <div class="observatory-footer">
            <strong>Indonesia Weather Observatory</strong>
            &mdash; Data Engineering Capstone Project 2026<br>
            Data: <a href="https://open-meteo.com" target="_blank">Open-Meteo API</a>
            &bull; Stack: dlt &rarr; DuckDB/BigQuery &rarr; dbt &rarr; Streamlit
            &bull; Orchestration: Kestra &bull; IaC: Terraform
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
