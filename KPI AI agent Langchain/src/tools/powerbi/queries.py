"""Predefined queries and query builder for Power BI"""
from typing import Dict, Any, List, Optional

class PowerBIQueryBuilder:
    """Build common Power BI DAX queries"""
    
    @staticmethod
    def build_time_series_query(table_name: str, 
                              date_column: str, 
                              value_columns: List[str],
                              time_granularity: str = "MONTH",
                              date_filter: Optional[str] = None) -> str:
        """Build time series analysis query"""
        value_summarizations = [
            f"SUM('{table_name}'[{col}]) AS {col}" 
            for col in value_columns
        ]
        
        date_function = {
            "DAY": f"FORMAT('{table_name}'[{date_column}], \"YYYY-MM-DD\")",
            "MONTH": f"FORMAT('{table_name}'[{date_column}], \"YYYY-MM\")",
            "YEAR": f"YEAR('{table_name}'[{date_column}])"
        }.get(time_granularity, f"FORMAT('{table_name}'[{date_column}], \"YYYY-MM\")")
        
        filter_clause = f"WHERE {date_filter}" if date_filter else ""
        
        query = f"""
        EVALUATE
        SUMMARIZE(
            '{table_name}',
            {date_function},
            {', '.join(value_summarizations)}
        )
        {filter_clause}
        ORDER BY {date_function}
        """
        return query.strip()
    
    @staticmethod
    def build_kpi_summary_query(table_name: str, 
                              kpi_columns: List[str],
                              group_by_columns: Optional[List[str]] = None) -> str:
        """Build KPI summary statistics query"""
        aggregations = []
        for col in kpi_columns:
            aggregations.extend([
                f"AVG('{table_name}'[{col}]) AS Avg_{col}",
                f"SUM('{table_name}'[{col}]) AS Sum_{col}",
                f"MIN('{table_name}'[{col}]) AS Min_{col}",
                f"MAX('{table_name}'[{col}]) AS Max_{col}",
                f"COUNT('{table_name}'[{col}]) AS Count_{col}"
            ])
        
        group_by_clause = ""
        if group_by_columns:
            group_by_list = [f"'{table_name}'[{col}]" for col in group_by_columns]
            group_by_clause = f", {', '.join(group_by_list)}"
        
        query = f"""
        EVALUATE
        SUMMARIZE(
            '{table_name}',
            {', '.join(aggregations)}
            {group_by_clause}
        )
        """
        return query.strip()