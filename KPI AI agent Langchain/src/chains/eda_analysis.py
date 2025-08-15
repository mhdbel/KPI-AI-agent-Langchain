"""EDA analysis chain"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import BaseChatModel

class EDAAnalysisChain(LLMChain):
    """Chain for EDA analysis interpretation"""
    
    @classmethod
    def from_llm(cls, llm: BaseChatModel, verbose: bool = True) -> "EDAAnalysisChain":
        prompt = PromptTemplate(
            template="""
            Interpret the following exploratory data analysis results:
            
            Data Summary: {data_summary}
            Statistical Analysis: {statistics}
            Correlations: {correlations}
            
            Provide insights on:
            1. Key patterns and trends
            2. Data quality issues
            3. Interesting relationships between variables
            4. Recommendations for further analysis
            5. Potential business implications
            
            Format your response with clear sections and actionable insights.
            """,
            input_variables=["data_summary", "statistics", "correlations"]
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)