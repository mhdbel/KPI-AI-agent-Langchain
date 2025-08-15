"""AHP configuration management"""
import json
from typing import Dict, Any
from pathlib import Path

class AHPConfigError(Exception):
    """Raised for invalid AHP configuration errors."""
    pass

class AHPConfigManager:
    """Manages AHP configuration loading and validation"""
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load AHP configuration from file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise AHPConfigError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise AHPConfigError(f"Invalid JSON format: {str(e)}")
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> None:
        """Validate the AHP configuration structure"""
        required_keys = ["criteria", "alternatives"]
        for key in required_keys:
            if key not in config:
                raise AHPConfigError(f"Missing required key: {key}")

        # Validate criteria structure
        criteria = config["criteria"]
        if not isinstance(criteria, dict) or "comparisons" not in criteria:
            raise AHPConfigError("Invalid criteria configuration")
        
        # Validate alternatives structure
        for alt in config["alternatives"]:
            if not all(k in alt for k in ("name", "comparisons")):
                raise AHPConfigError("Invalid alternative configuration")