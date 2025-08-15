#!/usr/bin/env python3
"""
Main Test Runner for AutocollableSNAgt Framework

This script provides a unified interface to run all tests in the project:
1. Unit Tests (ISM Agent, Global Agent)
2. Integration Tests
3. End-to-End Tests
4. Custom Test Suites

Usage:
    python tests/run_all_tests.py [test_type] [options]

Examples:
    python tests/run_all_tests.py all
    python tests/run_all_tests.py unit
    python tests/run_all_tests.py integration
    python tests/run_all_tests.py ism
    python tests/run_all_tests.py global
"""

import sys
import os
import asyncio
import argparse
import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestRunner:
    """Main test runner for the entire project"""
    
    def __init__(self):
        self.test_results = {
            "test_timestamp": datetime.now().isoformat(),
            "test_suites": {},
            "overall_score": 0.0,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "recommendations": []
        }
    
    async def run_all_tests(self, test_types: List[str] = None) -> Dict[str, Any]:
        """Run all tests or specific test types"""
        if test_types is None:
            test_types = ["unit", "integration", "e2e"]
        
        print("🚀 AutocollableSNAgt Framework - Test Runner")
        print("=" * 80)
        print(f"📋 Running test types: {', '.join(test_types)}")
        print("=" * 80)
        
        for test_type in test_types:
            await self._run_test_suite(test_type)
        
        # Calculate overall score
        self._calculate_overall_score()
        
        # Print summary
        self._print_summary()
        
        return self.test_results
    
    async def _run_test_suite(self, test_type: str):
        """Run a specific test suite"""
        print(f"\n🧪 Running {test_type.upper()} Tests")
        print("-" * 60)
        
        if test_type == "unit":
            await self._run_unit_tests()
        elif test_type == "integration":
            await self._run_integration_tests()
        elif test_type == "e2e":
            await self._run_e2e_tests()
        elif test_type == "ism":
            await self._run_ism_tests()
        elif test_type == "global":
            await self._run_global_tests()
        else:
            print(f"❌ Unknown test type: {test_type}")
    
    async def _run_unit_tests(self):
        """Run unit tests"""
        print("📋 Unit Tests")
        print("-" * 30)
        
        # ISM Agent Unit Tests
        try:
            from tests.unit.test_ism_agent import ISMAgentTester
            ism_tester = ISMAgentTester()
            ism_results = await ism_tester.run_all_tests()
            
            self.test_results["test_suites"]["ism_unit"] = {
                "success": ism_results["overall_score"] >= 6.0,
                "score": ism_results["overall_score"],
                "tests": ism_results["tests"]
            }
            
            print(f"✅ ISM Unit Tests: {ism_results['overall_score']:.1f}/10")
            
        except Exception as e:
            print(f"❌ ISM Unit Tests failed: {e}")
            self.test_results["test_suites"]["ism_unit"] = {
                "success": False,
                "error": str(e)
            }
        
        # Global Agent Unit Tests
        try:
            from tests.unit.test_global_agent import GlobalAgentTester
            global_tester = GlobalAgentTester()
            global_results = await global_tester.run_all_tests()
            
            self.test_results["test_suites"]["global_unit"] = {
                "success": global_results["overall_score"] >= 6.0,
                "score": global_results["overall_score"],
                "tests": global_results["tests"]
            }
            
            print(f"✅ Global Agent Unit Tests: {global_results['overall_score']:.1f}/10")
            
        except Exception as e:
            print(f"❌ Global Agent Unit Tests failed: {e}")
            self.test_results["test_suites"]["global_unit"] = {
                "success": False,
                "error": str(e)
            }
    
    async def _run_integration_tests(self):
        """Run integration tests"""
        print("📋 Integration Tests")
        print("-" * 30)
        
        try:
            # Import and run integration tests
            from tests.integration.run_integration_tests import IntegrationTestRunner
            
            runner = IntegrationTestRunner()
            integration_results = await runner.run_all_integration_tests()
            
            self.test_results["test_suites"]["integration"] = {
                "success": True,
                "results": integration_results
            }
            
            print("✅ Integration Tests completed")
            
        except Exception as e:
            print(f"❌ Integration Tests failed: {e}")
            self.test_results["test_suites"]["integration"] = {
                "success": False,
                "error": str(e)
            }
    
    async def _run_e2e_tests(self):
        """Run end-to-end tests"""
        print("📋 End-to-End Tests")
        print("-" * 30)
        
        try:
            # Import and run e2e tests
            from tests.integration.test_end_to_end_workflow import EndToEndWorkflowTester
            
            tester = EndToEndWorkflowTester()
            e2e_results = await tester.run_all_tests()
            
            self.test_results["test_suites"]["e2e"] = {
                "success": True,
                "results": e2e_results
            }
            
            print("✅ End-to-End Tests completed")
            
        except Exception as e:
            print(f"❌ End-to-End Tests failed: {e}")
            self.test_results["test_suites"]["e2e"] = {
                "success": False,
                "error": str(e)
            }
    
    async def _run_ism_tests(self):
        """Run ISM-specific tests"""
        print("📋 ISM Agent Tests")
        print("-" * 30)
        
        try:
            from tests.unit.test_ism_agent import ISMAgentTester
            ism_tester = ISMAgentTester()
            ism_results = await ism_tester.run_all_tests()
            
            self.test_results["test_suites"]["ism"] = {
                "success": ism_results["overall_score"] >= 6.0,
                "score": ism_results["overall_score"],
                "tests": ism_results["tests"]
            }
            
            print(f"✅ ISM Tests: {ism_results['overall_score']:.1f}/10")
            
        except Exception as e:
            print(f"❌ ISM Tests failed: {e}")
            self.test_results["test_suites"]["ism"] = {
                "success": False,
                "error": str(e)
            }
    
    async def _run_global_tests(self):
        """Run Global Agent-specific tests"""
        print("📋 Global Agent Tests")
        print("-" * 30)
        
        try:
            from tests.unit.test_global_agent import GlobalAgentTester
            global_tester = GlobalAgentTester()
            global_results = await global_tester.run_all_tests()
            
            self.test_results["test_suites"]["global"] = {
                "success": global_results["overall_score"] >= 6.0,
                "score": global_results["overall_score"],
                "tests": global_results["tests"]
            }
            
            print(f"✅ Global Agent Tests: {global_results['overall_score']:.1f}/10")
            
        except Exception as e:
            print(f"❌ Global Agent Tests failed: {e}")
            self.test_results["test_suites"]["global"] = {
                "success": False,
                "error": str(e)
            }
    
    def _calculate_overall_score(self):
        """Calculate overall test score"""
        total_suites = len(self.test_results["test_suites"])
        passed_suites = sum(1 for suite in self.test_results["test_suites"].values() if suite.get("success", False))
        
        if total_suites > 0:
            self.test_results["overall_score"] = (passed_suites / total_suites) * 10.0
            self.test_results["total_tests"] = total_suites
            self.test_results["passed_tests"] = passed_suites
            self.test_results["failed_tests"] = total_suites - passed_suites
        else:
            self.test_results["overall_score"] = 0.0
    
    def _print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        print(f"🎯 Overall Score: {self.test_results['overall_score']:.1f}/10")
        print(f"📅 Test Date: {self.test_results['test_timestamp']}")
        print(f"📊 Total Test Suites: {self.test_results['total_tests']}")
        print(f"✅ Passed: {self.test_results['passed_tests']}")
        print(f"❌ Failed: {self.test_results['failed_tests']}")
        
        print(f"\n📋 Test Suite Results:")
        for suite_name, result in self.test_results["test_suites"].items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            score = result.get("score", "N/A")
            print(f"   {status} {suite_name.replace('_', ' ').title()}")
            
            if isinstance(score, (int, float)):
                print(f"      Score: {score:.1f}/10")
            
            if not result.get("success", False):
                error = result.get("error", "Unknown error")
                print(f"      Error: {error}")
        
        # Generate recommendations
        self._generate_recommendations()
        
        if self.test_results["recommendations"]:
            print(f"\n💡 Recommendations:")
            for recommendation in self.test_results["recommendations"]:
                print(f"   • {recommendation}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"tests/results/comprehensive_test_results_{timestamp}.json"
        # Ensure results directory exists
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
        if self.test_results["overall_score"] >= 8:
            print("🎉 Excellent! All tests are passing.")
        elif self.test_results["overall_score"] >= 6:
            print("⚠️  Good, but some improvements needed.")
        else:
            print("🔧 Significant improvements needed before production use.")
    
    def _generate_recommendations(self):
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check for failed test suites
        failed_suites = [name for name, result in self.test_results["test_suites"].items() 
                        if not result.get("success", False)]
        
        if failed_suites:
            recommendations.append(f"Fix failed test suites: {', '.join(failed_suites)}")
        
        # Check for low scores
        low_score_suites = [name for name, result in self.test_results["test_suites"].items() 
                           if result.get("score", 10) < 6.0]
        
        if low_score_suites:
            recommendations.append(f"Improve test coverage for: {', '.join(low_score_suites)}")
        
        # General recommendations
        if self.test_results["overall_score"] < 8:
            recommendations.append("Add more comprehensive test coverage")
            recommendations.append("Implement automated testing in CI/CD pipeline")
        
        self.test_results["recommendations"] = recommendations


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run AutocollableSNAgt Framework Tests')
    parser.add_argument('test_type', nargs='?', default='all', 
                       choices=['all', 'unit', 'integration', 'e2e', 'ism', 'global'],
                       help='Type of tests to run')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose output')
    parser.add_argument('--save-results', action='store_true', 
                       help='Save detailed results to JSON file')
    
    args = parser.parse_args()
    
    # Setup logging if verbose
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Determine test types to run
    if args.test_type == 'all':
        test_types = ['unit', 'integration', 'e2e']
    else:
        test_types = [args.test_type]
    
    # Run tests
    runner = TestRunner()
    results = asyncio.run(runner.run_all_tests(test_types))
    
    # Exit with appropriate code
    if results["overall_score"] >= 6:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main() 