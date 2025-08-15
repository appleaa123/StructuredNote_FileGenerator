# PRS Agent — Pricing Supplement

Generate final pricing supplements with definitive terms, pricing, settlement details, and references to the base documents.

## ✅ Current status
- Large‑text templates with canonical sections: implemented
- DOCX rendering from templates: implemented (JSON/TXT saved alongside DOCX using same filename stem)
- LLM path (agent tools + instructions): implemented
- Document generator: minimal (sufficient for template rendering)
- Knowledge base directory: available at `knowledge_bases/prs_kb/` (populate with your docs)

## Quick start

### A) Template‑driven sections + DOCX
```python
from datetime import date
from agents.prs import LargeTextPRSAgent, PRSInput

agent = LargeTextPRSAgent()
inp = PRSInput(
    base_prospectus_reference="Base Shelf Prospectus",
    final_issue_price=100.0,
    final_principal_amount=1_000_000,
    currency="USD",
    pricing_date=date(2025, 1, 29),
    issue_date=date(2025, 1, 31),
    maturity_date=date(2030, 1, 31),
    settlement_date=date(2025, 2, 5),
    distribution_method="retail",
    minimum_denomination=100,
)
sections = await agent.generate_document_with_large_templates(inp, audience="retail")
docx = await agent.generate_docx_with_large_templates(inp, audience="retail", enforce_placeholder_validation=True)
```

### B) Via GlobalAgent (multi‑agent orchestration)
See root `README.md` for `GlobalAgent.process_request(...)` with `agents=["bsp","pds","prs"]`.

## 🏗️ Architecture
- `PRSAgent`: LLM path tools/instructions
- `LargeTextPRSAgent`: template pipeline and DOCX writer
- `PRSInput` / `PRSOutput`: typed I/O
- `PRSDocumentGenerator`: minimal DOCX helper for canonical sections

### Knowledge Base
- **Location**: `knowledge_bases/prs_kb/`
- **Content**: Pricing templates, market data, settlement procedures
- **LightRAG Integration**: Intelligent content retrieval (mockable in tests)
- **Cross-Reference**: Access to base prospectus, supplements, and other agents

## 📋 Input model (PRSInput)

### Reference Documents
- `base_prospectus_reference`: Reference to the base shelf prospectus
- `supplement_reference`: Reference to prospectus supplement if applicable

### Final Pricing Information
- `final_issue_price`: Final issue price as percentage of principal
- `final_principal_amount`: Final principal amount of the issuance
- `currency`: Currency of the note

### Final Dates
- `pricing_date`: Final pricing date
- `issue_date`: Final issue date
- `maturity_date`: Final maturity date
- `settlement_date`: Settlement date

### Final Terms
- `final_coupon_rate`: Final coupon rate if applicable
- `final_barrier_level`: Final barrier level
- `underlying_initial_level`: Initial level of underlying

### Market Data
- `underlying_price_at_pricing`: Underlying price at pricing
- `market_conditions`: Market conditions at pricing
- `volatility_at_pricing`: Implied volatility at pricing

### Distribution Information
- `distribution_method`: Final distribution method
- `minimum_denomination`: Minimum denomination

### Fees and Expenses
- `agent_discount`: Agent discount or fee
- `estimated_value`: Estimated value of the notes

## 📄 Output model (PRSOutput)

### Document Sections
1. **Document Header**: Title and pricing summary
2. **Reference Information**: References to base prospectus and supplements
3. **Final Terms Summary**: Summary of all final terms
4. **Final Terms Table**: Table format of final terms
5. **Pricing Information**: How the notes were priced
6. **Estimated Value Explanation**: Explanation of estimated value
7. **Settlement Information**: Settlement instructions and procedures
8. **Delivery Procedures**: Delivery procedures
9. **Distribution Details**: Distribution details and restrictions
10. **Market Information**: Relevant market data at pricing time
11. **Fees and Expenses**: Detailed fees and expenses
12. **Regulatory Notices**: Final regulatory notices and disclaimers
13. **Contact Information**: Contact information for inquiries
14. **Additional Sections**: Additional document sections

## ⚙️ Configuration (PRSConfig)

### Document Generation Settings
- `max_document_length`: Maximum document length in words (default: 8000)
- `include_pricing_summary`: Include pricing summary (default: True)
- `include_market_data`: Include relevant market data (default: True)

### Pricing Settings
- `include_estimated_value`: Include estimated value calculation (default: True)
- `show_pricing_methodology`: Show pricing methodology (default: True)
- `include_fees_breakdown`: Include detailed fees breakdown (default: True)

### Format Settings
- `use_tabular_format`: Use tables for final terms (default: True)
- `include_settlement_details`: Include settlement details (default: True)

## 🚀 Usage (LLM path)

### Basic Usage
```python
import asyncio
from datetime import date
from agents.prs import PRSAgent, PRSInput

async def generate_pricing_supplement():
    # Initialize agent (LLM path)
    prs_agent = PRSAgent()
    
    # Create input data
    input_data = PRSInput(
        base_prospectus_reference="Global Structured Notes Program",
        supplement_reference="S&P 500 Autocallable Note Series 2024-1",
        final_issue_price=100.0,
        final_principal_amount=50000000.00,
        currency="USD",
        pricing_date=date(2024, 7, 30),
        issue_date=date(2024, 8, 1),
        maturity_date=date(2029, 8, 1),
        settlement_date=date(2024, 8, 6),
        final_coupon_rate=8.5,
        final_barrier_level=60.0,
        underlying_initial_level=4500.0,
        underlying_price_at_pricing=4520.0,
        market_conditions="stable",
        volatility_at_pricing=0.25,
        distribution_method="broker_dealer",
        minimum_denomination=1000.0,
        agent_discount=0.5,
        estimated_value=98.5
    )
    
    # Generate document
    result = await prs_agent.generate_document(input_data)
    return result
```

## 🧪 Testing

### Test Structure
- `tests/agents/prs/test_prs_basic.py`: Large-text path basic
- `tests/agents/prs/test_llm_basic.py`: LLM-path smoke test with mocked RAG/LLM
- `tests/agents/prs/test_prs_pricing.py`: Pricing methodology testing (planned)
- `tests/agents/prs/test_prs_settlement.py`: Settlement procedures testing (planned)

## 🎯 Use cases

### Investment Banks
- Final pricing documentation
- Settlement procedure documentation
- Market data integration

### Trading Desks
- Final terms documentation
- Pricing methodology documentation
- Settlement coordination

### Compliance Teams
- Final regulatory compliance
- Settlement procedure validation
- Market data verification

## 🔗 Related components

- **Core Framework**: `core/base_agent.py`
- **RAG Manager**: `core/rag_manager.py`
- **Configuration**: `core/config.py`
- **Base Prospectus**: `agents/bsp/` (for cross-referencing)
- **Prospectus Supplement**: `agents/pds/` (for cross-referencing)
- **Test Suite**: `tests/agents/prs/` (when implemented)

## 📦 Outputs
Saved to `generated_documents/prs/`:
- DOCX (formatted)
- JSON and TXT (canonical order), using the DOCX filename stem

## 📞 Next steps
- Populate `knowledge_bases/prs_kb/` with pricing/settlement docs
- Extend templates and mappings as needed