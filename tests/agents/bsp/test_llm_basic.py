"""
LLM-path smoke test for BSPAgent with mocked LLM and LightRAG.
"""

import asyncio
from datetime import date

from agents.base_shelf_prospectus.agent import BSPAgent
from agents.base_shelf_prospectus.models import BSPInput, BSPOutput


class _FakeRunResult:
    def __init__(self, data):
        self.data = data


class _FakeLightRAG:
    async def aquery(self, q, param=None):
        return f"MOCK_RAG_RESULTS for: {q}"


def _sample_input() -> BSPInput:
    return BSPInput(
        issuer="The Bank of Nova Scotia",
        guarantor=None,
        program_name="Global Structured Notes Program",
        shelf_amount=5_000_000_000.0,
        currency="USD",
        regulatory_jurisdiction="SEC",
        sec_registration="Form F-3",
        legal_structure="Bank issuer with senior unsecured obligations",
        business_description="Diversified financial services",
        financial_condition="Strong capital ratios; see MD&A",
        note_types=["autocallable", "barrier"],
        distribution_methods=["broker_dealer", "private_placement"],
        additional_features={"Renewal": "Subject to approval"},
    )


def test_bsp_llm_basic(monkeypatch):
    # Ensure OpenAI client initialization does not fail
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    agent = BSPAgent(use_large_text_templates=False)

    async def _fake_init():
        return _FakeLightRAG()

    monkeypatch.setattr(agent, "initialize_lightrag", _fake_init)

    async def _fake_run(prompt, deps=None, message_history=None):
        output = BSPOutput(
            document_title="Global Structured Notes Program - Base Shelf Prospectus",
            cover_page="Cover with program title, issuer, shelf amount, dates.",
            issuer_description="Comprehensive issuer business description.",
            business_overview="Segments, market position, strategy.",
            financial_information="Key financials and capital ratios.",
            program_overview="Program structure, note types, distribution methods.",
            general_terms="General terms and conditions across issuances.",
            risk_factors="Market, credit, liquidity, product-specific, regulatory, operational.",
            legal_terms="Legal structure, governing law, dispute resolution.",
            regulatory_disclosures="SEC disclosures and compliance notices.",
            use_of_proceeds="General corporate purposes; hedging; working capital.",
            additional_sections=None,
            document_version="1.0",
            generation_date="2025-01-29",
        )
        return _FakeRunResult(output)

    monkeypatch.setattr(agent.agent, "run", _fake_run)

    prompt = agent._format_user_prompt(_sample_input())
    assert "retrieve_legal_templates" in prompt
    assert "retrieve_regulatory_requirements" in prompt
    assert "retrieve_issuer_information" in prompt
    assert "retrieve_program_structure_examples" in prompt
    assert "retrieve_risk_factor_templates" in prompt
    assert "retrieve_legal_terms_examples" in prompt

    async def _run():
        return await agent.generate_document(_sample_input())

    result = asyncio.run(_run())

    assert isinstance(result, BSPOutput)
    assert result.document_title.endswith("Base Shelf Prospectus")
    assert result.document_version == "1.0"

