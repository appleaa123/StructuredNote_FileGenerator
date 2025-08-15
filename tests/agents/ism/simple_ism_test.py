#!/usr/bin/env python3
"""
Simple ISM Agent Test Script

This script provides a basic test of the ISM agent functionality
without requiring full agent initialization.

Usage:
    python simple_ism_test.py
"""

import asyncio
import json
from datetime import date
from pathlib import Path

from agents.investor_summary import ISMInput, ISMOutput
from agents.investor_summary.large_text_templates import CUSTOM_PLACEHOLDERS


def test_ism_input_creation():
    """Test creating ISM input data."""
    print("🔧 Testing ISM Input Creation")
    print("=" * 50)
    
    try:
        # Create sample input
        input_data = ISMInput(
            issuer="Your Financial Services Ltd",
            product_name="S&P 500 Autocallable Note Series 2025-1",
            underlying_asset="S&P 500 Index",
            currency="USD",
            principal_amount=100000.00,
            issue_date=date(2025, 1, 29),
            maturity_date=date(2032, 1, 29),
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
            regulatory_jurisdiction="US",
            distribution_method="broker_dealer_network",
            minimum_investment=10000.00,
            additional_features={
                "monthly_observation": True,
                "european_barrier": True,
                "memory_coupon": True,
                "autocall_dates": ["2026-01-29", "2027-01-29", "2028-01-29", "2029-01-29", "2030-01-29", "2031-01-29"]
            }
        )
        
        print("✅ ISM Input created successfully!")
        print(f"   Product: {input_data.product_name}")
        print(f"   Type: {input_data.product_type}")
        print(f"   Amount: {input_data.principal_amount:,.2f} {input_data.currency}")
        print(f"   Term: {((input_data.maturity_date - input_data.issue_date).days / 365.25):.1f} years")
        print(f"   Barrier Level: {input_data.barrier_level}%")
        print(f"   Coupon Rate: {input_data.coupon_rate}%")
        
        return input_data
        
    except Exception as e:
        print(f"❌ Error creating ISM input: {e}")
        return None


def test_placeholder_configuration():
    """Test placeholder configuration."""
    print("\n🔧 Testing Placeholder Configuration")
    print("=" * 50)
    
    # Your placeholders - customize these with your actual data
    your_placeholders = {
        # Company Information
        "YOUR_COMPANY_NAME": "Your Financial Services Ltd",
        "YOUR_REGULATOR": "FCA",  # or SEC, FINRA, etc.
        "YOUR_PHONE": "+44 20 1234 5678",
        "YOUR_EMAIL": "info@yourfinancial.com",
        "YOUR_WEBSITE": "www.yourfinancial.com",
        
        # Product Information
        "ISSUER_RATING": "A+",
        "ASSET_DESCRIPTION": "S&P 500 Index - A market-capitalization-weighted index of 500 large-cap US stocks",
        "SELECTION_RATIONALE": "Provides broad exposure to US equity markets with established track record",
        "MARKET_EXPOSURE": "US Large Cap Equity",
        "INDEX_SPONSOR": "S&P Dow Jones Indices",
        "TRADEMARK_NOTICE": "S&P 500® is a registered trademark of S&P Dow Jones Indices LLC",
        
        # Risk Information
        "VOLATILITY_RANGE": "15-25% annually",
        "STRESS_LOSS_PERCENTAGE": "40-60%",
        "BREACH_FREQUENCY": "Historically 15-20% of observations",
        "PROBABILITY_ESTIMATE": "Based on historical market data",
        "RISK_LEVEL": "MEDIUM",
        "OPTIMISTIC_PROBABILITY": "30%",
        "BASE_CASE_PROBABILITY": "50%",
        "STRESS_PROBABILITY": "20%",
    }
    
    print("✅ Placeholders configured:")
    for key, value in your_placeholders.items():
        print(f"   {key}: {value}")
    
    # Save to file
    config_file = "ism_test_config.json"
    with open(config_file, 'w') as f:
        json.dump(your_placeholders, f, indent=2)
    
    print(f"\n✅ Placeholders saved to: {config_file}")
    return your_placeholders


def test_template_access():
    """Test access to large text templates."""
    print("\n📝 Testing Template Access")
    print("=" * 50)
    
    try:
        # Import template functions
        from agents.investor_summary.large_text_integration import (
            create_complete_document_from_templates,
            test_your_templates
        )
        
        print("✅ Template functions imported successfully!")
        
        # Test template generation with sample data
        sample_data = {
            "Note Title": "S&P 500 Index Autocallable Notes - Series 2025",
            "Underlying Asset Name": "S&P 500 Index",
            "Asset Manager Name": "Your Financial Services Ltd",
            "Fundserv Code": "SSP2501",
            "CUSIP Code": "06418YJF6",
            "Independent Agent Name": "Your Capital Inc.",
            "YOUR_COMPANY_NAME": "Your Financial Services Ltd",
            "YOUR_PHONE": "+44 20 1234 5678",
            "Final Fixed Return": "59.50%",
            "Barrier Percentage": "70.00%",
        }
        
        print("📋 Testing template generation...")
        document = create_complete_document_from_templates(sample_data, "retail")
        
        print("✅ Template generation successful!")
        print(f"   Generated sections: {len(document)}")
        
        for section, content in document.items():
            word_count = len(content.split())
            print(f"   {section}: {word_count} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing templates: {e}")
        return False


def test_output_validation():
    """Test ISM output validation."""
    print("\n📄 Testing Output Validation")
    print("=" * 50)
    
    try:
        # Create sample output
        sample_output = ISMOutput(
            document_title="Autocallable Investment Summary - S&P 500 Index",
            executive_summary="This is a sample executive summary for testing purposes. It contains three paragraphs as required. This investment may not be suitable for all investors.",
            product_description="Investment Overview: This is a sample product description.",
            how_it_works="1. Step one\n2. Step two\n3. Step three",
            key_features=["• Feature 1: Benefit 1 - Impact 1", "• Feature 2: Benefit 2 - Impact 2", "• Feature 3: Benefit 3 - Impact 3"],
            investment_details="Investment details here",
            potential_returns="Potential returns analysis",
            scenarios_analysis="Scenarios analysis",
            risk_summary="Risk summary here",
            key_risks=["Risk: Market Risk - explanation", "Risk: Credit Risk - explanation", "Risk: Liquidity Risk - explanation", "Risk: Product Risk - explanation"],
            risk_mitigation="Risk mitigation strategies",
            risk_level_indicator="Risk Level: MEDIUM - This is a medium risk investment. Investors should understand the risks involved.",
            important_dates="Important dates table",
            fees_and_charges="Fees and charges information",
            liquidity_information="Liquidity information",
            suitability_assessment="This investment is suitable for...",
            regulatory_notices="Important Notice: Regulatory information",
            tax_considerations="Tax implications may include...",
            contact_information="Contact information",
            next_steps="1. Step one\n2. Step two\n3. Step three",
            disclaimer="Past performance does not guarantee future results. All investments carry risk of loss. Please consult your financial advisor before investing. This summary is for informational purposes only.",
            generation_date="2025-01-15"
        )
        
        print("✅ ISM Output validation successful!")
        print(f"   Title: {sample_output.document_title}")
        print(f"   Risk Level: {sample_output.risk_level_indicator}")
        print(f"   Key Features: {len(sample_output.key_features)}")
        print(f"   Key Risks: {len(sample_output.key_risks)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating output: {e}")
        return False


def run_simple_tests():
    """Run all simple tests."""
    print("🧪 Simple ISM Agent Test Suite")
    print("=" * 60)
    print("This script tests basic ISM functionality without full agent initialization.")
    print()
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Input creation
    input_data = test_ism_input_creation()
    if input_data:
        tests_passed += 1
    
    # Test 2: Placeholder configuration
    placeholders = test_placeholder_configuration()
    if placeholders:
        tests_passed += 1
    
    # Test 3: Template access
    if test_template_access():
        tests_passed += 1
    
    # Test 4: Output validation
    if test_output_validation():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SIMPLE TEST SUMMARY")
    print("=" * 60)
    
    print(f"🎯 Tests Passed: {tests_passed}/{total_tests}")
    print(f"📈 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 All tests passed! Your ISM agent setup is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Run python test_ism_agent_comprehensive.py for full testing")
        print("   2. Run python test_ism_interactive.py for interactive testing")
        print("   3. Customize your placeholders in the test scripts")
        print("   4. Test with your actual product data")
    else:
        print(f"\n⚠️  {total_tests - tests_passed} test(s) failed.")
        print("Please check the errors above and fix any issues.")
    
    return tests_passed == total_tests


if __name__ == "__main__":
    success = run_simple_tests()
    exit(0 if success else 1) 