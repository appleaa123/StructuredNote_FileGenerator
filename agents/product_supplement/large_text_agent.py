"""
PDS Large Text Agent Implementation

This module provides the PDS-specific implementation of the large text agent
that extends the base mixin with PDS-specific template handling and field mapping.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from agents.core.large_text_mixin import LargeTextAgentMixin
from .models import PDSInput, PDSOutput
from .document_generator import PDSDocumentGenerator


class LargeTextPDSAgent(LargeTextAgentMixin[PDSInput, PDSOutput]):
    """PDS agent with large text template support"""
    
    def _get_agent_type(self) -> str:
        return "pds"
    
    def _get_template_module(self):
        from . import large_text_templates
        return large_text_templates
    
    def _get_output_model(self):
        return PDSOutput
    
    def _get_input_model(self):
        return PDSInput
    
    def _extract_agent_specific_variables(self, input_data: PDSInput) -> Dict[str, str]:
        """Extract PDS-specific variables from input data"""
        # Map input fields into the canonical placeholder names used by the
        # customized templates in large_text_templates.py. Do not change
        # placeholder names here.
        return {
            "Prospectus Supplement Date": datetime.now().strftime("%B %d, %Y"),
            "Base Shelf Prospectus Date": input_data.base_prospectus_date.strftime("%B %d, %Y"),
            "New Issue Date": input_data.issue_date.strftime("%B %d, %Y"),
            "Note Type": input_data.product_type if input_data.product_type else "Notes",
            "Underlying Asset Name": input_data.underlying_asset,
            "Specific Pricing Supplement": f"Pricing Supplement for {input_data.note_series} dated { (input_data.pricing_date or input_data.issue_date).strftime('%B %d, %Y') }",
            "Maturity Date": input_data.maturity_date.strftime("%B %d, %Y"),
            "Website for Note Information": "www.scotianotes.com",
            "Principal Amount": f"{input_data.principal_amount:,.0f}",
        }
    
    def _create_field_mapping(self, doc_dict: Dict[str, str], input_data: PDSInput) -> Dict[str, Any]:
        """Map PDS template sections to PDSOutput fields"""
        return {
            "document_title": self._create_document_title(input_data),
            "supplement_cover": self._extract_supplement_cover(doc_dict),
            "base_prospectus_reference": f"{input_data.base_prospectus_reference} dated {input_data.base_prospectus_date.strftime('%B %d, %Y')}",
            "supplement_purpose": self._extract_supplement_purpose(doc_dict),
            "specific_terms": self._extract_specific_terms(doc_dict),
            "underlying_description": self._extract_underlying_description(doc_dict),
            "calculation_methodology": self._extract_calculation_methodology(doc_dict, input_data),
            "payment_schedule": self._extract_payment_schedule(input_data),
            "additional_risks": self._extract_additional_risks(doc_dict),
            "pricing_details": self._extract_pricing_details(input_data),
            "market_information": self._extract_market_information(doc_dict),
            "tax_implications": self._extract_tax_implications(),
            "additional_sections": self._extract_additional_sections(doc_dict),
            "document_version": "1.0",
            "generation_date": datetime.now().strftime('%Y-%m-%d')
        }
    
    # PDS-specific extraction methods
    def _create_document_title(self, input_data: PDSInput) -> str:
        """Create document title in required format"""
        return f"Prospectus Supplement - {input_data.note_series}"
    
    def _extract_supplement_cover(self, doc_dict: Dict[str, str]) -> str:
        """Extract supplement cover content from offering details."""
        return self._extract_text_field(doc_dict, "offering_details", "Prospectus Supplement Cover Page")
    
    def _extract_base_prospectus_reference(self, doc_dict: Dict[str, str]) -> str:
        # Not parsed from templates; supplied directly by input_data in mapping.
        return ""
    
    def _extract_supplement_purpose(self, doc_dict: Dict[str, str]) -> str:
        """Use the first paragraph from prospectus structure as purpose."""
        content = self._extract_text_field(doc_dict, "prospectus_structure", "")
        return content.split("\n\n")[0].strip() if content else "This supplement provides specific information about the note issuance."
    
    def _extract_specific_terms(self, doc_dict: Dict[str, str]) -> str:
        """Combine offering details and nature/profile as specific terms."""
        offering = self._extract_text_field(doc_dict, "offering_details", "")
        nature = self._extract_text_field(doc_dict, "nature_and_profile", "")
        combined = "\n\n".join([s for s in [offering.strip(), nature.strip()] if s])
        return combined or "Specific terms are available in the full document."
    
    def _extract_underlying_description(self, doc_dict: Dict[str, str]) -> str:
        """Use the nature/profile section for underlying description."""
        content = self._extract_text_field(doc_dict, "nature_and_profile", "")
        return content or "Underlying asset description is available in the full document."
    
    def _extract_calculation_methodology(self, doc_dict: Dict[str, str], input_data: PDSInput) -> str:
        """Synthesize calculation methodology from available sections and inputs."""
        calc_agent = self._extract_text_field(doc_dict, "calculation_agent_determinations", "")
        if calc_agent:
            return calc_agent
        return input_data.calculation_methodology or "Calculation methodology is available in the full document."
    
    def _extract_payment_schedule(self, input_data: PDSInput) -> str:
        """Construct a basic payment schedule summary from dates."""
        return (
            f"Issue Date: {input_data.issue_date.strftime('%B %d, %Y')}. "
            f"Maturity Date: {input_data.maturity_date.strftime('%B %d, %Y')}. "
            f"Coupon Structure: {input_data.coupon_structure or 'N/A'}."
        )
    
    def _extract_additional_risks(self, doc_dict: Dict[str, str]) -> str:
        """Combine risk factor intro, principal at risk, and potential for loss."""
        parts = [
            self._extract_text_field(doc_dict, "risk_factor_introduction", ""),
            self._extract_text_field(doc_dict, "principal_at_risk_notes", ""),
            self._extract_text_field(doc_dict, "potential_for_loss", ""),
        ]
        combined = "\n\n".join([p.strip() for p in parts if p.strip()])
        return combined or "Additional risks are detailed in the full document."
    
    def _extract_pricing_details(self, input_data: PDSInput) -> str:
        """Summarize key pricing details from inputs."""
        return (
            f"Principal Amount: {input_data.principal_amount:,.2f} {input_data.currency}. "
            f"Issue Price: {input_data.issue_price:.2f}% of principal. "
            f"Pricing Date: {(input_data.pricing_date or input_data.issue_date).strftime('%B %d, %Y')}."
        )
    
    def _extract_market_information(self, doc_dict: Dict[str, str]) -> str:
        """Use website reference from prospectus structure where available."""
        return self._extract_text_field(doc_dict, "prospectus_structure", "Market information is available in the full document.")
    
    def _extract_tax_implications(self) -> str:
        """Static reference to prospectus for tax considerations."""
        return "Tax implications are described under Tax Considerations in the Prospectus and applicable pricing supplement."
    
    def _extract_additional_sections(self, doc_dict: Dict[str, str]) -> Dict[str, str]:
        """Extract additional sections"""
        additional_sections = {}
        
        # Include the raw canonical sections for downstream use
        for key in [
            "initial_disclaimers",
            "offering_details",
            "nature_and_profile",
            "prospectus_structure",
            "principal_at_risk_notes",
            "calculation_agent_determinations",
            "risk_factor_introduction",
            "potential_for_loss",
        ]:
            val = self._extract_text_field(doc_dict, key, "")
            if val:
                additional_sections[key] = val
        
        return additional_sections if additional_sections else None
    
    def _format_additional_terms(self, additional_terms: Optional[Dict[str, Any]]) -> str:
        """Format additional terms for template"""
        if not additional_terms:
            return "None"
        
        terms = []
        for key, value in additional_terms.items():
            terms.append(f"{key}: {value}")
        
        return "; ".join(terms) 

    async def generate_docx_with_large_templates(
        self,
        input_data: PDSInput,
        audience: str = "retail",
        custom_variables: Optional[dict] = None,
        title: Optional[str] = None,
        filename: Optional[str] = None,
        enforce_placeholder_validation: bool = True,
    ) -> str:
        """
        Convenience: render PDS large-text sections and create a DOCX with canonical ordering.

        Args:
            input_data: PDS input model
            audience: Target audience
            custom_variables: Additional substitution vars
            title: Optional top-level title
            filename: Optional output file name
            enforce_placeholder_validation: Validate unresolved placeholders
        Returns:
            Absolute path to the generated DOCX file
        """
        # Render sections using templates
        sections = await self.generate_document_with_large_templates(
            input_data=input_data,
            audience=audience,
            custom_variables=custom_variables,
        )

        # Validate placeholders if requested
        if enforce_placeholder_validation:
            unresolved = PDSDocumentGenerator.validate_no_unresolved_placeholders(sections)  # type: ignore[attr-defined]
            if unresolved:
                details = []
                for section_name, missing in unresolved.items():
                    details.append(f"- {section_name}: {', '.join(missing)}")
                raise ValueError(
                    "Unresolved placeholders detected in document sections.\n" + "\n".join(details)
                )

        # Create DOCX using generator convenience
        generator = PDSDocumentGenerator()
        if hasattr(generator, "create_docx_from_templates"):
            docx_path = generator.create_docx_from_templates(  # type: ignore[attr-defined]
                document_sections=sections,
                filename=filename,
                title=title or self._create_document_title(input_data),
                enforce_placeholder_validation=enforce_placeholder_validation,
            )
            # Additionally save JSON/TXT alongside DOCX for completeness
            try:
                pds_output = await self.generate_document_for_testing(
                    input_data, audience=audience, custom_variables=custom_variables
                )
                # Derive stem from docx filename
                import os
                stem = os.path.splitext(os.path.basename(docx_path))[0]
                generator.save_outputs(pds_output, input_data, filename_stem=stem, save_docx=False)
            except Exception:
                # Non-fatal if auxiliary saves fail
                pass
            return docx_path
        # Fallback to structured output path then docx
        pds_output = await self.generate_document_for_testing(input_data, audience=audience, custom_variables=custom_variables)
        return generator.create_docx_document(pds_output, input_data, filename)