"""Vector store memory for semantic search"""
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List, Dict, Any, Optional
import uuid

class KPIVectorMemory:
    """Semantic memory for KPI contexts using vector embeddings"""
    
    def __init__(self, embedding_model=None, persist_directory: str = "./kpi_memory"):
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model
        )
    
    def store_kpi_context(self, kpi_context: 'KPIContext', meta Optional[Dict] = None):
        """Store KPI context in vector memory"""
        # Convert KPI context to text
        context_text = self._kpi_context_to_text(kpi_context)
        
        # Split into chunks
        docs = self.text_splitter.create_documents(
            [context_text],
            metadatas=[metadata or {}]
        )
        
        # Add to vector store
        doc_ids = self.vector_store.add_documents(docs)
        return doc_ids
    
    def search_relevant_context(self, query: str, k: int = 4) -> List[Document]:
        """Search for relevant KPI contexts"""
        return self.vector_store.similarity_search(query, k=k)
    
    def _kpi_context_to_text(self, kpi_context: 'KPIContext') -> str:
        """Convert KPI context to searchable text"""
        return f"""
        KPI Name: {kpi_context.kpi_name}
        Description: {kpi_context.kpi_description}
        Data Source: {kpi_context.data_source}
        Business Domain: {kpi_context.business_domain}
        Stakeholders: {', '.join(kpi_context.stakeholders)}
        Last Analysis Results: {json.dumps(kpi_context.analysis_results) if kpi_context.analysis_results else 'None'}
        Recommendations: {', '.join(kpi_context.recommendations) if kpi_context.recommendations else 'None'}
        """