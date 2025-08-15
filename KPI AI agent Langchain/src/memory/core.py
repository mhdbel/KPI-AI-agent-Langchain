"""Core memory abstractions"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class KPIContext:
    """Structured KPI context information"""
    kpi_name: str
    kpi_description: str
    data_source: str
    business_domain: str
    stakeholders: List[str]
    last_analyzed: Optional[datetime] = None
    analysis_results: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None

@dataclass
class AnalysisSession:
    """Record of an analysis session"""
    session_id: str
    timestamp: datetime
    user_query: str
    context_used: Dict[str, Any]
    tools_used: List[str]
    results: Dict[str, Any]
    feedback: Optional[str] = None

class KPIMemory(ABC):
    """Abstract base class for KPI memory systems"""
    
    @abstractmethod
    def store_context(self, context: KPIContext) -> None:
        """Store KPI context information"""
        pass
    
    @abstractmethod
    def retrieve_context(self, kpi_name: str) -> Optional[KPIContext]:
        """Retrieve KPI context by name"""
        pass
    
    @abstractmethod
    def store_session(self, session: AnalysisSession) -> None:
        """Store analysis session"""
        pass
    
    @abstractmethod
    def get_recent_sessions(self, limit: int = 5) -> List[AnalysisSession]:
        """Get recent analysis sessions"""
        pass