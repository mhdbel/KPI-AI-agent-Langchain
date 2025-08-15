"""Factory for creating memory systems"""
from typing import Dict, Any, Optional
from langchain.chat_models import BaseChatModel
from langchain.memory import ConversationBufferMemory, CombinedMemory
from .conversation import KPIConversationMemory
from .vector import KPIVectorMemory
from .persistent import KPIPersistentMemory

def create_memory_system(llm: BaseChatModel, config: Dict[str, Any]) -> CombinedMemory:
    """Create memory system based on configuration"""
    memory_type = config.get("type", "simple")
    
    if memory_type == "simple":
        return create_simple_memory()
    elif memory_type == "conversational":
        return create_conversational_memory(llm)
    elif memory_type == "hybrid":
        return create_hybrid_memory(llm, config)
    else:
        return create_simple_memory()

def create_simple_memory() -> ConversationBufferMemory:
    """Create simple conversation buffer memory"""
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def create_conversational_memory(llm) -> KPIConversationMemory:
    """Create KPI conversation memory"""
    memory = KPIConversationMemory()
    memory.set_llm(llm)
    return memory

def create_hybrid_memory(llm, config: Dict[str, Any]) -> CombinedMemory:
    """Create hybrid memory combining multiple memory types"""
    memories = []
    
    # Add conversation memory
    conv_memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True,
        k=10
    )
    memories.append(conv_memory)
    
    # Add summary memory
    from langchain.memory import ConversationSummaryBufferMemory
    summary_memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_summary",
        max_token_limit=500
    )
    memories.append(summary_memory)
    
    return CombinedMemory(memories=memories)