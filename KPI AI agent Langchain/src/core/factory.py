"""Factory for creating KPI agent systems"""
from typing import Dict, Any, Optional
from .orchestrator import KPIAgentOrchestrator

class KPIAgentFactory:
    """Factory for creating KPI agent systems"""
    
    @staticmethod
    def create_agent_system(config: Optional[Dict[str, Any]] = None) -> KPIAgentOrchestrator:
        """Create complete KPI agent system"""
        if config is None:
            config = KPIAgentFactory._get_default_config()
        
        return KPIAgentOrchestrator(config)
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "llm": {
                "model": "gpt-4",
                "temperature": 0.0,
                "streaming": False
            },
            "memory": {
                "type": "hybrid",
                "persist_directory": "./kpi_memory"
            },
            "agent": {
                "verbose": True
            },
            "tools": {
                "powerbi": {
                    "enabled": True
                },
                "ahp": {
                    "enabled": True
                },
                "eda": {
                    "enabled": True
                },
                "predictive": {
                    "enabled": True
                },
                "data": {
                    "enabled": True
                }
            }
        }