"""Data processing utilities"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import json

class DataProcessor:
    """Utility class for data processing operations"""
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess data"""
        # Remove duplicate rows
        df = df.drop_duplicates()
        
        # Handle missing values
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
        
        return df
    
    @staticmethod
    def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize numeric data"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df_normalized = df.copy()
        
        for col in numeric_cols:
            col_min = df_normalized[col].min()
            col_max = df_normalized[col].max()
            if col_max != col_min:  # Avoid division by zero
                df_normalized[col] = (df_normalized[col] - col_min) / (col_max - col_min)
        
        return df_normalized
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, columns: List[str] = None) -> Dict[str, Any]:
        """Detect outliers using IQR method"""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers = {}
        for col in columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                outliers[col] = {
                    'count': outlier_mask.sum(),
                    'percentage': (outlier_mask.sum() / len(df)) * 100,
                    'bounds': {'lower': float(lower_bound), 'upper': float(upper_bound)}
                }
        
        return outliers