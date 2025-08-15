"""KPI Agent System Orchestrator"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from .agent import KPIAgent
from ..tools.factory import get_all_tools
from ..memory.factory import create_memory_system

class KPIAgentOrchestrator:
    """Orchestrates the complete KPI agent system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agent = None
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize all system components"""
        # Initialize LLM
        llm_config = self.config.get("llm", {})
        llm = ChatOpenAI(
            model=llm_config.get("model", "gpt-4"),
            temperature=llm_config.get("temperature", 0.0),
            streaming=llm_config.get("streaming", False)
        )
        
        # Initialize memory system
        memory_config = self.config.get("memory", {})
        memory = create_memory_system(llm, memory_config)
        
        # Initialize tools
        tools = get_all_tools(self.config)
        
        # Initialize agent
        agent_config = self.config.get("agent", {})
        self.agent = KPIAgent(
            llm=llm,
            tools=tools,
            memory=memory,
            verbose=agent_config.get("verbose", True)
        )
    
    def execute_analysis(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute complete KPI analysis"""
        try:
            # Add context to query if provided
            if context:
                enriched_query = f"""
                Context: {context}
                Query: {query}
                """
            else:
                enriched_query = query
            
            # Execute agent
            result = self.agent.run(enriched_query)
            
            return {
                "success": result["success"],
                "result": result["output"],
                "intermediate_steps": result.get("intermediate_steps", []),
                "query": query,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "agent_initialized": self.agent is not None,
            "model": self.config.get("llm", {}).get("model", "gpt-4"),
            "tools_count": len(self.agent.tools) if self.agent else 0,
            "memory_enabled": self.agent.memory is not None if self.agent else False,
            "timestamp": datetime.now().isoformat()
        }