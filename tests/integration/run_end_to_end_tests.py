#!/usr/bin/env python3
"""
End-to-End Workflow Test Runner

This script provides a simple interface to run the comprehensive end-to-end workflow tests
for the AutocollableSNAgt framework.

Usage:
    python run_end_to_end_tests.py [--verbose] [--save-results]

Options:
    --verbose: Enable detailed logging
    --save-results: Save detailed results to JSON file
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

# Ensure repository root is on sys.path so `tests` package is importable
# File path: tests/integration/run_end_to_end_tests.py → repo root is two levels up
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

from tests.integration.test_end_to_end_workflow import EndToEndWorkflowTester


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('end_to_end_tests.log')
        ]
    )


async def main():
    """Main function to run end-to-end workflow tests"""
    parser = argparse.ArgumentParser(description='Run End-to-End Workflow Tests')
    parser.add_argument('--verbose', action='store_true', help='Enable detailed logging')
    parser.add_argument('--save-results', action='store_true', help='Save detailed results to JSON file')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    print("🚀 AutocollableSNAgt Framework - End-to-End Workflow Tests")
    print("=" * 80)
    print("📋 Test Scenarios:")
    print("  1. Simple ISM Document Generation")
    print("  2. Complex Multi-Agent Workflow (with expected import errors)")
    print("  3. User Feedback Loop")
    print("  4. Error Recovery Workflow")
    print("=" * 80)
    
    try:
        # Create tester
        tester = EndToEndWorkflowTester()
        
        # Run tests
        results = await tester.run_all_tests()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 END-TO-END WORKFLOW TEST RESULTS")
        print("=" * 80)
        
        # Overall results
        success_rate = results["performance_metrics"]["success_rate"]
        print(f"🎯 Overall Success Rate: {success_rate:.1f}%")
        print(f"✅ Tests Passed: {results['performance_metrics']['tests_passed']}")
        print(f"❌ Tests Failed: {results['performance_metrics']['tests_failed']}")
        print(f"⏱️  Total Execution Time: {results['performance_metrics']['total_execution_time']:.2f} seconds")
        
        # Individual test results
        print("\n📋 Individual Test Results:")
        for scenario_key, scenario_result in results["test_scenarios"].items():
            status = "✅ PASS" if scenario_result["result"].get("success", False) else "❌ FAIL"
            print(f"  {status} {scenario_result['name']}")
            
            if not scenario_result["result"].get("success", False):
                error = scenario_result["result"].get("error", "Unknown error")
                print(f"    Error: {error}")
        
        # Recommendations
        if results["recommendations"]:
            print("\n💡 Recommendations:")
            for recommendation in results["recommendations"]:
                print(f"  {recommendation}")
        
        # Save results if requested
        if args.save_results:
            import json
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"end_to_end_workflow_results_{timestamp}.json"
            
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"\n💾 Detailed results saved to: {results_file}")
        
        # Exit with appropriate code
        if results["overall_success"]:
            print("\n🎉 All end-to-end workflow tests passed!")
            return 0
        else:
            print("\n⚠️ Some end-to-end workflow tests failed. Check results for details.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test runner failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 