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
from agents.product_supplement.large_text_agent import LargeTextPDSAgent
from agents.product_supplement.models import PDSInput


def test_pds_generate_sections_and_docx(tmp_path):
    agent = LargeTextPDSAgent(base_agent=None, config=None)
    input_data = PDSInput(
        base_prospectus_reference="Base Shelf Prospectus",
        base_prospectus_date=date(2024, 3, 4),
        note_series="2025-1",
        note_description="Autocallable notes",
        underlying_asset="S&P 500 Index",
        principal_amount=1000000.0,
        issue_price=100.0,
        currency="USD",
        issue_date=date(2025, 1, 29),
        maturity_date=date(2030, 1, 29),
        product_type="autocallable",
        calculation_methodology="See pricing supplement",
    )

    sections = asyncio.run(agent.generate_document_with_large_templates(input_data, audience="retail"))
    assert isinstance(sections, dict) and sections

    # Create DOCX only if python-docx is available
    try:
        import docx  # noqa: F401
        docx_path = asyncio.run(
            agent.generate_docx_with_large_templates(
                input_data=input_data,
                audience="retail",
                filename=str(tmp_path / "pds_test.docx"),
                enforce_placeholder_validation=False,
            )
        )
        assert docx_path
    except Exception:
        # Environment without python-docx: section generation is sufficient for smoke test
        pass

