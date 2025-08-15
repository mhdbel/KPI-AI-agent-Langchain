"""LangChain tool for EDA"""
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
import pandas as pd
import json

from .core import EDAProcessor

class EDATool(BaseTool):
    """LangChain tool for exploratory data analysis"""
    
    name = "eda_analysis"
    description = "Performs exploratory data analysis on provided data"
    
    def _run(
        self,
        data_json: str,
        analysis_type: str = "summary",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute EDA analysis"""
        try:
            # Parse data
            data = json.loads(data_json)
            df = pd.DataFrame(data)
            
            # Perform analysis based on type
            if analysis_type == "summary":
                summary = EDAProcessor.generate_summary_stats(df)
                return json.dumps(summary, indent=2, default=str)
            elif analysis_type == "correlation":
                correlations = EDAProcessor.generate_correlation_matrix(df)
                return json.dumps(correlations, indent=2)
            else:
                return "Unsupported analysis type. Use 'summary' or 'correlation'"
                
        except Exception as e:
            return f"EDA analysis failed: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        return self._run(*args, **kwargs)