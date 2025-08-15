"""
RAG Manager for handling multiple LightRAG instances across different agents.
"""

import asyncio
import os
import logging
from typing import Dict, Optional, Any, List


from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag import LightRAG, QueryParam

from .config import global_config

# Configure logging to use the level from global_config
logging.basicConfig(level=global_config.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RAGManager:
    """
    Manages multiple LightRAG instances for different knowledge domains/agents.
    
    This class provides a centralized way to:
    - Initialize and manage multiple LightRAG instances on-the-fly.
    - Insert new documents into the knowledge bases, triggering LightRAG's processing pipeline.
    - Query across different knowledge bases.
    - Handle cross-domain searches.
    - Manage LightRAG lifecycle and resources.
    """
    
    def __init__(self):
        """
        Initializes the RAGManager.
        """
        self.rag_instances: Dict[str, LightRAG] = {}
        self.initialized_domains: set = set()
    
    async def initialize_rag_instance(
        self, 
        domain: str, 
        force_reinit: bool = False
    ) -> LightRAG:
        """
        Initializes a LightRAG instance for a specific domain.
        The knowledge base path is automatically determined using the global configuration.
        
        Args:
            domain (str): The domain identifier (e.g., 'ism', 'bsp').
            force_reinit (bool): If True, forces reinitialization even if an instance already exists.
            
        Returns:
            LightRAG: The initialized LightRAG instance.
            
        Raises:
            ValueError: If the domain is invalid.
        """
        if not domain or not isinstance(domain, str):
            raise ValueError("Domain must be a non-empty string.")

        if domain in self.rag_instances and not force_reinit:
            logger.info(f"Returning existing LightRAG instance for domain '{domain}'.")
            return self.rag_instances[domain]
        
        knowledge_base_path = global_config.get_knowledge_base_path(domain)
        logger.info(f"Initializing LightRAG for domain '{domain}' at path: {knowledge_base_path}")
        
        os.makedirs(knowledge_base_path, exist_ok=True)
        
        try:
            rag = LightRAG(
                working_dir=knowledge_base_path,
                embedding_func=openai_embed,
                llm_model_func=gpt_4o_mini_complete
            )
            
            if domain not in self.initialized_domains or force_reinit:
                await rag.initialize_storages()
                self.initialized_domains.add(domain)
            
            self.rag_instances[domain] = rag
            logger.info(f"Successfully initialized LightRAG for domain '{domain}'.")
            return rag
        except Exception as e:
            logger.error(f"Failed to initialize LightRAG for domain '{domain}': {e}", exc_info=True)
            raise

    async def get_rag_instance(self, domain: str) -> Optional[LightRAG]:
        """
        Retrieves an existing LightRAG instance for a domain.
        
        Args:
            domain (str): The domain identifier.
            
        Returns:
            Optional[LightRAG]: The LightRAG instance if it exists, otherwise None.
        """
        return self.rag_instances.get(domain)

    async def insert_document(
        self,
        domain: str,
        document_content: str,
    ) -> Dict[str, Any]:
        """
        Inserts a new document into a specific domain's knowledge base.

        This method ensures a RAG instance for the domain is ready, then hands off the
        document to the LightRAG library, which handles chunking, embedding, and storage.

        Args:
            domain (str): The target domain for the document.
            document_content (str): The full text content of the document.
            document_id (Optional[str]): A unique identifier for the document.

        Returns:
            Dict[str, Any]: A dictionary with the result of the operation.
        """
        logger.info(f"Received request to insert document into domain '{domain}'.")
        try:
            rag_instance = await self.get_rag_instance(domain)
            if not rag_instance:
                logger.warning(f"RAG instance for domain '{domain}' not found. Initializing it now.")
                rag_instance = await self.initialize_rag_instance(domain)

            # Work around LightRAG pipeline KeyError('history_messages') by using
            # the direct custom-chunk insert path, which does not depend on the
            # pipeline shared state.
            full_text = document_content
            # Simple conservative chunking by characters to keep chunks reasonably sized
            chunk_size = 2000
            text_chunks = [
                full_text[i : i + chunk_size]
                for i in range(0, len(full_text), chunk_size)
            ] if full_text else []

            if not text_chunks:
                logger.info("No content to insert (empty document). Skipping.")
                return {"success": True, "message": "Empty document skipped."}

            await rag_instance.ainsert_custom_chunks(full_text=full_text, text_chunks=text_chunks)
            
            logger.info(f"Successfully inserted document into domain '{domain}'.")
            return {"success": True, "message": f"Document inserted successfully into domain '{domain}'."}

        except Exception as e:
            logger.error(f"Error inserting document into domain '{domain}': {e}", exc_info=True)
            return {"success": False, "message": str(e)}
            
    async def query_domain(
        self, 
        domain: str, 
        query: str, 
        mode: str = "mix",
        top_k: int = 5
    ) -> str:
        """
        Query a specific knowledge domain. Auto-initializes domain if needed.
        """
        rag_instance = self.rag_instances.get(domain)
        if not rag_instance:
            logger.warning(f"RAG instance for domain '{domain}' not found. Initializing on-demand.")
            rag_instance = await self.initialize_rag_instance(domain)
        
        param = QueryParam(mode=mode, top_k=top_k)
        result = await rag_instance.aquery(query, param=param)
        
        return result
    
    async def cross_domain_query(
        self, 
        domains: List[str], 
        query: str,
        mode: str = "mix",
        top_k: int = 5
    ) -> Dict[str, str]:
        """
        Query across multiple domains and return aggregated results.
        """
        results = {}
        
        async def query_single_domain(domain: str) -> tuple[str, str]:
            try:
                result = await self.query_domain(domain, query, mode, top_k)
                return domain, result
            except Exception as e:
                logger.error(f"Error querying domain {domain}: {str(e)}")
                return domain, f"Error querying domain {domain}: {str(e)}"
        
        tasks = [query_single_domain(domain) for domain in domains]
        query_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in query_results:
            if isinstance(result, tuple):
                domain, query_result = result
                results[domain] = query_result
            else:
                logger.error(f"An exception occurred during cross-domain query: {result}")
                results["error"] = str(result)
        
        return results

    def list_domains(self) -> List[str]:
        """Get a list of all initialized domains"""
        return list(self.rag_instances.keys())
    
    async def cleanup(self):
        """
        Clean up all RAG instances and resources
        """
        logger.info("Cleaning up all RAG instances.")
        for domain in list(self.rag_instances.keys()):
            try:
                del self.rag_instances[domain]
                logger.info(f"Cleaned up RAG instance for domain '{domain}'.")
            except Exception as e:
                logger.error(f"Error cleaning up RAG instance for domain '{domain}': {e}")
        
        self.rag_instances.clear()
        self.initialized_domains.clear()
        logger.info("All RAG instances have been cleared.")


# Global RAG manager instance
rag_manager = RAGManager()
