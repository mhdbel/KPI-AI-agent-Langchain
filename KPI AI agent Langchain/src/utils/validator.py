"""Data and configuration validation utilities"""
from typing import Dict, Any, List
import json

class Validator:
    """Utility class for validation operations"""
    
    @staticmethod
    def validate_json_structure(data: Dict[str, Any], required_keys: List[str]) -> bool:
        """Validate that JSON data contains required keys"""
        return all(key in data for key in required_keys)
    
    @staticmethod
    def validate_data_schema(df, expected_columns: List[str]) -> Dict[str, Any]:
        """Validate data schema against expected columns"""
        missing_columns = [col for col in expected_columns if col not in df.columns]
        extra_columns = [col for col in df.columns if col not in expected_columns]
        
        return {
            'valid': len(missing_columns) == 0,
            'missing_columns': missing_columns,
            'extra_columns': extra_columns,
            'column_count': len(df.columns)
        }
    
    @staticmethod
    def validate_numeric_range(value: float, min_val: float, max_val: float) -> bool:
        """Validate that numeric value is within range"""
        return min_val <= value <= max_val