"""
Basic tests for the PRS (Pricing Supplement) agent using large text templates.

This test avoids live LLM calls by exercising the LargeTextPRSAgent which
maps templates into the PRSOutput model.
"""

import asyncio
from datetime import date

from agents.pricing_supplement import LargeTextPRSAgent
from agents.pricing_supplement.models import PRSInput


def _sample_input() -> PRSInput:
    return PRSInput(
        base_prospectus_reference="The Bank of Nova Scotia Base Shelf Prospectus",
        supplement_reference="S&P 500 Autocallable Note Series 2025-1",
        final_issue_price=100.0,
        final_principal_amount=100_000_000.0,
        currency="USD",
        pricing_date=date(2025, 1, 29),
        issue_date=date(2025, 1, 31),
        maturity_date=date(2032, 1, 31),
        settlement_date=date(2025, 2, 4),
        final_coupon_rate=8.5,
        final_barrier_level=70.0,
        underlying_initial_level=4500.0,
        underlying_price_at_pricing=4485.0,
        market_conditions="Moderate volatility with stable rates",
        volatility_at_pricing=18.5,
        distribution_method="broker_dealer",
        minimum_denomination=1000.0,
        agent_discount=2.5,
        estimated_value=98.5,
        additional_terms={
            "Listing": "Not listed",
            "Settlement": "T+2 standard",
        },
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
    assert result.pricing_timestamp and isinstance(result.pricing_timestamp, str)


if __name__ == "__main__":
    # Allow running directly
    test_large_text_prs_generation()
    print("✅ PRS Large Text basic test passed")


