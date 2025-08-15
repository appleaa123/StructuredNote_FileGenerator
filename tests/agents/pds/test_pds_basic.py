"""
Basic tests for the PDS (Prospectus Supplement) agent using large text templates.

This test avoids live LLM calls by exercising the LargeTextPDSAgent which
maps templates into the PDSOutput model.
"""

import asyncio
from datetime import date

from agents.product_supplement import PDSInput
from agents.product_supplement import LargeTextPDSAgent
from agents.product_supplement.document_generator import PDSDocumentGenerator
from agents.product_supplement.large_text_templates import list_canonical_section_keys, get_template, customize_template


def _sample_input() -> PDSInput:
    return PDSInput(
        base_prospectus_reference="The Bank of Nova Scotia Base Shelf Prospectus",
        base_prospectus_date=date(2024, 3, 4),
        note_series="Series 2025-1",
        note_description="Autocallable Notes linked to S&P 500 Index",
        underlying_asset="S&P 500 Index",
        principal_amount=100_000_000.0,
        issue_price=100.0,
        currency="USD",
        issue_date=date(2025, 1, 29),
        maturity_date=date(2032, 1, 29),
        pricing_date=date(2025, 1, 29),
        product_type="autocallable",
        barrier_level=70.0,
        coupon_structure="Annual fixed return with autocall schedule",
        calculation_methodology="Performance-linked returns with autocall features",
        underlying_performance="Closing Index Level vs Initial Index Level",
        additional_terms={
            "Listing": "Not listed",
            "Secondary Market": "Reasonable efforts for daily liquidity",
        },
    )


def test_large_text_pds_generation():
    input_data = _sample_input()
    agent = LargeTextPDSAgent(base_agent=None)

    async def _run():
        result = await agent.generate_document_for_testing(input_data)
        return result

    result = asyncio.run(_run())

    # Basic assertions on required fields
    assert result.document_title and isinstance(result.document_title, str)
    assert result.supplement_cover and isinstance(result.supplement_cover, str)
    assert result.base_prospectus_reference and isinstance(result.base_prospectus_reference, str)
    assert result.specific_terms and isinstance(result.specific_terms, str)
    assert result.calculation_methodology and isinstance(result.calculation_methodology, str)
    assert result.payment_schedule and isinstance(result.payment_schedule, str)
    assert result.additional_risks and isinstance(result.additional_risks, str)
    assert result.pricing_details and isinstance(result.pricing_details, str)
    assert result.market_information and isinstance(result.market_information, str)
    assert result.tax_implications and isinstance(result.tax_implications, str)
    assert result.document_version == "1.0"
    assert result.generation_date and isinstance(result.generation_date, str)

    # Canonical templates: ensure non-empty
    for key in list_canonical_section_keys():
        tmpl = get_template(key)
        assert isinstance(tmpl, str) and len(tmpl) > 0

    # Validate variable substitution on one canonical section
    offering_template = get_template("offering_details")
    substituted = customize_template(offering_template, {
        "Base Shelf Prospectus Date": input_data.base_prospectus_date.strftime('%B %d, %Y'),
        "New Issue Date": input_data.issue_date.strftime('%B %d, %Y'),
        "Note Type": input_data.product_type,
    })
    assert "New Issue" in substituted and input_data.product_type in substituted

    # Save outputs JSON/TXT/DOCX
    generator = PDSDocumentGenerator()
    paths = generator.save_outputs(result, input_data, filename_stem="test_pds_output", save_docx=False)
    assert "json_path" in paths and "txt_path" in paths


if __name__ == "__main__":
    # Allow running directly
    test_large_text_pds_generation()
    print("✅ PDS Large Text basic test passed")


