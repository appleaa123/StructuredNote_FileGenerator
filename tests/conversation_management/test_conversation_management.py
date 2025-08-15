"""
Comprehensive test script for Conversation and Feedback Management System.

This script tests all components of the conversation management system:
- Conversation state management
- User feedback collection and processing
- Knowledge update approval workflows
- Agent-specific feedback routing
- Audit trail for changes
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any

from core.conversation_manager import (
    ConversationManager, ConversationSession, UserFeedback, KnowledgeUpdate,
    FeedbackStatus, KnowledgeUpdateType, ConversationStatus
)
from core.global_agent import GlobalAgent, FeedbackType, ConversationState


class ConversationManagementTester:
    """Comprehensive tester for conversation management system"""
    
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.global_agent = GlobalAgent()
        self.test_results = {}
    
    async def run_all_tests(self):
        """Run all conversation management tests"""
        print("🧪 Conversation and Feedback Management System Tests")
        print("=" * 65)
        print()
        
        tests = [
            ("Conversation Creation", self.test_conversation_creation),
            ("Message Management", self.test_message_management),
            ("Feedback Collection", self.test_feedback_collection),
            ("Feedback Processing", self.test_feedback_processing),
            ("Knowledge Update Workflow", self.test_knowledge_update_workflow),
            ("Audit Trail", self.test_audit_trail),
            ("Conversation Statistics", self.test_conversation_statistics),
            ("GlobalAgent Integration", self.test_global_agent_integration),
            ("Session Management", self.test_session_management),
            ("Error Handling", self.test_error_handling)
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
    
    async def test_conversation_creation(self) -> Dict[str, Any]:
        """Test conversation creation functionality"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_123",
            title="Test Document Generation",
            description="Testing conversation management system",
            tags=["test", "document_generation"]
        )
        
        # Verify conversation properties
        assert conversation.session_id is not None
        assert conversation.user_id == "test_user_123"
        assert conversation.title == "Test Document Generation"
        assert conversation.status == ConversationStatus.ACTIVE
        assert len(conversation.tags) == 2
        
        # Test conversation retrieval
        retrieved_conversation = self.conversation_manager.get_conversation(conversation.session_id)
        assert retrieved_conversation is not None
        assert retrieved_conversation.session_id == conversation.session_id
        
        return {
            "conversation_created": True,
            "session_id": conversation.session_id,
            "user_id": conversation.user_id,
            "title": conversation.title,
            "status": conversation.status.value,
            "tags": conversation.tags
        }
    
    async def test_message_management(self) -> Dict[str, Any]:
        """Test message management functionality"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_456",
            title="Message Management Test"
        )
        
        session_id = conversation.session_id
        
        # Add various message types
        messages = [
            ("user", "request", "Generate an investor summary"),
            ("system", "response", "Processing your request..."),
            ("ism", "document_generated", "Document generated successfully"),
            ("user", "feedback", "Add more risk information"),
            ("system", "feedback_processed", "Feedback processed")
        ]
        
        added_messages = []
        for sender, message_type, content in messages:
            message = self.conversation_manager.add_message(
                session_id=session_id,
                sender=sender,
                message_type=message_type,
                content=content
            )
            added_messages.append(message)
        
        # Test message retrieval
        all_messages = self.conversation_manager.get_conversation_history(session_id)
        user_messages = self.conversation_manager.get_conversation_history(
            session_id, message_types=["request", "feedback"]
        )
        
        return {
            "messages_added": len(added_messages),
            "total_messages": len(all_messages),
            "user_messages": len(user_messages),
            "session_id": session_id
        }
    
    async def test_feedback_collection(self) -> Dict[str, Any]:
        """Test feedback collection functionality"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_789",
            title="Feedback Collection Test"
        )
        
        session_id = conversation.session_id
        
        # Add different types of feedback
        feedback_types = [
            ("approval", "Document looks great", "normal"),
            ("rejection", "Please regenerate with more details", "high"),
            ("content_update", "Add more risk information", "normal"),
            ("knowledge_update", "Update with new regulations", "urgent"),
            ("clarification", "Need clarification on barrier levels", "low")
        ]
        
        added_feedback = []
        for feedback_type, content, priority in feedback_types:
            feedback = self.conversation_manager.add_feedback(
                session_id=session_id,
                feedback_type=feedback_type,
                content=content,
                priority=priority,
                target_agent="ism"
            )
            added_feedback.append(feedback)
        
        # Test feedback summary
        feedback_summary = self.conversation_manager.get_feedback_summary(session_id)
        
        return {
            "feedback_added": len(added_feedback),
            "total_feedback": feedback_summary["total_feedback"],
            "feedback_by_type": feedback_summary["feedback_by_type"],
            "feedback_by_status": feedback_summary["feedback_by_status"],
            "pending_feedback": feedback_summary["pending_feedback"]
        }
    
    async def test_feedback_processing(self) -> Dict[str, Any]:
        """Test feedback processing functionality"""
        # Create conversation and add feedback
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_101",
            title="Feedback Processing Test"
        )
        
        session_id = conversation.session_id
        
        feedback = self.conversation_manager.add_feedback(
            session_id=session_id,
            feedback_type="content_update",
            content="Add more risk information",
            target_agent="ism"
        )
        
        # Process feedback
        processing_result = self.conversation_manager.process_feedback(
            feedback_id=feedback.feedback_id,
            processor="ism_agent",
            status=FeedbackStatus.APPROVED,
            result={"action_taken": "Added risk section", "processing_time": 2.5}
        )
        
        # Verify processing
        assert processing_result == True
        
        # Check updated feedback
        updated_feedback = None
        for conv in self.conversation_manager.active_conversations.values():
            for fb in conv.feedback_history:
                if fb.feedback_id == feedback.feedback_id:
                    updated_feedback = fb
                    break
            if updated_feedback:
                break
        
        return {
            "feedback_processed": processing_result,
            "feedback_status": updated_feedback.status.value if updated_feedback else "unknown",
            "processor": updated_feedback.processed_by if updated_feedback else None,
            "processing_time": updated_feedback.metadata.get("processing_time") if updated_feedback else None
        }
    
    async def test_knowledge_update_workflow(self) -> Dict[str, Any]:
        """Test knowledge update workflow"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_202",
            title="Knowledge Update Workflow Test"
        )
        
        session_id = conversation.session_id
        
        # Create knowledge update
        knowledge_update = self.conversation_manager.create_knowledge_update(
            session_id=session_id,
            update_type=KnowledgeUpdateType.PRODUCT_KNOWLEDGE,
            target_agent="ism",
            content="Add new autocallable product templates",
            source_feedback="feedback_123"
        )
        
        # Approve knowledge update
        approval_result = self.conversation_manager.approve_knowledge_update(
            update_id=knowledge_update.update_id,
            approver="admin_user",
            comments="Approved for implementation"
        )
        
        # Implement knowledge update
        implementation_result = self.conversation_manager.implement_knowledge_update(
            update_id=knowledge_update.update_id,
            implementer="ism_agent",
            implementation_details={"templates_added": 5, "implementation_time": 10.5}
        )
        
        # Get knowledge update summary
        update_summary = self.conversation_manager.get_knowledge_update_summary(session_id)
        
        return {
            "knowledge_update_created": knowledge_update is not None,
            "update_approved": approval_result,
            "update_implemented": implementation_result,
            "total_updates": update_summary["total_updates"],
            "updates_by_status": update_summary["updates_by_status"]
        }
    
    async def test_audit_trail(self) -> Dict[str, Any]:
        """Test audit trail functionality"""
        # Create conversation and perform various actions
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_303",
            title="Audit Trail Test"
        )
        
        session_id = conversation.session_id
        
        # Perform actions that generate audit entries
        self.conversation_manager.add_message(
            session_id=session_id,
            sender="user",
            message_type="request",
            content="Test message for audit"
        )
        
        self.conversation_manager.add_feedback(
            session_id=session_id,
            feedback_type="approval",
            content="Test feedback"
        )
        
        # Get audit trail
        audit_entries = self.conversation_manager.get_audit_trail(session_id=session_id)
        
        # Get audit trail for specific actions
        message_audits = self.conversation_manager.get_audit_trail(
            session_id=session_id,
            action_types=["message_added", "feedback_added"]
        )
        
        return {
            "total_audit_entries": len(audit_entries),
            "message_audits": len(message_audits),
            "audit_actions": [entry.action for entry in audit_entries],
            "session_id": session_id
        }
    
    async def test_conversation_statistics(self) -> Dict[str, Any]:
        """Test conversation statistics"""
        # Create multiple conversations with various activities
        conversations = []
        for i in range(3):
            conversation = self.conversation_manager.create_conversation(
                user_id=f"test_user_{i}",
                title=f"Statistics Test {i}"
            )
            conversations.append(conversation)
            
            # Add messages and feedback
            for j in range(2):
                self.conversation_manager.add_message(
                    session_id=conversation.session_id,
                    sender="user",
                    message_type="request",
                    content=f"Test message {j}"
                )
            
            self.conversation_manager.add_feedback(
                session_id=conversation.session_id,
                feedback_type="approval",
                content="Test feedback"
            )
        
        # Get statistics
        stats = self.conversation_manager.get_statistics()
        
        return {
            "total_conversations": stats["total_conversations"],
            "active_conversations": stats["active_conversations"],
            "total_feedback": stats["total_feedback"],
            "pending_feedback": stats["pending_feedback"],
            "conversation_stats": stats["conversation_stats"],
            "feedback_stats": stats["feedback_stats"]
        }
    
    async def test_global_agent_integration(self) -> Dict[str, Any]:
        """Test GlobalAgent integration with conversation management"""
        # Process a request through GlobalAgent
        response = await self.global_agent.process_request(
            "Generate an investor summary for a structured note"
        )
        
        session_id = response.session_id
        
        # Add feedback through GlobalAgent
        feedback_response = await self.global_agent.handle_feedback(
            session_id=session_id,
            feedback="Add more risk information",
            feedback_type=FeedbackType.CONTENT_UPDATE,
            target_agent="ism",
            priority="high"
        )
        
        # Get conversation data
        conversation = self.global_agent.get_session_info(session_id)
        conversation_history = self.global_agent.get_conversation_history(session_id)
        feedback_summary = self.global_agent.get_feedback_summary(session_id)
        
        return {
            "request_processed": response.success,
            "feedback_processed": feedback_response.success,
            "conversation_created": conversation is not None,
            "messages_count": len(conversation_history),
            "feedback_count": feedback_summary.get("total_feedback", 0)
        }
    
    async def test_session_management(self) -> Dict[str, Any]:
        """Test session management functionality"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_404",
            title="Session Management Test"
        )
        
        session_id = conversation.session_id
        
        # Add some activity
        self.conversation_manager.add_message(
            session_id=session_id,
            sender="user",
            message_type="request",
            content="Test message"
        )
        
        # Archive conversation
        archive_result = self.conversation_manager.archive_conversation(session_id)
        
        # Try to get archived conversation
        archived_conversation = self.conversation_manager.get_conversation(session_id)
        
        return {
            "conversation_created": conversation is not None,
            "archived": archive_result,
            "archived_conversation_retrievable": archived_conversation is None,  # Should be None after archiving
            "session_id": session_id
        }
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling in conversation management"""
        error_tests = []
        
        # Test invalid session ID
        try:
            invalid_conversation = self.conversation_manager.get_conversation("invalid_session_id")
            error_tests.append({
                "test": "Invalid session ID",
                "expected_failure": True,
                "actual_result": invalid_conversation is None
            })
        except Exception as e:
            error_tests.append({
                "test": "Invalid session ID",
                "expected_failure": True,
                "actual_result": True,
                "error": str(e)
            })
        
        # Test adding message to non-existent session
        try:
            message = self.conversation_manager.add_message(
                session_id="non_existent_session",
                sender="user",
                message_type="request",
                content="Test message"
            )
            error_tests.append({
                "test": "Message to non-existent session",
                "expected_failure": True,
                "actual_result": message is None
            })
        except Exception as e:
            error_tests.append({
                "test": "Message to non-existent session",
                "expected_failure": True,
                "actual_result": True,
                "error": str(e)
            })
        
        # Test processing non-existent feedback
        try:
            result = self.conversation_manager.process_feedback(
                feedback_id="non_existent_feedback",
                processor="test_processor",
                status=FeedbackStatus.APPROVED
            )
            error_tests.append({
                "test": "Process non-existent feedback",
                "expected_failure": True,
                "actual_result": result == False
            })
        except Exception as e:
            error_tests.append({
                "test": "Process non-existent feedback",
                "expected_failure": True,
                "actual_result": True,
                "error": str(e)
            })
        
        return {
            "error_tests": len(error_tests),
            "expected_failures": len([t for t in error_tests if t.get("expected_failure", False)]),
            "actual_failures": len([t for t in error_tests if t.get("actual_result", False)]),
            "error_details": error_tests
        }
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("📊 Conversation Management Test Summary")
        print("=" * 45)
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
    """Run all conversation management tests"""
    tester = ConversationManagementTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main()) 