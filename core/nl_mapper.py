"""
Natural Language to Placeholder Mapper

This module provides utilities to translate user natural language paragraphs
into structured placeholders suitable for agent inputs or custom variables
JSONs (e.g., BSP custom_vars format).

It leverages SmartAgentRouter's extraction to parse entities and then maps
them into domain-specific placeholder dictionaries.
"""

from typing import Dict, Any

from .router import smart_router


def extract_structured_from_nl(text: str) -> Dict[str, Any]:
    """
    Use SmartAgentRouter to extract structured fields from natural language.

    Returns a dict mirroring ExtractedInformation fields in core.router.
    """
    decision = smart_router.analyze_request(text)
    return decision.extracted_data or {}


def map_to_bsp_custom_vars(extracted: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map extracted fields to BSP custom_vars placeholder keys similar to
    inputs/custom_vars_series5.json.

    This provides best-effort mapping and leaves unknowns as sensible TBDs.
    """
    issuer = extracted.get("issuer")
    product_name = extracted.get("product_name")
    currency = extracted.get("currency")
    jurisdiction = extracted.get("regulatory_jurisdiction")
    principal_amount = extracted.get("principal_amount")
    product_type = extracted.get("product_type")
    underlying_asset = extracted.get("underlying_asset")
    issue_date = extracted.get("issue_date")
    maturity_date = extracted.get("maturity_date")
    barrier_level = extracted.get("barrier_level")

    # Currency code/symbol heuristics
    currency_code = currency or "CAD"
    currency_symbol = {
        "USD": "$",
        "CAD": "C$",
        "EUR": "€",
        "GBP": "£",
        "AUD": "A$",
        "JPY": "¥",
    }.get(currency_code, "$")

    # Note types string
    note_types = None
    if product_type:
        # Expand a single type into a friendly label
        mapping = {
            "autocallable": "Autocallable Plus Notes",
            "barrier": "Barrier Notes",
            "reverse convertible": "Reverse Convertible Notes",
        }
        note_types = mapping.get(product_type.lower(), product_type)

    # Barrier/buffer mapping
    barrier_pct = None
    try:
        if isinstance(barrier_level, str) and barrier_level.endswith("%"):
            barrier_pct = barrier_level
        elif barrier_level is not None:
            barrier_pct = f"{float(barrier_level):.2f}%"
    except Exception:
        barrier_pct = None

    # Program name fallback from product_name
    program_name = product_name or (underlying_asset and f"{underlying_asset} Notes Program") or "Structured Notes Program"

    # Compose mapping aligned to inputs/custom_vars_series5.json
    placeholders: Dict[str, Any] = {
        "Program Name": program_name,
        "Issuer": issuer or "TBD",
        "Guarantor": "Not applicable",
        "Shelf Amount": "TBD",
        "Currency": currency_code,
        "Regulatory Jurisdiction": jurisdiction or "Canada",
        "Business Description": "TBD",
        "Financial Condition": "Available upon request",
        "Note Types": note_types or "Autocallable Plus Notes",
        "Distribution Methods": "Through registered investment dealers",
        "Additional Features": "Standard program features apply",
        "Regulatory Framework": "Compliant with applicable securities regulations",
        "Contact Phone": "1-866-416-7891",
        "Contact Email": "structured.products@scotiabank.com",
        "Contact Website": "www.scotiabank.com/structuredproducts",
        "Document Version": "1.0",
        "Document Type": "Base Shelf Prospectus",
        "Document Status": "Draft for Review",
        "Date of Prospectus": extracted.get("pricing_date") or extracted.get("issue_date") or "TBD",
        "Dealer Agreement Date": extracted.get("issue_date") or "TBD",
        "Specific Designation of Notes": f"{program_name} Notes",
        "Aggregate Principal Amount": "TBD",
        "Maturity Date": maturity_date or "TBD",
        "Offering Price": f"{currency_symbol}100 per note",
        "Variable Return Formula": "As described in the applicable pricing supplement",
        "Underlying Interests": underlying_asset or "TBD",
        "Minimum Principal Repayment": "0% unless otherwise specified",
        "Prospectus Supplement Date": extracted.get("pricing_date") or "TBD",
        "Base Shelf Prospectus Date": extracted.get("base_prospectus_date") or "TBD",
        "New Issue Date": issue_date or "TBD",
        "Note Name": f"{program_name}",
        "Series Number": "TBD",
        "Currency Code": currency_code,
        "Currency Symbol": currency_symbol,
        "Maximum Offering Size in Dollars": "TBD",
        "Maximum Number of Notes": "TBD",
        "Asset Type": "Equity",
        "Target Asset(s) Name": underlying_asset or "TBD",
        "Autocall Level/Price details": "100.00% of the Initial Level/Price",
        "First Possible Call Date": "TBD",
        "Barrier/Buffer Level Percentage": barrier_pct or "TBD",
        "Initial Level/Price": "Initial Portfolio Price",
        "Downside Risk Description": "the holder will be fully exposed to the decline in the Portfolio",
        "Minimum Number of Notes": "50",
    }

    # Principal amount mapping (if available)
    if principal_amount:
        try:
            placeholders["Principal Amount"] = f"{int(float(principal_amount)):,}"
        except Exception:
            placeholders["Principal Amount"] = str(principal_amount)

    return placeholders


def map_to_agent_input(agent_type: str, extracted: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map extracted fields to an agent input dict skeleton.
    Only fills what is reasonably inferable; callers can merge/override.
    """
    agent_type = (agent_type or "").lower()
    if agent_type == "ism":
        return {
            "issuer": extracted.get("issuer"),
            "product_name": extracted.get("product_name") or extracted.get("note_description"),
            "underlying_asset": extracted.get("underlying_asset"),
            "currency": extracted.get("currency") or "CAD",
            "principal_amount": extracted.get("principal_amount") or 100000.0,
            "issue_date": extracted.get("issue_date"),
            "maturity_date": extracted.get("maturity_date"),
            "product_type": extracted.get("product_type") or "autocallable",
            "barrier_level": extracted.get("barrier_level"),
            "coupon_rate": extracted.get("final_coupon_rate"),
            "target_audience": extracted.get("target_audience") or "retail_investors",
            "risk_tolerance": "medium",
            "investment_objective": "income_and_growth",
            "regulatory_jurisdiction": extracted.get("regulatory_jurisdiction") or "Canada",
            "distribution_method": extracted.get("distribution_method") or "retail",
        }
    if agent_type == "bsp":
        return {
            "issuer": extracted.get("issuer"),
            "program_name": extracted.get("product_name") or "Structured Notes Program",
            "shelf_amount": 1_000_000_000.0,
            "currency": extracted.get("currency") or "CAD",
            "regulatory_jurisdiction": extracted.get("regulatory_jurisdiction") or "Canada",
            "sec_registration": None,
            "legal_structure": "corporation",
            "business_description": "TBD",
            "financial_condition": "Available upon request",
            "note_types": [ (extracted.get("product_type") or "autocallable") ],
            "distribution_methods": [ extracted.get("distribution_method") or "broker-dealer" ],
        }
    # Simplified defaults for PDS/PRS
    if agent_type == "pds":
        return {
            "base_prospectus_reference": extracted.get("base_prospectus_reference") or "Base Shelf Prospectus",
            "base_prospectus_date": extracted.get("base_prospectus_date"),
            "note_series": extracted.get("note_series") or "Series 1",
            "note_description": extracted.get("note_description") or extracted.get("product_name"),
            "underlying_asset": extracted.get("underlying_asset"),
            "principal_amount": extracted.get("principal_amount") or 1000000.0,
            "issue_price": 100.0,
            "currency": extracted.get("currency") or "CAD",
            "issue_date": extracted.get("issue_date"),
            "maturity_date": extracted.get("maturity_date"),
            "product_type": extracted.get("product_type") or "autocallable",
            "calculation_methodology": extracted.get("calculation_methodology") or "See supplement",
        }
    if agent_type == "prs":
        return {
            "base_prospectus_reference": extracted.get("base_prospectus_reference") or "Base Shelf Prospectus",
            "final_issue_price": 100.0,
            "final_principal_amount": extracted.get("principal_amount") or 1000000.0,
            "currency": extracted.get("currency") or "CAD",
            "pricing_date": extracted.get("pricing_date") or extracted.get("issue_date"),
            "issue_date": extracted.get("issue_date"),
            "maturity_date": extracted.get("maturity_date"),
            "settlement_date": extracted.get("settlement_date") or extracted.get("issue_date"),
            "distribution_method": extracted.get("distribution_method") or "broker-dealer",
            "minimum_denomination": 1000.0,
        }
    return {}


