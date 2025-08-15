"""LangChain tool for data retrieval"""
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
import pandas as pd
import json
import os

from .core import DataRetriever

class DataRetrievalTool(BaseTool):
    """LangChain tool for data retrieval"""
    
    name = "data_retrieval"
    description = "Retrieves data from CSV files or JSON input"
    
    def _run(
        self,
        source_type: str = "csv",
        file_path: str = None,
        json_ str = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Retrieve data"""
        try:
            if source_type == "csv":
                if not file_path:
                    return "File path required for CSV source"
                if not os.path.exists(file_path):
                    return f"File not found: {file_path}"
                
                df = DataRetriever.load_csv_data(file_path)
                summary = DataRetriever.get_data_summary(df)
                return json.dumps({
                    'data': df.head(10).to_dict(orient='records'),
                    'summary': summary
                }, indent=2, default=str)
                
            elif source_type == "json":
                if not json_
                    return "JSON data required for JSON source"
                
                df = DataRetriever.load_json_data(json_data)
                summary = DataRetriever.get_data_summary(df)
                return json.dumps({
                    'data': df.to_dict(orient='records'),
                    'summary': summary
                }, indent=2, default=str)
                
            else:
                return "Unsupported source type. Use 'csv' or 'json'"
                
        except Exception as e:
            return f"Data retrieval failed: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        return self._run(*args, **kwargs)