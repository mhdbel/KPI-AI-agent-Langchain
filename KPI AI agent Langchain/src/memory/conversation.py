"""Conversation memory management"""
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.schema import BaseMessage
from typing import List, Dict, Any, Optional
import json

class KPIConversationMemory:
    """Manages conversation history for KPI analysis"""
    
    def __init__(self, max_tokens: int = 2000):
        self.buffer_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.summary_memory = ConversationSummaryBufferMemory(
            llm=None,  # Will be set later
            memory_key="chat_summary",
            max_token_limit=max_tokens
        )
        self.context_memory = {}
    
    def set_llm(self, llm):
        """Set LLM for summary memory"""
        self.summary_memory.llm = llm
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add message to conversation memory"""
        # Add to buffer memory
        if role == "user":
            self.buffer_memory.chat_memory.add_user_message(content)
        else:
            self.buffer_memory.chat_memory.add_ai_message(content)
        
        # Add to summary memory
        if role == "user":
            self.summary_memory.chat_memory.add_user_message(content)
        else:
            self.summary_memory.chat_memory.add_ai_message(content)
        
        # Store context metadata if provided
        if metadata:
            message_id = len(self.buffer_memory.chat_memory.messages)
            self.context_memory[message_id] = metadata
    
    def get_recent_history(self, k: int = 5) -> List[BaseMessage]:
        """Get recent conversation history"""
        messages = self.buffer_memory.chat_memory.messages
        return messages[-k:] if len(messages) > k else messages
    
    def get_summary(self) -> str:
        """Get conversation summary"""
        return self.summary_memory.load_memory_variables({}).get("chat_summary", "")
    
    def clear(self):
        """Clear conversation memory"""
        self.buffer_memory.clear()
        self.summary_memory.clear()
        self.context_memory.clear()