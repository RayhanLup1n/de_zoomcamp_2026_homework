"""
NYC Taxi Analytics Dashboard

Streamlit dashboard for visualizing NYC taxi trip data.
"""

import os
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.cloud import bigquery
from google.oauth2 import service_account

# Page configuration
st.set_page_config(
    page_title="NYC Taxi Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# Database Connection Logic
# ──────────────────────────────────────────────────────

def get_gcp_config():
    """Get GCP configuration from environment."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    credentials_path = os.environ.get("LOCAL_GCP_CREDENTIALS") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return project_id, credentials_path


def get_duckdb_path():
    """Get DuckDB database path from environment."""
    return os.environ.get("DUCKDB_PATH", "./data/capstone.duckdb")


def is_cloud_mode() -> bool:
    """Check if we should use BigQuery (Cloud Mode)."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        return False
    
    # On Cloud Run, ADC is available automatically via the service identity
    if os.environ.get("K_SERVICE"):
        return True
    
    # Local development: check for explicit credentials file
    _, creds_path = get_gcp_config()
    return bool(creds_path and os.path.exists(creds_path))


@st.cache_resource
def get_bigquery_client():
    """Initialize and cache BigQuery client."""
    if not is_cloud_mode():
        return None
    
    project_id, creds_path = get_gcp_config()
    
    # On Cloud Run: use Application Default Credentials (no file needed)
    if os.environ.get("K_SERVICE") or not creds_path or not os.path.exists(creds_path):
        return bigquery.Client(project=project_id)
    
    # Local development: use explicit credentials file
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    return bigquery.Client(credentials=credentials, project=project_id)


def check_database_exists() -> tuple[bool, str]:
    """Check if any database (BQ or DuckDB) is accessible."""
    if is_cloud_mode():
        try:
            client = get_bigquery_client()
            # Just try to list datasets to verify connection
            list(client.list_datasets(max_results=1))
            return True, "Connected to BigQuery"
        except Exception as e:
            return False, f"Cloud Mode error: {e}"
    else:
        db_path = get_duckdb_path()
        if os.path.exists(db_path):
            try:
                con = duckdb.connect(db_path, read_only=True)
                con.close()
                return True, "Connected to local DuckDB"
            except Exception as e:
                return False, f"DuckDB connection error: {e}"
        return False, "No database found (Cloud or Local)"


@st.cache_data(ttl=600)  # Cache results for 10 minutes
def query_data(query: str, params: list = None) -> pd.DataFrame:
    """Execute query on either BigQuery or DuckDB based on mode."""
    if is_cloud_mode():
        try:
            client = get_bigquery_client()
            # BigQuery uses named parameters (@param) or format strings
            # For simplicity, we'll replace ? with @p1, @p2 etc. if needed
            # or just use the query as is if it's already formatted.
            
            # Convert ? placeholders to @p1, @p2 etc for BigQuery
            bq_query = query
            job_config = None
            if params:
                for i in range(len(params)):
                    bq_query = bq_query.replace("?", f"@p{i+1}", 1)
                
                query_params = [
                    bigquery.ScalarQueryParameter(f"p{i+1}", 
                        "INT64" if isinstance(params[i], int) else "STRING", 
                        params[i])
                    for i in range(len(params))
                ]
                job_config = bigquery.QueryJobConfig(query_parameters=query_params)
            
            df = client.query(bq_query, job_config=job_config).to_dataframe()
            return df
        except Exception as e:
            st.error(f"Error querying BigQuery: {e}")
            return pd.DataFrame()
    else:
        try:
            db_path = get_duckdb_path()
            con = duckdb.connect(db_path)
            df = con.execute(query, params or []).df()
            con.close()
            return df
        except Exception as e:
            st.error(f"Error querying DuckDB: {e}")
            return pd.DataFrame()


@st.cache_data(ttl=300, show_spinner=False)
def get_schemas() -> list:
    """Get all tables available in the current mode with caching."""
    if is_cloud_mode():
        try:
            client = get_bigquery_client()
            datasets = ["raw", "analytics"]
            all_tables = []
            for ds in datasets:
                tables = client.list_tables(ds)
                all_tables.extend([f"{ds}.{t.table_id}" for t in tables])
            return all_tables
        except Exception:
            return []
    else:
        try:
            db_path = get_duckdb_path()
            con = duckdb.connect(db_path)
            tables = con.execute("SHOW ALL TABLES").df()
            con.close()
            return [f"{row['schema']}.{row['name']}" for _, row in tables.iterrows()]
        except Exception:
            return []


# ──────────────────────────────────────────────────────
# Data Fetching Logic (with caching)
# ──────────────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner="Loading available years...")
def get_available_years() -> list:
    """Get available years in database (filtered to valid range)."""
    query = """
        SELECT DISTINCT trip_year
        FROM analytics.fct_trips
        WHERE trip_year BETWEEN 2019 AND 2025
        ORDER BY trip_year DESC
    """
    df = query_data(query)
    return df['trip_year'].tolist() if not df.empty else []


@st.cache_data(ttl=300, show_spinner="Loading metrics...")
def get_total_metrics(year: int, taxi_type: str) -> dict:
    """Get summary metrics for selected filters with caching."""
    params = [year, taxi_type]

    query = """
        SELECT
            COUNT(*) AS total_trips,
            COALESCE(SUM(fare_amount + tip_amount + tolls_amount), 0) AS total_revenue,
            COALESCE(AVG(trip_distance), 0) AS avg_distance,
            COALESCE(AVG(fare_amount), 0) AS avg_fare,
            COALESCE(AVG(tip_amount), 0) AS avg_tip
        FROM analytics.fct_trips
        WHERE trip_year = ?
            AND taxi_type = ?
    """
    df = query_data(query, params)

    if df.empty:
        return {
            'total_trips': 0,
            'total_revenue': 0.0,
            'avg_distance': 0.0,
            'avg_fare': 0.0,
            'avg_tip': 0.0
        }

    return df.iloc[0].to_dict()


def plot_payment_distribution(df: pd.DataFrame, year: int, taxi_type: str) -> go.Figure:
    """Create payment type distribution chart (Tile 1)."""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"Payment Type Distribution - {taxi_type} {year}",
            annotations=[{
                'text': 'No data available',
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.5,
                'y': 0.5,
                'showarrow': False
            }]
        )
        return fig

    fig = px.bar(
        df,
        x='payment_type_name',
        y='trip_count',
        text='percentage',
        title=f"Payment Type Distribution - {taxi_type} {year}",
        labels={
            'payment_type_name': 'Payment Type',
            'trip_count': 'Trip Count',
            'percentage': 'Percentage'
        },
        color='payment_type_name'
    )

    fig.update_traces(
        texttemplate='%{y:,.0f}<br>%{text:.1f}%',
        textposition='outside'
    )

    fig.update_layout(
        xaxis_title='Payment Type',
        yaxis_title='Trip Count',
        showlegend=False,
        height=400
    )

    return fig


def plot_hourly_patterns(df: pd.DataFrame, year: int, taxi_type: str) -> go.Figure:
    """Create hourly trip pattern chart (Tile 2)."""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"Hourly Trip Patterns - {taxi_type} {year}",
            annotations=[{
                'text': 'No data available',
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.5,
                'y': 0.5,
                'showarrow': False
            }]
        )
        return fig

    # Aggregate by hour across all days
    hourly_data = df.groupby('trip_hour').agg({
        'trip_count': 'sum',
        'avg_fare_amount': 'mean',
        'avg_trip_distance': 'mean'
    }).reset_index()

    fig = go.Figure()

    # Add line for trip count
    fig.add_trace(go.Scatter(
        x=hourly_data['trip_hour'],
        y=hourly_data['trip_count'],
        mode='lines+markers',
        name='Trip Count',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    # Add secondary y-axis for average fare
    fig.add_trace(go.Scatter(
        x=hourly_data['trip_hour'],
        y=hourly_data['avg_fare_amount'],
        mode='lines+markers',
        name='Avg Fare ($)',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(size=8),
        yaxis='y2'
    ))

    fig.update_layout(
        title=f"Hourly Trip Patterns - {taxi_type} {year}",
        xaxis_title='Hour of Day',
        yaxis_title='Trip Count',
        yaxis2=dict(
            title='Average Fare ($)',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02
        ),
        height=400
    )

    return fig


def main():
    """Main dashboard application."""
    # Header
    st.markdown('<div class="main-header">🚕 NYC Taxi Analytics Dashboard</div>',
                unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Check database
        db_exists, db_status = check_database_exists()

        if db_exists:
            st.success(f"✅ Database: Connected")

            # Get all tables/schemas
            all_tables = get_schemas()

            if all_tables:
                st.info(f"📊 Tables found: {len(all_tables)}")
                with st.expander("View all tables"):
                    for table in all_tables:
                        st.text(f"- {table}")
            else:
                st.warning("⚠️ No tables found in database")
        else:
            st.error(f"❌ Database {db_status}")
            st.info("Please run the ingestion pipeline first")
            return

        st.divider()

        # Get available years
        try:
            available_years = get_available_years()
        except Exception:
            available_years = []

        if not available_years:
            st.warning("⚠️ No data available. Please run ingestion pipeline.")
            st.info("The ingestion container should load data into DuckDB.")
            return

        # Year selector
        selected_year = st.selectbox(
            "Select Year",
            options=available_years,
            index=0
        )

        # Taxi type selector
        taxi_types = ['Green', 'Yellow', 'Both']
        selected_taxi_type = st.selectbox(
            "Taxi Type",
            options=taxi_types,
            index=0
        )

        st.divider()

        # Info
        st.info(f"""
        **Dashboard Info**
        - Year: {selected_year}
        - Taxi Type: {selected_taxi_type}
        - Mode: {"☁️ Cloud (BigQuery)" if is_cloud_mode() else "🏠 Local (DuckDB)"}
        """)

        st.divider()

        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.rerun()

    # Metrics row
    st.subheader("📊 Key Metrics")
    metrics_cols = st.columns(5)

    if selected_taxi_type == 'Both':
        # Get metrics for both taxi types
        green_metrics = get_total_metrics(selected_year, 'Green')
        yellow_metrics = get_total_metrics(selected_year, 'Yellow')

        total_trips = green_metrics['total_trips'] + yellow_metrics['total_trips']
        total_revenue = green_metrics['total_revenue'] + yellow_metrics['total_revenue']

        # For averages, only include non-zero values to avoid skewing
        g_trips = green_metrics['total_trips']
        y_trips = yellow_metrics['total_trips']
        denom = max(g_trips + y_trips, 1)
        avg_distance = (green_metrics['avg_distance'] * g_trips + yellow_metrics['avg_distance'] * y_trips) / denom
        avg_fare = (green_metrics['avg_fare'] * g_trips + yellow_metrics['avg_fare'] * y_trips) / denom
        avg_tip = (green_metrics['avg_tip'] * g_trips + yellow_metrics['avg_tip'] * y_trips) / denom
    else:
        metrics = get_total_metrics(selected_year, selected_taxi_type)
        total_trips = metrics['total_trips']
        total_revenue = metrics['total_revenue']
        avg_distance = metrics['avg_distance']
        avg_fare = metrics['avg_fare']
        avg_tip = metrics['avg_tip']

    with metrics_cols[0]:
        st.metric("Total Trips", f"{total_trips:,}")
    with metrics_cols[1]:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    with metrics_cols[2]:
        st.metric("Avg Distance", f"{avg_distance:.2f} mi")
    with metrics_cols[3]:
        st.metric("Avg Fare", f"${avg_fare:.2f}")
    with metrics_cols[4]:
        st.metric("Avg Tip", f"${avg_tip:.2f}")

    st.divider()

    # Main content - Two tiles
    col1, col2 = st.columns(2)

    # Tile 1: Categorical Distribution (Payment Types)
    with col1:
        st.subheader("💳 Payment Type Distribution")

        if selected_taxi_type == 'Both':
            query = """
                SELECT
                    payment_type_name,
                    SUM(trip_count) AS trip_count,
                    SUM(trip_count) * 100.0 / SUM(SUM(trip_count)) OVER () AS percentage
                FROM analytics.trips_payment_type
                WHERE trip_year = ?
                GROUP BY payment_type_name
                ORDER BY trip_count DESC
            """
            params = [selected_year]
        else:
            query = """
                SELECT
                    payment_type_name,
                    trip_count,
                    percentage
                FROM analytics.trips_payment_type
                WHERE trip_year = ?
                    AND taxi_type = ?
                ORDER BY trip_count DESC
            """
            params = [selected_year, selected_taxi_type]

        payment_df = query_data(query, params)

        if not payment_df.empty:
            fig_payment = plot_payment_distribution(
                payment_df,
                selected_year,
                selected_taxi_type
            )
            st.plotly_chart(fig_payment, use_container_width=True)

            # Table view
            with st.expander("View Data"):
                st.dataframe(
                    payment_df,
                    column_config={
                        'trip_count': st.column_config.NumberColumn(
                            format='%,d'
                        ),
                        'percentage': st.column_config.NumberColumn(
                            format='%.2f%%'
                        )
                    },
                    hide_index=True
                )
        else:
            st.warning("No payment type data available.")

    # Tile 2: Temporal Distribution (Hourly Patterns)
    with col2:
        st.subheader("⏰ Hourly Trip Patterns")

        if selected_taxi_type == 'Both':
            query = """
                SELECT
                    trip_hour,
                    SUM(trip_count) AS trip_count,
                    AVG(
                        CASE WHEN avg_fare_amount > 0 THEN avg_fare_amount END
                    ) AS avg_fare_amount,
                    AVG(
                        CASE WHEN avg_trip_distance > 0 THEN avg_trip_distance END
                    ) AS avg_trip_distance
                FROM analytics.trips_by_hour
                WHERE trip_year = ?
                GROUP BY trip_hour
                ORDER BY trip_hour
            """
            hourly_params = [selected_year]
        else:
            query = """
                SELECT
                    trip_hour,
                    trip_count,
                    avg_fare_amount,
                    avg_trip_distance
                FROM analytics.trips_by_hour
                WHERE trip_year = ?
                    AND taxi_type = ?
                ORDER BY trip_hour
            """
            hourly_params = [selected_year, selected_taxi_type]

        hourly_df = query_data(query, hourly_params)

        if not hourly_df.empty:
            fig_hourly = plot_hourly_patterns(
                hourly_df,
                selected_year,
                selected_taxi_type
            )
            st.plotly_chart(fig_hourly, use_container_width=True)

            # Table view
            with st.expander("View Data"):
                st.dataframe(
                    hourly_df,
                    column_config={
                        'trip_count': st.column_config.NumberColumn(format='%,d'),
                        'avg_fare_amount': st.column_config.NumberColumn('$%.2f'),
                        'avg_trip_distance': st.column_config.NumberColumn('%.2f mi')
                    },
                    hide_index=True
                )
        else:
            st.warning("No hourly pattern data available.")

    st.divider()

    # Footer
    st.caption("""
    NYC Taxi Analytics Dashboard - Capstone Project 2026
    Data Source: NYC Taxi & Limousine Commission
    Built with Streamlit, DuckDB, and Plotly
    """)


if __name__ == "__main__":
    main()
