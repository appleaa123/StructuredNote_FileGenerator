#!/usr/bin/env python3
"""
Interactive ISM Agent Test Script

This script allows you to interactively test the ISM agent with your placeholders
and see how it handles missing data and requests for clarification.

Usage:
    python test_ism_interactive.py
"""

import asyncio
import json
from datetime import date
from typing import Dict, Any

from agents.investor_summary import ISMInput
from agents.investor_summary.large_text_integration import LargeTextISMAgent


class InteractiveISMTester:
    """
    Interactive tester for ISM agent with LLM interaction capabilities.
    """
    
    def __init__(self):
        """Initialize the interactive tester."""
        self.agent = LargeTextISMAgent()
        
        # Your placeholders - customize these with your actual data
        self.your_placeholders = {
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
    
    def create_base_input(self) -> ISMInput:
        """Create a base input with minimal required data."""
        return ISMInput(
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
            target_audience="retail_investors",
            risk_tolerance="medium",
            investment_objective="capital_growth_with_income",
            regulatory_jurisdiction="US",
            distribution_method="broker_dealer_network",
            minimum_investment=10000.00
        )
    
    async def test_missing_data_handling(self):
        """Test how the agent handles missing data."""
        print("\n🤖 Testing Missing Data Handling")
        print("=" * 50)
        
        # Create input with missing data
        input_data = self.create_base_input()
        
        # Remove some fields to test missing data handling
        input_data.additional_features = None
        input_data.market_outlook = None
        input_data.volatility_level = None
        input_data.autocall_barrier = None
        input_data.memory_feature = None
        input_data.protection_level = None
        
        print("📝 Testing with missing data:")
        print("   ❌ additional_features")
        print("   ❌ market_outlook")
        print("   ❌ volatility_level")
        print("   ❌ autocall_barrier")
        print("   ❌ memory_feature")
        print("   ❌ protection_level")
        print()
        
        try:
            print("⏳ Generating document with missing data...")
            result = await self.agent.generate_document_with_large_templates(
                input_data=input_data,
                audience="retail"
            )
            
            print("✅ Document generated successfully!")
            print(f"📄 Title: {result.document_title}")
            print(f"📋 Executive Summary: {result.executive_summary[:200]}...")
            print(f"⚠️  Risk Level: {result.risk_level_indicator}")
            
            # Check for placeholder issues
            self._check_placeholder_issues(result)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _check_placeholder_issues(self, result):
        """Check for unreplaced placeholders in the result."""
        import re
        
        text_fields = [
            result.document_title,
            result.executive_summary,
            result.product_description,
            result.how_it_works,
            result.investment_details,
            result.potential_returns,
            result.scenarios_analysis,
            result.risk_summary,
            result.risk_mitigation,
            result.important_dates,
            result.fees_and_charges,
            result.liquidity_information,
            result.suitability_assessment,
            result.regulatory_notices,
            result.tax_considerations,
            result.contact_information,
            result.next_steps,
            result.disclaimer
        ]
        
        placeholder_issues = []
        for i, text in enumerate(text_fields):
            if "[" in text and "]" in text:
                placeholders = re.findall(r'\[([^\]]+)\]', text)
                if placeholders:
                    field_name = list(result.__dict__.keys())[i]
                    placeholder_issues.extend([(field_name, p) for p in placeholders])
        
        if placeholder_issues:
            print(f"\n⚠️  Found {len(placeholder_issues)} placeholder issues:")
            for field, placeholder in placeholder_issues[:5]:  # Show first 5
                print(f"   {field}: [{placeholder}]")
            if len(placeholder_issues) > 5:
                print(f"   ... and {len(placeholder_issues) - 5} more")
        else:
            print("\n✅ No placeholder issues found!")
    
    async def test_custom_placeholders(self):
        """Test custom placeholder integration."""
        print("\n🔧 Testing Custom Placeholder Integration")
        print("=" * 50)
        
        input_data = self.create_base_input()
        
        # Add custom placeholder data
        existing_features = input_data.additional_features or {}
        input_data.additional_features = {
            **existing_features,
            "custom_placeholders": self.your_placeholders
        }
        
        print("📝 Testing with custom placeholders:")
        for key, value in self.your_placeholders.items():
            print(f"   {key}: {value}")
        print()
        
        try:
            print("⏳ Generating document with custom placeholders...")
            result = await self.agent.generate_document_with_large_templates(
                input_data=input_data,
                audience="retail"
            )
            
            print("✅ Document generated successfully!")
            print(f"📄 Title: {result.document_title}")
            
            # Check which custom placeholders were used
            used_placeholders = self._check_custom_placeholder_usage(result)
            
            if used_placeholders:
                print(f"\n✅ Custom placeholders used: {len(used_placeholders)}")
                for placeholder in used_placeholders[:3]:
                    print(f"   - {placeholder}")
            else:
                print("\n⚠️  No custom placeholders were used in the output")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _check_custom_placeholder_usage(self, result) -> list:
        """Check which custom placeholders were used in the output."""
        used_placeholders = []
        
        text_fields = [
            result.document_title,
            result.executive_summary,
            result.product_description,
            result.how_it_works,
            result.investment_details,
            result.potential_returns,
            result.scenarios_analysis,
            result.risk_summary,
            result.risk_mitigation,
            result.important_dates,
            result.fees_and_charges,
            result.liquidity_information,
            result.suitability_assessment,
            result.regulatory_notices,
            result.tax_considerations,
            result.contact_information,
            result.next_steps,
            result.disclaimer
        ]
        
        for placeholder, value in self.your_placeholders.items():
            for text in text_fields:
                if value in text or placeholder in text:
                    used_placeholders.append(placeholder)
                    break
        
        return used_placeholders
    
    async def test_interactive_adjustments(self):
        """Test interactive adjustments to the output."""
        print("\n🔄 Testing Interactive Adjustments")
        print("=" * 50)
        
        input_data = self.create_base_input()
        
        try:
            print("⏳ Generating initial document...")
            result = await self.agent.generate_document_with_large_templates(
                input_data=input_data,
                audience="retail"
            )
            
            print("✅ Initial document generated!")
            print(f"📄 Title: {result.document_title}")
            print(f"⚠️  Risk Level: {result.risk_level_indicator}")
            print(f"✨ Key Features: {len(result.key_features)} items")
            print(f"⚠️  Key Risks: {len(result.key_risks)} items")
            
            # Simulate user feedback
            print("\n🤔 Simulating user feedback...")
            print("   User: 'The risk level seems too low for this product'")
            print("   User: 'Can you add more specific details about the autocall feature?'")
            print("   User: 'The executive summary is too technical'")
            
            # In a real scenario, you would send these feedback points to the LLM
            # and regenerate the document with adjustments
            print("\n💡 In a real implementation, the LLM would:")
            print("   1. Analyze the user feedback")
            print("   2. Adjust the risk level assessment")
            print("   3. Add more autocall details")
            print("   4. Simplify the executive summary language")
            print("   5. Regenerate the document with improvements")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def run_interactive_tests(self):
        """Run all interactive tests."""
        print("🧪 Interactive ISM Agent Test Suite")
        print("=" * 60)
        print("This script tests LLM interaction capabilities")
        print("including missing data handling and custom placeholders.")
        print()
        
        # Test 1: Missing data handling
        await self.test_missing_data_handling()
        
        # Test 2: Custom placeholders
        await self.test_custom_placeholders()
        
        # Test 3: Interactive adjustments
        await self.test_interactive_adjustments()
        
        print("\n" + "=" * 60)
        print("🎉 Interactive tests completed!")
        print("\n💡 Next steps:")
        print("   1. Customize your placeholders in the script")
        print("   2. Test with your actual product data")
        print("   3. Implement real-time LLM feedback loops")
        print("   4. Add more sophisticated error handling")


async def main():
    """Main interactive test function."""
    tester = InteractiveISMTester()
    
    try:
        await tester.run_interactive_tests()
    except Exception as e:
        print(f"\n❌ Interactive test failed: {e}")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    asyncio.run(main()) 