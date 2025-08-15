"""
Pydantic models for the BSP (Base Shelf Prospectus) agent.

TODO: Full implementation pending ISM agent completion.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date
from core.base_agent import BaseFinancialAgentDeps


class BSPInput(BaseModel):
    """
    Input model for BSP (Base Shelf Prospectus) document generation.
    
    TODO: Define comprehensive input parameters for base shelf prospectus generation.
    """
    # Core Issuer Information
    issuer: str = Field(..., description="The name of the issuing entity")
    guarantor: Optional[str] = Field(None, description="The guarantor of the notes, if any")
    
    # Program Information
    program_name: str = Field(..., description="Name of the structured notes program")
    shelf_amount: float = Field(..., description="Total shelf registration amount")
    currency: str = Field(..., description="Base currency for the program")
    
    # Legal and Regulatory
    regulatory_jurisdiction: str = Field(..., description="Primary regulatory jurisdiction")
    sec_registration: Optional[str] = Field(None, description="SEC registration details")
    legal_structure: str = Field(..., description="Legal structure of the program")
    
    # Business Information
    business_description: str = Field(..., description="Description of issuer's business")
    financial_condition: Optional[str] = Field(None, description="Summary of financial condition")
    
    # Program Features
    note_types: List[str] = Field(..., description="Types of notes that can be issued under the program")
    distribution_methods: List[str] = Field(..., description="Permitted distribution methods")
    
    # Additional Parameters
    additional_features: Optional[Dict[str, Any]] = Field(default=None, description="Additional program features")


class BSPOutput(BaseModel):
    """
    Output model for BSP (Base Shelf Prospectus) document.
    
    TODO: Define comprehensive output structure for base shelf prospectus.
    """
    # Document Header
    document_title: str = Field(..., description="Title of the base shelf prospectus")
    cover_page: str = Field(..., description="Cover page content")
    
    # Issuer Information
    issuer_description: str = Field(..., description="Comprehensive issuer description")
    business_overview: str = Field(..., description="Overview of issuer's business")
    financial_information: str = Field(..., description="Financial information and condition")
    
    # Program Description
    program_overview: str = Field(..., description="Overview of the structured notes program")
    general_terms: str = Field(..., description="General terms and conditions")
    
    # Risk Factors
    risk_factors: str = Field(..., description="Comprehensive risk factors")
    
    # Legal Terms
    legal_terms: str = Field(..., description="Legal terms and conditions")
    
    # Regulatory Information
    regulatory_disclosures: str = Field(..., description="Required regulatory disclosures")
    
    # Use of Proceeds
    use_of_proceeds: str = Field(..., description="Description of use of proceeds")
    
    # Additional Sections
    additional_sections: Optional[Dict[str, str]] = Field(default=None, description="Additional document sections")
    
    # Document Metadata
    document_version: str = Field(default="1.0", description="Document version")
    generation_date: str = Field(..., description="Date when document was generated")


class BSPAgentDeps(BaseFinancialAgentDeps):
    """
    Dependencies specific to the BSP agent.
    
    TODO: Define BSP-specific dependencies.
    """
    input_data: BSPInput
    program_template: Optional[str] = None
    legal_template: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True