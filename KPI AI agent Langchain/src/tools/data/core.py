"""Core data retrieval functionality"""
import pandas as pd
import os
from typing import Dict, Any
import json

class DataRetriever:
    """Retrieve data from various sources"""
    
    @staticmethod
    def load_csv_data(file_path: str) -> pd.DataFrame:
        """Load data from CSV file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return pd.read_csv(file_path)
    
    @staticmethod
    def load_json_data(json_string: str) -> pd.DataFrame:
        """Load data from JSON string"""
        data = json.loads(json_string)
        return pd.DataFrame(data)
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary of data"""
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'numeric_columns': list(df.select_dtypes(include=['number']).columns),
            'categorical_columns': list(df.select_dtypes(include=['object']).columns),
            'missing_values': df.isnull().sum().to_dict()
        }