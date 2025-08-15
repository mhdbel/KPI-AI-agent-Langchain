"""AHP reasoning chain"""
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import BaseChatModel

class AHPReasoningChain(SequentialChain):
    """LangChain-based AHP reasoning system"""
    
    def __init__(self, llm: BaseChatModel):
        chains = [
            self._create_context_analysis_chain(llm),
            self._create_criteria_generation_chain(llm),
            self._create_pairwise_comparisons_chain(llm),
            self._create_recommendation_chain(llm)
        ]
        super().__init__(
            chains=chains,
            input_variables=["kpi_data_summary", "problem_context", "alternatives", "criteria_context"],
            output_variables=["final_recommendations"]
        )
    
    def _create_context_analysis_chain(self, llm: BaseChatModel) -> LLMChain:
        prompt = PromptTemplate(
            template="""
            Analyze the KPI data and problem context to prepare for AHP analysis:
            
            KPI Data Summary: {kpi_data_summary}
            Problem Context: {problem_context}
            Available Alternatives: {alternatives}
            Additional Criteria Context: {criteria_context}
            
            Provide a structured analysis that will guide the AHP process:
            1. Key decision factors from the KPI data
            2. Stakeholder perspectives to consider
            3. Potential biases or constraints in the data
            4. How the alternatives relate to the problem context
            """,
            input_variables=["kpi_data_summary", "problem_context", "alternatives", "criteria_context"]
        )
        return LLMChain(llm=llm, prompt=prompt, output_key="context_analysis")
    
    def _create_criteria_generation_chain(self, llm: BaseChatModel) -> LLMChain:
        prompt = PromptTemplate(
            template="""
            Based on the context analysis, generate appropriate AHP criteria for decision making:
            
            Context Analysis: {context_analysis}
            Available Alternatives: {alternatives}
            
            Generate 3-5 criteria that are:
            - Mutually exclusive and collectively exhaustive
            - Measurable and relevant to the alternatives
            - Balanced between quantitative and qualitative factors
            
            For each criterion, provide:
            1. Name (concise, descriptive)
            2. Description (clear explanation of what it measures)
            """,
            input_variables=["context_analysis", "alternatives"]
        )
        return LLMChain(llm=llm, prompt=prompt, output_key="generated_criteria")
    
    def _create_pairwise_comparisons_chain(self, llm: BaseChatModel) -> LLMChain:
        prompt = PromptTemplate(
            template="""
            Generate pairwise comparison matrices for AHP analysis:
            
            Generated Criteria: {generated_criteria}
            Available Alternatives: {alternatives}
            Context Analysis: {context_analysis}
            
            Create two comparison structures:
            
            1. Criteria Comparisons: Compare each criterion against others in importance (1-9 scale)
            2. Alternative Comparisons: For each criterion, compare alternatives (1-9 scale)
            
            Use the 1-9 Saaty scale where:
            1 = Equal importance, 3 = Moderate, 5 = Strong, 7 = Very strong, 9 = Extreme
            """,
            input_variables=["generated_criteria", "alternatives", "context_analysis"]
        )
        return LLMChain(llm=llm, prompt=prompt, output_key="pairwise_comparisons")
    
    def _create_recommendation_chain(self, llm: BaseChatModel) -> LLMChain:
        prompt = PromptTemplate(
            template="""
            Generate actionable recommendations based on AHP analysis results:
            
            Context Analysis: {context_analysis}
            Problem Context: {problem_context}
            
            Provide:
            1. Ranked alternatives with their scores
            2. Key insights about the decision factors
            3. Risk considerations for top alternatives
            4. Implementation recommendations
            """,
            input_variables=["context_analysis", "problem_context"]
        )
        return LLMChain(llm=llm, prompt=prompt, output_key="final_recommendations")