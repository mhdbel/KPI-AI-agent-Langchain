"""Reusable dashboard components"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

def render_data_table(df: pd.DataFrame, title: str = "Data Table"):
    """Render interactive data table"""
    st.subheader(title)
    st.dataframe(df, use_container_width=True)

def render_metric_card(title: str, value: Any, delta: Any = None, 
                      help_text: str = None):
    """Render metric card"""
    if delta:
        st.metric(title, value, delta, help=help_text)
    else:
        st.metric(title, value, help=help_text)

def render_chart(df: pd.DataFrame, chart_type: str, x_col: str, y_col: str,
                title: str = ""):
    """Render interactive chart"""
    if chart_type == "line":
        fig = px.line(df, x=x_col, y=y_col, title=title)
    elif chart_type == "bar":
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    elif chart_type == "scatter":
        fig = px.scatter(df, x=x_col, y=y_col, title=title)
    else:
        fig = px.line(df, x=x_col, y=y_col, title=title)
    
    st.plotly_chart(fig, use_container_width=True)

def render_kpi_summary(kpi_data: Dict[str, Any]):
    """Render KPI summary dashboard"""
    cols = st.columns(4)
    with cols[0]:
        render_metric_card("Total Records", kpi_data.get("total_records", 0))
    with cols[1]:
        render_metric_card("Avg Value", kpi_data.get("avg_value", 0))
    with cols[2]:
        render_metric_card("Trend", kpi_data.get("trend", "Stable"))
    with cols[3]:
        render_metric_card("Health Score", kpi_data.get("health_score", 0))