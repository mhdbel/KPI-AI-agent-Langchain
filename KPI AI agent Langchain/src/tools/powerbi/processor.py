"""Data processing and transformation for Power BI"""
import pandas as pd
from typing import Dict, Any, List
import json

class PowerBIDataProcessor:
    """Process and transform Power BI data"""
    
    @staticmethod
    def process_query_results(results: Dict[str, Any]) -> pd.DataFrame:
        """Convert Power BI query results to pandas DataFrame"""
        try:
            # Extract data from Power BI response structure
            data = results.get('tables', [{}])[0].get('rows', [])
            columns = results.get('tables', [{}])[0].get('columns', [])
            
            # Create column mapping
            column_names = [col['name'] for col in columns]
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=column_names)
            
            # Convert data types
            df = PowerBIDataProcessor._convert_data_types(df, columns)
            
            return df
        except Exception as e:
            raise ValueError(f"Failed to process query results: {str(e)}")
    
    @staticmethod
    def _convert_data_types(df: pd.DataFrame, columns: List[Dict]) -> pd.DataFrame:
        """Convert columns to appropriate data types"""
        type_mapping = {
            'Int64': 'int64',
            'Double': 'float64',
            'DateTime': 'datetime64[ns]',
            'Boolean': 'bool',
            'String': 'object'
        }
        
        for col_info in columns:
            col_name = col_info['name']
            col_type = col_info.get('dataType', 'String')
            
            if col_name in df.columns:
                target_type = type_mapping.get(col_type, 'object')
                try:
                    if target_type == 'datetime64[ns]':
                        df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
                    elif target_type == 'int64':
                        df[col_name] = pd.to_numeric(df[col_name], errors='coerce').astype('Int64')
                    elif target_type == 'float64':
                        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                    else:
                        df[col_name] = df[col_name].astype(target_type)
                except Exception:
                    # Keep as object if conversion fails
                    df[col_name] = df[col_name].astype('object')
        
        return df