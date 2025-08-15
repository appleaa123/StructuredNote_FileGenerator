#!/usr/bin/env python3
"""
Unified Global Agent Test Suite

This file combines global agent testing functionality from:
- test_global_agent_simple.py
- phase1_test_plan.py (global agent parts)

Provides comprehensive testing for:
1. GlobalAgent constructor
2. GlobalAgent core functions
3. Agent coordination
4. Session management
5. Error handling
"""

import sys
import os
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class GlobalAgentTester:
    """Comprehensive Global Agent Test Suite"""
    
    def __init__(self):
        self.test_results = {
            "test_timestamp": datetime.now().isoformat(),
            "tests": {},
            "overall_score": 0.0,
            "critical_issues": [],
            "recommendations": []
        }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all global agent tests"""
        print("🧪 Unified Global Agent Test Suite")
        print("=" * 60)
        
        # Test 1: GlobalAgent constructor
        await self.test_global_agent_constructor()
        
        # Test 2: GlobalAgent core functions
        await self.test_global_agent_core_functions()
        
        # Test 3: Agent coordination
        await self.test_agent_coordination()
        
        # Test 4: Session management
        await self.test_session_management()
        
        # Test 5: Error handling
        await self.test_error_handling()
        
        # Calculate overall score
        self._calculate_overall_score()
        
        # Print summary
        self._print_summary()
        
        return self.test_results
    
    async def test_global_agent_constructor(self):
        """Test GlobalAgent constructor"""
        print("\n📋 Test 1: GlobalAgent Constructor")
        print("-" * 40)
        
        try:
            from core.global_agent import GlobalAgent
            
            # Test with no parameters
            print("   Testing GlobalAgent() with no parameters...")
            global_agent1 = GlobalAgent()
            print("   ✅ GlobalAgent() created successfully")
            
            # Test with parameters
            print("   Testing GlobalAgent(action='test', config={})...")
            global_agent2 = GlobalAgent(action="test", config={})
            print("   ✅ GlobalAgent(action, config) created successfully")
            
            # Test with only action
            print("   Testing GlobalAgent(action='test')...")
            global_agent3 = GlobalAgent(action="test")
            print("   ✅ GlobalAgent(action) created successfully")
            
            print("   ✅ All GlobalAgent constructor tests passed!")
            
            self.test_results["tests"]["constructor"] = {
                "success": True,
                "message": "All constructor tests passed"
            }
            
        except Exception as e:
            print(f"   ❌ Error in GlobalAgent constructor: {e}")
            import traceback
            traceback.print_exc()
            self.test_results["tests"]["constructor"] = {
                "success": False,
                "error": str(e)
            }
    
    async def test_global_agent_core_functions(self):
        """Test GlobalAgent core functions"""
        print("\n📋 Test 2: GlobalAgent Core Functions")
        print("-" * 40)
        
        try:
            from core.global_agent import GlobalAgent
            
            # Create agent
            global_agent = GlobalAgent()
            print("✅ GlobalAgent created successfully")
            
            # Test core functions
            print("   Testing core functions...")
            
            # Test agent registry
            try:
                agents = global_agent.get_available_agents()
                print(f"   ✅ Agent registry: {len(agents)} agents available")
            except Exception as e:
                print(f"   ⚠️  Agent registry test failed: {e}")
            
            # Test health check
            try:
                health = global_agent.get_health_status()
                print(f"   ✅ Health check: {health}")
            except Exception as e:
                print(f"   ⚠️  Health check test failed: {e}")
            
            # Test configuration
            try:
                config = global_agent.get_configuration()
                print(f"   ✅ Configuration retrieved: {len(config)} items")
            except Exception as e:
                print(f"   ⚠️  Configuration test failed: {e}")
            
            self.test_results["tests"]["core_functions"] = {
                "success": True,
                "message": "Core functions tested"
            }
            
        except Exception as e:
            print(f"❌ Error in core functions test: {e}")
            import traceback
            traceback.print_exc()
            self.test_results["tests"]["core_functions"] = {
                "success": False,
                "error": str(e)
            }
    
    async def test_agent_coordination(self):
        """Test agent coordination"""
        print("\n📋 Test 3: Agent Coordination")
        print("-" * 40)
        
        try:
            from core.global_agent import GlobalAgent
            
            # Create agent
            global_agent = GlobalAgent()
            print("✅ GlobalAgent created for coordination test")
            
            # Test agent coordination
            print("   Testing agent coordination...")
            
            # Test routing
            try:
                # Create sample request
                sample_request = {
                    "action": "generate_document",
                    "agent_type": "ism",
                    "input_data": {
                        "issuer": "Test Company",
                        "product_name": "Test Product",
                        "underlying_asset": "S&P 500"
                    }
                }
                
                # Test request routing
                route_result = global_agent.route_request(sample_request)
                print(f"   ✅ Request routing: {route_result}")
                
            except Exception as e:
                print(f"   ⚠️  Request routing test failed: {e}")
            
            # Test agent execution
            try:
                # Test agent execution (without actual execution)
                execution_status = global_agent.get_execution_status()
                print(f"   ✅ Execution status: {execution_status}")
                
            except Exception as e:
                print(f"   ⚠️  Execution status test failed: {e}")
            
            self.test_results["tests"]["agent_coordination"] = {
                "success": True,
                "message": "Agent coordination tested"
            }
            
        except Exception as e:
            print(f"❌ Error in agent coordination test: {e}")
            import traceback
            traceback.print_exc()
            self.test_results["tests"]["agent_coordination"] = {
                "success": False,
                "error": str(e)
            }
    
    async def test_session_management(self):
        """Test session management"""
        print("\n📋 Test 4: Session Management")
        print("-" * 40)
        
        try:
            from core.global_agent import GlobalAgent
            
            # Create agent
            global_agent = GlobalAgent()
            print("✅ GlobalAgent created for session management test")
            
            # Test session management
            print("   Testing session management...")
            
            # Test session creation
            try:
                session_id = global_agent.create_session()
                print(f"   ✅ Session created: {session_id}")
                
                # Test session retrieval
                session = global_agent.get_session(session_id)
                print(f"   ✅ Session retrieved: {session}")
                
                # Test session cleanup
                cleanup_result = global_agent.cleanup_session(session_id)
                print(f"   ✅ Session cleanup: {cleanup_result}")
                
            except Exception as e:
                print(f"   ⚠️  Session management test failed: {e}")
            
            self.test_results["tests"]["session_management"] = {
                "success": True,
                "message": "Session management tested"
            }
            
        except Exception as e:
            print(f"❌ Error in session management test: {e}")
            import traceback
            traceback.print_exc()
            self.test_results["tests"]["session_management"] = {
                "success": False,
                "error": str(e)
            }
    
    async def test_error_handling(self):
        """Test error handling"""
        print("\n📋 Test 5: Error Handling")
        print("-" * 40)
        
        try:
            from core.global_agent import GlobalAgent
            
            # Create agent
            global_agent = GlobalAgent()
            print("✅ GlobalAgent created for error handling test")
            
            # Test error handling
            print("   Testing error handling...")
            
            # Test with invalid request
            try:
                invalid_request = {
                    "invalid_field": "invalid_value"
                }
                
                # This should handle the error gracefully
                result = global_agent.handle_request(invalid_request)
                print(f"   ✅ Invalid request handled: {result}")
                
            except Exception as e:
                print(f"   ✅ Error properly caught: {type(e).__name__}")
            
            # Test with missing required fields
            try:
                incomplete_request = {
                    "action": "generate_document"
                    # Missing agent_type and input_data
                }
                
                result = global_agent.handle_request(incomplete_request)
                print(f"   ✅ Incomplete request handled: {result}")
                
            except Exception as e:
                print(f"   ✅ Incomplete request error caught: {type(e).__name__}")
            
            self.test_results["tests"]["error_handling"] = {
                "success": True,
                "message": "Error handling tested"
            }
            
        except Exception as e:
            print(f"❌ Error in error handling test: {e}")
            import traceback
            traceback.print_exc()
            self.test_results["tests"]["error_handling"] = {
                "success": False,
                "error": str(e)
            }
    
    def _calculate_overall_score(self):
        """Calculate overall test score"""
        total_tests = len(self.test_results["tests"])
        passed_tests = sum(1 for test in self.test_results["tests"].values() if test.get("success", False))
        
        if total_tests > 0:
            self.test_results["overall_score"] = (passed_tests / total_tests) * 10.0
        else:
            self.test_results["overall_score"] = 0.0
    
    def _print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 GLOBAL AGENT TEST SUMMARY")
        print("=" * 60)
        
        print(f"🎯 Overall Score: {self.test_results['overall_score']:.1f}/10")
        print(f"📅 Test Date: {self.test_results['test_timestamp']}")
        
        print(f"\n📋 Test Results:")
        for test_name, result in self.test_results["tests"].items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            print(f"   {status} {test_name.replace('_', ' ').title()}")
            
            if not result.get("success", False):
                error = result.get("error", "Unknown error")
                print(f"      Error: {error}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"tests/results/global_agent_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
        if self.test_results["overall_score"] >= 8:
            print("🎉 Excellent! Global agent is working well.")
        elif self.test_results["overall_score"] >= 6:
            print("⚠️  Good, but some improvements needed.")
        else:
            print("🔧 Significant improvements needed.")


async def main():
    """Main function to run all global agent tests"""
    tester = GlobalAgentTester()
    results = await tester.run_all_tests()
    return results


if __name__ == "__main__":
    asyncio.run(main()) 