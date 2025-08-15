"""LangChain tools for Power BI integration"""
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from typing import Optional, Dict, Any, List
import json
import pandas as pd

from .core import PowerBIClient, PowerBIConfig, PowerBIAPIError
from .processor import PowerBIDataProcessor
from .queries import PowerBIQueryBuilder

class PowerBITool(BaseTool):
    """LangChain tool for Power BI data retrieval"""
    
    name = "powerbi_data_retrieval"
    description = """
    Retrieves data from Power BI datasets using DAX queries.
    Can execute custom queries or generate common analysis queries.
    Returns data as JSON or summary statistics.
    """
    
    def __init__(self, config: PowerBIConfig):
        super().__init__()
        self.client = PowerBIClient(config)
        self.processor = PowerBIDataProcessor()
        self.query_builder = PowerBIQueryBuilder()
    
    def _run(
        self,
        query_type: str = "custom",
        table_name: Optional[str] = None,
        dax_query: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute Power BI query"""
        try:
            # Build or use provided query
            if dax_query:
                query = dax_query
            else:
                query = self._build_query(query_type, table_name, parameters or {})
            
            # Execute query
            results = self.client.execute_query(query)
            
            # Process results
            df = self.processor.process_query_results(results)
            return df.to_json(orient='records')
                
        except Exception as e:
            return f"Power BI query failed: {str(e)}"
    
    def _build_query(self, query_type: str, table_name: str, parameters: Dict[str, Any]) -> str:
        """Build query based on type and parameters"""
        if query_type == "time_series":
            return self.query_builder.build_time_series_query(
                table_name=table_name,
                date_column=parameters.get('date_column', 'Date'),
                value_columns=parameters.get('value_columns', []),
                time_granularity=parameters.get('time_granularity', 'MONTH'),
                date_filter=parameters.get('date_filter')
            )
        elif query_type == "kpi_summary":
            return self.query_builder.build_kpi_summary_query(
                table_name=table_name,
                kpi_columns=parameters.get('kpi_columns', []),
                group_by_columns=parameters.get('group_by_columns')
            )
        elif query_type == "custom" and 'query' in parameters:
            return parameters['query']
        else:
            raise ValueError(f"Unsupported query type: {query_type}")
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version of the tool"""
        return self._run(*args, **kwargs)

class PowerBIMetadataTool(BaseTool):
    """Tool for retrieving Power BI metadata"""
    
    name = "powerbi_metadata"
    description = "Retrieves metadata about Power BI datasets, tables, and columns"
    
    def __init__(self, config: PowerBIConfig):
        super().__init__()
        self.client = PowerBIClient(config)
    
    def _run(
        self,
        action: str = "datasets",  # datasets, tables, metadata
        dataset_id: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Retrieve Power BI metadata"""
        try:
            if action == "datasets":
                datasets = self.client.get_datasets()
                return json.dumps(datasets, indent=2)
            elif action == "tables":
                tables = self.client.get_tables(dataset_id)
                return json.dumps(tables, indent=2)
            else:
                return "Invalid action. Use 'datasets' or 'tables'"
        except Exception as e:
            return f"Metadata retrieval failed: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        return self._run(*args, **kwargs)