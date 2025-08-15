#!/usr/bin/env python3
"""
Standalone test script for Conversation and Feedback Management System.

This script tests the core conversation management functionality
by directly importing the conversation manager module.
"""

import asyncio
import json
import time
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import conversation manager directly
try:
    from core.conversation_manager import (
        ConversationManager, ConversationSession, UserFeedback, KnowledgeUpdate,
        FeedbackStatus, KnowledgeUpdateType, ConversationStatus
    )
    print("✅ Successfully imported conversation manager")
except ImportError as e:
    print(f"❌ Failed to import conversation manager: {e}")
    sys.exit(1)


class StandaloneConversationTester:
    """Standalone tester for conversation management system"""
    
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.test_results = {}
    
    async def run_basic_tests(self):
        """Run basic conversation management tests"""
        print("🧪 Standalone Conversation and Feedback Management System Tests")
        print("=" * 70)
        print()
        
        tests = [
            ("Conversation Creation", self.test_conversation_creation),
            ("Message Management", self.test_message_management),
            ("Feedback Collection", self.test_feedback_collection),
            ("Knowledge Update Workflow", self.test_knowledge_update_workflow),
            ("Audit Trail", self.test_audit_trail),
            ("Conversation Statistics", self.test_conversation_statistics),
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
        
        # Add messages
        message1 = self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="user",
            message_type="request",
            content="Generate a document",
            metadata={"priority": "high"}
        )
        
        message2 = self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="response",
            content="Document generated successfully",
            metadata={"processing_time": 2.5}
        )
        
        # Verify messages
        assert message1 is not None
        assert message2 is not None
        assert message1.content == "Generate a document"
        assert message2.content == "Document generated successfully"
        
        # Get conversation history
        history = self.conversation_manager.get_conversation_history(conversation.session_id)
        assert len(history) == 2
        
        return {
            "messages_added": 2,
            "history_length": len(history),
            "first_message": history[0].content,
            "last_message": history[-1].content
        }
    
    async def test_feedback_collection(self) -> Dict[str, Any]:
        """Test feedback collection functionality"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_789",
            title="Feedback Test"
        )
        
        # Add feedback
        feedback1 = self.conversation_manager.add_feedback(
            session_id=conversation.session_id,
            feedback_type="content_update",
            content="Add more risk information",
            target_agent="ism",
            priority="high"
        )
        
        feedback2 = self.conversation_manager.add_feedback(
            session_id=conversation.session_id,
            feedback_type="approval",
            content="Document looks good",
            priority="normal"
        )
        
        # Verify feedback
        assert feedback1 is not None
        assert feedback2 is not None
        assert feedback1.feedback_type == "content_update"
        assert feedback2.feedback_type == "approval"
        assert feedback1.target_agent == "ism"
        
        # Get feedback summary
        summary = self.conversation_manager.get_feedback_summary(conversation.session_id)
        assert summary["total_feedback"] == 2
        
        return {
            "feedback_added": 2,
            "feedback_types": [feedback1.feedback_type, feedback2.feedback_type],
            "target_agents": [feedback1.target_agent],
            "summary": summary
        }
    
    async def test_knowledge_update_workflow(self) -> Dict[str, Any]:
        """Test knowledge update workflow"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_knowledge",
            title="Knowledge Update Test"
        )
        
        # Add feedback that triggers knowledge update
        feedback = self.conversation_manager.add_feedback(
            session_id=conversation.session_id,
            feedback_type="knowledge_update",
            content="Add new regulatory requirements",
            target_agent="ism",
            priority="urgent"
        )
        
        # Create knowledge update
        knowledge_update = self.conversation_manager.create_knowledge_update(
            session_id=conversation.session_id,
            update_type=KnowledgeUpdateType.REGULATORY_UPDATE,
            target_agent="ism",
            content="Add new regulatory requirements for structured notes",
            source_feedback=feedback.feedback_id
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
            implementation_details={"regulations_added": 3}
        )
        
        # Verify workflow
        assert knowledge_update is not None
        assert approval_result is True
        assert implementation_result is True
        
        return {
            "knowledge_update_created": True,
            "update_type": knowledge_update.update_type.value,
            "approved": approval_result,
            "implemented": implementation_result
        }
    
    async def test_audit_trail(self) -> Dict[str, Any]:
        """Test audit trail functionality"""
        # Create conversation
        conversation = self.conversation_manager.create_conversation(
            user_id="test_user_audit",
            title="Audit Trail Test"
        )
        
        # Add some actions
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="user",
            message_type="request",
            content="Test audit trail"
        )
        
        self.conversation_manager.add_feedback(
            session_id=conversation.session_id,
            feedback_type="content_update",
            content="Test feedback",
            target_agent="ism"
        )
        
        # Get audit trail
        audit_entries = self.conversation_manager.get_audit_trail(
            session_id=conversation.session_id
        )
        
        # Verify audit trail
        assert len(audit_entries) > 0
        
        # Check for specific actions
        actions = [entry.action for entry in audit_entries]
        assert "conversation_created" in actions
        assert "message_added" in actions
        assert "feedback_added" in actions
        
        return {
            "audit_entries_count": len(audit_entries),
            "actions_found": actions,
            "has_conversation_created": "conversation_created" in actions,
            "has_message_added": "message_added" in actions,
            "has_feedback_added": "feedback_added" in actions
        }
    
    async def test_conversation_statistics(self) -> Dict[str, Any]:
        """Test conversation statistics"""
        # Create multiple conversations
        for i in range(3):
            conversation = self.conversation_manager.create_conversation(
                user_id=f"test_user_{i}",
                title=f"Test Conversation {i}"
            )
            
            # Add some messages and feedback
            self.conversation_manager.add_message(
                session_id=conversation.session_id,
                sender="user",
                message_type="request",
                content=f"Test message {i}"
            )
            
            self.conversation_manager.add_feedback(
                session_id=conversation.session_id,
                feedback_type="content_update",
                content=f"Test feedback {i}",
                target_agent="ism"
            )
        
        # Get statistics
        stats = self.conversation_manager.get_statistics()
        
        # Verify statistics
        assert "total_conversations" in stats
        assert "active_conversations" in stats
        assert "total_feedback" in stats
        assert "total_knowledge_updates" in stats
        
        return {
            "total_conversations": stats["total_conversations"],
            "active_conversations": stats["active_conversations"],
            "total_feedback": stats["total_feedback"],
            "total_knowledge_updates": stats["total_knowledge_updates"]
        }
    
    def print_test_summary(self):
        """Print test summary"""
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = 0
        failed = 0
        
        for test_name, result in self.test_results.items():
            status = result["status"]
            if status == "PASS":
                passed += 1
                print(f"✅ {test_name}: PASS")
            else:
                failed += 1
                print(f"❌ {test_name}: FAIL")
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print()
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed / len(self.test_results)) * 100:.1f}%")
        
        if failed == 0:
            print("\n🎉 All tests passed! Conversation management system is working correctly.")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please check the implementation.")


async def main():
    """Main test function"""
    tester = StandaloneConversationTester()
    await tester.run_basic_tests()


if __name__ == "__main__":
    asyncio.run(main()) 