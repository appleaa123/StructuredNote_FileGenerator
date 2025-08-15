#!/usr/bin/env python3
"""
Minimal test script for Conversation and Feedback Management System.

This script tests the core conversation management functionality
by directly implementing the essential components.
"""

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ConversationStatus(Enum):
    """Status of a conversation"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    ERROR = "error"


class FeedbackStatus(Enum):
    """Status of feedback processing"""
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    FAILED = "failed"


class KnowledgeUpdateType(Enum):
    """Types of knowledge updates"""
    TEMPLATE_ADDITION = "template_addition"
    TEMPLATE_UPDATE = "template_update"
    REGULATORY_UPDATE = "regulatory_update"
    PRODUCT_KNOWLEDGE = "product_knowledge"
    RISK_INFORMATION = "risk_information"
    COMPLIANCE_RULE = "compliance_rule"
    BEST_PRACTICE = "best_practice"


@dataclass
class ConversationMessage:
    """Represents a message in a conversation"""
    message_id: str
    timestamp: datetime
    sender: str
    message_type: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    attachments: List[str] = field(default_factory=list)


@dataclass
class UserFeedback:
    """Represents user feedback"""
    feedback_id: str
    session_id: str
    timestamp: datetime
    feedback_type: str
    content: str
    target_agent: Optional[str] = None
    priority: str = "normal"
    status: FeedbackStatus = FeedbackStatus.PENDING
    processed_by: Optional[str] = None
    processed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeUpdate:
    """Represents a knowledge update request"""
    update_id: str
    session_id: str
    timestamp: datetime
    update_type: KnowledgeUpdateType
    target_agent: str
    content: str
    source_feedback: Optional[str] = None
    approval_required: bool = True
    status: FeedbackStatus = FeedbackStatus.PENDING
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    implemented_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEntry:
    """Represents an audit trail entry"""
    entry_id: str
    timestamp: datetime
    session_id: str
    action: str
    resource_type: str
    resource_id: str
    user_id: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class ConversationSession:
    """Enhanced conversation session with full state management"""
    session_id: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str] = None
    status: ConversationStatus = ConversationStatus.ACTIVE
    title: Optional[str] = None
    description: Optional[str] = None
    
    # Messages and interactions
    messages: List[ConversationMessage] = field(default_factory=list)
    feedback_history: List[UserFeedback] = field(default_factory=list)
    knowledge_updates: List[KnowledgeUpdate] = field(default_factory=list)
    
    # Agent interactions
    active_agents: Set[str] = field(default_factory=set)
    agent_results: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Audit trail
    audit_entries: List[AuditEntry] = field(default_factory=list)


class ConversationManager:
    """Main conversation management system"""
    
    def __init__(self, storage_path: str = "conversation_data/"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # In-memory storage for testing
        self.conversations: Dict[str, ConversationSession] = {}
        self.audit_entries: List[AuditEntry] = []
        
        # Load existing data
        self._load_existing_data()
    
    def create_conversation(
        self, 
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> ConversationSession:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        conversation = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            updated_at=now,
            title=title,
            description=description,
            tags=tags or []
        )
        
        self.conversations[session_id] = conversation
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=user_id,
            action="conversation_created",
            resource_type="conversation",
            resource_id=session_id,
            details={
                "title": title,
                "description": description,
                "tags": tags
            }
        )
        
        return conversation
    
    def get_conversation(self, session_id: str) -> Optional[ConversationSession]:
        """Get a conversation by session ID"""
        return self.conversations.get(session_id)
    
    def add_message(
        self, 
        session_id: str,
        sender: str,
        message_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[str]] = None
    ) -> Optional[ConversationMessage]:
        """Add a message to a conversation"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return None
        
        message_id = str(uuid.uuid4())
        now = datetime.now()
        
        message = ConversationMessage(
            message_id=message_id,
            timestamp=now,
            sender=sender,
            message_type=message_type,
            content=content,
            metadata=metadata or {},
            attachments=attachments or []
        )
        
        conversation.messages.append(message)
        conversation.updated_at = now
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=conversation.user_id,
            action="message_added",
            resource_type="message",
            resource_id=message_id,
            details={
                "sender": sender,
                "message_type": message_type,
                "content_length": len(content)
            }
        )
        
        return message
    
    def add_feedback(
        self,
        session_id: str,
        feedback_type: str,
        content: str,
        target_agent: Optional[str] = None,
        priority: str = "normal",
        user_id: Optional[str] = None
    ) -> Optional[UserFeedback]:
        """Add user feedback to a conversation"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return None
        
        feedback_id = str(uuid.uuid4())
        now = datetime.now()
        
        feedback = UserFeedback(
            feedback_id=feedback_id,
            session_id=session_id,
            timestamp=now,
            feedback_type=feedback_type,
            content=content,
            target_agent=target_agent,
            priority=priority,
            metadata={"user_id": user_id} if user_id else {}
        )
        
        conversation.feedback_history.append(feedback)
        conversation.updated_at = now
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=user_id or conversation.user_id,
            action="feedback_added",
            resource_type="feedback",
            resource_id=feedback_id,
            details={
                "feedback_type": feedback_type,
                "target_agent": target_agent,
                "priority": priority
            }
        )
        
        return feedback
    
    def create_knowledge_update(
        self,
        session_id: str,
        update_type: KnowledgeUpdateType,
        target_agent: str,
        content: str,
        source_feedback: Optional[str] = None,
        approval_required: bool = True,
        user_id: Optional[str] = None
    ) -> Optional[KnowledgeUpdate]:
        """Create a knowledge update request"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return None
        
        update_id = str(uuid.uuid4())
        now = datetime.now()
        
        knowledge_update = KnowledgeUpdate(
            update_id=update_id,
            session_id=session_id,
            timestamp=now,
            update_type=update_type,
            target_agent=target_agent,
            content=content,
            source_feedback=source_feedback,
            approval_required=approval_required
        )
        
        conversation.knowledge_updates.append(knowledge_update)
        conversation.updated_at = now
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=user_id or conversation.user_id,
            action="knowledge_update_created",
            resource_type="knowledge_update",
            resource_id=update_id,
            details={
                "update_type": update_type.value,
                "target_agent": target_agent,
                "approval_required": approval_required
            }
        )
        
        return knowledge_update
    
    def approve_knowledge_update(
        self,
        update_id: str,
        approver: str,
        comments: Optional[str] = None
    ) -> bool:
        """Approve a knowledge update"""
        # Find the knowledge update
        knowledge_update = None
        for conversation in self.conversations.values():
            for update in conversation.knowledge_updates:
                if update.update_id == update_id:
                    knowledge_update = update
                    break
            if knowledge_update:
                break
        
        if not knowledge_update:
            return False
        
        now = datetime.now()
        knowledge_update.status = FeedbackStatus.APPROVED
        knowledge_update.approved_by = approver
        knowledge_update.approved_at = now
        
        # Add audit entry
        self._add_audit_entry(
            session_id=knowledge_update.session_id,
            user_id=approver,
            action="knowledge_update_approved",
            resource_type="knowledge_update",
            resource_id=update_id,
            details={
                "approver": approver,
                "comments": comments
            }
        )
        
        return True
    
    def implement_knowledge_update(
        self,
        update_id: str,
        implementer: str,
        implementation_details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Implement a knowledge update"""
        # Find the knowledge update
        knowledge_update = None
        for conversation in self.conversations.values():
            for update in conversation.knowledge_updates:
                if update.update_id == update_id:
                    knowledge_update = update
                    break
            if knowledge_update:
                break
        
        if not knowledge_update:
            return False
        
        now = datetime.now()
        knowledge_update.status = FeedbackStatus.IMPLEMENTED
        knowledge_update.implemented_at = now
        if implementation_details:
            knowledge_update.metadata.update(implementation_details)
        
        # Add audit entry
        self._add_audit_entry(
            session_id=knowledge_update.session_id,
            user_id=implementer,
            action="knowledge_update_implemented",
            resource_type="knowledge_update",
            resource_id=update_id,
            details={
                "implementer": implementer,
                "implementation_details": implementation_details
            }
        )
        
        return True
    
    def get_conversation_history(
        self, 
        session_id: str, 
        limit: Optional[int] = None,
        message_types: Optional[List[str]] = None
    ) -> List[ConversationMessage]:
        """Get conversation history"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return []
        
        messages = conversation.messages
        
        # Filter by message types if specified
        if message_types:
            messages = [msg for msg in messages if msg.message_type in message_types]
        
        # Apply limit if specified
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def get_feedback_summary(self, session_id: str) -> Dict[str, Any]:
        """Get feedback summary for a session"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return {}
        
        feedback_by_type = {}
        feedback_by_status = {}
        
        for feedback in conversation.feedback_history:
            # Count by type
            feedback_by_type[feedback.feedback_type] = feedback_by_type.get(feedback.feedback_type, 0) + 1
            
            # Count by status
            feedback_by_status[feedback.status.value] = feedback_by_status.get(feedback.status.value, 0) + 1
        
        return {
            "total_feedback": len(conversation.feedback_history),
            "feedback_by_type": feedback_by_type,
            "feedback_by_status": feedback_by_status,
            "pending_feedback": feedback_by_status.get(FeedbackStatus.PENDING.value, 0)
        }
    
    def get_audit_trail(
        self, 
        session_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        action_types: Optional[List[str]] = None
    ) -> List[AuditEntry]:
        """Get audit trail with optional filtering"""
        entries = self.audit_entries
        
        # Filter by session ID
        if session_id:
            entries = [entry for entry in entries if entry.session_id == session_id]
        
        # Filter by time range
        if start_time:
            entries = [entry for entry in entries if entry.timestamp >= start_time]
        if end_time:
            entries = [entry for entry in entries if entry.timestamp <= end_time]
        
        # Filter by action types
        if action_types:
            entries = [entry for entry in entries if entry.action in action_types]
        
        return entries
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        total_conversations = len(self.conversations)
        active_conversations = len([c for c in self.conversations.values() if c.status == ConversationStatus.ACTIVE])
        
        total_feedback = sum(len(c.feedback_history) for c in self.conversations.values())
        total_knowledge_updates = sum(len(c.knowledge_updates) for c in self.conversations.values())
        
        return {
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "total_feedback": total_feedback,
            "total_knowledge_updates": total_knowledge_updates,
            "total_audit_entries": len(self.audit_entries)
        }
    
    def _add_audit_entry(
        self,
        session_id: str,
        user_id: Optional[str],
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Add an audit entry"""
        entry_id = str(uuid.uuid4())
        now = datetime.now()
        
        audit_entry = AuditEntry(
            entry_id=entry_id,
            timestamp=now,
            session_id=session_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {}
        )
        
        self.audit_entries.append(audit_entry)
    
    def _load_existing_data(self):
        """Load existing data from storage"""
        # For this minimal test, we start with empty data
        pass


class MinimalConversationTester:
    """Minimal tester for conversation management system"""
    
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.test_results = {}
    
    async def run_basic_tests(self):
        """Run basic conversation management tests"""
        print("🧪 Minimal Conversation and Feedback Management System Tests")
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
    tester = MinimalConversationTester()
    await tester.run_basic_tests()


if __name__ == "__main__":
    asyncio.run(main()) 