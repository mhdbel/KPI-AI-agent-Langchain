"""LangChain tool for predictive analysis"""
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
import pandas as pd
import json

from .core import PredictiveAnalyzer

class PredictiveAnalysisTool(BaseTool):
    """LangChain tool for predictive analysis"""
    
    name = "predictive_analysis"
    description = "Performs predictive analysis and forecasting on KPI data"
    
    def _run(
        self,
        data_json: str,
        target_column: str,
        analysis_type: str = "forecast",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute predictive analysis"""
        try:
            # Parse data
            data = json.loads(data_json)
            df = pd.DataFrame(data)
            
            # Perform analysis based on type
            if analysis_type == "forecast":
                results = PredictiveAnalyzer.forecast_future(df, target_column)
                return json.dumps(results, indent=2)
            elif analysis_type == "model":
                X, y = PredictiveAnalyzer.prepare_data(df, target_column)
                results = PredictiveAnalyzer.train_forecast_model(X, y)
                return json.dumps(results, indent=2)
            else:
                return "Unsupported analysis type. Use 'forecast' or 'model'"
                
        except Exception as e:
            return f"Predictive analysis failed: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        return self._run(*args, **kwargs)