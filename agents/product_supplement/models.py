"""
Pydantic models for the PDS (Prospectus Supplement) agent.

TODO: Full implementation pending ISM agent completion.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date
from core.base_agent import BaseFinancialAgentDeps


class PDSInput(BaseModel):
    """
    Input model for PDS (Prospectus Supplement) document generation.
    
    TODO: Define comprehensive input parameters for prospectus supplement generation.
    """
    # Reference to Base Prospectus
    base_prospectus_reference: str = Field(..., description="Reference to the base shelf prospectus")
    base_prospectus_date: date = Field(..., description="Date of the base prospectus")
    
    # Specific Note Information
    note_series: str = Field(..., description="Series identifier for this note")
    note_description: str = Field(..., description="Specific description of this note")
    underlying_asset: str = Field(..., description="The underlying asset for this note")
    
    # Financial Terms
    principal_amount: float = Field(..., description="Principal amount of this issuance")
    issue_price: float = Field(..., description="Issue price as percentage of principal")
    currency: str = Field(..., description="Currency of the note")
    
    # Dates
    issue_date: date = Field(..., description="Date when the notes are issued")
    maturity_date: date = Field(..., description="Date when the notes mature")
    pricing_date: Optional[date] = Field(None, description="Pricing date for the notes")
    
    # Product Structure
    product_type: str = Field(..., description="Type of structured product")
    barrier_level: Optional[float] = Field(None, description="Barrier level if applicable")
    coupon_structure: Optional[str] = Field(None, description="Coupon payment structure")
    
    # Specific Terms
    calculation_methodology: str = Field(..., description="Methodology for calculating payments")
    underlying_performance: Optional[str] = Field(None, description="How underlying performance is measured")
    
    # Additional Parameters
    additional_terms: Optional[Dict[str, Any]] = Field(default=None, description="Additional specific terms")


class PDSOutput(BaseModel):
    """
    Output model for PDS (Prospectus Supplement) document.
    
    TODO: Define comprehensive output structure for prospectus supplement.
    """
    # Document Header
    document_title: str = Field(..., description="Title of the prospectus supplement")
    supplement_cover: str = Field(..., description="Cover page for the supplement")
    
    # Reference Information
    base_prospectus_reference: str = Field(..., description="Reference to base prospectus")
    supplement_purpose: str = Field(..., description="Purpose of this supplement")
    
    # Specific Note Terms
    specific_terms: str = Field(..., description="Specific terms for this note issuance")
    underlying_description: str = Field(..., description="Detailed description of underlying asset")
    
    # Calculation Details
    calculation_methodology: str = Field(..., description="Detailed calculation methodology")
    payment_schedule: str = Field(..., description="Payment schedule and dates")
    
    # Additional Risks
    additional_risks: str = Field(..., description="Risks specific to this note")
    
    # Pricing Information
    pricing_details: str = Field(..., description="Pricing and valuation details")
    
    # Market Information
    market_information: str = Field(..., description="Relevant market information")
    
    # Tax Considerations
    tax_implications: str = Field(..., description="Tax implications specific to this note")
    
    # Additional Sections
    additional_sections: Optional[Dict[str, str]] = Field(default=None, description="Additional sections")
    
    # Document Metadata
    document_version: str = Field(default="1.0", description="Document version")
    generation_date: str = Field(..., description="Date when document was generated")


class PDSAgentDeps(BaseFinancialAgentDeps):
    """
    Dependencies specific to the PDS agent.
    
    TODO: Define PDS-specific dependencies.
    """
    input_data: PDSInput
    base_prospectus_content: Optional[str] = None
    supplement_template: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True