"""Data formatting utilities"""
import pandas as pd
import json
from typing import Dict, Any, List

class Formatter:
    """Utility class for data formatting operations"""
    
    @staticmethod
    def format_for_llm(data: Dict[str, Any], max_length: int = 2000) -> str:
        """Format data for LLM consumption with length limits"""
        formatted = json.dumps(data, indent=2, default=str)
        if len(formatted) > max_length:
            # Truncate while preserving structure
            truncated = formatted[:max_length-100] + "... [truncated]"
            return truncated
        return formatted
    
    @staticmethod
    def dataframe_to_summary(df: pd.DataFrame, max_rows: int = 10) -> Dict[str, Any]:
        """Convert DataFrame to summary format"""
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'sample_data': df.head(max_rows).to_dict(orient='records'),
            'data_types': df.dtypes.to_dict(),
            'missing_counts': df.isnull().sum().to_dict()
        }
    
    @staticmethod
    def format_recommendations(recommendations: List[str]) -> str:
        """Format recommendations as a numbered list"""
        if not recommendations:
            return "No recommendations available."
        
        formatted = "Recommended Actions:\n"
        for i, rec in enumerate(recommendations, 1):
            formatted += f"{i}. {rec}\n"
        
        return formatted