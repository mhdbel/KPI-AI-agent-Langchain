"""Core Power BI API functionality"""
import requests
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

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

class PowerBIAPIError(Exception):
    """Custom exception for Power BI API errors"""
    pass

class PowerBIClient:
    """Core Power BI API client"""
    
    def __init__(self, config: PowerBIConfig):
        self.config = config
        self.access_token = None
        self.token_expires_at = None
    
    def _get_access_token(self) -> str:
        """Get OAuth2 access token"""
        if self.access_token and self.token_expires_at and datetime.now().timestamp() < self.token_expires_at:
            return self.access_token
        
        url = f"{self.config.authority_url}/{self.config.tenant_id}/oauth2/token"
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'resource': self.config.resource_url
        }
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data['access_token']
            # Set expiration (subtract 5 minutes for safety)
            expires_in = token_data.get('expires_in', 3600) - 300
            self.token_expires_at = datetime.now().timestamp() + expires_in
            
            return self.access_token
        except requests.exceptions.RequestException as e:
            raise PowerBIAPIError(f"Failed to get access token: {str(e)}")
    
    def _make_api_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated API request"""
        token = self._get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.config.api_url}/{endpoint}"
        
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise PowerBIAPIError(f"API request failed: {str(e)}")
    
    def get_datasets(self) -> List[Dict[str, Any]]:
        """Get all datasets in workspace"""
        endpoint = f"groups/{self.config.workspace_id}/datasets"
        response = self._make_api_request('GET', endpoint)
        return response.get('value', [])
    
    def get_tables(self, dataset_id: str = None) -> List[Dict[str, Any]]:
        """Get tables in dataset"""
        dataset_id = dataset_id or self.config.dataset_id
        endpoint = f"groups/{self.config.workspace_id}/datasets/{dataset_id}/tables"
        response = self._make_api_request('GET', endpoint)
        return response.get('value', [])
    
    def execute_query(self, dax_query: str, dataset_id: str = None) -> Dict[str, Any]:
        """Execute DAX query and return results"""
        dataset_id = dataset_id or self.config.dataset_id
        endpoint = f"groups/{self.config.workspace_id}/datasets/{dataset_id}/executeQueries"
        
        payload = {
            "queries": [{"query": dax_query}],
            "serializerSettings": {
                "includeNulls": True
            }
        }
        
        response = self._make_api_request('POST', endpoint, json=payload)
        return response.get('results', [{}])[0]