"""
Comprehensive test script for Phase 2 GlobalAgent orchestration layer.

This script tests all components of the Phase 2 implementation:
- GlobalAgent orchestration
- Agent registry and factory
- Health monitoring
- Request routing and processing
- User feedback handling
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any

from core.global_agent import GlobalAgent, FeedbackType, ConversationState
from agents import agent_registry, get_agent_status_summary, AgentStatus, AgentCapability
from agents.factory import agent_factory, create_agent_with_factory
from agents.monitor import agent_monitor, start_monitoring, stop_monitoring, get_monitoring_summary


class Phase2Tester:
    """Comprehensive tester for Phase 2 components"""
    
    def __init__(self):
        self.global_agent = GlobalAgent()
        self.test_results = {}
        self.start_time = datetime.now()
    
    async def run_all_tests(self):
        """Run all Phase 2 tests"""
        print("🧪 Phase 2 GlobalAgent Orchestration Layer Tests")
        print("=" * 60)
        print()
        
        tests = [
            ("Agent Registry", self.test_agent_registry),
            ("Agent Factory", self.test_agent_factory),
            ("Health Monitoring", self.test_health_monitoring),
            ("GlobalAgent Initialization", self.test_global_agent_init),
            ("Request Routing", self.test_request_routing),
            ("Agent Execution", self.test_agent_execution),
            ("Feedback Processing", self.test_feedback_processing),
            ("Session Management", self.test_session_management),
            ("Error Handling", self.test_error_handling),
            ("Performance Metrics", self.test_performance_metrics)
        ]
        
        for test_name, test_func in tests:
            print(f"Running {test_name}...")
            try:
                result = await test_func()
                self.test_results[test_name] = {"status": "PASS", "details": result}
                print(f"✅ {test_name}: PASS")
            except Exception as e:
                self.test_results[test_name] = {"status": "FAIL", "error": str(e)}
                print(f"❌ {test_name}: FAIL - {e}")
            print()
        
        self.print_test_summary()
    
    async def test_agent_registry(self) -> Dict[str, Any]:
        """Test agent registry functionality"""
        # Test registry access
        registry = agent_registry
        all_agents = registry.get_all_agents()
        
        # Test agent metadata
        ism_metadata = registry.get_agent_metadata("ism")
        bsp_metadata = registry.get_agent_metadata("bsp")
        
        # Test capability filtering
        doc_gen_agents = registry.get_agents_by_capability(AgentCapability.DOCUMENT_GENERATION)
        available_agents = registry.get_agents_by_status(AgentStatus.AVAILABLE)
        
        # Test status summary
        status_summary = registry.get_agent_status_summary()
        
        return {
            "total_agents": len(all_agents),
            "ism_available": ism_metadata is not None,
            "bsp_available": bsp_metadata is not None,
            "doc_gen_agents_count": len(doc_gen_agents),
            "available_agents_count": len(available_agents),
            "status_summary": status_summary
        }
    
    async def test_agent_factory(self) -> Dict[str, Any]:
        """Test agent factory functionality"""
        # Test agent creation
        ism_agent = agent_factory.create_agent("ism")
        bsp_agent = agent_factory.create_agent("bsp")
        
        # Test agent creation with retry
        ism_agent_retry = agent_factory.create_agent_with_retry("ism")
        
        # Test capability-based creation
        doc_gen_agents = agent_factory.create_agents_by_capability(AgentCapability.DOCUMENT_GENERATION)
        
        # Test health checking
        ism_health = agent_factory.get_agent_health("ism")
        all_health = agent_factory.get_all_agent_health()
        
        return {
            "ism_created": ism_agent is not None,
            "bsp_created": bsp_agent is not None,
            "ism_retry_created": ism_agent_retry is not None,
            "doc_gen_agents_created": len(doc_gen_agents),
            "ism_health_checked": ism_health is not None,
            "all_health_checked": len(all_health) > 0
        }
    
    async def test_health_monitoring(self) -> Dict[str, Any]:
        """Test health monitoring functionality"""
        # Start monitoring
        start_monitoring()
        
        # Wait for initial checks
        await asyncio.sleep(3)
        
        # Test health checks
        ism_health = agent_monitor.run_health_check("ism")
        all_health = agent_monitor.run_all_health_checks()
        
        # Test performance metrics
        ism_metrics = agent_monitor.get_agent_performance("ism")
        all_metrics = agent_monitor.get_all_performance_metrics()
        
        # Test monitoring summary
        summary = agent_monitor.get_monitoring_summary()
        
        # Stop monitoring
        stop_monitoring()
        
        return {
            "ism_health_status": ism_health.status.value if ism_health else "unknown",
            "all_health_checks": len(all_health),
            "ism_metrics_available": ism_metrics is not None,
            "all_metrics_available": len(all_metrics) > 0,
            "monitoring_summary": summary
        }
    
    async def test_global_agent_init(self) -> Dict[str, Any]:
        """Test GlobalAgent initialization"""
        # Test GlobalAgent creation
        global_agent = GlobalAgent()
        
        # Test agent status
        agent_status = global_agent.get_agent_status()
        
        # Test session info (should be empty initially)
        session_info = global_agent.get_session_info("nonexistent")
        
        return {
            "global_agent_created": global_agent is not None,
            "router_available": hasattr(global_agent, 'router'),
            "sessions_available": hasattr(global_agent, 'sessions'),
            "agent_registry_available": hasattr(global_agent, 'agent_registry'),
            "agent_status_count": len(agent_status),
            "session_info_nonexistent": session_info is None
        }
    
    async def test_request_routing(self) -> Dict[str, Any]:
        """Test request routing functionality"""
        # Test different types of requests
        test_requests = [
            "Generate an investor summary for a structured note",
            "Create a base shelf prospectus for a program",
            "Generate a prospectus supplement",
            "Create a pricing supplement for a product"
        ]
        
        routing_results = []
        for request in test_requests:
            try:
                routing_decision = self.global_agent.router.analyze_request(request)
                routing_results.append({
                    "request": request[:50] + "...",
                    "primary_agent": routing_decision.primary_agent.value,
                    "confidence": routing_decision.confidence_score,
                    "secondary_agents": len(routing_decision.secondary_agents)
                })
            except Exception as e:
                routing_results.append({
                    "request": request[:50] + "...",
                    "error": str(e)
                })
        
        return {
            "routing_tests": len(routing_results),
            "successful_routing": len([r for r in routing_results if "error" not in r]),
            "routing_results": routing_results
        }
    
    async def test_agent_execution(self) -> Dict[str, Any]:
        """Test agent execution through GlobalAgent"""
        # Test with a simple ISM request
        test_request = "Generate an investor summary for a S&P 500 autocallable note from Global Finance Inc."
        
        try:
            response = await self.global_agent.process_request(test_request)
            
            return {
                "request_processed": True,
                "response_success": response.success,
                "session_id": response.session_id,
                "conversation_state": response.conversation_state.value,
                "primary_result_available": response.primary_result is not None,
                "confidence_score": response.confidence_score,
                "next_actions_count": len(response.next_actions)
            }
        except Exception as e:
            return {
                "request_processed": False,
                "error": str(e)
            }
    
    async def test_feedback_processing(self) -> Dict[str, Any]:
        """Test user feedback processing"""
        # Create a session first
        test_request = "Generate an investor summary for a structured note"
        response = await self.global_agent.process_request(test_request)
        session_id = response.session_id
        
        # Test different feedback types
        feedback_tests = [
            (FeedbackType.APPROVAL, "Document looks great"),
            (FeedbackType.REJECTION, "Please regenerate with more details"),
            (FeedbackType.CONTENT_UPDATE, "Add more risk information"),
            (FeedbackType.KNOWLEDGE_UPDATE, "Update knowledge base with new regulations"),
            (FeedbackType.CLARIFICATION_REQUEST, "Need clarification on barrier levels")
        ]
        
        feedback_results = []
        for feedback_type, feedback_text in feedback_tests:
            try:
                feedback_response = await self.global_agent.handle_feedback(
                    session_id=session_id,
                    feedback=feedback_text,
                    feedback_type=feedback_type
                )
                feedback_results.append({
                    "type": feedback_type.value,
                    "success": feedback_response.success,
                    "state": feedback_response.conversation_state.value
                })
            except Exception as e:
                feedback_results.append({
                    "type": feedback_type.value,
                    "error": str(e)
                })
        
        return {
            "session_created": session_id is not None,
            "feedback_tests": len(feedback_results),
            "successful_feedback": len([r for r in feedback_results if "error" not in r]),
            "feedback_results": feedback_results
        }
    
    async def test_session_management(self) -> Dict[str, Any]:
        """Test session management functionality"""
        # Create multiple sessions
        requests = [
            "Generate ISM document",
            "Create BSP document",
            "Generate PDS document"
        ]
        
        session_ids = []
        for request in requests:
            response = await self.global_agent.process_request(request)
            session_ids.append(response.session_id)
        
        # Test session info retrieval
        session_infos = []
        for session_id in session_ids:
            session_info = self.global_agent.get_session_info(session_id)
            session_infos.append({
                "session_id": session_id,
                "available": session_info is not None,
                "state": session_info.conversation_state.value if session_info else None
            })
        
        # Test session cleanup
        cleanup_results = []
        for session_id in session_ids:
            result = self.global_agent.cleanup_session(session_id)
            cleanup_results.append(result)
        
        return {
            "sessions_created": len(session_ids),
            "session_infos_retrieved": len(session_infos),
            "sessions_cleaned_up": sum(cleanup_results),
            "session_details": session_infos
        }
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling capabilities"""
        error_tests = [
            # Invalid agent type
            ("invalid_agent", "Test invalid agent"),
            # Empty request
            ("", "Test empty request"),
            # Malformed request
            ("Generate document with invalid data", "Test malformed request")
        ]
        
        error_results = []
        for agent_type, description in error_tests:
            try:
                if agent_type == "invalid_agent":
                    # Test invalid agent creation
                    agent = agent_factory.create_agent("invalid_agent_type")
                    error_results.append({
                        "test": description,
                        "success": agent is None,
                        "expected_failure": True
                    })
                else:
                    # Test request processing with potential errors
                    response = await self.global_agent.process_request(agent_type)
                    error_results.append({
                        "test": description,
                        "success": response.success,
                        "expected_failure": False
                    })
            except Exception as e:
                error_results.append({
                    "test": description,
                    "error": str(e),
                    "expected_failure": True
                })
        
        return {
            "error_tests": len(error_results),
            "expected_failures": len([r for r in error_results if r.get("expected_failure", False)]),
            "error_results": error_results
        }
    
    async def test_performance_metrics(self) -> Dict[str, Any]:
        """Test performance metrics collection"""
        # Run multiple operations to generate metrics
        operations = [
            ("Create ISM agent", lambda: agent_factory.create_agent("ism")),
            ("Create BSP agent", lambda: agent_factory.create_agent("bsp")),
            ("Health check ISM", lambda: agent_monitor.run_health_check("ism")),
            ("Process request", lambda: self.global_agent.process_request("Test request"))
        ]
        
        performance_results = []
        for operation_name, operation_func in operations:
            start_time = time.time()
            try:
                result = operation_func()
                if asyncio.iscoroutine(result):
                    result = await result
                duration = time.time() - start_time
                performance_results.append({
                    "operation": operation_name,
                    "success": True,
                    "duration": duration
                })
            except Exception as e:
                duration = time.time() - start_time
                performance_results.append({
                    "operation": operation_name,
                    "success": False,
                    "error": str(e),
                    "duration": duration
                })
        
        # Get performance metrics
        all_metrics = agent_monitor.get_all_performance_metrics()
        
        return {
            "operations_tested": len(performance_results),
            "successful_operations": len([r for r in performance_results if r["success"]]),
            "average_duration": sum(r["duration"] for r in performance_results) / len(performance_results),
            "metrics_available": len(all_metrics),
            "performance_results": performance_results
        }
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("📊 Phase 2 Test Summary")
        print("=" * 40)
        print()
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results.values() if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("Failed Tests:")
            for test_name, result in self.test_results.items():
                if result["status"] == "FAIL":
                    print(f"  ❌ {test_name}: {result.get('error', 'Unknown error')}")
            print()
        
        # Print detailed results for key tests
        print("Key Test Results:")
        for test_name, result in self.test_results.items():
            if result["status"] == "PASS" and "details" in result:
                details = result["details"]
                if isinstance(details, dict):
                    print(f"  ✅ {test_name}:")
                    for key, value in details.items():
                        if isinstance(value, (int, float, str, bool)):
                            print(f"    {key}: {value}")
                    print()


async def main():
    """Run all Phase 2 tests"""
    tester = Phase2Tester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main()) 