"""
Configuration settings for the PRS (Pricing Supplement) agent.

TODO: Full implementation pending ISM agent completion.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class PRSConfig(BaseModel):
    """
    Configuration settings specific to the PRS agent.
    
    TODO: Define comprehensive configuration for pricing supplement generation.
    """
    
    # Document Generation Settings
    max_document_length: int = Field(default=8000, description="Maximum document length in words")
    include_pricing_summary: bool = Field(default=True, description="Include pricing summary")
    include_market_data: bool = Field(default=True, description="Include relevant market data")
    
    # Pricing Settings
    include_estimated_value: bool = Field(default=True, description="Include estimated value calculation")
    show_pricing_methodology: bool = Field(default=True, description="Show pricing methodology")
    include_fees_breakdown: bool = Field(default=True, description="Include detailed fees breakdown")
    
    # Format Settings
    use_tabular_format: bool = Field(default=True, description="Use tables for final terms")
    include_settlement_details: bool = Field(default=True, description="Include settlement details")
    
    # TODO: Add more PRS-specific configuration options
    
    @classmethod
    def get_default_config(cls) -> "PRSConfig":
        """Get default configuration for PRS agent"""
        return cls()