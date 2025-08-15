"""
Pydantic models for the ISM (Investor Summary) agent.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date
from core.base_agent import BaseFinancialAgentDeps


class ISMInput(BaseModel):
    """
    Input model for ISM (Investor Summary) document generation.
    Contains all necessary parameters for creating investor-friendly summaries.
    """
    # Core Product Information
    issuer: str = Field(..., description="The name of the issuing entity")
    product_name: str = Field(..., description="Name/title of the structured note")
    underlying_asset: str = Field(..., description="The underlying asset or reference")
    
    # Financial Terms
    currency: str = Field(..., description="Currency of the note (e.g., USD, EUR)")
    principal_amount: float = Field(..., description="Principal amount of the investment")
    issue_date: date = Field(..., description="Date when the notes are issued")
    maturity_date: date = Field(..., description="Date when the notes mature")
    
    # Product Structure
    product_type: str = Field(..., description="Type of structured product (e.g., autocallable, barrier)")
    barrier_level: Optional[float] = Field(None, description="Barrier level as percentage")
    coupon_rate: Optional[float] = Field(None, description="Coupon rate as percentage")
    protection_level: Optional[float] = Field(None, description="Capital protection level")
    
    # Autocallable Specific Features
    autocall_barrier: Optional[float] = Field(None, description="Autocall barrier level as percentage")
    observation_dates: Optional[List[str]] = Field(None, description="Observation dates for autocall feature")
    memory_feature: Optional[bool] = Field(None, description="Whether the product has memory feature")
    
    # Client Information
    target_audience: str = Field(default="retail_investors", description="Target investor type")
    risk_tolerance: str = Field(..., description="Risk tolerance level (low/medium/high)")
    investment_objective: str = Field(..., description="Primary investment objective")
    
    # Market and Risk Information
    market_outlook: Optional[str] = Field(None, description="Current market outlook for the underlying")
    volatility_level: Optional[str] = Field(None, description="Expected volatility level (low/medium/high)")
    
    # Additional Parameters
    regulatory_jurisdiction: str = Field(..., description="Regulatory jurisdiction")
    distribution_method: str = Field(..., description="How the product will be distributed")
    minimum_investment: Optional[float] = Field(None, description="Minimum investment amount")
    additional_features: Optional[Dict[str, Any]] = Field(default=None, description="Any additional product features")


class ISMOutput(BaseModel):
    """
    Output model for ISM (Investor Summary) document.
    Contains investor-friendly content sections optimized for clarity and accessibility.
    """
    # Document Header
    document_title: str = Field(..., description="EXACT FORMAT: '[Product Type] Investment Summary - [Underlying Asset]'. Must be under 80 characters. Example: 'Autocallable Investment Summary - S&P 500 Index'")
    executive_summary: str = Field(..., description="EXACTLY 3 paragraphs: (1) What this investment is, (2) How it works and key terms, (3) Target investors and risks. MUST END with 'This investment may not be suitable for all investors.'")
    
    # Product Overview Section  
    product_description: str = Field(..., description="Clear explanation using 'Investment Overview' as heading. Explain in simple terms without jargon. Use analogies where helpful. End with summary sentence starting 'In summary,'")
    how_it_works: str = Field(..., description="Step-by-step explanation of investment mechanism. Use numbered steps (1, 2, 3). Include specific examples with the actual investment amount. Avoid technical jargon.")
    key_features: List[str] = Field(..., description="EXACTLY 3 bullet points. Format: '• [Feature]: [Benefit] - [Impact explanation]'. Each bullet must be 15-25 words. Focus on investor benefits.")
    
    # Investment Information Section
    investment_details: str = Field(..., description="Include minimum investment, currency, dates in 'Month DD, YYYY' format, and investment period calculation. Use tables or bullet points for clarity.")
    potential_returns: str = Field(..., description="3 scenarios with actual dollar amounts: Best Case '[condition] could result in [X]% return ([dollar amount])', Expected Case, Worst Case. Calculate based on provided investment amount.")
    scenarios_analysis: str = Field(..., description="Use heading 'Potential Outcomes' instead of scenarios. Provide 3 detailed scenarios with market conditions and specific numerical outcomes. Include probability estimates.")
    
    # Risk Information Section
    risk_summary: str = Field(..., description="High-level overview in 2-3 sentences. Use plain language. Must mention that losses are possible. End with 'All investments carry risk of loss.'")
    key_risks: List[str] = Field(..., description="EXACTLY 4 risks. Each starts with 'Risk: [Name] - [explanation with example]'. Each explanation 15-30 words. Include market, credit, liquidity, and product-specific risks.")
    risk_mitigation: str = Field(..., description="Explain protective features and risk management. If no protections exist, clearly state this. Use positive but honest language.")
    risk_level_indicator: str = Field(..., description="EXACT FORMAT: 'Risk Level: [HIGH/MEDIUM/LOW] - [2-sentence explanation]'. First sentence: why this level. Second sentence: what this means for investor.")
    
    # Important Information Section
    important_dates: str = Field(..., description="List key dates in table format. Use 'Month DD, YYYY' format. Include issue date, observation dates, maturity date. Add explanations for each date's significance.")
    fees_and_charges: str = Field(..., description="List all costs in bullet points or table. Include percentages and dollar amounts. Be transparent about all fees. If no fees, clearly state 'No additional fees apply.'")
    liquidity_information: str = Field(..., description="Explain secondary market availability. Use clear language: 'You may/may not be able to sell before maturity.' Include any restrictions or conditions.")
    suitability_assessment: str = Field(..., description="Start with 'This investment is suitable for...' List 3-4 investor characteristics. End with 'This investment may not be suitable for all investors.'")
    
    # Regulatory and Legal Section
    regulatory_notices: str = Field(..., description="Include required disclosures using 'Important Notice:' format. Must include jurisdiction-specific mandatory text. Use accessible language while maintaining compliance.")
    tax_considerations: str = Field(..., description="Basic tax treatment explanation. Start with 'Tax implications may include...' Add disclaimer 'Consult your tax advisor for specific guidance.' Keep simple and general.")
    
    # Contact and Support Section
    contact_information: str = Field(..., description="Provide specific contact details: phone, email, website. Include hours of operation. Format as bullet points for clarity.")
    next_steps: str = Field(..., description="Clear action items for investors. Use numbered steps (1, 2, 3). Include timeline expectations. End with 'Please consult your financial advisor before investing.'")
    
    # Footer Information
    disclaimer: str = Field(..., description="MUST include exact phrases: 'Past performance does not guarantee future results', 'All investments carry risk of loss', 'Please consult your financial advisor before investing', 'This summary is for informational purposes only'. Format as single paragraph.")
    document_version: str = Field(default="1.0", description="Document version for tracking")
    generation_date: str = Field(..., description="Date when the document was generated")


class ISMAgentDeps(BaseFinancialAgentDeps):
    """
    Dependencies specific to the ISM agent.
    
    Extends the base dependencies with ISM-specific requirements
    for document generation and knowledge retrieval.
    """
    input_data: ISMInput
    document_template: Optional[str] = None
    regulatory_template: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
        from_attributes = True