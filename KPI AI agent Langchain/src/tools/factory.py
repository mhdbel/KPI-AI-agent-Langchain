"""Factory for creating tools"""
from typing import List, Dict, Any
from langchain.tools import BaseTool

def get_all_tools(config: Dict[str, Any]) -> List[BaseTool]:
    """Get all enabled tools based on configuration"""
    tools = []
    tool_config = config.get("tools", {})
    
    if tool_config.get("powerbi", {}).get("enabled", True):
        from .powerbi.tool import PowerBITool, PowerBIMetadataTool
        from ...config.settings import get_powerbi_config
        pb_config = get_powerbi_config()
        if pb_config:
            tools.extend([PowerBITool(pb_config), PowerBIMetadataTool(pb_config)])
    
    if tool_config.get("ahp", {}).get("enabled", True):
        from .ahp.tool import AHPReasoningTool
        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(temperature=0, model=config.get("llm", {}).get("model", "gpt-4"))
        tools.append(AHPReasoningTool(llm))
    
    if tool_config.get("eda", {}).get("enabled", True):
        from .eda.tool import EDATool
        tools.append(EDATool())
    
    if tool_config.get("predictive", {}).get("enabled", True):
        from .predictive.tool import PredictiveAnalysisTool
        tools.append(PredictiveAnalysisTool())
    
    if tool_config.get("data", {}).get("enabled", True):
        from .data.tool import DataRetrievalTool
        tools.append(DataRetrievalTool())
    
    return tools