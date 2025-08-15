"""
Configuration settings for the PDS (Prospectus Supplement) agent.

TODO: Full implementation pending ISM agent completion.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class PDSConfig(BaseModel):
    """
    Configuration settings specific to the PDS agent.
    
    TODO: Define comprehensive configuration for prospectus supplement generation.
    """
    
    # Document Generation Settings
    max_document_length: int = Field(default=15000, description="Maximum document length in words")
    include_base_prospectus_summary: bool = Field(default=True, description="Include base prospectus summary")
    focus_on_specific_terms: bool = Field(default=True, description="Focus on note-specific terms")
    
    # Reference Management
    auto_cross_reference: bool = Field(default=True, description="Automatically cross-reference base prospectus")
    include_modification_summary: bool = Field(default=True, description="Include summary of modifications")
    
    # Technical Settings
    technical_level: str = Field(default="detailed", description="Level of technical detail")
    include_calculations: bool = Field(default=True, description="Include detailed calculations")
    
    # TODO: Add more PDS-specific configuration options
    
    @classmethod
    def get_default_config(cls) -> "PDSConfig":
        """Get default configuration for PDS agent"""
        return cls()