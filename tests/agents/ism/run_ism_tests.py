#!/usr/bin/env python3
"""
Run ISM Agent Tests

This script provides easy access to run ISM agent tests from the root directory.

Usage:
    python run_ism_tests.py [test_name]

Available tests:
    - basic: Run basic functionality test
    - config: Test with your configuration
    - comprehensive: Run full comprehensive test
    - interactive: Test interactive LLM capabilities
    - output: Test actual output format
    - all: Run all tests
"""

import sys
import subprocess
import os
from pathlib import Path


def run_test(test_name: str):
    """Run a specific test"""
    test_dir = Path("tests")
    
    if not test_dir.exists():
        print("❌ Tests directory not found. Please ensure you're in the project root.")
        return False
    
    # Map test names to files
    test_files = {
        "basic": "ism/simple_ism_test.py",
        "config": "ism/test_with_your_config.py",
        "comprehensive": "ism/test_ism_agent_comprehensive.py",
        "interactive": "ism/test_ism_interactive.py",
        "output": "ism/test_ism_actual_output.py",
        "setup": "ism/setup_ism_test.py",
        "create": "ism/create_ism_output_file.py"
    }
    
    if test_name not in test_files:
        print(f"❌ Unknown test: {test_name}")
        print(f"Available tests: {', '.join(test_files.keys())}")
        return False
    
    test_file = test_files[test_name]
    test_path = test_dir / test_file
    
    if not test_path.exists():
        print(f"❌ Test file not found: {test_path}")
        return False
    
    print(f"🚀 Running {test_name} test...")
    print(f"📁 Test file: {test_path}")
    print("=" * 60)
    
    try:
        # Run the test with proper Python path
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())
        
        result = subprocess.run([
            sys.executable, test_file
        ], cwd=test_dir, env=env, check=True)
        
        print("=" * 60)
        print(f"✅ {test_name} test completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print("=" * 60)
        print(f"❌ {test_name} test failed with exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ Python executable not found. Please ensure Python is installed.")
        return False


def run_all_tests():
    """Run all tests in sequence"""
    tests = ["basic", "config", "output", "interactive", "comprehensive"]
    
    print("🧪 Running all ISM agent tests...")
    print("=" * 60)
    
    results = {}
    for test in tests:
        print(f"\n📋 Running {test} test...")
        success = run_test(test)
        results[test] = success
        
        if not success:
            print(f"⚠️  {test} test failed, continuing with next test...")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {test}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your ISM agent is working perfectly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("📋 ISM Agent Test Runner")
        print("=" * 40)
        print("Usage: python run_ism_tests.py [test_name]")
        print("\nAvailable tests:")
        print("  basic          - Basic functionality test")
        print("  config         - Test with your configuration")
        print("  comprehensive  - Full comprehensive test")
        print("  interactive    - Interactive LLM capabilities")
        print("  output         - Actual output format test")
        print("  setup          - Setup and configuration test")
        print("  create         - Output file generation test")
        print("  all            - Run all tests")
        print("\nExamples:")
        print("  python run_ism_tests.py basic")
        print("  python run_ism_tests.py all")
        return
    
    test_name = sys.argv[1].lower()
    
    if test_name == "all":
        success = run_all_tests()
        sys.exit(0 if success else 1)
    else:
        success = run_test(test_name)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 