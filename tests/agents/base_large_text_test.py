"""
Base Test Framework for Large Text Agents

This module provides a unified testing framework for all large text agents
(ISM, BSP, PDS, PRS) with consistent test methods and validation.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional, Type
from pathlib import Path

from agents.factory import create_agent_with_factory, create_large_text_agent_with_factory


class BaseLargeTextAgentTester:
    """Base tester for large text agents"""
    
    def __init__(self, agent_type: str, use_large_text_templates: bool = True):
        """
        Initialize the tester.
        
        Args:
            agent_type: Type of agent to test (ism, bsp, pds, prs)
            use_large_text_templates: Whether to use large text templates
        """
        self.agent_type = agent_type
        self.use_large_text_templates = use_large_text_templates
        
        if use_large_text_templates:
            self.agent = self._create_large_text_agent()
        else:
            self.agent = self._create_base_agent()
    
    def _create_large_text_agent(self):
        """Create large text agent for testing"""
        return create_large_text_agent_with_factory(self.agent_type)
    
    def _create_base_agent(self):
        """Create base agent for testing"""
        return create_agent_with_factory(self.agent_type)
    
    async def test_basic_generation(self, input_data) -> Any:
        """Test basic document generation"""
        print(f"🔧 Testing {self.agent_type.upper()} Basic Document Generation...")
        print(f"   Using Large Text Templates: {self.use_large_text_templates}")
        
        try:
            if self.use_large_text_templates:
                result = await self.agent.generate_document_with_large_templates(
                    input_data=input_data,
                    audience="retail"
                )
            else:
                result = await self.agent.generate_document(input_data)
            
            print(f"✅ {self.agent_type.upper()} document generated successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Error in {self.agent_type} document generation: {e}")
            raise
    
    async def test_for_testing(self, input_data) -> Any:
        """Test document generation for testing (returns Pydantic model)"""
        print(f"🧪 Testing {self.agent_type.upper()} Document Generation for Testing...")
        
        try:
            if self.use_large_text_templates:
                result = await self.agent.generate_document_for_testing(
                    input_data=input_data,
                    audience="retail"
                )
            else:
                result = await self.agent.generate_document(input_data)
            
            print(f"✅ {self.agent_type.upper()} testing document generated successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Error in {self.agent_type} testing document generation: {e}")
            raise
    
    def analyze_output(self, result) -> Dict[str, Any]:
        """Analyze the generated output for quality and completeness"""
        print(f"\n📊 Analyzing Generated {self.agent_type.upper()} Output...")
        
        if hasattr(result, 'document_title'):
            # Pydantic model output
            analysis = self._analyze_ism_output(result)
        elif isinstance(result, dict):
            # Dictionary output
            analysis = self._analyze_dict_output(result)
        else:
            analysis = {"error": f"Unknown result type: {type(result)}"}
        
        return analysis
    
    def _analyze_ism_output(self, result) -> Dict[str, Any]:
        """Analyze ISMOutput-like Pydantic model"""
        analysis = {
            "document_title_length": len(result.document_title) if hasattr(result, 'document_title') else 0,
            "has_required_fields": self._check_required_fields(result),
            "content_quality": self._assess_content_quality(result),
            "field_count": len(result.__dict__) if hasattr(result, '__dict__') else 0
        }
        
        # Print analysis results
        if hasattr(result, 'document_title'):
            print(f"   📄 Document Title: {result.document_title}")
            print(f"   📏 Title Length: {analysis['document_title_length']} chars")
        
        print(f"   ✅ Required Fields: {analysis['has_required_fields']}")
        print(f"   📈 Content Quality Score: {analysis['content_quality']}/10")
        print(f"   📋 Field Count: {analysis['field_count']}")
        
        return analysis
    
    def _analyze_dict_output(self, result: Dict[str, str]) -> Dict[str, Any]:
        """Analyze dictionary output from large text templates"""
        analysis = {
            "sections_count": len(result),
            "total_content_length": sum(len(content) for content in result.values()),
            "sections": list(result.keys()),
            "content_quality": self._assess_dict_content_quality(result)
        }
        
        # Print analysis results
        print(f"   📋 Sections: {analysis['sections_count']}")
        print(f"   📏 Total Content Length: {analysis['total_content_length']} chars")
        print(f"   📄 Sections: {', '.join(analysis['sections'])}")
        print(f"   📈 Content Quality Score: {analysis['content_quality']}/10")
        
        return analysis
    
    def _check_required_fields(self, result) -> bool:
        """Check if required fields are present"""
        required_fields = ['document_title', 'generation_date']
        
        for field in required_fields:
            if not hasattr(result, field):
                return False
        
        return True
    
    def _assess_content_quality(self, result) -> int:
        """Assess content quality on a scale of 1-10"""
        score = 10
        
        # Deduct points for various issues
        if hasattr(result, 'document_title') and len(result.document_title) > 100:
            score -= 2
        
        if hasattr(result, 'document_title') and len(result.document_title) < 10:
            score -= 2
        
        if not self._check_required_fields(result):
            score -= 3
        
        return max(1, score)
    
    def _assess_dict_content_quality(self, result: Dict[str, str]) -> int:
        """Assess dictionary content quality on a scale of 1-10"""
        score = 10
        
        # Deduct points for various issues
        if len(result) < 3:
            score -= 2
        
        total_length = sum(len(content) for content in result.values())
        if total_length < 1000:
            score -= 2
        
        if any(len(content) < 50 for content in result.values()):
            score -= 1
        
        return max(1, score)
    
    async def test_scenario(self, scenario: str, input_data) -> Dict[str, Any]:
        """Test a specific scenario"""
        print(f"\n📋 Testing {self.agent_type.upper()} {scenario.upper()} Scenario")
        print("-" * 40)
        
        try:
            # Test basic generation
            result = await self.test_basic_generation(input_data)
            
            # Test for testing (Pydantic model)
            testing_result = await self.test_for_testing(input_data)
            
            # Analyze both outputs
            basic_analysis = self.analyze_output(result)
            testing_analysis = self.analyze_output(testing_result)
            
            return {
                "scenario": scenario,
                "success": True,
                "basic_result": result,
                "testing_result": testing_result,
                "basic_analysis": basic_analysis,
                "testing_analysis": testing_analysis
            }
            
        except Exception as e:
            print(f"❌ {scenario} scenario failed: {e}")
            return {
                "scenario": scenario,
                "success": False,
                "error": str(e)
            }
    
    async def run_comprehensive_test(self, scenarios: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        print(f"🧪 {self.agent_type.upper()} Agent Comprehensive Test Suite")
        print("=" * 60)
        print(f"Using Large Text Templates: {self.use_large_text_templates}")
        print()
        
        test_results = {
            "test_timestamp": datetime.now().isoformat(),
            "agent_type": self.agent_type,
            "use_large_text_templates": self.use_large_text_templates,
            "scenarios_tested": [],
            "overall_score": 0
        }
        
        # Test different scenarios
        for scenario_name, input_data in scenarios.items():
            scenario_result = await self.test_scenario(scenario_name, input_data)
            test_results["scenarios_tested"].append(scenario_result)
        
        # Calculate overall score
        successful_scenarios = sum(1 for s in test_results["scenarios_tested"] if s["success"])
        test_results["overall_score"] = (successful_scenarios / len(scenarios)) * 10
        
        # Print summary
        self._print_test_summary(test_results)
        
        return test_results
    
    def _print_test_summary(self, results: Dict[str, Any]):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print(f"📊 {self.agent_type.upper()} COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        print(f"🎯 Overall Score: {results['overall_score']:.1f}/10")
        print(f"📅 Test Date: {results['test_timestamp']}")
        print(f"🔧 Large Text Templates: {'✅' if results['use_large_text_templates'] else '❌'}")
        
        print(f"\n📋 Scenario Tests:")
        for scenario in results["scenarios_tested"]:
            status = "✅" if scenario["success"] else "❌"
            print(f"   {status} {scenario['scenario'].upper()}")
        
        print(f"\n💡 Recommendations:")
        if results["overall_score"] >= 8:
            print("   🎉 Excellent! Your agent is ready for production use.")
        elif results["overall_score"] >= 6:
            print("   ⚠️  Good, but some improvements recommended.")
        else:
            print("   🔧 Significant improvements needed before production use.")
        
        # Save results to file
        output_file = f"{self.agent_type}_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {output_file}")


# Example usage for ISM agent
async def example_ism_test():
    """Example test for ISM agent"""
    from agents.investor_summary.models import ISMInput
    from datetime import date
    
    # Create sample input data
    sample_input = ISMInput(
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
        distribution_method="broker_dealer_network"
    )
    
    # Create scenarios
    scenarios = {
        "autocallable": sample_input
    }
    
    # Create tester
    tester = BaseLargeTextAgentTester("ism", use_large_text_templates=True)
    
    # Run comprehensive test
    results = await tester.run_comprehensive_test(scenarios)
    
    return results


if __name__ == "__main__":
    # Run example test
    asyncio.run(example_ism_test()) 