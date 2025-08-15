#!/usr/bin/env python3
"""
Test ISM Agent with Actual Output Format

This script tests the ISM agent with the actual output format from large text templates.

Usage:
    python test_ism_actual_output.py
"""

import asyncio
import pytest
import json
from datetime import date
from pathlib import Path

from agents.investor_summary import ISMInput
from agents.investor_summary.large_text_integration import LargeTextISMAgent


def load_your_config():
    """Load your actual placeholders from config file."""
    config_file = "ism_test_config.json"
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


def analyze_document_output(document: dict, placeholders: dict):
    """Analyze the generated document output."""
    print("\n📊 Analyzing Generated Document Output")
    print("=" * 50)
    
    # Document statistics
    total_sections = len(document)
    total_words = sum(len(content.split()) for content in document.values())
    total_chars = sum(len(content) for content in document.values())
    
    print(f"📄 Document Statistics:")
    print(f"   Sections: {total_sections}")
    print(f"   Total Words: {total_words:,}")
    print(f"   Total Characters: {total_chars:,}")
    print(f"   Average Words per Section: {total_words/total_sections:.1f}")
    
    # Section breakdown
    print(f"\n📋 Section Breakdown:")
    for section, content in document.items():
        word_count = len(content.split())
        char_count = len(content)
        print(f"   {section}: {word_count} words, {char_count} characters")
    
    # Check for placeholder usage
    print(f"\n🔍 Checking for your placeholders in output:")
    placeholder_usage = {}
    for placeholder, value in placeholders.items():
        for section, content in document.items():
            if value in content or placeholder in content:
                placeholder_usage[placeholder] = section
                break
    
    if placeholder_usage:
        print("✅ Your placeholders found in output:")
        for placeholder, section in placeholder_usage.items():
            print(f"   {placeholder} -> {section}")
    else:
        print("⚠️  No placeholders found in output")
    
    # Content quality assessment
    quality_score = assess_content_quality(document)
    print(f"\n📈 Content Quality Score: {quality_score}/10")
    
    return {
        "total_sections": total_sections,
        "total_words": total_words,
        "total_chars": total_chars,
        "placeholder_usage": len(placeholder_usage),
        "quality_score": quality_score
    }


def assess_content_quality(document: dict) -> int:
    """Assess content quality on a scale of 1-10."""
    score = 10
    
    # Check for required sections
    required_sections = ["executive_summary", "key_terms", "disclaimer"]
    for section in required_sections:
        if section not in document:
            score -= 2
    
    # Check content length
    for section, content in document.items():
        word_count = len(content.split())
        if word_count < 50:  # Too short
            score -= 1
        elif word_count > 2000:  # Too long
            score -= 1
    
    # Check for regulatory compliance
    disclaimer_text = document.get("disclaimer", "").lower()
    required_phrases = [
        "risk",
        "investment",
        "regulatory",
        "disclaimer"
    ]
    
    for phrase in required_phrases:
        if phrase not in disclaimer_text:
            score -= 1
    
    return max(1, score)


@pytest.mark.asyncio
async def test_document_generation_with_your_data():
    """Test document generation with your actual data."""
    print("🧪 Testing ISM Agent Document Generation")
    print("=" * 60)
    
    # Load your configuration
    placeholders = load_your_config()
    if not placeholders:
        print("❌ Cannot proceed without configuration")
        return False
    
    print("✅ Your configuration loaded successfully!")
    print(f"📋 Company: {placeholders.get('YOUR_COMPANY_NAME', 'N/A')}")
    print(f"📞 Phone: {placeholders.get('YOUR_PHONE', 'N/A')}")
    print(f"🏛️  Regulator: {placeholders.get('YOUR_REGULATOR', 'N/A')}")
    print(f"📊 Asset: {placeholders.get('ASSET_DESCRIPTION', 'N/A')[:50]}...")
    print(f"📈 Volatility: {placeholders.get('VOLATILITY_RANGE', 'N/A')}")
    
    try:
        # Create agent
        agent = LargeTextISMAgent()
        
        # Create test input with your data
        input_data = create_test_input_with_your_data(placeholders)
        
        print(f"\n📋 Test Input Created:")
        print(f"   Product: {input_data.product_name}")
        print(f"   Issuer: {input_data.issuer}")
        print(f"   Underlying: {input_data.underlying_asset}")
        print(f"   Currency: {input_data.currency}")
        print(f"   Amount: {input_data.principal_amount:,.2f} {input_data.currency}")
        print(f"   Term: {((input_data.maturity_date - input_data.issue_date).days / 365.25):.1f} years")
        
        # Generate document
        print(f"\n🚀 Generating document...")
        document = await agent.generate_document_with_large_templates(
            input_data=input_data,
            audience="retail"
        )
        
        print("✅ Document generated successfully!")
        
        # Analyze the output
        analysis = analyze_document_output(document, placeholders)
        
        # Summary
        print(f"\n" + "=" * 60)
        print(f"📊 TEST SUMMARY")
        print(f"=" * 60)
        
        print(f"🎯 Quality Score: {analysis['quality_score']}/10")
        print(f"📄 Sections Generated: {analysis['total_sections']}")
        print(f"📝 Total Words: {analysis['total_words']:,}")
        print(f"🔧 Placeholders Used: {analysis['placeholder_usage']}")
        
        if analysis['quality_score'] >= 8:
            print(f"\n🎉 Excellent! Your ISM agent is working perfectly.")
        elif analysis['quality_score'] >= 6:
            print(f"\n✅ Good! Your ISM agent is working well.")
        else:
            print(f"\n⚠️  Your ISM agent needs some improvements.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in document generation: {e}")
        return False


@pytest.mark.asyncio
async def test_missing_data_handling():
    """Test how the agent handles missing data."""
    print(f"\n🤖 Testing Missing Data Handling")
    print("=" * 50)
    
    placeholders = load_your_config()
    if not placeholders:
        return False
    
    try:
        agent = LargeTextISMAgent()
        
        # Create input with missing data
        input_data = create_test_input_with_your_data(placeholders)
        incomplete_input = input_data.model_copy()
        incomplete_input.additional_features = None
        incomplete_input.market_outlook = None
        incomplete_input.volatility_level = None
        
        print("📝 Testing with incomplete data:")
        print("   ❌ additional_features")
        print("   ❌ market_outlook")
        print("   ❌ volatility_level")
        
        # Generate document with missing data
        document = await agent.generate_document_with_large_templates(
            input_data=incomplete_input,
            audience="retail"
        )
        
        print("✅ Document generated successfully with missing data!")
        print(f"   Generated {len(document)} sections")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling missing data: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 ISM Agent Test with Your Configuration")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Document generation
    if await test_document_generation_with_your_data():
        tests_passed += 1
    
    # Test 2: Missing data handling
    if await test_missing_data_handling():
        tests_passed += 1
    
    # Final summary
    print(f"\n" + "=" * 60)
    print(f"📊 FINAL TEST SUMMARY")
    print(f"=" * 60)
    
    print(f"🎯 Tests Passed: {tests_passed}/{total_tests}")
    print(f"📈 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print(f"\n🎉 All tests passed! Your ISM agent is ready for use.")
        print(f"\n💡 Next Steps:")
        print(f"   1. Test with different product types")
        print(f"   2. Customize templates further")
        print(f"   3. Integrate with your production system")
    else:
        print(f"\n⚠️  Some tests failed. Please check the errors above.")
    
    return tests_passed == total_tests


if __name__ == "__main__":
    asyncio.run(main()) 