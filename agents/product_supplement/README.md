# PDS Agent — Prospectus Supplement

The PDS agent produces prospectus supplements for specific note issuances, cross‑referencing the Base Shelf Prospectus and detailing series‑specific terms, calculation methodology, schedules, and risks.

## ✅ Current status
- Large‑text templates with canonical sections: implemented
- DOCX rendering from templates: implemented (JSON/TXT saved alongside DOCX using same filename stem)
- LLM path (agent tools + instructions): implemented
- Document generator: minimal (sufficient for template rendering)
- Knowledge base directory: available at `knowledge_bases/pds_kb/` (populate with your docs)

## Quick start

### A) Template‑driven sections + DOCX
```python
from datetime import date
from agents.pds import LargeTextPDSAgent, PDSInput

agent = LargeTextPDSAgent()
inp = PDSInput(
    base_prospectus_reference="Base Shelf Prospectus",
    base_prospectus_date=date(2024, 3, 4),
    note_series="2025-1",
    note_description="Autocallable notes",
    underlying_asset="S&P 500 Index",
    principal_amount=1_000_000,
    issue_price=100.0,
    currency="USD",
    issue_date=date(2025, 1, 29),
    maturity_date=date(2030, 1, 29),
    product_type="autocallable",
    calculation_methodology="See pricing supplement",
)
sections = await agent.generate_document_with_large_templates(inp, audience="retail")
docx = await agent.generate_docx_with_large_templates(inp, audience="retail")
```

### B) Via GlobalAgent (multi‑agent orchestration)
See `README.md` root for `GlobalAgent.process_request(...)` usage with `agents=["bsp","pds","prs"]`.

## Models
- `PDSInput`: reference docs + series/terms (required fields include `base_prospectus_reference`, `base_prospectus_date`, `note_series`, `note_description`, `underlying_asset`, `principal_amount`, `issue_price`, `currency`, `issue_date`, `maturity_date`, `product_type`, `calculation_methodology`)
- `PDSOutput`: title, cover, references, specific terms, underlying, calc methodology, schedule, risks, pricing, market info, tax, additional sections, metadata

## Agent tools (LLM path)
- `retrieve_base_prospectus`
- `retrieve_note_specific_terms`
- `retrieve_regulatory_requirements`
- `retrieve_risk_factors`

## Customization
- Templates: `agents/pds/large_text_templates.py`
- Mapping: `agents/pds/large_text_agent.py`
- Config: `agents/pds/config.py`

## Outputs
Saved to `generated_documents/pds/`:
- DOCX (formatted)
- JSON and TXT (canonical order), using the DOCX filename stem

## Knowledge base
Place source PDFs/texts in `knowledge_bases/pds_kb/` and use RAG helpers from core to ingest.

## Testing
```bash
pytest tests/agents/pds/test_pds_basic.py -q
```