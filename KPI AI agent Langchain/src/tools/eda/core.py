"""Core EDA functionality"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from typing import Dict, Any
import io
import base64

class EDAProcessor:
    """Process exploratory data analysis"""
    
    @staticmethod
    def generate_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive summary statistics"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        summary = {
            'shape': df.shape,
            'numeric_summary': {},
            'categorical_summary': {},
            'missing_data': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict()
        }
        
        # Numeric columns summary
        if len(numeric_cols) > 0:
            summary['numeric_summary'] = df[numeric_cols].describe().to_dict()
        
        # Categorical columns summary
        for col in categorical_cols:
            summary['categorical_summary'][col] = {
                'unique_count': df[col].nunique(),
                'top_values': df[col].value_counts().head(5).to_dict()
            }
        
        return summary
    
    @staticmethod
    def generate_correlation_matrix(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate correlation matrix for numeric columns"""
        numeric_df = df.select_dtypes(include=['number'])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr().to_dict()
            return corr_matrix
        return {}