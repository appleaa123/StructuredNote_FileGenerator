"""
Large Text Integration for ISM Agent

This module provides the LargeTextISMAgent class that integrates large text templates
with the standard ISM agent for enhanced document generation capabilities.
"""

from typing import Dict, Any, Optional, List
import os
from datetime import datetime, date
from pathlib import Path

from .agent import ISMAgent
from .models import ISMInput, ISMOutput
from .document_generator import ISMDocumentGenerator
from .large_text_templates import (
    get_template, 
    create_complete_document_from_templates,
    customize_template,
    CUSTOM_PLACEHOLDERS
)


class LargeTextISMAgent:
    """
    Large Text ISM Agent that integrates large text templates with the standard ISM agent.
    
    This class provides enhanced document generation capabilities using pre-defined
    large text templates while maintaining compatibility with the standard ISM agent.
    """
    
    def __init__(self, base_agent: Optional[ISMAgent] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Large Text ISM Agent.
        
        Args:
            base_agent: Optional base ISM agent instance
            config: Optional configuration dictionary
        """
        self.base_agent = base_agent or ISMAgent(use_large_text_templates=True)
        self.config = config or {}
        self.agent_type = "ism"
        
        print("✅ Large Text ISM Agent initialized successfully")
    
    def _extract_agent_specific_variables(self, input_data: ISMInput) -> Dict[str, Any]:
        """
        Extract ISM-specific variables from input data for template substitution.
        
        Args:
            input_data: ISM input data
            
        Returns:
            Dictionary of variables for template substitution
        """
        variables = {}
        
        # Basic product information
        variables.update({
            "Note Title": input_data.product_name,
            "Maturity Date": input_data.maturity_date.strftime("%B %d, %Y"),
            "Document Date": datetime.now().strftime("%B %d, %Y"),
            "Pricing Supplement Number": f"PS-{datetime.now().strftime('%Y%m%d')}-001",
            "Pricing Supplement Date": input_data.issue_date.strftime("%B %d, %Y"),
            
            # Underlying asset information
            "Underlying Asset Type": "Index" if "index" in input_data.underlying_asset.lower() else "Reference Portfolio and Reference Companies",
            "Underlying Asset Description": self._generate_asset_description(input_data),
            "Underlying Asset Name": input_data.underlying_asset,
            "levels/prices": "levels" if "index" in input_data.underlying_asset.lower() else "prices",
            "Closing Level/Price Name": "Closing Index Level" if "index" in input_data.underlying_asset.lower() else "Closing Portfolio Price",
            "Autocall Level/Price Name": "Autocall Level" if "index" in input_data.underlying_asset.lower() else "Autocall Price",
            "Final Level/Price Name": "Final Index Level" if "index" in input_data.underlying_asset.lower() else "Final Portfolio Price",
            "Barrier Level/Price Name": "Barrier Level" if "index" in input_data.underlying_asset.lower() else "Barrier Price",
            "Initial Level/Price Name": "Initial Index Level" if "index" in input_data.underlying_asset.lower() else "Initial Portfolio Price",
            
            # Product terms
            "First Call Date": self._calculate_first_call_date(input_data),
            "Additional Return Percentage": "5.00%",  # Default value
            "Return Calculation Metric Name": "Index Return" if "index" in input_data.underlying_asset.lower() else "Price Return",
            # Use safe defaults if barrier_level is not provided
            "Contingent Principal Protection Percentage": f"{(100.0 - (input_data.barrier_level if input_data.barrier_level is not None else 70.0)):.2f}%",
            "Barrier Percentage": f"{(input_data.barrier_level if input_data.barrier_level is not None else 70.0):.2f}%",
            "Final Fixed Return": "59.50%",  # Default value
            
            # Autocall schedule
            "Valuation Date 1": self._calculate_valuation_date(input_data.issue_date, 1),
            "Valuation Date 2": self._calculate_valuation_date(input_data.issue_date, 2),
            "Valuation Date 3": self._calculate_valuation_date(input_data.issue_date, 3),
            "Valuation Date 4": self._calculate_valuation_date(input_data.issue_date, 4),
            "Valuation Date 5": self._calculate_valuation_date(input_data.issue_date, 5),
            "Valuation Date 6": self._calculate_valuation_date(input_data.issue_date, 6),
            "Fixed Return 1": "8.50%",
            "Fixed Return 2": "17.00%",
            "Fixed Return 3": "25.50%",
            "Fixed Return 4": "34.00%",
            "Fixed Return 5": "42.50%",
            "Fixed Return 6": "51.00%",
            "Autocall Level/Price Description": "100.00% of the Initial Index Level" if "index" in input_data.underlying_asset.lower() else "100.00% of the Initial Portfolio Price",
            
            # Product details
            "Fundserv Code": self._generate_fundserv_code(input_data),
            "Available Until Date": self._calculate_available_until_date(input_data.issue_date),
            "Issue Date": input_data.issue_date.strftime("%B %d, %Y"),
            "Term": f"{((input_data.maturity_date - input_data.issue_date).days / 365.25):.0f} years",
            "CUSIP Code": self._generate_cusip_code(input_data),
            "Initial Valuation Date": input_data.issue_date.strftime("%B %d, %Y"),
            "Final Valuation Date": input_data.maturity_date.strftime("%B %d, %Y"),
            
            # Fees and parties
            "Fees and Expenses Description": self._generate_fees_description(input_data),
            "Independent Agent Name": "Scotia Capital Inc.",
            "Asset Manager Name": input_data.issuer,
            
            # Company information
            "YOUR_COMPANY_NAME": input_data.issuer,
            "YOUR_REGULATOR": self._get_regulator_name(input_data.regulatory_jurisdiction),
            "YOUR_PHONE": "1-866-416-7891",
            "YOUR_EMAIL": "structured.products@scotiabank.com",
            "YOUR_WEBSITE": "www.gbm.scotiabank.com",
            
            # Legacy variables for backward compatibility
            "PRODUCT_NAME": input_data.product_name,
            "UNDERLYING_ASSET": input_data.underlying_asset,
            "DOLLAR_AMOUNT": f"${input_data.principal_amount:,.0f}",
            "PERCENTAGE": str(input_data.coupon_rate or 8.5),
            "TIME_PERIOD": f"{((input_data.maturity_date - input_data.issue_date).days / 365.25):.0f} years",
            "BARRIER_PERCENTAGE": str(input_data.barrier_level or 70),
            "ISSUER_NAME": input_data.issuer,
            "RISK_LEVEL": input_data.risk_tolerance.upper(),
            "REGULATOR": self._get_regulator_name(input_data.regulatory_jurisdiction),
            "COMPANY_NAME": input_data.issuer,
        })
        
        return variables
    
    def _generate_asset_description(self, input_data: ISMInput) -> str:
        """Generate asset description based on underlying asset"""
        if "index" in input_data.underlying_asset.lower():
            return f"The {input_data.underlying_asset}, a broad market index representing large-cap equities with strong historical performance and liquidity characteristics."
        else:
            return f"A basket of reference companies providing exposure to {input_data.underlying_asset} with diversified risk characteristics."
    
    def _calculate_first_call_date(self, input_data: ISMInput) -> str:
        """Calculate first call date (typically 1 year after issue)"""
        first_call = input_data.issue_date.replace(year=input_data.issue_date.year + 1)
        return first_call.strftime("%B %d, %Y")
    
    def _calculate_valuation_date(self, issue_date: date, year_offset: int) -> str:
        """Calculate valuation date for a given year offset"""
        valuation_date = issue_date.replace(year=issue_date.year + year_offset)
        return valuation_date.strftime("%B %d, %Y")
    
    def _generate_fundserv_code(self, input_data: ISMInput) -> str:
        """Generate Fundserv code based on product details"""
        year = input_data.issue_date.year
        product_type = input_data.product_type[:3].upper()
        return f"SSP{year}{product_type}01"
    
    def _generate_cusip_code(self, input_data: ISMInput) -> str:
        """Generate CUSIP code based on product details"""
        # Simplified CUSIP generation
        year = str(input_data.issue_date.year)[-2:]
        return f"06418Y{year}01"
    
    def _calculate_available_until_date(self, issue_date: date) -> str:
        """Calculate available until date (typically 1 week before issue)"""
        available_until = issue_date.replace(day=issue_date.day - 7)
        return available_until.strftime("%B %d, %Y")
    
    def _generate_fees_description(self, input_data: ISMInput) -> str:
        """Generate fees and expenses description"""
        if input_data.distribution_method == "retail":
            return "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 2.50% of the Principal Amount per Note. No additional independent agent fees apply for retail distribution."
        else:
            return "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 1.75% of the Principal Amount per Note for institutional distribution. Additional structuring fees of 0.50% apply."
    
    def _get_regulator_name(self, jurisdiction: str) -> str:
        """Get regulator name based on jurisdiction"""
        regulators = {
            "Canada": "Canadian Securities Regulators",
            "US": "Securities and Exchange Commission",
            "UK": "Financial Conduct Authority",
            "EU": "European Securities and Markets Authority"
        }
        return regulators.get(jurisdiction, "Local Securities Regulators")
    
    async def generate_document_with_large_templates(
        self, 
        input_data: ISMInput,
        audience: str = "retail",
        custom_variables: Optional[dict] = None
    ) -> dict:
        """
        Generate document using large text templates.
        
        Args:
            input_data: ISM input data
            audience: Target audience ("retail" or "institutional")
            custom_variables: Additional variables for template substitution
            
        Returns:
            Dictionary with generated document sections using large text templates
        """
        print(f"🚀 Generating document with large text templates for {audience} audience...")
        
        # Extract variables from input data
        template_variables = self._extract_agent_specific_variables(input_data)
        
        # Add custom variables if provided
        if custom_variables:
            template_variables.update(custom_variables)
        
        # Generate document using large text templates
        document = create_complete_document_from_templates(template_variables, audience)
        
        print("✅ Document generated successfully using large text templates!")
        return document
    
    async def generate_document(self, input_data: ISMInput) -> ISMOutput:
        """
        Generate document using the base ISM agent.
        
        Args:
            input_data: ISM input data
            
        Returns:
            ISMOutput with generated document
        """
        if self.base_agent:
            return await self.base_agent.generate_document(input_data)
        else:
            raise ValueError("Base agent not available")
    
    async def generate_docx_with_large_templates(
        self,
        input_data: ISMInput,
        audience: str = "retail",
        custom_variables: Optional[dict] = None,
        title: Optional[str] = None,
        filename: Optional[str] = None,
        enforce_placeholder_validation: bool = True,
    ) -> str:
        """
        Convenience: render ISM large-text sections and create a DOCX with canonical ordering.
        """
        sections = await self.generate_document_with_large_templates(
            input_data=input_data,
            audience=audience,
            custom_variables=custom_variables,
        )

        generator = ISMDocumentGenerator()
        docx_path = generator.create_docx_from_templates(
            document_sections=sections,
            filename=filename,
            title=title or f"Investment Summary - {input_data.product_name}",
            enforce_placeholder_validation=enforce_placeholder_validation,
        )

        # Also save JSON/TXT alongside DOCX using the DOCX filename stem
        try:
            stem = os.path.splitext(os.path.basename(docx_path))[0]
            generator.save_sections(sections, filename_stem=stem, title=title)
        except Exception:
            # Non-fatal
            pass

        return docx_path

    async def generate_customized_document(
        self, 
        input_data: ISMInput,
        audience_override: Optional[str] = None,
        config_override: Optional[Dict[str, Any]] = None
    ) -> ISMOutput:
        """
        Generate customized document with optional overrides.
        
        Args:
            input_data: ISM input data
            audience_override: Optional audience override
            config_override: Optional configuration override
            
        Returns:
            ISMOutput with generated document
        """
        if self.base_agent:
            return await self.base_agent.generate_customized_document(
                input_data, audience_override, config_override
            )
        else:
            raise ValueError("Base agent not available")
    
    def get_template_variables(self, input_data: ISMInput) -> Dict[str, Any]:
        """
        Get template variables for debugging and customization.
        
        Args:
            input_data: ISM input data
            
        Returns:
            Dictionary of template variables
        """
        return self._extract_agent_specific_variables(input_data)
    
    def customize_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Customize a specific template with variables.
        
        Args:
            template_name: Name of the template to customize
            variables: Variables for substitution
            
        Returns:
            Customized template string
        """
        template = get_template(template_name, "retail")
        return customize_template(template, variables)


# Convenience function for creating LargeTextISMAgent
def create_large_text_ism_agent(
    knowledge_base_path: str = "knowledge_bases/ism_kb/",
    model_name: str = "openai:gpt-4o-mini",
    config: Optional[Dict[str, Any]] = None
) -> LargeTextISMAgent:
    """
    Create a LargeTextISMAgent instance with default configuration.
    
    Args:
        knowledge_base_path: Path to knowledge base
        model_name: LLM model name
        config: Optional configuration dictionary
        
    Returns:
        LargeTextISMAgent instance
    """
    base_agent = ISMAgent(
        knowledge_base_path=knowledge_base_path,
        model_name=model_name,
        use_large_text_templates=True
    )
    
    return LargeTextISMAgent(base_agent, config) 