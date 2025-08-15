#!/usr/bin/env python3
"""
ISM Agent Test Setup Script

This script helps you configure your placeholders and test the ISM agent.
It will guide you through the setup process and run initial tests.

Usage:
    python setup_ism_test.py
"""

import asyncio
import json
import os
from datetime import date
from pathlib import Path

from agents.investor_summary import ISMInput
from agents.investor_summary.large_text_integration import LargeTextISMAgent


def setup_environment():
    """Set up the testing environment."""
    print("🔧 Setting up ISM Agent Test Environment")
    print("=" * 60)
    
    # Check if virtual environment is activated
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Warning: Virtual environment not detected")
        print("   It's recommended to run this in a virtual environment")
        print("   Run: source ism_test_env/bin/activate")
        print()
    
    # Check for required files
    required_files = [
        "agents/ism/agent.py",
        "agents/ism/large_text_integration.py",
        "agents/ism/large_text_templates.py",
        "agents/ism/models.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease ensure all ISM agent files are present.")
        return False
    
    print("✅ Environment setup complete!")
    return True


def configure_placeholders():
    """Configure your custom placeholders."""
    print("\n🔧 Configuring Your Placeholders")
    print("=" * 60)
    
    print("Please provide your company and product information.")
    print("Press Enter to use default values or type your information.")
    print()
    
    placeholders = {}
    
    # Company Information
    print("🏢 Company Information:")
    placeholders["YOUR_COMPANY_NAME"] = input("Company Name (default: Your Financial Services Ltd): ").strip() or "Your Financial Services Ltd"
    placeholders["YOUR_REGULATOR"] = input("Regulator (FCA/SEC/FINRA) (default: FCA): ").strip() or "FCA"
    placeholders["YOUR_PHONE"] = input("Phone (default: +44 20 1234 5678): ").strip() or "+44 20 1234 5678"
    placeholders["YOUR_EMAIL"] = input("Email (default: info@yourfinancial.com): ").strip() or "info@yourfinancial.com"
    placeholders["YOUR_WEBSITE"] = input("Website (default: www.yourfinancial.com): ").strip() or "www.yourfinancial.com"
    
    print("\n📊 Product Information:")
    placeholders["ISSUER_RATING"] = input("Issuer Rating (default: A+): ").strip() or "A+"
    placeholders["ASSET_DESCRIPTION"] = input("Asset Description (default: S&P 500 Index description): ").strip() or "S&P 500 Index - A market-capitalization-weighted index of 500 large-cap US stocks"
    placeholders["SELECTION_RATIONALE"] = input("Selection Rationale (default: Broad US equity exposure): ").strip() or "Provides broad exposure to US equity markets with established track record"
    placeholders["MARKET_EXPOSURE"] = input("Market Exposure (default: US Large Cap Equity): ").strip() or "US Large Cap Equity"
    placeholders["INDEX_SPONSOR"] = input("Index Sponsor (default: S&P Dow Jones Indices): ").strip() or "S&P Dow Jones Indices"
    placeholders["TRADEMARK_NOTICE"] = input("Trademark Notice (default: S&P 500® trademark): ").strip() or "S&P 500® is a registered trademark of S&P Dow Jones Indices LLC"
    
    print("\n⚠️  Risk Information:")
    placeholders["VOLATILITY_RANGE"] = input("Volatility Range (default: 15-25% annually): ").strip() or "15-25% annually"
    placeholders["STRESS_LOSS_PERCENTAGE"] = input("Stress Loss Percentage (default: 40-60%): ").strip() or "40-60%"
    placeholders["BREACH_FREQUENCY"] = input("Barrier Breach Frequency (default: 15-20% of observations): ").strip() or "Historically 15-20% of observations"
    placeholders["PROBABILITY_ESTIMATE"] = input("Probability Estimate Basis (default: Historical market data): ").strip() or "Based on historical market data"
    placeholders["RISK_LEVEL"] = input("Risk Level (HIGH/MEDIUM/LOW) (default: MEDIUM): ").strip() or "MEDIUM"
    placeholders["OPTIMISTIC_PROBABILITY"] = input("Optimistic Probability (default: 30%): ").strip() or "30%"
    placeholders["BASE_CASE_PROBABILITY"] = input("Base Case Probability (default: 50%): ").strip() or "50%"
    placeholders["STRESS_PROBABILITY"] = input("Stress Probability (default: 20%): ").strip() or "20%"
    
    # Save placeholders to file
    config_file = "ism_test_config.json"
    with open(config_file, 'w') as f:
        json.dump(placeholders, f, indent=2)
    
    print(f"\n✅ Placeholders saved to: {config_file}")
    return placeholders


def create_test_input():
    """Create test input data."""
    print("\n📋 Creating Test Input Data")
    print("=" * 60)
    
    print("Creating sample autocallable note for testing...")
    
    input_data = ISMInput(
        # Core Product Information
        issuer="Your Financial Services Ltd",
        product_name="S&P 500 Autocallable Note Series 2025-1",
        underlying_asset="S&P 500 Index",
        
        # Financial Terms
        currency="USD",
        principal_amount=100000.00,
        issue_date=date(2025, 1, 29),
        maturity_date=date(2032, 1, 29),
        
        # Product Structure
        product_type="autocallable",
        barrier_level=70.0,
        coupon_rate=8.5,
        autocall_barrier=100.0,
        memory_feature=True,
        protection_level=70.0,
        
        # Client Information
        target_audience="retail_investors",
        risk_tolerance="medium",
        investment_objective="capital_growth_with_income",
        
        # Market Information
        market_outlook="neutral_to_positive",
        volatility_level="medium",
        
        # Additional Parameters
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
    
    print("✅ Test input created:")
    print(f"   Product: {input_data.product_name}")
    print(f"   Type: {input_data.product_type}")
    print(f"   Amount: {input_data.principal_amount:,.2f} {input_data.currency}")
    print(f"   Term: {((input_data.maturity_date - input_data.issue_date).days / 365.25):.1f} years")
    
    return input_data


async def run_quick_test(placeholders):
    """Run a quick test to verify everything works."""
    print("\n🧪 Running Quick Test")
    print("=" * 60)
    
    try:
        # Create agent
        agent = LargeTextISMAgent()
        
        # Create test input
        input_data = create_test_input()
        
        # Add custom placeholders
        existing_features = input_data.additional_features or {}
        input_data.additional_features = {
            **existing_features,
            "custom_placeholders": placeholders
        }
        
        print("⏳ Generating test document...")
        result = await agent.generate_document_with_large_templates(
            input_data=input_data,
            audience="retail"
        )
        
        print("✅ Test successful!")
        print(f"📄 Generated: {result.document_title}")
        print(f"📋 Executive Summary: {len(result.executive_summary)} characters")
        print(f"✨ Key Features: {len(result.key_features)} items")
        print(f"⚠️  Key Risks: {len(result.key_risks)} items")
        print(f"🎯 Risk Level: {result.risk_level_indicator}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your API keys are set")
        print("   2. Ensure all dependencies are installed")
        print("   3. Verify the ISM agent files are present")
        return False


def print_next_steps():
    """Print next steps for testing."""
    print("\n📋 Next Steps for Testing")
    print("=" * 60)
    
    print("🎯 Your ISM agent is now configured and ready for testing!")
    print()
    
    print("📝 Available Test Scripts:")
    print("   1. python test_ism_agent_comprehensive.py")
    print("      - Full comprehensive test suite")
    print("      - Tests multiple scenarios")
    print("      - Generates detailed reports")
    print()
    print("   2. python test_ism_interactive.py")
    print("      - Interactive testing")
    print("      - Tests missing data handling")
    print("      - Tests custom placeholders")
    print()
    print("   3. python agents/ism/test_your_format.py")
    print("      - Tests Bank of Nova Scotia templates")
    print("      - Validates placeholder replacement")
    print()
    
    print("🔧 Customization Options:")
    print("   1. Edit placeholders in test scripts")
    print("   2. Modify templates in agents/ism/large_text_templates.py")
    print("   3. Add new product types in agents/ism/models.py")
    print("   4. Customize agent behavior in agents/ism/agent.py")
    print()
    
    print("💡 LLM Interaction Features:")
    print("   ✅ Handles missing data gracefully")
    print("   ✅ Asks for clarification when needed")
    print("   ✅ Adjusts output based on feedback")
    print("   ✅ Validates placeholder replacement")
    print("   ✅ Generates regulatory-compliant content")
    print()
    
    print("🚀 Ready to test your ISM agent!")


async def main():
    """Main setup function."""
    print("🚀 ISM Agent Test Setup")
    print("=" * 60)
    
    # Step 1: Setup environment
    if not setup_environment():
        print("❌ Environment setup failed. Please check the errors above.")
        return
    
    # Step 2: Configure placeholders
    placeholders = configure_placeholders()
    
    # Step 3: Run quick test
    test_success = await run_quick_test(placeholders)
    
    if test_success:
        print_next_steps()
    else:
        print("\n❌ Setup incomplete. Please fix the issues and try again.")


if __name__ == "__main__":
    asyncio.run(main()) 