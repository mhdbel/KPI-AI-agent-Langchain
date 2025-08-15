"""Main KPI Agent implementation"""
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import BaseTool
from langchain.memory import BaseMemory
from langchain.chat_models import BaseChatModel
from langchain.prompts import ChatPromptTemplate
from typing import List, Optional
import logging

class KPIAgent:
    """Main KPI Agent that orchestrates all components"""
    
    def __init__(self, 
                 llm: BaseChatModel,
                 tools: List[BaseTool],
                 memory: Optional[BaseMemory] = None,
                 verbose: bool = True):
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        self.agent_executor = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent executor"""
        agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self._get_prompt()
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose,
            handle_parsing_errors=True
        )
    
    def _get_prompt(self):
        """Get the agent prompt template"""
        return ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert KPI Analysis Agent specializing in remote fix case data analysis.
            
            Your capabilities include:
            1. Data retrieval from CSV files and Power BI
            2. Exploratory Data Analysis and visualization
            3. Predictive analytics and forecasting
            4. Multi-criteria decision analysis using AHP
            5. Actionable recommendation generation
            
            Always provide clear, data-driven insights and maintain professional communication.
            When uncertainty exists, acknowledge it and suggest verification steps.
            """),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
    
    def run(self, query: str) -> dict:
        """Execute the agent with a query"""
        try:
            result = self.agent_executor.invoke({"input": query})
            return {
                "success": True,
                "output": result["output"],
                "intermediate_steps": result.get("intermediate_steps", [])
            }
        except Exception as e:
            self.logger.error(f"Agent execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "output": f"Error executing agent: {str(e)}"
            }