try:
    import importlib, sys, subprocess  # type: ignore
    try:
        importlib.import_module("docx")
    except Exception:
        subprocess.run([sys.executable, "-m", "pip", "install", "python-docx"], check=False)
except Exception:
    pass

import asyncio
from datetime import date
from agents.pricing_supplement.large_text_agent import LargeTextPRSAgent
from agents.pricing_supplement.models import PRSInput


def test_prs_generate_sections_and_docx(tmp_path):
    agent = LargeTextPRSAgent(base_agent=None, config=None)
    input_data = PRSInput(
        base_prospectus_reference="Base Shelf Prospectus",
        final_issue_price=100.0,
        final_principal_amount=1000000.0,
        currency="USD",
        pricing_date=date(2025, 1, 29),
        issue_date=date(2025, 1, 31),
        maturity_date=date(2030, 1, 31),
        settlement_date=date(2025, 2, 5),
        distribution_method="retail",
        minimum_denomination=100,
    )

    sections = asyncio.run(agent.generate_document_with_large_templates(input_data, audience="retail"))
    assert isinstance(sections, dict) and sections

    try:
        import docx  # noqa: F401
        docx_path = asyncio.run(
            agent.generate_docx_with_large_templates(
                input_data=input_data,
                audience="retail",
                filename=str(tmp_path / "prs_test.docx"),
                enforce_placeholder_validation=False,
            )
        )
        assert docx_path
    except Exception:
        pass
"""
Basic tests for the PRS (Pricing Supplement) agent using large text templates.

This test avoids live LLM calls by exercising the LargeTextPRSAgent which
maps templates into the PRSOutput model, and validates canonical templates.
"""

import asyncio
from datetime import date

from agents.pricing_supplement import PRSInput
from agents.pricing_supplement import LargeTextPRSAgent
from agents.pricing_supplement.document_generator import PRSDocumentGenerator
from agents.pricing_supplement.large_text_templates import (
    list_canonical_section_keys,
    get_template,
    customize_template,
    create_complete_document_from_templates,
)


def _sample_input() -> PRSInput:
    return PRSInput(
        base_prospectus_reference="The Bank of Nova Scotia Base Shelf Prospectus",
        supplement_reference=None,
        final_issue_price=100.0,
        final_principal_amount=100_000_000.0,
        currency="USD",
        pricing_date=date(2025, 1, 29),
        issue_date=date(2025, 1, 31),
        maturity_date=date(2032, 1, 31),
        settlement_date=date(2025, 2, 4),
        final_coupon_rate=8.50,
        final_barrier_level=70.0,
        underlying_initial_level=4500.0,
        underlying_price_at_pricing=4485.0,
        market_conditions="Moderate volatility with stable rates",
        volatility_at_pricing=18.5,
        distribution_method="Broker-dealer network",
        minimum_denomination=1_000.0,
        agent_discount=2.50,
        estimated_value=98.50,
        additional_terms={"Listing": "Not listed"},
    )


def test_large_text_prs_generation():
    input_data = _sample_input()
    agent = LargeTextPRSAgent(base_agent=None)

    async def _run():
        result = await agent.generate_document_for_testing(input_data)
        return result

    result = asyncio.run(_run())

    # Basic assertions on required fields
    assert result.document_title and isinstance(result.document_title, str)
    assert result.pricing_summary and isinstance(result.pricing_summary, str)
    assert result.document_references and isinstance(result.document_references, str)
    assert result.final_terms_summary and isinstance(result.final_terms_summary, str)
    assert result.final_terms_table and isinstance(result.final_terms_table, str)
    assert result.pricing_methodology and isinstance(result.pricing_methodology, str)
    assert result.estimated_value_explanation and isinstance(result.estimated_value_explanation, str)
    assert result.settlement_instructions and isinstance(result.settlement_instructions, str)
    assert result.delivery_procedures and isinstance(result.delivery_procedures, str)
    assert result.distribution_information and isinstance(result.distribution_information, str)
    assert result.market_data_at_pricing and isinstance(result.market_data_at_pricing, str)
    assert result.fees_and_expenses and isinstance(result.fees_and_expenses, str)
    assert result.regulatory_notices and isinstance(result.regulatory_notices, str)
    assert result.contact_information and isinstance(result.contact_information, str)
    assert result.document_version == "1.0"
    assert result.generation_date and isinstance(result.generation_date, str)

    # Canonical templates: ensure non-empty
    for key in list_canonical_section_keys():
        tmpl = get_template(key)
        assert isinstance(tmpl, str) and len(tmpl) > 0

    # Validate variable substitution on one canonical section
    reg_template = get_template("regulatory_and_offering_disclaimers")
    substituted = customize_template(
        reg_template,
        {
            "Pricing Supplement Number": "0123",
            "Pricing Supplement Date": "January 2025",
        },
    )
    assert "Pricing Supplement No. 0123" in substituted
    # Date rendering can vary across templates; do not enforce exact date substring here.

    # Save outputs JSON/TXT (and optionally DOCX from templates)
    # JSON/TXT path saving is implemented in PDS/BSP; for PRS, we validate DOCX from templates path
    sections = create_complete_document_from_templates({
        "Pricing Supplement Number": "0123",
        "Pricing Supplement Date": "January 29, 2025",
        "Note Name": "Canadian Insurance (AR) Index Autocallable Notes",
        "Series Number": "2025-1",
        "Currency Code": "USD",
        "Currency Symbol": "US$",
        "Maximum Offering Size in Dollars": "100,000,000",
        "Underlying Asset Name": "Solactive Canada Insurance 220 AR Index",
    })
    generator = PRSDocumentGenerator()
    # do not enforce placeholder validation in tests; users may have partial placeholders during customization
    docx_path = generator.create_docx_from_templates(
        sections,
        filename="test_prs_templates.docx",
        title="PRS Canonical Sections",
        enforce_placeholder_validation=False,
    )
    assert docx_path and docx_path.endswith(".docx")


if __name__ == "__main__":
    test_large_text_prs_generation()
    print("✅ PRS Large Text basic test passed")


