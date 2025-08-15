"""
LLM-path smoke test for PDSAgent with mocked LLM and LightRAG.
"""

import asyncio
from datetime import date

from agents.product_supplement.agent import PDSAgent
from agents.product_supplement.models import PDSInput, PDSOutput


class _FakeRunResult:
    def __init__(self, data):
        self.data = data


class _FakeLightRAG:
    async def aquery(self, q, param=None):
        return f"MOCK_RAG_RESULTS for: {q}"


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
        additional_terms={"Listing": "Not listed"},
    )


def test_pds_llm_basic(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    agent = PDSAgent()

    async def _fake_init():
        return _FakeLightRAG()

    monkeypatch.setattr(agent, "initialize_lightrag", _fake_init)

    async def _fake_run(prompt, deps=None, message_history=None):
        output = PDSOutput(
            document_title="Prospectus Supplement - Series 2025-1",
            supplement_cover="Offering summary and references.",
            base_prospectus_reference="Base Prospectus dated March 4, 2024",
            supplement_purpose="To set out specific terms for Series 2025-1.",
            specific_terms="Principal, price, structure, currency.",
            underlying_description="S&P 500 Index overview.",
            calculation_methodology="Formulae and triggers, observation dates.",
            payment_schedule="Annual schedule and autocall observation dates.",
            additional_risks="Market, credit, liquidity, product-specific risks.",
            pricing_details="Issue price 100%, concessions, secondary market.",
            market_information="Relevant market context.",
            tax_implications="General tax treatment; consult advisor.",
            additional_sections=None,
            document_version="1.0",
            generation_date="2025-01-29",
        )
        return _FakeRunResult(output)

    monkeypatch.setattr(agent.agent, "run", _fake_run)

    prompt = agent._format_user_prompt(_sample_input())
    assert "retrieve_base_prospectus" in prompt
    assert "retrieve_note_specific_terms" in prompt
    assert "retrieve_regulatory_requirements" in prompt
    assert "retrieve_risk_factors" in prompt

    async def _run():
        return await agent.generate_document(_sample_input())

    result = asyncio.run(_run())

    assert isinstance(result, PDSOutput)
    assert result.document_title.startswith("Prospectus Supplement")
    assert result.document_version == "1.0"


