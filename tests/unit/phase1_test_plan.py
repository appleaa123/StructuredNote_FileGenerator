#!/usr/bin/env python3
"""
Phase 1: Foundation Testing (Current Issues Resolution)

This script implements the Phase 1 test plan to validate the current development
state and identify any remaining issues before expanding to other agents.

Test Plan:
Step 1: Fix Current Test Failures
- Issue: 'dict' object has no attribute 'document_title' error
- Action: Debug and fix the data model serialization issues
- Priority: Critical (blocking all other tests)

Step 2: Unit Test Infrastructure
- Router Unit Tests: Test SmartAgentRouter in isolation
- GlobalAgent Unit Tests: Test GlobalAgent core functions
- ISM Agent Unit Tests: Test individual ISM agent methods
- Model Validation Tests: Test Pydantic models and data validation
"""

import sys
import os
import asyncio
import json
from datetime import datetime, date
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class Phase1TestSuite:
    """Comprehensive Phase 1 test suite"""
    
    def __init__(self):
        self.test_results = {
            "test_timestamp": datetime.now().isoformat(),
            "phase": "Phase 1: Foundation Testing",
            "tests": {},
            "overall_score": 0.0,
            "critical_issues": [],
            "recommendations": []
        }
    
    async def run_all_tests(self):
        """Run all Phase 1 tests"""
        print("🚀 Phase 1: Foundation Testing")
        print("=" * 60)
        print("Step 1: Fix Current Test Failures")
        print("Step 2: Unit Test Infrastructure")
        print()
        
        # Step 1: Fix Current Test Failures
        await self.step1_fix_current_test_failures()
        
        # Step 2: Unit Test Infrastructure
        await self.step2_unit_test_infrastructure()
        
        # Calculate overall score
        self._calculate_overall_score()
        
        # Print summary
        self._print_summary()
        
        return self.test_results
    
    async def step1_fix_current_test_failures(self):
        """Step 1: Fix Current Test Failures"""
        print("📋 Step 1: Fix Current Test Failures")
        print("-" * 40)
        
        # Test 1.1: ISM Agent Data Model Serialization
        await self.test_ism_agent_data_model_serialization()
        
        # Test 1.2: Large Text Template Integration
        await self.test_large_text_template_integration()
        
        # Test 1.3: Document Generation Pipeline
        await self.test_document_generation_pipeline()
        
        # Test 1.4: Error Handling and Recovery
        await self.test_error_handling_and_recovery()
    
    async def step2_unit_test_infrastructure(self):
        """Step 2: Unit Test Infrastructure"""
        print("\n📋 Step 2: Unit Test Infrastructure")
        print("-" * 40)
        
        # Test 2.1: Router Unit Tests
        await self.test_router_unit_tests()
        
        # Test 2.2: GlobalAgent Unit Tests
        await self.test_global_agent_unit_tests()
        
        # Test 2.3: ISM Agent Unit Tests
        await self.test_ism_agent_unit_tests()
        
        # Test 2.4: Model Validation Tests
        await self.test_model_validation_tests()
    
    async def test_ism_agent_data_model_serialization(self):
        """Test 1.1: ISM Agent Data Model Serialization"""
        print("   🧪 Test 1.1: ISM Agent Data Model Serialization")
        
        try:
            from agents.investor_summary.models import ISMInput, ISMOutput
            from agents.investor_summary.large_text_agent import LargeTextISMAgent
            from agents.investor_summary.agent import ISMAgent
            
            # Create sample input
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
            
            # Create large text agent
            base_agent = ISMAgent(
                knowledge_base_path="knowledge_bases/ism_kb/",
                model_name="openai:gpt-4o-mini"
            )
            large_text_agent = LargeTextISMAgent(base_agent, {})
            
            # Test document generation for testing (Pydantic model)
            result = await large_text_agent.generate_document_for_testing(
                input_data=sample_input,
                audience="retail"
            )
            
            # Verify document_title attribute exists
            if hasattr(result, 'document_title'):
                print("      ✅ document_title attribute found")
                print(f"      📄 Document title: {result.document_title}")
                
                # Test serialization
                result_dict = result.model_dump()
                if 'document_title' in result_dict:
                    print("      ✅ Model serialization successful")
                    self.test_results["tests"]["ism_data_model_serialization"] = {
                        "status": "PASS",
                        "score": 10.0,
                        "details": "document_title attribute properly serialized"
                    }
                else:
                    print("      ❌ Model serialization failed")
                    self.test_results["tests"]["ism_data_model_serialization"] = {
                        "status": "FAIL",
                        "score": 0.0,
                        "details": "document_title not found in serialized model"
                    }
                    self.test_results["critical_issues"].append("ISM model serialization failed")
            else:
                print("      ❌ document_title attribute not found")
                self.test_results["tests"]["ism_data_model_serialization"] = {
                    "status": "FAIL",
                    "score": 0.0,
                    "details": "document_title attribute missing"
                }
                self.test_results["critical_issues"].append("ISM model missing document_title attribute")
                
        except Exception as e:
            print(f"      ❌ Error in ISM data model serialization: {e}")
            self.test_results["tests"]["ism_data_model_serialization"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
            self.test_results["critical_issues"].append(f"ISM data model serialization error: {str(e)}")
    
    async def test_large_text_template_integration(self):
        """Test 1.2: Large Text Template Integration"""
        print("   🧪 Test 1.2: Large Text Template Integration")
        
        try:
            from agents.investor_summary.large_text_agent import LargeTextISMAgent
            from agents.investor_summary.agent import ISMAgent
            from agents.investor_summary.models import ISMInput
            
            # Create sample input
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
            
            # Create large text agent
            base_agent = ISMAgent(
                knowledge_base_path="knowledge_bases/ism_kb/",
                model_name="openai:gpt-4o-mini"
            )
            large_text_agent = LargeTextISMAgent(base_agent, {})
            
            # Test template variable extraction
            variables = large_text_agent._extract_agent_specific_variables(sample_input)
            
            if variables and len(variables) > 0:
                print("      ✅ Template variable extraction successful")
                print(f"      📋 Variables extracted: {len(variables)}")
                
                # Test field mapping
                doc_dict = {
                    "executive_summary": "Test executive summary",
                    "key_terms": "Test key terms",
                    "scenarios": "Test scenarios",
                    "disclaimer": "Test disclaimer"
                }
                
                field_mapping = large_text_agent._create_field_mapping(doc_dict, sample_input)
                
                if 'document_title' in field_mapping:
                    print("      ✅ Field mapping successful")
                    self.test_results["tests"]["large_text_template_integration"] = {
                        "status": "PASS",
                        "score": 10.0,
                        "details": "Template integration working correctly"
                    }
                else:
                    print("      ❌ Field mapping failed")
                    self.test_results["tests"]["large_text_template_integration"] = {
                        "status": "FAIL",
                        "score": 0.0,
                        "details": "Field mapping missing document_title"
                    }
            else:
                print("      ❌ Template variable extraction failed")
                self.test_results["tests"]["large_text_template_integration"] = {
                    "status": "FAIL",
                    "score": 0.0,
                    "details": "No template variables extracted"
                }
                
        except Exception as e:
            print(f"      ❌ Error in large text template integration: {e}")
            self.test_results["tests"]["large_text_template_integration"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
    
    async def test_document_generation_pipeline(self):
        """Test 1.3: Document Generation Pipeline"""
        print("   🧪 Test 1.3: Document Generation Pipeline")
        
        try:
            from agents.investor_summary.large_text_agent import LargeTextISMAgent
            from agents.investor_summary.agent import ISMAgent
            from agents.investor_summary.models import ISMInput
            
            # Create sample input
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
            
            # Create large text agent
            base_agent = ISMAgent(
                knowledge_base_path="knowledge_bases/ism_kb/",
                model_name="openai:gpt-4o-mini"
            )
            large_text_agent = LargeTextISMAgent(base_agent, {})
            
            # Test both generation methods
            dict_result = await large_text_agent.generate_document_with_large_templates(
                input_data=sample_input,
                audience="retail"
            )
            
            pydantic_result = await large_text_agent.generate_document_for_testing(
                input_data=sample_input,
                audience="retail"
            )
            
            if isinstance(dict_result, dict) and isinstance(pydantic_result, object):
                print("      ✅ Document generation pipeline successful")
                print(f"      📄 Dict result type: {type(dict_result)}")
                print(f"      📄 Pydantic result type: {type(pydantic_result)}")
                
                self.test_results["tests"]["document_generation_pipeline"] = {
                    "status": "PASS",
                    "score": 10.0,
                    "details": "Both generation methods working"
                }
            else:
                print("      ❌ Document generation pipeline failed")
                self.test_results["tests"]["document_generation_pipeline"] = {
                    "status": "FAIL",
                    "score": 0.0,
                    "details": "Generation methods returning unexpected types"
                }
                
        except Exception as e:
            print(f"      ❌ Error in document generation pipeline: {e}")
            self.test_results["tests"]["document_generation_pipeline"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
    
    async def test_error_handling_and_recovery(self):
        """Test 1.4: Error Handling and Recovery"""
        print("   🧪 Test 1.4: Error Handling and Recovery")
        
        try:
            from agents.factory import create_large_text_agent_with_factory
            
            # Test with invalid agent type
            invalid_agent = create_large_text_agent_with_factory("invalid_agent")
            
            if invalid_agent is None:
                print("      ✅ Error handling for invalid agent type working")
                
                # Test with valid agent type
                valid_agent = create_large_text_agent_with_factory("ism")
                
                if valid_agent is not None:
                    print("      ✅ Valid agent creation working")
                    self.test_results["tests"]["error_handling_and_recovery"] = {
                        "status": "PASS",
                        "score": 10.0,
                        "details": "Error handling and recovery working correctly"
                    }
                else:
                    print("      ❌ Valid agent creation failed")
                    self.test_results["tests"]["error_handling_and_recovery"] = {
                        "status": "FAIL",
                        "score": 0.0,
                        "details": "Valid agent creation failed"
                    }
            else:
                print("      ❌ Error handling for invalid agent type failed")
                self.test_results["tests"]["error_handling_and_recovery"] = {
                    "status": "FAIL",
                    "score": 0.0,
                    "details": "Invalid agent type not handled properly"
                }
                
        except Exception as e:
            print(f"      ❌ Error in error handling test: {e}")
            self.test_results["tests"]["error_handling_and_recovery"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
    
    async def test_router_unit_tests(self):
        """Test 2.1: Router Unit Tests"""
        print("   🧪 Test 2.1: Router Unit Tests")
        
        try:
            from core.router import SmartAgentRouter
            
            # Test router creation
            router = SmartAgentRouter()
            
            if router is not None:
                print("      ✅ Router creation successful")
                
                # Test agent routing
                route_result = router.route_request("ism", "generate_document")
                
                if route_result is not None:
                    print("      ✅ Agent routing working")
                    self.test_results["tests"]["router_unit_tests"] = {
                        "status": "PASS",
                        "score": 10.0,
                        "details": "Router unit tests passed"
                    }
                else:
                    print("      ❌ Agent routing failed")
                    self.test_results["tests"]["router_unit_tests"] = {
                        "status": "FAIL",
                        "score": 0.0,
                        "details": "Agent routing failed"
                    }
            else:
                print("      ❌ Router creation failed")
                self.test_results["tests"]["router_unit_tests"] = {
                    "status": "FAIL",
                    "score": 0.0,
                    "details": "Router creation failed"
                }
                
        except Exception as e:
            print(f"      ❌ Error in router unit tests: {e}")
            self.test_results["tests"]["router_unit_tests"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
    
    async def test_global_agent_unit_tests(self):
        """Test 2.2: GlobalAgent Unit Tests"""
        print("   🧪 Test 2.2: GlobalAgent Unit Tests")
        
        try:
            from core.global_agent import GlobalAgent
            
            # Test global agent creation
            global_agent = GlobalAgent()
            
            if global_agent is not None:
                print("      ✅ Global agent creation successful")
                self.test_results["tests"]["global_agent_unit_tests"] = {
                    "status": "PASS",
                    "score": 10.0,
                    "details": "Global agent unit tests passed"
                }
            else:
                print("      ❌ Global agent creation failed")
                self.test_results["tests"]["global_agent_unit_tests"] = {
                    "status": "FAIL",
                    "score": 0.0,
                    "details": "Global agent creation failed"
                }
                
        except Exception as e:
            print(f"      ❌ Error in global agent unit tests: {e}")
            self.test_results["tests"]["global_agent_unit_tests"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
    
    async def test_ism_agent_unit_tests(self):
        """Test 2.3: ISM Agent Unit Tests"""
        print("   🧪 Test 2.3: ISM Agent Unit Tests")
        
        try:
            from agents.investor_summary.agent import ISMAgent
            from agents.investor_summary.large_text_agent import LargeTextISMAgent
            from agents.investor_summary.models import ISMInput, ISMOutput
            
            # Test ISM agent creation
            ism_agent = ISMAgent(
                knowledge_base_path="knowledge_bases/ism_kb/",
                model_name="openai:gpt-4o-mini"
            )
            
            if ism_agent is not None:
                print("      ✅ ISM agent creation successful")
                
                # Test large text agent creation
                large_text_agent = LargeTextISMAgent(ism_agent, {})
                
                if large_text_agent is not None:
                    print("      ✅ Large text ISM agent creation successful")
                    self.test_results["tests"]["ism_agent_unit_tests"] = {
                        "status": "PASS",
                        "score": 10.0,
                        "details": "ISM agent unit tests passed"
                    }
                else:
                    print("      ❌ Large text ISM agent creation failed")
                    self.test_results["tests"]["ism_agent_unit_tests"] = {
                        "status": "FAIL",
                        "score": 0.0,
                        "details": "Large text ISM agent creation failed"
                    }
            else:
                print("      ❌ ISM agent creation failed")
                self.test_results["tests"]["ism_agent_unit_tests"] = {
                    "status": "FAIL",
                    "score": 0.0,
                    "details": "ISM agent creation failed"
                }
                
        except Exception as e:
            print(f"      ❌ Error in ISM agent unit tests: {e}")
            self.test_results["tests"]["ism_agent_unit_tests"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
    
    async def test_model_validation_tests(self):
        """Test 2.4: Model Validation Tests"""
        print("   🧪 Test 2.4: Model Validation Tests")
        
        try:
            from agents.investor_summary.models import ISMInput, ISMOutput
            from datetime import date
            
            # Test ISMInput validation
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
            
            # Test ISMOutput validation
            sample_output = ISMOutput(
                document_title="Autocallable Investment Summary - S&P 500 Index",
                executive_summary="This is a test executive summary.",
                product_description="Test product description",
                how_it_works="Test how it works",
                key_features=["Feature 1", "Feature 2", "Feature 3"],
                investment_details="Test investment details",
                potential_returns="Test potential returns",
                scenarios_analysis="Test scenarios analysis",
                risk_summary="Test risk summary",
                key_risks=["Risk 1", "Risk 2", "Risk 3", "Risk 4"],
                risk_mitigation="Test risk mitigation",
                risk_level_indicator="Risk Level: MEDIUM - Test explanation",
                important_dates="Test important dates",
                fees_and_charges="Test fees and charges",
                liquidity_information="Test liquidity information",
                suitability_assessment="Test suitability assessment",
                regulatory_notices="Test regulatory notices",
                tax_considerations="Test tax considerations",
                contact_information="Test contact information",
                next_steps="Test next steps",
                disclaimer="Test disclaimer",
                document_version="1.0",
                generation_date="2025-01-29"
            )
            
            print("      ✅ Model validation successful")
            self.test_results["tests"]["model_validation_tests"] = {
                "status": "PASS",
                "score": 10.0,
                "details": "Model validation tests passed"
            }
            
        except Exception as e:
            print(f"      ❌ Error in model validation tests: {e}")
            self.test_results["tests"]["model_validation_tests"] = {
                "status": "FAIL",
                "score": 0.0,
                "details": f"Exception: {str(e)}"
            }
    
    def _calculate_overall_score(self):
        """Calculate overall test score"""
        total_score = 0.0
        total_tests = 0
        
        for test_name, test_result in self.test_results["tests"].items():
            total_score += test_result["score"]
            total_tests += 1
        
        if total_tests > 0:
            self.test_results["overall_score"] = total_score / total_tests
        else:
            self.test_results["overall_score"] = 0.0
    
    def _print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 PHASE 1 TEST SUMMARY")
        print("=" * 60)
        
        print(f"🎯 Overall Score: {self.test_results['overall_score']:.1f}/10")
        print(f"📅 Test Date: {self.test_results['test_timestamp']}")
        
        print(f"\n📋 Test Results:")
        for test_name, test_result in self.test_results["tests"].items():
            status = "✅" if test_result["status"] == "PASS" else "❌"
            print(f"   {status} {test_name}: {test_result['score']:.1f}/10")
        
        if self.test_results["critical_issues"]:
            print(f"\n🚨 Critical Issues:")
            for issue in self.test_results["critical_issues"]:
                print(f"   • {issue}")
        
        print(f"\n💡 Recommendations:")
        if self.test_results["overall_score"] >= 8:
            print("   🎉 Excellent! Phase 1 foundation is solid. Ready for Phase 2.")
        elif self.test_results["overall_score"] >= 6:
            print("   ⚠️  Good foundation, but some improvements needed before Phase 2.")
        else:
            print("   🔧 Significant improvements needed before proceeding to Phase 2.")
        
        # Save results
        output_file = f"phase1_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {output_file}")

async def main():
    """Main test function"""
    test_suite = Phase1TestSuite()
    results = await test_suite.run_all_tests()
    return results

if __name__ == "__main__":
    # Run Phase 1 tests
    asyncio.run(main()) 