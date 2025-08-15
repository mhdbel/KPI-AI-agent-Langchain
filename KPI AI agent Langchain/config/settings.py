"""Configuration settings"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class PowerBIConfig:
    """Power BI API configuration"""
    tenant_id: str
    client_id: str
    client_secret: str
    workspace_id: str
    dataset_id: str
    authority_url: str = "https://login.microsoftonline.com"
    resource_url: str = "https://analysis.windows.net/powerbi/api"
    api_url: str = "https://api.powerbi.com/v1.0/myorg"

def get_powerbi_config() -> Optional[PowerBIConfig]:
    """Get Power BI configuration from environment"""
    required_vars = [
        "POWERBI_TENANT_ID",
        "POWERBI_CLIENT_ID", 
        "POWERBI_CLIENT_SECRET",
        "POWERBI_WORKSPACE_ID",
        "POWERBI_DATASET_ID"
    ]
    
    # Check if all required variables are present
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        return None
    
    return PowerBIConfig(
        tenant_id=os.getenv("POWERBI_TENANT_ID"),
        client_id=os.getenv("POWERBI_CLIENT_ID"),
        client_secret=os.getenv("POWERBI_CLIENT_SECRET"),
        workspace_id=os.getenv("POWERBI_WORKSPACE_ID"),
        dataset_id=os.getenv("POWERBI_DATASET_ID")
    )

def get_openai_config() -> Dict[str, Any]:
    """Get OpenAI configuration"""
    return {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "organization": os.getenv("OPENAI_ORG_ID")
    }

def get_app_config() -> Dict[str, Any]:
    """Get application configuration"""
    return {
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "memory_persist_dir": os.getenv("MEMORY_PERSIST_DIR", "./kpi_memory")
    }