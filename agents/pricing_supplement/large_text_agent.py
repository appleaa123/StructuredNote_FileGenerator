"""
PRS Large Text Agent Implementation

This module provides the PRS-specific implementation of the large text agent
that extends the base mixin with PRS-specific template handling and field mapping.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from agents.core.large_text_mixin import LargeTextAgentMixin
from .models import PRSInput, PRSOutput
from .document_generator import PRSDocumentGenerator
import os


class LargeTextPRSAgent(LargeTextAgentMixin[PRSInput, PRSOutput]):
    """PRS agent with large text template support"""
    
    def _get_agent_type(self) -> str:
        return "prs"
    
    def _get_template_module(self):
        from . import large_text_templates
        return large_text_templates
    
    def _get_output_model(self):
        return PRSOutput
    
    def _get_input_model(self):
        return PRSInput
    
    def _extract_agent_specific_variables(self, input_data: PRSInput) -> Dict[str, str]:
        """Extract PRS-specific variables from input data"""
        return {
            # ===== DOCUMENT HEADER =====
            "Document Date": datetime.now().strftime("%B %d, %Y"),
            "Generation Date": datetime.now().strftime('%Y-%m-%d'),
            
            # ===== REFERENCE DOCUMENTS =====
            "Base Prospectus Reference": input_data.base_prospectus_reference,
            "Supplement Reference": input_data.supplement_reference or "Not applicable",
            
            # ===== FINAL PRICING INFORMATION =====
            "Final Issue Price": f"{input_data.final_issue_price:.2f}",
            "Final Principal Amount": f"{input_data.final_principal_amount:,.0f}",
            "Currency": input_data.currency,
            
            # ===== FINAL DATES =====
            "Pricing Date": input_data.pricing_date.strftime("%B %d, %Y"),
            "Issue Date": input_data.issue_date.strftime("%B %d, %Y"),
            "Maturity Date": input_data.maturity_date.strftime("%B %d, %Y"),
            "Settlement Date": input_data.settlement_date.strftime("%B %d, %Y"),
            
            # ===== FINAL TERMS =====
            "Final Coupon Rate": f"{input_data.final_coupon_rate:.2f}" if input_data.final_coupon_rate else "Not applicable",
            "Final Barrier Level": f"{input_data.final_barrier_level:.2f}" if input_data.final_barrier_level else "Not applicable",
            "Underlying Initial Level": f"{input_data.underlying_initial_level:,.2f}" if input_data.underlying_initial_level else "To be determined",
            
            # ===== MARKET DATA =====
            "Underlying Price at Pricing": f"{input_data.underlying_price_at_pricing:,.2f}" if input_data.underlying_price_at_pricing else "To be determined",
            "Market Conditions": input_data.market_conditions or "Standard market conditions",
            "Volatility at Pricing": f"{input_data.volatility_at_pricing:.1f}" if input_data.volatility_at_pricing else "To be determined",
            
            # ===== DISTRIBUTION INFORMATION =====
            "Distribution Method": input_data.distribution_method,
            "Minimum Denomination": f"{input_data.minimum_denomination:,.0f}",
            
            # ===== FEES AND EXPENSES =====
            "Agent Discount": f"{input_data.agent_discount:.2f}" if input_data.agent_discount else "Not applicable",
            "Estimated Value": f"{input_data.estimated_value:.2f}" if input_data.estimated_value else "To be determined",
            
            # ===== ADDITIONAL FINAL TERMS =====
            "Additional Terms": self._format_additional_terms(input_data.additional_terms),
        }
    
    def _create_field_mapping(self, doc_dict: Dict[str, str], input_data: PRSInput) -> Dict[str, Any]:
        """Map PRS template sections to PRSOutput fields using canonical keys"""
        return {
            "document_title": self._create_document_title(input_data),
            "pricing_summary": self._extract_pricing_summary(doc_dict),
            "document_references": self._extract_document_references(doc_dict),
            "final_terms_summary": self._extract_final_terms_summary_from_input(input_data),
            "final_terms_table": self._extract_final_terms_table_from_input(input_data),
            "pricing_methodology": self._extract_pricing_methodology(doc_dict, input_data),
            "estimated_value_explanation": self._extract_estimated_value_explanation(doc_dict, input_data),
            "settlement_instructions": self._extract_settlement_instructions(doc_dict, input_data),
            "delivery_procedures": self._extract_delivery_procedures(doc_dict, input_data),
            "distribution_information": self._extract_distribution_information(input_data),
            "market_data_at_pricing": self._extract_market_data_at_pricing(doc_dict, input_data),
            "fees_and_expenses": self._extract_fees_and_expenses(input_data),
            "regulatory_notices": self._extract_regulatory_notices(doc_dict),
            "contact_information": self._create_contact_information(),
            "additional_sections": self._extract_additional_sections(doc_dict),
            "document_version": "1.0",
            "pricing_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "generation_date": datetime.now().strftime('%Y-%m-%d')
        }
    
    # PRS-specific extraction methods
    def _create_document_title(self, input_data: PRSInput) -> str:
        """Create document title in required format"""
        return f"Pricing Supplement - {input_data.pricing_date.strftime('%Y%m%d')}"
    
    def _extract_pricing_summary(self, doc_dict: Dict[str, str]) -> str:
        """Use offering overview as pricing summary"""
        return self._extract_text_field(doc_dict, "offering_overview", "Pricing Summary is available in the full document.")
    
    def _extract_document_references(self, doc_dict: Dict[str, str]) -> str:
        """Combine prospectus/capitalized terms and documents incorporated sections"""
        parts = [
            self._extract_text_field(doc_dict, "prospectus_and_capitalized_terms", ""),
            self._extract_text_field(doc_dict, "documents_incorporated_by_reference", ""),
        ]
        combined = "\n\n".join([p.strip() for p in parts if p.strip()])
        return combined or "Document references are available in the full document."
    
    def _extract_final_terms_summary_from_input(self, input_data: PRSInput) -> str:
        """Synthesize a concise final terms summary directly from input data"""
        parts = [
            f"Issue Price: {input_data.final_issue_price:.2f}% of principal",
            f"Principal Amount: {input_data.final_principal_amount:,.0f} {input_data.currency}",
            f"Pricing Date: {input_data.pricing_date.strftime('%B %d, %Y')}",
            f"Issue Date: {input_data.issue_date.strftime('%B %d, %Y')}",
            f"Maturity Date: {input_data.maturity_date.strftime('%B %d, %Y')}",
            f"Settlement Date: {input_data.settlement_date.strftime('%B %d, %Y')}",
        ]
        if input_data.final_coupon_rate is not None:
            parts.append(f"Coupon: {input_data.final_coupon_rate:.2f}%")
        if input_data.final_barrier_level is not None:
            parts.append(f"Barrier: {input_data.final_barrier_level:.2f}%")
        return "; ".join(parts)
    
    def _extract_final_terms_table_from_input(self, input_data: PRSInput) -> str:
        """Create a fixed-width table of final terms from input data"""
        table_lines = [
            "┌─────────────────────────────┬─────────────────────────────────┐",
            "│ Term                        │ Value                           │",
            "├─────────────────────────────┼─────────────────────────────────┤",
            f"│ Final Issue Price           │ {input_data.final_issue_price:.2f}% of principal       │",
            f"│ Final Principal Amount      │ {input_data.final_principal_amount:,.0f} {input_data.currency:<11} │",
            f"│ Pricing Date                │ {input_data.pricing_date.strftime('%B %d, %Y'):<29} │",
            f"│ Issue Date                  │ {input_data.issue_date.strftime('%B %d, %Y'):<29} │",
            f"│ Maturity Date               │ {input_data.maturity_date.strftime('%B %d, %Y'):<29} │",
            f"│ Settlement Date             │ {input_data.settlement_date.strftime('%B %d, %Y'):<29} │",
        ]
        if input_data.final_coupon_rate is not None:
            table_lines.append(f"│ Final Coupon Rate           │ {input_data.final_coupon_rate:.2f}%                       │")
        if input_data.final_barrier_level is not None:
            table_lines.append(f"│ Final Barrier Level         │ {input_data.final_barrier_level:.2f}%                      │")
        table_lines.append("└─────────────────────────────┴─────────────────────────────────┘")
        return "\n".join(table_lines)
    
    def _extract_pricing_methodology(self, doc_dict: Dict[str, str], input_data: PRSInput) -> str:
        """Synthesize pricing methodology from market conditions if available"""
        market = input_data.market_conditions or "prevailing market conditions"
        return f"Notes were priced based on {market}, issuer funding curve, and hedging costs at the pricing date."
    
    def _extract_estimated_value_explanation(self, doc_dict: Dict[str, str], input_data: PRSInput) -> str:
        """Explain estimated value using input if present"""
        if input_data.estimated_value is not None:
            return (
                f"The Bank's estimated value of the Notes on the Pricing Date was "
                f"{input_data.estimated_value:.2f}% of principal, which reflects the Bank's internal funding rate and "
                f"estimated hedging costs."
            )
        return "The Bank's estimated value will be disclosed in the final pricing supplement."
    
    def _extract_settlement_instructions(self, doc_dict: Dict[str, str], input_data: PRSInput) -> str:
        """Basic settlement instructions synthesized from dates"""
        return (
            f"Settlement on {input_data.settlement_date.strftime('%B %d, %Y')} through CDS. "
            f"Minimum denomination {int(input_data.minimum_denomination):,} {input_data.currency}."
        )
    
    def _extract_delivery_procedures(self, doc_dict: Dict[str, str], input_data: PRSInput) -> str:
        """Delivery and DRS procedures - generic text for PRS"""
        return "Delivery will be made in book-entry form through CDS participants to beneficial holders."
    
    def _extract_distribution_information(self, input_data: PRSInput) -> str:
        """Summarize distribution method and denomination"""
        return (
            f"Distribution Method: {input_data.distribution_method}. "
            f"Minimum Denomination: {int(input_data.minimum_denomination):,} {input_data.currency}."
        )
    
    def _extract_market_data_at_pricing(self, doc_dict: Dict[str, str], input_data: PRSInput) -> str:
        """Summarize key market data points from input"""
        parts = []
        if input_data.underlying_price_at_pricing is not None:
            parts.append(f"Underlying at pricing: {input_data.underlying_price_at_pricing:,.2f}")
        if input_data.volatility_at_pricing is not None:
            parts.append(f"Implied vol: {input_data.volatility_at_pricing:.1f}%")
        if input_data.market_conditions:
            parts.append(f"Conditions: {input_data.market_conditions}")
        return "; ".join(parts) if parts else "Market data at pricing is available in the full document."
    
    def _extract_fees_and_expenses(self, input_data: PRSInput) -> str:
        """Summarize fees and expenses from input"""
        if input_data.agent_discount is not None:
            return f"Agent discount/commission: {input_data.agent_discount:.2f}% of principal."
        return "Fees and expenses will be disclosed in the final pricing supplement."
    
    def _extract_regulatory_notices(self, doc_dict: Dict[str, str]) -> str:
        """Extract regulatory notices from regulatory_and_offering_disclaimers"""
        content = self._extract_text_field(doc_dict, "regulatory_and_offering_disclaimers", "")
        if not content:
            return "Regulatory notices are available in the full document."
        lines = content.split('\n')
        regulatory_section = []
        for line in lines:
            if "No securities regulatory authority" in line or "regulatory" in line.lower():
                regulatory_section.append(line.strip())
        return ' '.join(regulatory_section) if regulatory_section else content.strip().split('\n')[0]
    
    def _create_contact_information(self) -> str:
        """Create contact information"""
        return "• Phone: 1-866-416-7891\n• Email: structured.products@scotiabank.com\n• Website: www.scotiabank.com/structuredproducts"
    
    def _extract_additional_sections(self, doc_dict: Dict[str, str]) -> Dict[str, str]:
        """Extract a subset of canonical legal sections for reference"""
        additional_sections: Dict[str, str] = {}
        for key in [
            "regulatory_and_offering_disclaimers",
            "documents_incorporated_by_reference",
            "forward_looking_statements",
            "suitability_for_investment",
            "deferred_payment",
        ]:
            val = self._extract_text_field(doc_dict, key, "")
            if val and val != "Template not found.":
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
        input_data: PRSInput,
        audience: str = "retail",
        custom_variables: Optional[dict] = None,
        title: Optional[str] = None,
        filename: Optional[str] = None,
        enforce_placeholder_validation: bool = True,
    ) -> str:
        """
        Convenience: render PRS large-text sections and create a DOCX with canonical ordering.

        Args:
            input_data: PRS input model
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

        # Create DOCX using generator convenience with placeholder validation
        generator = PRSDocumentGenerator()
        docx_path = generator.create_docx_from_templates(
            document_sections=sections,
            filename=filename,
            title=title or self._create_document_title(input_data),
            enforce_placeholder_validation=enforce_placeholder_validation,
        )
        # Save JSON/TXT alongside DOCX using filename stem
        try:
            stem = os.path.splitext(os.path.basename(docx_path))[0]
            generator.save_sections(sections, filename_stem=stem, title=title)
        except Exception:
            pass
        return docx_path