"""
Large Text Integration for BSP Agent

This module provides integration between the BSP agent and large text templates,
enabling the generation of comprehensive base shelf prospectus documents using
pre-defined templates with dynamic variable substitution.
"""

from typing import Optional, Dict, Any
import os
from datetime import date, datetime
from agents.base_shelf_prospectus.agent import BSPAgent
from agents.base_shelf_prospectus.models import BSPInput, BSPOutput
from agents.base_shelf_prospectus.large_text_templates import (
    get_template,
    create_complete_document_from_templates,
    customize_template
)
from agents.base_shelf_prospectus.document_generator import BSPDocumentGenerator


class LargeTextBSPAgent:
    """
    Enhanced BSP agent with large text template integration.
    
    This class provides a wrapper around the standard BSP agent that enables
    the use of large text templates for document generation, providing more
    consistent and professional output formatting.
    """
    
    def __init__(
        self, 
        base_agent: Optional[BSPAgent] = None, 
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the large text BSP agent.
        
        Args:
            base_agent: Base BSP agent instance
            config: Configuration dictionary
        """
        self.base_agent = base_agent or BSPAgent()
        self.config = config or {}
        self.template_variables = {}
        
        print("✅ LargeTextBSPAgent initialized with template integration")
    
    def _extract_agent_specific_variables(self, input_data: BSPInput) -> Dict[str, Any]:
        """
        Extract BSP-specific variables from input data for template substitution.
        
        Args:
            input_data: BSP input data
            
        Returns:
            Dictionary of variables for template substitution
        """
        # Calculate program duration
        program_duration = "3 years"  # Default shelf registration period
        
        # Generate program codes
        program_code = self._generate_program_code(input_data)
        shelf_registration_number = self._generate_shelf_registration_number(input_data)
        
        # Prepare variables for large text templates
        variables = {
            # Document header
            "Program Name": input_data.program_name,
            "Issuer": input_data.issuer,
            "Guarantor": input_data.guarantor or "Not applicable",
            "Shelf Amount": f"{input_data.shelf_amount:,.0f}",
            "Currency": input_data.currency,
            "Regulatory Jurisdiction": input_data.regulatory_jurisdiction,
            "Document Date": datetime.now().strftime("%B %d, %Y"),
            "Generation Date": datetime.now().strftime("%Y-%m-%d"),
            
            # Program details
            "Program Code": program_code,
            "Shelf Registration Number": shelf_registration_number,
            "Program Duration": program_duration,
            "Legal Structure": input_data.legal_structure,
            "SEC Registration": input_data.sec_registration or "Not applicable",
            
            # Business information
            "Business Description": input_data.business_description,
            "Financial Condition": input_data.financial_condition or "Available upon request",
            
            # Note types and distribution
            "Note Types": ", ".join(input_data.note_types),
            "Distribution Methods": ", ".join(input_data.distribution_methods),
            
            # Additional features
            "Additional Features": self._format_additional_features(input_data.additional_features),
            
            # Regulatory information
            "Regulatory Framework": f"Compliant with {input_data.regulatory_jurisdiction} regulations",
            "Compliance Status": "Fully compliant with all applicable regulations",
            
            # Contact information (defaults)
            "Contact Phone": "1-800-STRUCTURED",
            "Contact Email": "structuredproducts@issuer.com",
            "Contact Website": "www.issuer.com/structuredproducts",
            "Legal Department": "legal@issuer.com",
            "Compliance Department": "compliance@issuer.com",
            
            # Document metadata
            "Document Version": "1.0",
            "Document Type": "Base Shelf Prospectus",
            "Document Status": "Draft for Review",
            
            # Risk categories
            "Market Risk Level": "High",
            "Credit Risk Level": "Medium",
            "Liquidity Risk Level": "Medium",
            "Regulatory Risk Level": "Low",
            "Operational Risk Level": "Low",
            
            # Program capabilities
            "Maximum Note Size": f"{input_data.shelf_amount * 0.1:,.0f} {input_data.currency}",
            "Minimum Note Size": f"{input_data.shelf_amount * 0.001:,.0f} {input_data.currency}",
            "Shelf Period": "3 years from effective date",
            "Renewal Process": "Subject to regulatory approval and market conditions",
            
            # Distribution channels
            "Primary Distribution": "Institutional investors and qualified purchasers",
            "Secondary Distribution": "Broker-dealer networks and private placements",
            "Retail Distribution": "Limited to accredited investors and qualified purchasers",
            
            # Regulatory compliance
            "SEC Compliance": "Full compliance with Regulation S-K and other applicable regulations",
            "Ongoing Disclosures": "Quarterly and annual reports as required by applicable regulations",
            "Material Events": "Immediate disclosure of material events affecting the program",
            
            # Legal framework
            "Governing Law": "New York law",
            "Dispute Resolution": "Arbitration in accordance with FINRA rules",
            "Jurisdiction": "Federal and state courts in New York",
            
            # Use of proceeds
            "Primary Use": "General corporate purposes including funding structured products",
            "Secondary Use": "Hedging activities and risk management",
            "Tertiary Use": "Working capital and other business purposes",
            
            # Risk management
            "Risk Management Framework": "Comprehensive risk management policies and procedures",
            "Credit Risk Management": "Regular credit assessments and monitoring",
            "Market Risk Management": "Dynamic hedging strategies and position limits",
            "Operational Risk Management": "Robust internal controls and monitoring systems"
        }
        
        # Extend with BSP canonical placeholder coverage
        variables.update({
            "Date of Prospectus": variables.get("Document Date", datetime.now().strftime("%B %d, %Y")),
            "Dealer Agreement Date": variables.get("Document Date", datetime.now().strftime("%B %d, %Y")),
            "List of Investment Dealers": "To be determined and disclosed in applicable pricing supplement",
            "Directors Resident Outside of Canada": "None",
            "Bank Legal Counsel": "To be determined",
            "Dealers Legal Counsel": "To be determined",
            "Specific Designation of Notes": f"{input_data.program_name} Notes",
            "Aggregate Principal Amount": "See applicable product or pricing supplement",
            "Maturity Date": "See applicable product or pricing supplement",
            "Offering Price": "See applicable product or pricing supplement",
            "Variable Return Formula": "As described in the applicable product or pricing supplement",
            "Underlying Interests": "As described in the applicable product or pricing supplement",
            "Minimum Principal Repayment": "0% unless otherwise specified in the applicable supplement",
        })

        return variables
    
    def _generate_program_code(self, input_data: BSPInput) -> str:
        """Generate a unique program code based on input data"""
        import hashlib
        
        # Create a hash from program name and issuer
        program_string = f"{input_data.program_name}_{input_data.issuer}"
        hash_object = hashlib.md5(program_string.encode())
        hash_hex = hash_object.hexdigest()[:6].upper()
        
        return f"BSP-{hash_hex}"
    
    def _generate_shelf_registration_number(self, input_data: BSPInput) -> str:
        """Generate a shelf registration number"""
        import hashlib
        
        # Create a hash from program details
        registration_string = f"{input_data.program_name}_{input_data.issuer}_{input_data.shelf_amount}"
        hash_object = hashlib.md5(registration_string.encode())
        hash_hex = hash_object.hexdigest()[:8].upper()
        
        return f"SR-{hash_hex}"
    
    def _format_additional_features(self, additional_features: Optional[Dict[str, Any]]) -> str:
        """Format additional features for template use"""
        if not additional_features:
            return "Standard program features apply"
        
        features = []
        for key, value in additional_features.items():
            if isinstance(value, (list, tuple)):
                features.append(f"{key}: {', '.join(map(str, value))}")
            else:
                features.append(f"{key}: {value}")
        
        return "; ".join(features)
    
    async def generate_document_with_large_templates(
        self, 
        input_data: BSPInput,
        audience: str = "institutional",
        custom_variables: Optional[dict] = None
    ) -> dict:
        """
        Generate document using large text templates.
        
        Args:
            input_data: BSP input data
            audience: Target audience ("institutional", "retail", or "regulatory")
            custom_variables: Additional variables for template substitution
            
        Returns:
            Dictionary with generated document sections using large text templates
        """
        print(f"🚀 Generating BSP document with large text templates for {audience} audience...")
        
        # Extract template variables from input data
        template_variables = self._extract_agent_specific_variables(input_data)
        
        # Add custom variables if provided
        if custom_variables:
            template_variables.update(custom_variables)
        
        # Generate document using large text templates
        document = create_complete_document_from_templates(template_variables, audience)
        
        print("✅ BSP document generated successfully using large text templates!")
        return document

    # Backward/alternate naming alias expected by some orchestrators
    async def generate_document_with_large_text_templates(
        self,
        input_data: BSPInput,
        audience: str = "institutional",
        custom_variables: Optional[dict] = None
    ) -> dict:
        return await self.generate_document_with_large_templates(
            input_data=input_data,
            audience=audience,
            custom_variables=custom_variables,
        )
    
    async def generate_document(self, input_data: BSPInput) -> BSPOutput:
        """
        Generate document using the base BSP agent.
        
        Args:
            input_data: BSP input data
            
        Returns:
            Generated BSP document
        """
        return await self.base_agent.generate_document(input_data)

    async def generate_docx_with_large_templates(
        self,
        input_data: BSPInput,
        audience: str = "institutional",
        custom_variables: Optional[dict] = None,
        title: Optional[str] = None,
        filename: Optional[str] = None,
        enforce_placeholder_validation: bool = True,
    ) -> str:
        """
        Generate a DOCX file directly from large text templates.

        Args:
            input_data: BSP input data
            audience: Target audience (institutional|retail|regulatory)
            custom_variables: Additional variables to merge for substitution
            title: Optional document title for the DOCX (level 0 heading)
            filename: Optional output filename
            enforce_placeholder_validation: If True, error on unresolved placeholders

        Returns:
            Absolute path to the generated DOCX file
        """
        # Render canonical section text using templates
        sections = await self.generate_document_with_large_text_templates(
            input_data=input_data,
            audience=audience,
            custom_variables=custom_variables,
        )

        # Default title
        computed_title = title or f"{input_data.program_name} - Base Shelf Prospectus"

        generator = BSPDocumentGenerator()
        path = generator.create_docx_from_templates(
            document_sections=sections,
            filename=filename,
            title=computed_title,
            enforce_placeholder_validation=enforce_placeholder_validation,
        )
        # Save JSON/TXT alongside DOCX using filename stem
        try:
            stem = os.path.splitext(os.path.basename(path))[0]
            generator.save_sections(sections, filename_stem=stem, title=computed_title)
        except Exception:
            pass
        return path
    
    async def generate_customized_document(
        self, 
        input_data: BSPInput,
        audience_override: Optional[str] = None,
        config_override: Optional[Dict[str, Any]] = None
    ) -> BSPOutput:
        """
        Generate a document with custom audience or configuration.
        
        Args:
            input_data: Input parameters for document generation
            audience_override: Override the target audience
            config_override: Override the agent configuration
            
        Returns:
            Generated BSP document
        """
        # Create a copy of input data with audience override if provided
        if audience_override:
            input_dict = input_data.model_dump()
            # Note: BSP doesn't have target_audience field, so we'll handle this differently
            input_data = BSPInput(**input_dict)
        
        # Temporarily update configuration if override provided
        original_config = self.base_agent.bsp_config
        if config_override:
            # This would need to be implemented in the base agent
            pass
        
        try:
            result = await self.base_agent.generate_document(input_data)
            return result
        finally:
            # Restore original configuration
            if config_override:
                pass  # Restore original config
    
    def get_template_variables(self, input_data: BSPInput) -> Dict[str, Any]:
        """
        Get template variables for a given input.
        
        Args:
            input_data: BSP input data
            
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
            Customized template content
        """
        template = get_template(template_name, "institutional")
        return customize_template(template, variables)


def create_large_text_bsp_agent(
    knowledge_base_path: str = "knowledge_bases/bsp_kb/",
    model_name: str = "openai:gpt-4o-mini",
    config: Optional[Dict[str, Any]] = None
) -> LargeTextBSPAgent:
    """
    Create a large text BSP agent with the specified configuration.
    
    Args:
        knowledge_base_path: Path to BSP knowledge base
        model_name: LLM model to use
        config: Configuration dictionary
        
    Returns:
        Configured LargeTextBSPAgent instance
    """
    base_agent = BSPAgent(
        knowledge_base_path=knowledge_base_path,
        model_name=model_name
    )
    
    return LargeTextBSPAgent(base_agent=base_agent, config=config)



