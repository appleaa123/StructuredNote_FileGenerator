"""
Integration Test Runner

This script runs all component integration tests and provides comprehensive reporting.
Tests are organized by component:
- Router Integration Tests
- GlobalAgent Integration Tests  
- ISM Agent Integration Tests
"""

import pytest
import sys
import os
import time
import json
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from tests.integration.test_router_integration import TestRouterIntegration
from tests.integration.test_global_agent_integration import TestGlobalAgentIntegration
from tests.integration.test_ism_agent_integration import TestISMAgentIntegration
from tests.integration.test_end_to_end_workflow import EndToEndWorkflowTester


class IntegrationTestRunner:
    """Comprehensive integration test runner with reporting"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
    def run_router_integration_tests(self) -> Dict[str, Any]:
        """Run Router integration tests"""
        print("\n" + "="*80)
        print("ROUTER INTEGRATION TESTS")
        print("="*80)
        
        test_results = {
            "component": "Router",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "test_details": []
        }
        
        router_tests = [
            "test_single_agent_routing_ism_only",
            "test_multi_agent_routing_ism_bsp", 
            "test_confidence_scoring_accuracy",
            "test_information_extraction_accuracy",
            "test_task_decomposition_validation",
            "test_error_handling_invalid_requests",
            "test_routing_decision_validation",
            "test_agent_capabilities_retrieval",
            "test_route_request_method",
            "test_edge_cases_and_boundaries"
        ]
        
        router = TestRouterIntegration()
        
        for test_name in router_tests:
            test_results["tests_run"] += 1
            try:
                test_method = getattr(router, test_name)
                test_method()
                test_results["tests_passed"] += 1
                test_results["test_details"].append({
                    "test": test_name,
                    "status": "PASSED",
                    "error": None
                })
                print(f"✓ {test_name}")
            except Exception as e:
                test_results["tests_failed"] += 1
                test_results["test_details"].append({
                    "test": test_name,
                    "status": "FAILED",
                    "error": str(e)
                })
                print(f"✗ {test_name}: {str(e)}")
        
        return test_results
    
    def run_global_agent_integration_tests(self) -> Dict[str, Any]:
        """Run GlobalAgent integration tests"""
        print("\n" + "="*80)
        print("GLOBAL AGENT INTEGRATION TESTS")
        print("="*80)
        
        test_results = {
            "component": "GlobalAgent",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "test_details": []
        }
        
        global_agent_tests = [
            "test_session_management",
            "test_agent_coordination",
            "test_result_aggregation", 
            "test_feedback_processing",
            "test_conversation_state_transitions",
            "test_error_recovery_mechanisms",
            "test_conversation_history_management",
            "test_agent_status_retrieval",
            "test_audit_trail_functionality",
            "test_conversation_statistics",
            "test_edge_cases_and_error_handling"
        ]
        
        global_agent = TestGlobalAgentIntegration()
        
        for test_name in global_agent_tests:
            test_results["tests_run"] += 1
            try:
                test_method = getattr(global_agent, test_name)
                # Run async tests
                import asyncio
                asyncio.run(test_method())
                test_results["tests_passed"] += 1
                test_results["test_details"].append({
                    "test": test_name,
                    "status": "PASSED",
                    "error": None
                })
                print(f"✓ {test_name}")
            except Exception as e:
                test_results["tests_failed"] += 1
                test_results["test_details"].append({
                    "test": test_name,
                    "status": "FAILED",
                    "error": str(e)
                })
                print(f"✗ {test_name}: {str(e)}")
        
        return test_results
    
    def run_ism_agent_integration_tests(self) -> Dict[str, Any]:
        """Run ISM Agent integration tests"""
        print("\n" + "="*80)
        print("ISM AGENT INTEGRATION TESTS")
        print("="*80)
        
        test_results = {
            "component": "ISMAgent",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "test_details": []
        }
        
        ism_agent_tests = [
            "test_document_generation_workflow",
            "test_template_retrieval_and_customization",
            "test_knowledge_base_integration",
            "test_large_text_template_handling",
            "test_custom_placeholder_processing",
            "test_output_validation_and_formatting",
            "test_customized_document_generation",
            "test_knowledge_update_integration",
            "test_edge_cases_and_error_handling"
        ]
        
        ism_agent = TestISMAgentIntegration()
        
        for test_name in ism_agent_tests:
            test_results["tests_run"] += 1
            try:
                test_method = getattr(ism_agent, test_name)
                # Run async tests
                import asyncio
                asyncio.run(test_method())
                test_results["tests_passed"] += 1
                test_results["test_details"].append({
                    "test": test_name,
                    "status": "PASSED",
                    "error": None
                })
                print(f"✓ {test_name}")
            except Exception as e:
                test_results["tests_failed"] += 1
                test_results["test_details"].append({
                    "test": test_name,
                    "status": "FAILED",
                    "error": str(e)
                })
                print(f"✗ {test_name}: {str(e)}")
        
        return test_results
    
    async def run_end_to_end_workflow_tests(self) -> Dict[str, Any]:
        """Run end-to-end workflow tests"""
        print("\n" + "="*80)
        print("END-TO-END WORKFLOW TESTS")
        print("="*80)
        
        test_results = {
            "component": "EndToEndWorkflow",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "test_details": []
        }
        
        try:
            # Create end-to-end tester
            tester = EndToEndWorkflowTester()
            
            # Run all end-to-end tests
            results = await tester.run_all_tests()
            
            # Extract test details
            test_results["tests_run"] = len(results["test_scenarios"])
            test_results["tests_passed"] = results["performance_metrics"]["tests_passed"]
            test_results["tests_failed"] = results["performance_metrics"]["tests_failed"]
            
            # Add individual test details
            for scenario_key, scenario_result in results["test_scenarios"].items():
                test_results["test_details"].append({
                    "test": scenario_result["name"],
                    "status": "PASSED" if scenario_result["result"].get("success", False) else "FAILED",
                    "error": scenario_result["result"].get("error", None)
                })
            
            # Print individual test results
            for detail in test_results["test_details"]:
                if detail["status"] == "PASSED":
                    print(f"✓ {detail['test']}")
                else:
                    print(f"✗ {detail['test']}: {detail['error']}")
            
        except Exception as e:
            test_results["tests_failed"] += 1
            test_results["test_details"].append({
                "test": "End-to-End Workflow Tests",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"✗ End-to-End Workflow Tests: {str(e)}")
        
        return test_results
    
    async def run_all_integration_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("\n" + "="*80)
        print("COMPONENT INTEGRATION TEST SUITE")
        print("="*80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = time.time()
        
        # Run all test suites
        router_results = self.run_router_integration_tests()
        global_agent_results = self.run_global_agent_integration_tests()
        ism_agent_results = self.run_ism_agent_integration_tests()
        end_to_end_results = await self.run_end_to_end_workflow_tests()
        
        self.end_time = time.time()
        
        # Compile overall results
        overall_results = {
            "test_suite": "Component Integration Tests",
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": self.end_time - self.start_time,
            "components": {
                "Router": router_results,
                "GlobalAgent": global_agent_results,
                "ISMAgent": ism_agent_results,
                "EndToEndWorkflow": end_to_end_results
            },
            "summary": {
                "total_tests": (
                    router_results["tests_run"] + 
                    global_agent_results["tests_run"] + 
                    ism_agent_results["tests_run"] +
                    end_to_end_results["tests_run"]
                ),
                "total_passed": (
                    router_results["tests_passed"] + 
                    global_agent_results["tests_passed"] + 
                    ism_agent_results["tests_passed"] +
                    end_to_end_results["tests_passed"]
                ),
                "total_failed": (
                    router_results["tests_failed"] + 
                    global_agent_results["tests_failed"] + 
                    ism_agent_results["tests_failed"] +
                    end_to_end_results["tests_failed"]
                )
            }
        }
        
        return overall_results
    
    def print_summary_report(self, results: Dict[str, Any]):
        """Print a comprehensive summary report"""
        print("\n" + "="*80)
        print("INTEGRATION TEST SUMMARY REPORT")
        print("="*80)
        
        summary = results["summary"]
        duration = results["duration_seconds"]
        
        print(f"Test Suite: {results['test_suite']}")
        print(f"Timestamp: {results['timestamp']}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['total_passed']}")
        print(f"Failed: {summary['total_failed']}")
        print(f"Success Rate: {(summary['total_passed'] / summary['total_tests'] * 100):.1f}%")
        
        print("\nComponent Breakdown:")
        for component_name, component_results in results["components"].items():
            success_rate = (component_results["tests_passed"] / component_results["tests_run"] * 100) if component_results["tests_run"] > 0 else 0
            print(f"  {component_name}: {component_results['tests_passed']}/{component_results['tests_run']} ({success_rate:.1f}%)")
        
        # Show failed tests
        failed_tests = []
        for component_name, component_results in results["components"].items():
            for test_detail in component_results["test_details"]:
                if test_detail["status"] == "FAILED":
                    failed_tests.append(f"{component_name}.{test_detail['test']}: {test_detail['error']}")
        
        if failed_tests:
            print(f"\nFailed Tests ({len(failed_tests)}):")
            for failed_test in failed_tests:
                print(f"  - {failed_test}")
        else:
            print("\n✓ All tests passed!")
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"integration_test_results_{timestamp}.json"
        
        output_path = Path("tests/integration/results") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {output_path}")
        return output_path


async def main():
    """Main function to run all integration tests"""
    runner = IntegrationTestRunner()
    
    try:
        # Run all integration tests
        results = await runner.run_all_integration_tests()
        
        # Print summary report
        runner.print_summary_report(results)
        
        # Save results
        runner.save_results(results)
        
        # Return appropriate exit code
        if results["summary"]["total_failed"] > 0:
            print(f"\n❌ Integration tests failed: {results['summary']['total_failed']} failures")
            sys.exit(1)
        else:
            print(f"\n✅ All integration tests passed!")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ Test runner failed with error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 