"""Recommendation generation chain"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import BaseChatModel

class RecommendationChain(LLMChain):
    """Chain for generating recommendations"""
    
    @classmethod
    def from_llm(cls, llm: BaseChatModel, verbose: bool = True) -> "RecommendationChain":
        prompt = PromptTemplate(
            template="""
            Based on the following analysis, generate actionable recommendations:
            
            Analysis Results: {analysis_results}
            Business Context: {business_context}
            Stakeholders: {stakeholders}
            
            Provide recommendations that are:
            1. Specific and measurable
            2. Prioritized by impact and feasibility
            3. Aligned with business objectives
            4. Include implementation steps
            5. Consider resource constraints
            
            Format as a prioritized list with clear action items.
            """,
            input_variables=["analysis_results", "business_context", "stakeholders"]
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)