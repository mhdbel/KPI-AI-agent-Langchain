"""LangChain tool for AHP reasoning"""
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from typing import List, Optional
import json

from .core import AHPCalculator, AHPResult
from .reasoning import AHPReasoningComponents
from pydantic import BaseModel, Field

class AHPAnalysisInput(BaseModel):
    """Input schema for AHP analysis"""
    kpi_data_summary: str = Field(description="Summary of KPI data for analysis")
    problem_context: str = Field(description="Context about the problem to solve")
    alternatives: List[str] = Field(description="List of alternatives to evaluate")
    criteria_context: Optional[str] = Field(default=None, description="Additional context for criteria definition")

class AHPReasoningTool(BaseTool):
    """LangChain tool for AHP analysis"""
    
    name = "ahp_analysis"
    description = "Performs Analytic Hierarchy Process analysis for decision making"
    reasoning_components: AHPReasoningComponents
    
    def _run(
        self,
        kpi_data_summary: str,
        problem_context: str,
        alternatives: List[str],
        criteria_context: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute AHP analysis"""
        try:
            # Context analysis
            context_result = self.reasoning_components.context_analysis_chain().run({
                'kpi_data': kpi_data_summary,
                'problem_context': problem_context,
                'alternatives': alternatives
            })
            
            # Generate criteria
            criteria_result = self.reasoning_components.criteria_generation_chain().run({
                'context_analysis': context_result,
                'alternatives': alternatives
            })
            
            # Generate comparisons
            comparison_result = self.reasoning_components.pairwise_comparisons_chain().run({
                'generated_criteria': criteria_result,
                'alternatives': alternatives,
                'context_analysis': context_result
            })
            
            # Parse comparisons and execute AHP
            comparisons_data = json.loads(comparison_result)
            ahp_result = AHPCalculator.execute_ahp(
                comparisons_data['criteria_comparisons'],
                comparisons_data['alternative_comparisons']
            )
            
            # Generate recommendations
            recommendations = self.reasoning_components.recommendation_chain().run({
                'ahp_weights': ahp_result.weights,
                'context_analysis': context_result,
                'problem_context': problem_context
            })
            
            return json.dumps({
                'success': True,
                'weights': ahp_result.weights,
                'consistency': ahp_result.consistency_ratios,
                'recommendations': recommendations,
                'report': ahp_result.report
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, indent=2)
    
    async def _arun(self, *args, **kwargs) -> str:
        return self._run(*args, **kwargs)