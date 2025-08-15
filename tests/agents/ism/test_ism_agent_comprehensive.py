#!/usr/bin/env python3
"""
Comprehensive ISM Agent Test Script

This script tests the ISM agent with your placeholders and templates,
including LLM interaction capabilities for missing data and output adjustments.

Usage:
    python test_ism_agent_comprehensive.py
"""

import asyncio
import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Import ISM components
from agents.investor_summary import ISMAgent, ISMInput, ISMOutput
from agents.investor_summary.large_text_integration import LargeTextISMAgent
from agents.investor_summary.large_text_templates import CUSTOM_PLACEHOLDERS


class ISMAgentTester:
    """
    Comprehensive tester for ISM agent with interactive LLM capabilities.
    """
    
    def __init__(self, use_large_text_templates: bool = True):
        """
        Initialize the tester.
        
        Args:
            use_large_text_templates: Whether to use large text templates (recommended)
        """
        self.use_large_text_templates = use_large_text_templates
        
        if use_large_text_templates:
            self.agent = LargeTextISMAgent()
        else:
            self.agent = ISMAgent()
        
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
    
    def create_sample_input(self, scenario: str = "autocallable") -> ISMInput:
        """
        Create sample input data for testing.
        
        Args:
            scenario: Type of product to test ("autocallable", "barrier", "reverse_convertible")
            
        Returns:
            ISMInput with sample data
        """
        if scenario == "autocallable":
            return ISMInput(
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
        
        elif scenario == "barrier":
            return ISMInput(
                issuer="Your Financial Services Ltd",
                product_name="S&P 500 Barrier Note Series 2025-2",
                underlying_asset="S&P 500 Index",
                currency="USD",
                principal_amount=50000.00,
                issue_date=date(2025, 2, 15),
                maturity_date=date(2028, 2, 15),
                product_type="barrier",
                barrier_level=80.0,
                coupon_rate=12.0,
                protection_level=80.0,
                target_audience="retail_investors",
                risk_tolerance="high",
                investment_objective="high_income",
                market_outlook="bullish",
                volatility_level="high",
                regulatory_jurisdiction="US",
                distribution_method="private_placement",
                minimum_investment=25000.00
            )
        
        else:  # reverse_convertible
            return ISMInput(
                issuer="Your Financial Services Ltd",
                product_name="Tech Basket Reverse Convertible Series 2025-3",
                underlying_asset="Technology Stock Basket",
                currency="USD",
                principal_amount=75000.00,
                issue_date=date(2025, 3, 1),
                maturity_date=date(2027, 3, 1),
                product_type="reverse_convertible",
                barrier_level=60.0,
                coupon_rate=15.0,
                protection_level=60.0,
                target_audience="accredited_investors",
                risk_tolerance="high",
                investment_objective="high_income",
                market_outlook="neutral",
                volatility_level="high",
                regulatory_jurisdiction="US",
                distribution_method="private_placement",
                minimum_investment=50000.00
            )
    
    async def test_basic_generation(self, input_data: ISMInput) -> ISMOutput:
        """
        Test basic document generation.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Generated document output
        """
        print("🔧 Testing Basic Document Generation...")
        print(f"   Product: {input_data.product_name}")
        print(f"   Type: {input_data.product_type}")
        print(f"   Amount: {input_data.principal_amount:,.2f} {input_data.currency}")
        print()
        
        try:
            if self.use_large_text_templates:
                result = await self.agent.generate_document_with_large_templates(
                    input_data=input_data,
                    audience="retail"
                )
            else:
                result = await self.agent.generate_document(input_data)
            
            print("✅ Document generated successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Error in document generation: {e}")
            raise
    
    def analyze_output(self, result: ISMOutput) -> Dict[str, Any]:
        """
        Analyze the generated output for quality and completeness.
        
        Args:
            result: Generated document output
            
        Returns:
            Analysis results
        """
        print("\n📊 Analyzing Generated Output...")
        
        analysis = {
            "document_title_length": len(result.document_title),
            "executive_summary_paragraphs": result.executive_summary.count('\n\n') + 1,
            "key_features_count": len(result.key_features),
            "key_risks_count": len(result.key_risks),
            "risk_level_indicator": result.risk_level_indicator,
            "has_required_disclaimers": self._check_required_disclaimers(result),
            "placeholder_issues": self._check_placeholder_issues(result),
            "content_quality": self._assess_content_quality(result)
        }
        
        # Print analysis results
        print(f"   📄 Document Title: {result.document_title}")
        print(f"   📏 Title Length: {analysis['document_title_length']} chars")
        print(f"   📋 Executive Summary: {analysis['executive_summary_paragraphs']} paragraphs")
        print(f"   ✨ Key Features: {analysis['key_features_count']} items")
        print(f"   ⚠️  Key Risks: {analysis['key_risks_count']} items")
        print(f"   🎯 Risk Level: {analysis['risk_level_indicator']}")
        
        if analysis['has_required_disclaimers']:
            print("   ✅ Required disclaimers present")
        else:
            print("   ❌ Missing required disclaimers")
        
        if analysis['placeholder_issues']:
            print(f"   ⚠️  Found {len(analysis['placeholder_issues'])} placeholder issues")
            for issue in analysis['placeholder_issues'][:3]:
                print(f"      - {issue}")
        
        print(f"   📈 Content Quality Score: {analysis['content_quality']}/10")
        
        return analysis
    
    def _check_required_disclaimers(self, result: ISMOutput) -> bool:
        """Check if required disclaimers are present."""
        disclaimer_text = result.disclaimer.lower()
        required_phrases = [
            "past performance does not guarantee future results",
            "all investments carry risk of loss",
            "consult your financial advisor",
            "informational purposes only"
        ]
        
        return all(phrase in disclaimer_text for phrase in required_phrases)
    
    def _check_placeholder_issues(self, result: ISMOutput) -> list:
        """Check for unreplaced placeholders in the output."""
        issues = []
        
        # Check all text fields for placeholders
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
        
        for i, text in enumerate(text_fields):
            if "[" in text and "]" in text:
                import re
                placeholders = re.findall(r'\[([^\]]+)\]', text)
                if placeholders:
                    field_name = list(result.__dict__.keys())[i]
                    issues.append(f"{field_name}: {', '.join(placeholders)}")
        
        return issues
    
    def _assess_content_quality(self, result: ISMOutput) -> int:
        """Assess content quality on a scale of 1-10."""
        score = 10
        
        # Deduct points for various issues
        if len(result.document_title) > 80:
            score -= 2
        
        if len(result.key_features) != 3:
            score -= 1
        
        if len(result.key_risks) != 4:
            score -= 1
        
        if not result.executive_summary.endswith("This investment may not be suitable for all investors."):
            score -= 2
        
        if "risk of loss" not in result.disclaimer.lower():
            score -= 1
        
        return max(1, score)
    
    async def test_llm_interaction(self, input_data: ISMInput) -> Dict[str, Any]:
        """
        Test LLM interaction capabilities for missing data and adjustments.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Interaction test results
        """
        print("\n🤖 Testing LLM Interaction Capabilities...")
        
        # Create incomplete input to test missing data handling
        incomplete_input = input_data.model_copy()
        incomplete_input.additional_features = None  # Remove additional features
        incomplete_input.market_outlook = None  # Remove market outlook
        
        print("   📝 Testing with incomplete data...")
        print("   Missing: additional_features, market_outlook")
        
        try:
            # Test if agent can handle missing data
            result = await self.test_basic_generation(incomplete_input)
            
            # Analyze how well it handled missing data
            analysis = self.analyze_output(result)
            
            interaction_results = {
                "handled_missing_data": True,
                "content_quality_with_missing_data": analysis['content_quality'],
                "placeholder_issues": analysis['placeholder_issues'],
                "suggestions_for_improvement": self._generate_improvement_suggestions(analysis)
            }
            
            print("   ✅ Agent handled missing data gracefully")
            
            return interaction_results
            
        except Exception as e:
            print(f"   ❌ Agent struggled with missing data: {e}")
            return {
                "handled_missing_data": False,
                "error": str(e)
            }
    
    def _generate_improvement_suggestions(self, analysis: Dict[str, Any]) -> list:
        """Generate suggestions for improving the output."""
        suggestions = []
        
        if analysis['content_quality'] < 8:
            suggestions.append("Consider adding more specific product details")
        
        if analysis['placeholder_issues']:
            suggestions.append("Review and update placeholder mappings")
        
        if not analysis['has_required_disclaimers']:
            suggestions.append("Ensure all required regulatory disclaimers are included")
        
        if len(analysis['placeholder_issues']) > 5:
            suggestions.append("Comprehensive placeholder review needed")
        
        return suggestions
    
    async def test_custom_placeholders(self) -> Dict[str, Any]:
        """
        Test custom placeholder integration.
        
        Returns:
            Placeholder test results
        """
        print("\n🔧 Testing Custom Placeholder Integration...")
        
        # Test with your custom placeholders
        test_input = self.create_sample_input("autocallable")
        
        # Add custom placeholder data
        existing_features = test_input.additional_features or {}
        test_input.additional_features = {
            **existing_features,
            "custom_placeholders": self.your_placeholders
        }
        
        try:
            result = await self.test_basic_generation(test_input)
            analysis = self.analyze_output(result)
            
            # Check if custom placeholders were properly integrated
            custom_placeholder_usage = self._check_custom_placeholder_usage(result)
            
            return {
                "custom_placeholders_used": custom_placeholder_usage,
                "integration_success": len(custom_placeholder_usage) > 0,
                "analysis": analysis
            }
            
        except Exception as e:
            print(f"   ❌ Custom placeholder test failed: {e}")
            return {"integration_success": False, "error": str(e)}
    
    def _check_custom_placeholder_usage(self, result: ISMOutput) -> list:
        """Check which custom placeholders were used in the output."""
        used_placeholders = []
        
        # Check all text fields for custom placeholder usage
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
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """
        Run comprehensive test suite.
        
        Returns:
            Complete test results
        """
        print("🧪 ISM Agent Comprehensive Test Suite")
        print("=" * 60)
        print(f"Using Large Text Templates: {self.use_large_text_templates}")
        print(f"Custom Placeholders: {len(self.your_placeholders)} configured")
        print()
        
        test_results = {
            "test_timestamp": datetime.now().isoformat(),
            "use_large_text_templates": self.use_large_text_templates,
            "scenarios_tested": [],
            "llm_interaction_tests": {},
            "custom_placeholder_tests": {},
            "overall_score": 0
        }
        
        # Test different scenarios
        scenarios = ["autocallable", "barrier", "reverse_convertible"]
        
        for scenario in scenarios:
            print(f"\n📋 Testing {scenario.upper()} Scenario")
            print("-" * 40)
            
            try:
                input_data = self.create_sample_input(scenario)
                result = await self.test_basic_generation(input_data)
                analysis = self.analyze_output(result)
                
                test_results["scenarios_tested"].append({
                    "scenario": scenario,
                    "success": True,
                    "analysis": analysis
                })
                
            except Exception as e:
                print(f"❌ {scenario} scenario failed: {e}")
                test_results["scenarios_tested"].append({
                    "scenario": scenario,
                    "success": False,
                    "error": str(e)
                })
        
        # Test LLM interaction
        print(f"\n🤖 Testing LLM Interaction")
        print("-" * 40)
        llm_results = await self.test_llm_interaction(self.create_sample_input("autocallable"))
        test_results["llm_interaction_tests"] = llm_results
        
        # Test custom placeholders
        print(f"\n🔧 Testing Custom Placeholders")
        print("-" * 40)
        placeholder_results = await self.test_custom_placeholders()
        test_results["custom_placeholder_tests"] = placeholder_results
        
        # Calculate overall score
        successful_scenarios = sum(1 for s in test_results["scenarios_tested"] if s["success"])
        test_results["overall_score"] = (successful_scenarios / len(scenarios)) * 10
        
        # Print summary
        self._print_test_summary(test_results)
        
        return test_results
    
    def _print_test_summary(self, results: Dict[str, Any]):
        """Print comprehensive test summary."""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        print(f"🎯 Overall Score: {results['overall_score']:.1f}/10")
        print(f"📅 Test Date: {results['test_timestamp']}")
        print(f"🔧 Large Text Templates: {'✅' if results['use_large_text_templates'] else '❌'}")
        
        print(f"\n📋 Scenario Tests:")
        for scenario in results["scenarios_tested"]:
            status = "✅" if scenario["success"] else "❌"
            print(f"   {status} {scenario['scenario'].upper()}")
        
        print(f"\n🤖 LLM Interaction:")
        llm_tests = results["llm_interaction_tests"]
        if llm_tests.get("handled_missing_data"):
            print("   ✅ Handles missing data gracefully")
        else:
            print("   ❌ Struggles with missing data")
        
        print(f"\n🔧 Custom Placeholders:")
        placeholder_tests = results["custom_placeholder_tests"]
        if placeholder_tests.get("integration_success"):
            print("   ✅ Custom placeholders integrated successfully")
        else:
            print("   ❌ Custom placeholder integration issues")
        
        print(f"\n💡 Recommendations:")
        if results["overall_score"] >= 8:
            print("   🎉 Excellent! Your ISM agent is ready for production use.")
        elif results["overall_score"] >= 6:
            print("   ⚠️  Good, but some improvements recommended.")
        else:
            print("   🔧 Significant improvements needed before production use.")
        
        # Save results to file
        output_file = f"ism_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {output_file}")


async def main():
    """Main test function."""
    print("🚀 Starting ISM Agent Comprehensive Test")
    print("=" * 60)
    
    # Test with large text templates (recommended)
    tester = ISMAgentTester(use_large_text_templates=True)
    
    try:
        results = await tester.run_comprehensive_test()
        
        print("\n🎉 Test completed successfully!")
        print(f"Overall Score: {results['overall_score']:.1f}/10")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    asyncio.run(main()) 