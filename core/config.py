"""
Global configuration settings for the multi-agent financial document generation system.
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GlobalConfig(BaseModel):
    """
    Global configuration settings shared across all agents.
    """
    
    # API Configuration
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    default_model: str = Field(default="openai:gpt-4o-mini")
    
    # LightRAG Configuration  
    knowledge_bases_root: str = Field(default="knowledge_bases")
    default_embedding_func: str = Field(default="openai_embed")
    default_llm_func: str = Field(default="gpt_4o_mini_complete")
    
    # Document Generation Configuration
    generated_documents_root: str = Field(default="generated_documents")
    max_retries: int = Field(default=3)
    timeout_seconds: int = Field(default=300)
    
    # Agent Configuration
    enable_streaming: bool = Field(default=True)
    enable_tool_calls: bool = Field(default=True)
    max_tool_calls_per_run: int = Field(default=10)
    
    # Logging and Monitoring
    log_level: str = Field(default="INFO")
    enable_usage_tracking: bool = Field(default=True)
    
    def model_post_init(self, __context: Any) -> None:  # type: ignore[override]
        """Pydantic v2 post-init hook: ensure dirs and validate non-fatal settings.
        
        This avoids hard failures at import-time while still surfacing misconfiguration early.
        """
        # Ensure required directories exist
        try:
            self.ensure_directories_exist()
        except Exception:
            # Do not raise at import time; downstream callers can surface a clearer error
            pass

        # Non-fatal warning if API key is missing. Runtime components that actually
        # require the key should perform their own strict validation.
        if not (self.openai_api_key and self.openai_api_key.strip()):
            import logging
            logging.basicConfig(level=self.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            logging.getLogger(__name__).warning(
                "OPENAI_API_KEY is not set. LLM-backed features will fail until it's provided."
            )
    
    @classmethod
    def get_default(cls) -> "GlobalConfig":
        """Get default global configuration"""
        return cls()
    
    def get_knowledge_base_path(self, agent_type: str) -> str:
        """Get the knowledge base path for a specific agent type"""
        # Map old agent names to new official names
        agent_name_mapping = {
            "ism": "investor_summary",
            "bsp": "base_shelf_prospectus", 
            "pds": "product_supplement",
            "prs": "pricing_supplement"
        }
        # Use mapped name if available, otherwise use original
        mapped_name = agent_name_mapping.get(agent_type, agent_type)
        return os.path.join(self.knowledge_bases_root, f"{mapped_name}_kb")
    
    def get_output_path(self, agent_type: str) -> str:
        """Get the output directory path for a specific agent type"""
        # Map old agent names to new official names
        agent_name_mapping = {
            "ism": "investor_summary",
            "bsp": "base_shelf_prospectus",
            "pds": "product_supplement", 
            "prs": "pricing_supplement"
        }
        # Use mapped name if available, otherwise use original
        mapped_name = agent_name_mapping.get(agent_type, agent_type)
        return os.path.join(self.generated_documents_root, mapped_name)
    
    def ensure_directories_exist(self):
        """Ensure all required directories exist"""
        os.makedirs(self.knowledge_bases_root, exist_ok=True)
        os.makedirs(self.generated_documents_root, exist_ok=True)


# Global configuration instance (created at import time)
global_config = GlobalConfig.get_default()