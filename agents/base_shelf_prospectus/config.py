"""
Configuration settings for the BSP (Base Shelf Prospectus) agent.

TODO: Full implementation pending ISM agent completion.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class BSPConfig(BaseModel):
    """
    Configuration settings specific to the BSP agent.
    
    TODO: Define comprehensive configuration for base shelf prospectus generation.
    """
    
    # Document Generation Settings
    max_document_length: int = Field(default=20000, description="Maximum document length in words")
    include_executive_summary: bool = Field(default=True, description="Whether to include executive summary")
    include_financial_statements: bool = Field(default=True, description="Whether to include financial statements")
    
    # Legal and Regulatory Settings
    include_legal_opinions: bool = Field(default=True, description="Include legal opinion sections")
    include_regulatory_compliance: bool = Field(default=True, description="Include regulatory compliance details")
    sec_compliance_level: str = Field(default="full", description="Level of SEC compliance required")
    
    # Content Preferences
    technical_level: str = Field(default="institutional", description="Technical detail level")
    include_risk_factors: bool = Field(default=True, description="Include comprehensive risk factors")
    
    # TODO: Add more BSP-specific configuration options
    
    @classmethod
    def get_default_config(cls) -> "BSPConfig":
        """Get default configuration for BSP agent"""
        return cls()