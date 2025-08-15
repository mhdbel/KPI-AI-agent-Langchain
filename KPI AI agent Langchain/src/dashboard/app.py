"""Main Streamlit dashboard application"""
import streamlit as st
import pandas as pd
from typing import Dict, Any
import json
from datetime import datetime

from ..core.factory import KPIAgentFactory
from ..config.settings import get_powerbi_config

def initialize_app():
    """Initialize the Streamlit application"""
    st.set_page_config(
        page_title="KPI AI Agent Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "agent_system" not in st.session_state:
        config = {
            "llm": {
                "model": "gpt-4",
                "temperature": st.sidebar.slider("Temperature", 0.0, 1.0, 0.0)
            },
            "agent": {
                "verbose": True
            }
        }
        st.session_state.agent_system = KPIAgentFactory.create_agent_system(config)

def main():
    """Main application function"""
    initialize_app()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Data Overview", 
        "📈 KPI Analysis", 
        "🎯 Decision Support", 
        "🤖 AI Assistant"
    ])
    
    with tab1:
        render_data_overview()
    
    with tab2:
        render_kpi_analysis()
    
    with tab3:
        render_decision_support()
    
    with tab4:
        render_ai_assistant()

def render_data_overview():
    """Render data overview tab"""
    st.header("📊 Data Overview")
    st.info("Data loading functionality will be integrated here")

def render_kpi_analysis():
    """Render KPI analysis tab"""
    st.header("📈 KPI Analysis")
    st.info("KPI analysis functionality will be integrated here")

def render_decision_support():
    """Render decision support tab"""
    st.header("🎯 Decision Support")
    st.info("AHP decision support functionality will be integrated here")

def render_ai_assistant():
    """Render AI assistant tab"""
    st.header("🤖 AI Assistant")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your KPI data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if st.session_state.agent_system:
                    response = st.session_state.agent_system.execute_analysis(prompt)
                    if response["success"]:
                        st.markdown(response["result"])
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response["result"]
                        })
                    else:
                        st.error(f"Error: {response['error']}")
                else:
                    st.error("Agent system not initialized")

if __name__ == "__main__":
    main()