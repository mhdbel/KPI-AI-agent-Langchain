"""KPI analysis chain"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import BaseChatModel

class KPIAnalysisChain(LLMChain):
    """Chain for KPI data analysis"""
    
    @classmethod
    def from_llm(cls, llm: BaseChatModel, verbose: bool = True) -> "KPIAnalysisChain":
        prompt = PromptTemplate(
            template="""
            Analyze the following KPI data and provide insights:
            
            Data Context: {data_context}
            KPI Focus: {kpi_focus}
            Analysis Requirements: {requirements}
            
            Provide a structured analysis including:
            1. Key trends and patterns
            2. Statistical significance
            3. Business implications
            4. Data quality observations
            5. Recommendations for further analysis
            
            Format your response clearly with headers and bullet points.
            """,
            input_variables=["data_context", "kpi_focus", "requirements"]
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)