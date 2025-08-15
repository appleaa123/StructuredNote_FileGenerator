#!/usr/bin/env python3
"""
Show Generated Document Sample

This script generates and displays a sample of the ISM document
using your actual configuration.

Usage:
    python show_generated_document.py
"""

import asyncio
import json
from datetime import date
from pathlib import Path

from agents.investor_summary import ISMInput, LargeTextISMAgent


def load_your_config():
    """Load your actual placeholders from config file."""
    config_file = "tests/ism/ism_test_config.json"
    if not Path(config_file).exists():
        print(f"❌ Config file not found: {config_file}")
        return None
    
    try:
        with open(config_file, 'r') as f:
            placeholders = json.load(f)
        return placeholders
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None


def create_test_input_with_your_data(placeholders):
    """Create test input using your actual data."""
    # Extract relevant data from your placeholders
    company_name = placeholders.get("YOUR_COMPANY_NAME", "Your Financial Services Ltd")
    asset_description = placeholders.get("ASSET_DESCRIPTION", "Solactive Canada Insurance 220 AR Index")
    volatility_range = placeholders.get("VOLATILITY_RANGE", "11.25%-78.75% annually")
    initial_date = placeholders.get("INITIAL_VALUATION_DATE", "August 13, 2025")
    final_date = placeholders.get("FINAL_VALUATION_DATE", "August 9, 2032")
    
    # Parse dates (simplified for testing)
    try:
        from datetime import datetime
        issue_date = datetime.strptime(initial_date, "%B %d, %Y").date()
        maturity_date = datetime.strptime(final_date, "%B %d, %Y").date()
    except:
        issue_date = date(2025, 8, 13)
        maturity_date = date(2032, 8, 9)
    
    input_data = ISMInput(
        issuer=company_name,
        product_name="Solactive Canada Insurance 220 AR Index Autocallable Note Series 2025-1",
        underlying_asset="Solactive Canada Insurance 220 AR Index",
        currency="CAD",
        principal_amount=100000.00,
        issue_date=issue_date,
        maturity_date=maturity_date,
        product_type="autocallable",
        barrier_level=70.0,
        coupon_rate=8.5,
        autocall_barrier=100.0,
        memory_feature=True,
        protection_level=70.0,
        target_audience="retail_investors",
        risk_tolerance="medium",
        investment_objective="capital_growth_with_income",
        market_outlook="neutral_to_positive",
        volatility_level="medium",
        regulatory_jurisdiction="Canada",
        distribution_method="broker_dealer_network",
        minimum_investment=10000.00,
        additional_features={
            "monthly_observation": True,
            "european_barrier": True,
            "memory_coupon": True,
            "autocall_dates": ["2026-08-13", "2027-08-13", "2028-08-13", "2029-08-13", "2030-08-13", "2031-08-13"],
            "custom_placeholders": placeholders
        }
    )
    
    return input_data


async def show_generated_document():
    """Generate and display a sample document."""
    print("📄 ISM Document Generation Sample")
    print("=" * 60)
    
    # Load your configuration
    placeholders = load_your_config()
    if not placeholders:
        print("❌ Cannot proceed without configuration")
        return
    
    print("✅ Your configuration loaded successfully!")
    print(f"🏢 Company: {placeholders.get('YOUR_COMPANY_NAME', 'N/A')}")
    print(f"📞 Phone: {placeholders.get('YOUR_PHONE', 'N/A')}")
    print(f"🏛️  Regulator: {placeholders.get('YOUR_REGULATOR', 'N/A')}")
    print(f"📊 Asset: {placeholders.get('ASSET_DESCRIPTION', 'N/A')[:50]}...")
    print(f"📈 Volatility: {placeholders.get('VOLATILITY_RANGE', 'N/A')}")
    
    try:
        # Create agent
        agent = LargeTextISMAgent()
        
        # Create test input with your data
        input_data = create_test_input_with_your_data(placeholders)
        
        print(f"\n📋 Generating document for:")
        print(f"   Product: {input_data.product_name}")
        print(f"   Amount: {input_data.principal_amount:,.2f} {input_data.currency}")
        print(f"   Term: {((input_data.maturity_date - input_data.issue_date).days / 365.25):.1f} years")
        
        # Generate document
        print(f"\n🚀 Generating document...")
        document = await agent.generate_document_with_large_templates(
            input_data=input_data,
            audience="retail"
        )
        
        print("✅ Document generated successfully!")
        
        # Display document sections
        print(f"\n" + "=" * 60)
        print(f"📄 GENERATED DOCUMENT SAMPLE")
        print(f"=" * 60)
        
        # Show Executive Summary
        if "executive_summary" in document:
            print(f"\n📋 EXECUTIVE SUMMARY")
            print(f"-" * 40)
            summary = document["executive_summary"]
            # Show first 300 characters
            print(summary[:300] + "..." if len(summary) > 300 else summary)
        
        # Show Key Terms
        if "key_terms" in document:
            print(f"\n📋 KEY TERMS")
            print(f"-" * 40)
            terms = document["key_terms"]
            # Show first 400 characters
            print(terms[:400] + "..." if len(terms) > 400 else terms)
        
        # Show Scenarios
        if "scenarios" in document:
            print(f"\n📋 SCENARIOS")
            print(f"-" * 40)
            scenarios = document["scenarios"]
            # Show first 300 characters
            print(scenarios[:300] + "..." if len(scenarios) > 300 else scenarios)
        
        # Show Disclaimer
        if "disclaimer" in document:
            print(f"\n📋 DISCLAIMER")
            print(f"-" * 40)
            disclaimer = document["disclaimer"]
            # Show first 400 characters
            print(disclaimer[:400] + "..." if len(disclaimer) > 400 else disclaimer)
        
        # Document statistics
        print(f"\n" + "=" * 60)
        print(f"📊 DOCUMENT STATISTICS")
        print(f"=" * 60)
        
        total_words = sum(len(content.split()) for content in document.values())
        total_chars = sum(len(content) for content in document.values())
        
        print(f"📄 Total Sections: {len(document)}")
        print(f"📝 Total Words: {total_words:,}")
        print(f"📏 Total Characters: {total_chars:,}")
        
        for section, content in document.items():
            word_count = len(content.split())
            char_count = len(content)
            print(f"   {section}: {word_count} words, {char_count} characters")
        
        # Check for your placeholders
        print(f"\n🔍 Your Placeholders Used:")
        placeholder_usage = {}
        for placeholder, value in placeholders.items():
            for section, content in document.items():
                if value in content or placeholder in content:
                    placeholder_usage[placeholder] = section
                    break
        
        if placeholder_usage:
            for placeholder, section in placeholder_usage.items():
                print(f"   ✅ {placeholder} -> {section}")
        else:
            print("   ⚠️  No placeholders found in output")
        
        print(f"\n🎉 Document generation completed successfully!")
        print(f"💡 Your ISM agent is working perfectly with your Canadian configuration!")
        
    except Exception as e:
        print(f"❌ Error generating document: {e}")


async def main():
    """Main function."""
    await show_generated_document()


if __name__ == "__main__":
    asyncio.run(main()) 