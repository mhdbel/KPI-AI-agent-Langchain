"""Dashboard callback handlers"""
import streamlit as st
from typing import Dict, Any
import json

def handle_data_upload(uploaded_file) -> Dict[str, Any]:
    """Handle data file upload"""
    try:
        if uploaded_file.name.endswith('.csv'):
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            return {
                "success": True,
                "data": df.to_dict(orient='records'),
                "summary": {
                    "shape": df.shape,
                    "columns": list(df.columns)
                }
            }
        else:
            return {"success": False, "error": "Unsupported file format"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_agent_query(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle agent query execution"""
    try:
        if "agent_system" in st.session_state:
            result = st.session_state.agent_system.execute_analysis(query, context)
            return result
        else:
            return {"success": False, "error": "Agent system not initialized"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_export_data( Dict[str, Any], format: str = "json") -> str:
    """Handle data export"""
    try:
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "csv":
            import pandas as pd
            df = pd.DataFrame(data.get("data", []))
            return df.to_csv(index=False)
        else:
            return json.dumps(data, indent=2)
    except Exception as e:
        return f"Export failed: {str(e)}"