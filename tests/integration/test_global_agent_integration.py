# --- Auto-install dev test dependencies if missing (best-effort) ---
try:
    import importlib, sys, subprocess  # type: ignore
    for _pkg in ("pytest", "python-docx"):
        mod_name = "docx" if _pkg == "python-docx" else _pkg
        try:
            importlib.import_module(mod_name)
        except Exception:
            subprocess.run([sys.executable, "-m", "pip", "install", _pkg], check=False)
except Exception:
    pass

import asyncio
from core.global_agent import GlobalAgent


def test_global_agent_runs_with_large_text_paths():
    ga = GlobalAgent()
    # NL prompt that should route to ISM but we explicitly select others via agents param
    prompt = "Create a prospectus supplement and pricing supplement for an autocallable linked to S&P 500."

    # Call process_request and then explicitly execute PDS/PRS via internal API using use_large_text_templates
    # Since process_request does its own routing, we directly exercise _execute_agent through public API by crafting
    # a request that includes the flags in extracted_data-like dict. This is a smoke test that should not raise.
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(
        ga.process_request(
            prompt,
            use_large_text_templates=True,
            render_docx=False,
            audience="retail",
        )
    )
    assert response.session_id

    # Manually execute PDS via large-text + docx path with minimal inputs (defaults will be scaffolded)
    pds_result = loop.run_until_complete(
        ga._execute_agent(
            "pds",
            {
                "use_large_text_templates": True,
                "render_docx": True,
                "audience": "retail",
            },
            response.session_id,
        )
    )
    assert isinstance(pds_result.success, bool)

    prs_result = loop.run_until_complete(
        ga._execute_agent(
            "prs",
            {
                "use_large_text_templates": True,
                "render_docx": True,
                "audience": "retail",
            },
            response.session_id,
        )
    )
    assert isinstance(prs_result.success, bool)


def test_bsp_llm_path_smoke():
    ga = GlobalAgent()
    loop = asyncio.get_event_loop()
    # Non-large-text default LLM path; defaults will be scaffolded
    result = loop.run_until_complete(
        ga._execute_agent(
            "bsp",
            {
                # no large-text flags
                "issuer": "Example Bank",
                "program_name": "Structured Products Program",
                "shelf_amount": 50000000.0,
                "currency": "USD",
                "regulatory_jurisdiction": "Canada",
            },
            session_id="test_bsp_session",
        )
    )
    assert isinstance(result.success, bool)
"""
GlobalAgent Integration Tests

This module tests the GlobalAgent's integration capabilities including:
- Session management
- Agent coordination
- Result aggregation
- Feedback processing
- Conversation state transitions
- Error recovery mechanisms
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import Dict, List, Any, Optional
import sys
import os
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.global_agent import GlobalAgent, GlobalAgentResponse, ConversationState, FeedbackType, AgentResult
from core.router import RoutingDecision, AgentType
from core.conversation_manager import ConversationSession, UserFeedback


class TestGlobalAgentIntegration:
    """Test class for GlobalAgent integration scenarios"""
    
    @pytest.fixture
    def global_agent(self):
        """Create a fresh GlobalAgent instance for each test"""
        return GlobalAgent()
    
    @pytest.fixture
    def sample_ism_request(self):
        """Sample ISM request"""
        return "Generate an investor summary for a SP 500 autocallable note issued by Global Finance Inc"
    
    @pytest.fixture
    def sample_multi_agent_request(self):
        """Sample multi-agent request"""
        return "Create both an investor summary and base shelf prospectus for a structured note product"
    
    @pytest.fixture
    def mock_routing_decision(self):
        """Mock routing decision for testing"""
        return RoutingDecision(
            primary_agent=AgentType.ISM,
            secondary_agents=[AgentType.BSP],
            extracted_data={
                "issuer": "Global Finance Inc",
                "product_name": "SP 500 autocallable note",
                "principal_amount": 10000.0
            },
            confidence_score=0.85,
            reasoning="Request clearly asks for investor summary",
            task_decomposition=[
                {
                    "task_type": "document_generation",
                    "agent_type": "ism",
                    "description": "Generate investor summary",
                    "priority": "high"
                }
            ]
        )

    @pytest.mark.asyncio
    async def test_session_management(self, global_agent, sample_ism_request):
        """Test session management capabilities"""
        print("\n=== Testing Session Management ===")
        
        # Test session creation
        session_id = "test_session_001"
        response = await global_agent.process_request(sample_ism_request, session_id)
        
        # Verify session was created
        assert response.session_id == session_id
        assert response.success is True
        assert response.conversation_state in [ConversationState.PROCESSING, ConversationState.COMPLETED]
        
        # Test session retrieval
        session_info = global_agent.get_session_info(session_id)
        assert session_info is not None
        assert session_info.session_id == session_id
        assert session_info.user_request == sample_ism_request
        
        # Test session cleanup
        cleanup_result = global_agent.cleanup_session(session_id)
        assert cleanup_result is True
        
        print(f"✓ Session created: {response.session_id}")
        print(f"✓ Session state: {response.conversation_state}")
        print(f"✓ Session cleanup: {cleanup_result}")

    @pytest.mark.asyncio
    async def test_agent_coordination(self, global_agent, sample_multi_agent_request):
        """Test agent coordination for multi-agent requests"""
        print("\n=== Testing Agent Coordination ===")
        
        # Mock the agent execution to avoid actual agent calls
        with patch.object(global_agent, '_execute_agent', new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = AgentResult(
                agent_type="ism",
                success=True,
                processing_time=1.5,
                output={"document": "Sample ISM document"},
                metadata={"word_count": 500}
            )
            
            response = await global_agent.process_request(sample_multi_agent_request)
            
            # Verify coordination
            assert response.success is True
            assert response.primary_result is not None
            assert response.primary_result.success is True
            assert len(response.secondary_results) >= 0
            
            # Verify agent execution was called
            assert mock_execute.called
            
        print(f"✓ Primary result success: {response.primary_result.success}")
        print(f"✓ Secondary results count: {len(response.secondary_results)}")
        print(f"✓ Agent execution called: {mock_execute.called}")

    @pytest.mark.asyncio
    async def test_result_aggregation(self, global_agent, sample_multi_agent_request):
        """Test result aggregation from multiple agents"""
        print("\n=== Testing Result Aggregation ===")
        
        # Mock multiple agent results
        with patch.object(global_agent, '_execute_agent', new_callable=AsyncMock) as mock_execute:
            mock_execute.side_effect = [
                AgentResult(
                    agent_type="ism",
                    success=True,
                    processing_time=1.5,
                    output={"document": "ISM Document", "word_count": 500}
                ),
                AgentResult(
                    agent_type="bsp",
                    success=True,
                    processing_time=2.0,
                    output={"document": "BSP Document", "word_count": 800}
                )
            ]
            
            response = await global_agent.process_request(sample_multi_agent_request)
            
            # Verify aggregation
            assert response.success is True
            assert response.aggregated_content is not None
            assert len(response.aggregated_content) > 0
            
            # Verify aggregated content structure
            assert "documents" in response.aggregated_content or "results" in response.aggregated_content
            
        print(f"✓ Aggregated content keys: {list(response.aggregated_content.keys())}")
        print(f"✓ Aggregation successful: {response.success}")

    @pytest.mark.asyncio
    async def test_feedback_processing(self, global_agent, sample_ism_request):
        """Test feedback processing capabilities"""
        print("\n=== Testing Feedback Processing ===")
        
        # First process a request to create a session
        session_id = "feedback_test_session"
        initial_response = await global_agent.process_request(sample_ism_request, session_id)
        
        # Test approval feedback
        approval_response = await global_agent.handle_feedback(
            session_id=session_id,
            feedback="The document looks good, please proceed",
            feedback_type=FeedbackType.APPROVAL
        )
        
        assert approval_response.success is True
        assert approval_response.conversation_state == ConversationState.COMPLETED
        
        # Test content update feedback
        update_response = await global_agent.handle_feedback(
            session_id=session_id,
            feedback="Please add more risk disclosure information",
            feedback_type=FeedbackType.CONTENT_UPDATE
        )
        
        assert update_response.success is True
        assert update_response.conversation_state in [ConversationState.PROCESSING, ConversationState.UPDATING]
        
        print(f"✓ Approval feedback processed: {approval_response.success}")
        print(f"✓ Update feedback processed: {update_response.success}")

    @pytest.mark.asyncio
    async def test_conversation_state_transitions(self, global_agent, sample_ism_request):
        """Test conversation state transitions"""
        print("\n=== Testing Conversation State Transitions ===")
        
        session_id = "state_transition_test"
        
        # Test initial state
        response = await global_agent.process_request(sample_ism_request, session_id)
        initial_state = response.conversation_state
        
        # Test state transitions based on feedback
        states_observed = [initial_state]
        
        # Test rejection feedback
        rejection_response = await global_agent.handle_feedback(
            session_id=session_id,
            feedback="This needs to be completely redone",
            feedback_type=FeedbackType.REJECTION
        )
        states_observed.append(rejection_response.conversation_state)
        
        # Test knowledge update feedback
        knowledge_response = await global_agent.handle_feedback(
            session_id=session_id,
            feedback="Update the knowledge base with new regulations",
            feedback_type=FeedbackType.KNOWLEDGE_UPDATE
        )
        states_observed.append(knowledge_response.conversation_state)
        
        # Verify state transitions
        assert len(set(states_observed)) >= 2  # At least 2 different states
        assert ConversationState.ERROR not in states_observed
        
        print(f"✓ States observed: {states_observed}")
        print(f"✓ Unique states: {len(set(states_observed))}")

    @pytest.mark.asyncio
    async def test_error_recovery_mechanisms(self, global_agent):
        """Test error recovery mechanisms"""
        print("\n=== Testing Error Recovery Mechanisms ===")
        
        # Test with invalid request
        invalid_request = ""
        response = await global_agent.process_request(invalid_request)
        
        # Should handle gracefully
        assert response.conversation_state != ConversationState.ERROR
        assert response.success is False or response.confidence_score < 0.5
        
        # Test with malformed session ID
        try:
            await global_agent.handle_feedback(
                session_id="nonexistent_session",
                feedback="test",
                feedback_type=FeedbackType.APPROVAL
            )
        except Exception as e:
            # Should handle gracefully
            assert "session" in str(e).lower() or "not found" in str(e).lower()
        
        print(f"✓ Invalid request handled: {response.success}")
        print(f"✓ Error recovery successful")

    @pytest.mark.asyncio
    async def test_conversation_history_management(self, global_agent, sample_ism_request):
        """Test conversation history management"""
        print("\n=== Testing Conversation History Management ===")
        
        session_id = "history_test_session"
        
        # Process multiple requests
        await global_agent.process_request(sample_ism_request, session_id)
        await global_agent.handle_feedback(session_id, "Good", FeedbackType.APPROVAL)
        await global_agent.handle_feedback(session_id, "Update needed", FeedbackType.CONTENT_UPDATE)
        
        # Test history retrieval
        history = global_agent.get_conversation_history(session_id)
        assert len(history) >= 3  # At least 3 interactions
        
        # Test feedback summary
        feedback_summary = global_agent.get_feedback_summary(session_id)
        assert feedback_summary is not None
        assert "feedback_count" in feedback_summary or "feedback_types" in feedback_summary
        
        # Test knowledge update summary
        knowledge_summary = global_agent.get_knowledge_update_summary(session_id)
        assert knowledge_summary is not None
        
        print(f"✓ History entries: {len(history)}")
        print(f"✓ Feedback summary: {feedback_summary}")
        print(f"✓ Knowledge summary: {knowledge_summary}")

    def test_agent_status_retrieval(self, global_agent):
        """Test agent status retrieval"""
        print("\n=== Testing Agent Status Retrieval ===")
        
        status = global_agent.get_agent_status()
        
        # Verify status structure
        assert isinstance(status, dict)
        assert len(status) > 0
        
        # Verify agent information
        for agent_name, agent_info in status.items():
            assert "status" in agent_info
            assert "capabilities" in agent_info or "description" in agent_info
        
        print(f"✓ Available agents: {list(status.keys())}")
        print(f"✓ Status structure valid: {isinstance(status, dict)}")

    @pytest.mark.asyncio
    async def test_audit_trail_functionality(self, global_agent, sample_ism_request):
        """Test audit trail functionality"""
        print("\n=== Testing Audit Trail Functionality ===")
        
        session_id = "audit_test_session"
        
        # Perform some actions
        await global_agent.process_request(sample_ism_request, session_id)
        await global_agent.handle_feedback(session_id, "Test feedback", FeedbackType.APPROVAL)
        
        # Test audit trail retrieval
        audit_trail = global_agent.get_audit_trail(session_id=session_id, hours=24)
        assert isinstance(audit_trail, list)
        
        # Test global audit trail
        global_audit = global_agent.get_audit_trail(hours=24)
        assert isinstance(global_audit, list)
        
        print(f"✓ Session audit entries: {len(audit_trail)}")
        print(f"✓ Global audit entries: {len(global_audit)}")

    @pytest.mark.asyncio
    async def test_conversation_statistics(self, global_agent):
        """Test conversation statistics"""
        print("\n=== Testing Conversation Statistics ===")
        
        stats = global_agent.get_conversation_statistics()
        
        # Verify statistics structure
        assert isinstance(stats, dict)
        assert "total_sessions" in stats or "active_sessions" in stats
        
        print(f"✓ Statistics keys: {list(stats.keys())}")
        print(f"✓ Statistics valid: {isinstance(stats, dict)}")

    @pytest.mark.asyncio
    async def test_edge_cases_and_error_handling(self, global_agent):
        """Test edge cases and error handling"""
        print("\n=== Testing Edge Cases and Error Handling ===")
        
        # Test with very long request
        long_request = "Generate document " * 1000
        response = await global_agent.process_request(long_request)
        assert response.success is False or response.confidence_score < 0.5
        
        # Test with special characters
        special_request = "Generate ISM for S&P 500® note with 100% protection"
        response = await global_agent.process_request(special_request)
        assert response.success is True
        
        # Test concurrent session handling
        session_ids = [f"concurrent_{i}" for i in range(5)]
        responses = []
        
        for session_id in session_ids:
            response = await global_agent.process_request("Test request", session_id)
            responses.append(response)
        
        # All should succeed
        success_count = sum(1 for r in responses if r.success)
        assert success_count >= 3  # At least 3 should succeed
        
        print(f"✓ Long request handled: {response.success}")
        print(f"✓ Special chars handled: {response.success}")
        print(f"✓ Concurrent sessions successful: {success_count}/{len(responses)}")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"]) 