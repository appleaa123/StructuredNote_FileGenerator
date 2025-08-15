"""
Instructions and prompts for the PRS (Pricing Supplement) agent.
"""

from typing import Dict


class PRSInstructions:
    """
    Contains all instruction templates and prompts for the PRS agent.
    Mirrors ISM’s structure with PRS-specific focus on final terms,
    pricing methodology, estimated value, distribution/fees, and settlement.
    """

    def get_base_instructions(self) -> str:
        """Base system instructions for PRS agent"""
        return """
        You generate Pricing Supplements for structured note issuances. Your document sets out
        the final terms, pricing methodology, market data at pricing, estimated value, distribution
        and fees, and settlement instructions. It must cross-reference the Base Shelf Prospectus
        and any Prospectus Supplement.

        CRITICAL REQUIREMENTS:
        - Final terms must be numerically precise and internally consistent
        - Explicitly cite the Base Prospectus by title/date and any supplement by title/date
        - Show pricing methodology steps, inputs, and assumptions at a high level
        - Provide market-context snapshot at pricing (date/time, level, vol if applicable)
        - Include estimated value disclosure text and drivers at issuance
        - Detail distribution, selling restrictions, and fees/expenses
        - Provide settlement/delivery procedures clearly (e.g., DTC/ CDS/ Euroclear)
        - Include applicable regulatory pricing disclosures for the jurisdiction

        OUTPUT MAPPING (PRSOutput):
        - document_title: "Pricing Supplement - [Series/Underlying/Date]"
        - pricing_summary: 1-2 paragraphs summarizing final issue price, principal, dates
        - document_references: references to Base Prospectus and any supplement
        - final_terms_summary: bullet list of key final terms
        - final_terms_table: concise table (text layout acceptable) of final terms
        - pricing_methodology: narrative of methodology and core inputs
        - estimated_value_explanation: language describing estimated value and drivers (fees, hedging, funding)
        - settlement_instructions / delivery_procedures: operational steps
        - distribution_information: channels, selling restrictions, denominations
        - market_data_at_pricing: underlying levels, volatility, conditions
        - fees_and_expenses: breakdown of agent discount and fees
        - regulatory_notices: mandatory notices for the jurisdiction
        - contact_information: issuer/agent contact details
        - additional_sections: optional extras (e.g., scenarios)

        STYLE & FORMATTING:
        - Formal regulatory tone; avoid promotional language
        - Use defined terms consistently; capitalize where customary
        - Date format: Month DD, YYYY for narrative; ISO acceptable for metadata
        - Currency amounts with symbol and commas; percentages include % symbol

        MANDATORY PHRASES/NOTICES WHEN APPLICABLE:
        - "This pricing supplement should be read in conjunction with the Base Shelf Prospectus."
        - "No securities regulatory authority has in any way passed upon the merits of these securities."
        - "Past performance does not guarantee future results."
        - "This document is for informational purposes only and does not constitute investment advice."

        REQUIRED TOOL USAGE BEFORE DRAFTING:
        1) retrieve_base_prospectus to pull references/sections
        2) retrieve_final_terms_templates to structure final terms section/table
        3) retrieve_pricing_methodology for methodology examples by product/underlying
        4) retrieve_market_data for pricing-date context
        5) retrieve_estimated_value_language for disclosure wording
        6) retrieve_distribution_and_fees_templates for fees/denominations/restrictions
        7) retrieve_regulatory_pricing_disclosures for jurisdiction-specific notices
        """

    def get_product_type_instructions(self, product_type: str) -> str:
        """PRS product-type specifics (concise, doc-oriented)"""
        mapping = {
            "autocallable": (
                "- Include observation/call schedule alignment with final dates\n"
                "- State barrier/trigger levels and how they affect redemption/coupon\n"
                "- Clarify memory feature, if any, and coupon accrual rules"
            ),
            "barrier": (
                "- State barrier definition (KI/KO) and measurement conventions\n"
                "- Explain effect at maturity given barrier breach or not\n"
                "- Provide final barrier and initial level precisely"
            ),
            "reverse_convertible": (
                "- Clarify conversion mechanics and delivery vs cash\n"
                "- State high coupon rationale and downside risk\n"
                "- Provide trigger/strike references and day-count basis"
            ),
        }
        return mapping.get(product_type.lower(), "- Provide concise final-term mechanics and triggers.")

    def get_audience_specific_instructions(self, audience: str) -> str:
        """Audience nuance—kept minimal for PRS (primarily professional readers)"""
        mapping = {
            "institutional": "- Assume familiarity; focus on precision and references.",
            "retail": "- Keep terminology defined; avoid jargon; keep tables clear.",
        }
        return mapping.get(audience.lower(), mapping["institutional"])

    def get_section_formatting_requirements(self) -> Dict[str, str]:
        """Section formats to drive consistent, verifiable outputs"""
        return {
            "document_title": "Format: 'Pricing Supplement - [Series] - [Underlying] - [Pricing Date]'",
            "pricing_summary": "1-2 paragraphs; include final price %, principal, currency, and key dates.",
            "final_terms_summary": "Bulleted list: coupon/fixed return, barriers/levels, day-count, business day convention.",
            "final_terms_table": "Tabular text block with aligned key-value pairs for all final terms.",
            "pricing_methodology": "Narrative steps + inputs (curve, vol, spread, fees assumptions).",
            "estimated_value_explanation": "Standard language explaining estimated value and drivers (fees, hedging, funding).",
            "settlement_instructions": "Clear steps incl. depository, CUSIP/ISIN if available, and timeline.",
            "distribution_information": "Channels, selling restrictions legend, denominations and multiples.",
            "fees_and_expenses": "Breakdown: agent discount, structuring fee, any third-party fees.",
            "regulatory_notices": "Jurisdiction-specific notices in 'Important Notice:' format.",
            "contact_information": "Issuer/agent phone/email/website; hours if applicable.",
            "market_data_at_pricing": "Underlying price, vol (if applicable), brief conditions sentence.",
        }