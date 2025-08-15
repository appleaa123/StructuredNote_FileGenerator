"""
Pydantic models for the PRS (Pricing Supplement) agent.

TODO: Full implementation pending ISM agent completion.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from core.base_agent import BaseFinancialAgentDeps


class PRSInput(BaseModel):
    """
    Input model for PRS (Pricing Supplement) document generation.
    
    TODO: Define comprehensive input parameters for pricing supplement generation.
    """
    # Reference Documents
    base_prospectus_reference: str = Field(..., description="Reference to the base shelf prospectus")
    supplement_reference: Optional[str] = Field(None, description="Reference to prospectus supplement if applicable")
    
    # Final Pricing Information
    final_issue_price: float = Field(..., description="Final issue price as percentage of principal")
    final_principal_amount: float = Field(..., description="Final principal amount of the issuance")
    currency: str = Field(..., description="Currency of the note")
    
    # Final Dates
    pricing_date: date = Field(..., description="Final pricing date")
    issue_date: date = Field(..., description="Final issue date")
    maturity_date: date = Field(..., description="Final maturity date")
    settlement_date: date = Field(..., description="Settlement date")
    
    # Final Terms
    final_coupon_rate: Optional[float] = Field(None, description="Final coupon rate if applicable")
    final_barrier_level: Optional[float] = Field(None, description="Final barrier level")
    underlying_initial_level: Optional[float] = Field(None, description="Initial level of underlying")
    
    # Market Data
    underlying_price_at_pricing: Optional[float] = Field(None, description="Underlying price at pricing")
    market_conditions: Optional[str] = Field(None, description="Market conditions at pricing")
    volatility_at_pricing: Optional[float] = Field(None, description="Implied volatility at pricing")
    
    # Distribution Information
    distribution_method: str = Field(..., description="Final distribution method")
    minimum_denomination: float = Field(..., description="Minimum denomination")
    
    # Fees and Expenses
    agent_discount: Optional[float] = Field(None, description="Agent discount or fee")
    estimated_value: Optional[float] = Field(None, description="Estimated value of the notes")
    
    # Additional Final Terms
    additional_terms: Optional[Dict[str, Any]] = Field(default=None, description="Additional final terms")


class PRSOutput(BaseModel):
    """
    Output model for PRS (Pricing Supplement) document.
    
    TODO: Define comprehensive output structure for pricing supplement.
    """
    # Document Header
    document_title: str = Field(..., description="Title of the pricing supplement")
    pricing_summary: str = Field(..., description="Summary of final pricing")
    
    # Reference Information
    document_references: str = Field(..., description="References to base prospectus and supplements")
    
    # Final Terms Summary
    final_terms_summary: str = Field(..., description="Summary of all final terms")
    final_terms_table: str = Field(..., description="Table format of final terms")
    
    # Pricing Information
    pricing_methodology: str = Field(..., description="How the notes were priced")
    estimated_value_explanation: str = Field(..., description="Explanation of estimated value")
    
    # Settlement Information
    settlement_instructions: str = Field(..., description="Settlement instructions and procedures")
    delivery_procedures: str = Field(..., description="Delivery procedures")
    
    # Distribution Details
    distribution_information: str = Field(..., description="Distribution details and restrictions")
    
    # Market Information
    market_data_at_pricing: str = Field(..., description="Relevant market data at pricing time")
    
    # Fees and Expenses
    fees_and_expenses: str = Field(..., description="Detailed fees and expenses")
    
    # Regulatory Notices
    regulatory_notices: str = Field(..., description="Final regulatory notices and disclaimers")
    
    # Contact Information
    contact_information: str = Field(..., description="Contact information for inquiries")
    
    # Additional Sections
    additional_sections: Optional[Dict[str, str]] = Field(default=None, description="Additional sections")
    
    # Document Metadata
    document_version: str = Field(default="1.0", description="Document version")
    generation_date: str = Field(..., description="Date when document was generated")
    pricing_timestamp: str = Field(..., description="Timestamp of pricing")


class PRSAgentDeps(BaseFinancialAgentDeps):
    """
    Dependencies specific to the PRS agent.
    
    TODO: Define PRS-specific dependencies.
    """
    input_data: PRSInput
    base_prospectus_content: Optional[str] = None
    supplement_content: Optional[str] = None
    pricing_template: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True