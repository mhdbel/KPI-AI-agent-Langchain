"""LLM-based AHP reasoning components"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import BaseChatModel
from typing import Dict, Any, List

class AHPReasoningComponents:
    """Modular LLM reasoning components for AHP"""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    def context_analysis_chain(self) -> LLMChain:
        """Analyze context to inform AHP structure"""
        prompt = PromptTemplate(
            template="""
            Analyze KPI context for AHP decision making:
            KPI Data: {kpi_data}
            Problem: {problem_context}
            Alternatives: {alternatives}
            
            Provide analysis of decision factors and stakeholder perspectives.
            """,
            input_variables=["kpi_data", "problem_context", "alternatives"]
        )
        return LLMChain(llm=self.llm, prompt=prompt, output_key="context_analysis")
    
    def criteria_generation_chain(self) -> LLMChain:
        """Generate appropriate AHP criteria"""
        prompt = PromptTemplate(
            template="""
            Generate AHP criteria based on analysis:
            Context: {context_analysis}
            Alternatives: {alternatives}
            
            Return 3-5 criteria as JSON with names and descriptions.
            """,
            input_variables=["context_analysis", "alternatives"]
        )
        return LLMChain(llm=self.llm, prompt=prompt, output_key="generated_criteria")
    
    def pairwise_comparisons_chain(self) -> LLMChain:
        """Generate pairwise comparisons"""
        prompt = PromptTemplate(
            template="""
            Generate pairwise comparisons using 1-9 scale:
            Criteria: {generated_criteria}
            Alternatives: {alternatives}
            Context: {context_analysis}
            
            Return JSON with criteria_comparisons and alternative_comparisons.
            """,
            input_variables=["generated_criteria", "alternatives", "context_analysis"]
        )
        return LLMChain(llm=self.llm, prompt=prompt, output_key="pairwise_comparisons")
    
    def recommendation_chain(self) -> LLMChain:
        """Generate final recommendations"""
        prompt = PromptTemplate(
            template="""
            Generate recommendations based on AHP results:
            Weights: {ahp_weights}
            Context: {context_analysis}
            Problem: {problem_context}
            
            Provide ranked alternatives and implementation suggestions.
            """,
            input_variables=["ahp_weights", "context_analysis", "problem_context"]
        )
        return LLMChain(llm=self.llm, prompt=prompt, output_key="recommendations")