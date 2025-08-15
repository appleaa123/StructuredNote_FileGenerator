"""
LLM-path smoke test for PRSAgent with mocked LLM and LightRAG.

Verifies that generate_document(...) returns a structured PRSOutput without
calling external services, and that the prompt contains required tool names
to drive consistent behavior.
"""

import asyncio
from datetime import date

from agents.pricing_supplement.agent import PRSAgent
from agents.pricing_supplement.models import PRSInput, PRSOutput


class _FakeRunResult:
    def __init__(self, data):
        self.data = data


class _FakeLightRAG:
    async def aquery(self, q, param=None):  # pragma: no cover - smoke stub
        return f"MOCK_RAG_RESULTS for: {q}"


def _sample_input() -> PRSInput:
    return PRSInput(
        base_prospectus_reference="Global Structured Notes Program",
        supplement_reference="Autocallable Series 2025-1",
        final_issue_price=100.0,
        final_principal_amount=1_000_000.0,
        currency="USD",
        pricing_date=date(2025, 1, 29),
        issue_date=date(2025, 1, 31),
        maturity_date=date(2032, 1, 31),
        settlement_date=date(2025, 2, 4),
        final_coupon_rate=8.5,
        final_barrier_level=70.0,
        underlying_initial_level=4500.0,
        underlying_price_at_pricing=4485.0,
        market_conditions="Moderate volatility",
        volatility_at_pricing=19.2,
        distribution_method="broker_dealer",
        minimum_denomination=1000.0,
        agent_discount=2.0,
        estimated_value=98.7,
        additional_terms={"Listing": "Not listed"},
    )


def test_prs_llm_basic(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    agent = PRSAgent()

    # Monkeypatch LightRAG init to avoid IO
    async def _fake_init():
        return _FakeLightRAG()

    monkeypatch.setattr(agent, "initialize_lightrag", _fake_init)

    # Monkeypatch agent.run to avoid any LLM calls
    async def _fake_run(prompt, deps=None, message_history=None):
        # Return a minimal, consistent PRSOutput
        output = PRSOutput(
            document_title="Pricing Supplement - Series 2025-1 - S&P 500 - January 29, 2025",
            pricing_summary="Final issue price 100% of principal; settlement T+2.",
            document_references="Base Prospectus dated March 4, 2024; Supplement as referenced.",
            final_terms_summary="• Coupon: 8.5% pa; • Barrier: 70%; • Currency: USD",
            final_terms_table="Issue Price: 100% | Principal: $1,000,000 | Denom: $1,000",
            pricing_methodology="Priced using issuer curves, vol surfaces, and fees.",
            estimated_value_explanation="Estimated value reflects fees and hedging/funding costs.",
            settlement_instructions="DTC delivery; see CUSIP when assigned.",
            delivery_procedures="Book-entry via DTC participants.",
            distribution_information="Broker-dealer; selling restrictions apply; $1,000 and multiples of $1,000.",
            market_data_at_pricing="Underlying ~4485; vol ~19.2%; stable conditions.",
            fees_and_expenses="Agent discount 2.0%; structuring fees as applicable.",
            regulatory_notices="Important Notice: Past performance does not guarantee future results.",
            contact_information="Issuer Desk: +1-800-000-0000; email@example.com",
            additional_sections=None,
            document_version="1.0",
            generation_date="2025-01-29",
            pricing_timestamp="2025-01-29T16:00:00Z",
        )
        return _FakeRunResult(output)

    monkeypatch.setattr(agent.agent, "run", _fake_run)

    # Prompt contains tool markers (ensures instruction-driven tool usage)
    prompt = agent._format_user_prompt(_sample_input())
    assert "retrieve_base_prospectus" in prompt
    assert "retrieve_pricing_methodology" in prompt
    assert "retrieve_market_data" in prompt
    assert "retrieve_regulatory_pricing_disclosures" in prompt

    async def _run():
        return await agent.generate_document(_sample_input())

    result = asyncio.run(_run())

    assert isinstance(result, PRSOutput)
    assert result.document_title.startswith("Pricing Supplement")
    assert result.document_version == "1.0"


