"""
Conversation and Feedback Management System.

This module provides comprehensive conversation management including:
- Conversation state tracking and persistence
- User feedback collection and processing
- Knowledge update approval workflows
- Agent-specific feedback routing
- Audit trail for all changes and interactions
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .config import global_config

# Configure logging
logging.basicConfig(level=global_config.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    sender: str  # "user" or "system" or agent_type
    message_type: str  # "request", "response", "feedback", "update", "error"
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    attachments: List[str] = field(default_factory=list)


@dataclass
class UserFeedback:
    """Represents user feedback"""
    feedback_id: str
    session_id: str
    timestamp: datetime
    feedback_type: str  # "approval", "rejection", "content_update", "knowledge_update", "clarification"
    content: str
    target_agent: Optional[str] = None
    priority: str = "normal"  # "low", "normal", "high", "urgent"
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
    resource_type: str  # "conversation", "feedback", "knowledge_update", "agent"
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
    """
    Comprehensive conversation and feedback management system.
    
    This class provides:
    - Conversation state management and persistence
    - User feedback collection and processing
    - Knowledge update approval workflows
    - Agent-specific feedback routing
    - Comprehensive audit trail
    - Conversation analytics and reporting
    """
    
    def __init__(self, storage_path: str = "conversation_data/"):
        """
        Initialize the conversation manager.
        
        Args:
            storage_path: Path for storing conversation data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Active conversations
        self.active_conversations: Dict[str, ConversationSession] = {}
        
        # Feedback processing queue
        self.feedback_queue: List[UserFeedback] = []
        
        # Knowledge update approval queue
        self.knowledge_update_queue: List[KnowledgeUpdate] = []
        
        # Audit trail
        self.audit_trail: List[AuditEntry] = []
        
        # Statistics
        self.stats = {
            "total_conversations": 0,
            "active_conversations": 0,
            "total_feedback": 0,
            "pending_feedback": 0,
            "total_knowledge_updates": 0,
            "pending_knowledge_updates": 0
        }
        
        # Load existing data
        self._load_existing_data()
    
    def create_conversation(
        self,
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        session_id: Optional[str] = None,
    ) -> ConversationSession:
        """
        Create a new conversation session.
        
        Args:
            user_id: Optional user identifier
            title: Optional conversation title
            description: Optional conversation description
            tags: Optional tags for categorization
            
        Returns:
            New conversation session
        """
        # Use provided session_id if supplied (for orchestration compatibility), otherwise generate a new one
        session_id = session_id or str(uuid.uuid4())
        
        conversation = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            title=title,
            description=description,
            tags=tags or []
        )
        
        self.active_conversations[session_id] = conversation
        self.stats["total_conversations"] += 1
        self.stats["active_conversations"] += 1
        
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
        
        logger.info(f"Created conversation session: {session_id}")
        return conversation
    
    def get_conversation(self, session_id: str) -> Optional[ConversationSession]:
        """Get a conversation session by ID"""
        return self.active_conversations.get(session_id)
    
    def add_message(
        self, 
        session_id: str,
        sender: str,
        message_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[str]] = None
    ) -> Optional[ConversationMessage]:
        """
        Add a message to a conversation.
        
        Args:
            session_id: Session ID
            sender: Message sender ("user", "system", or agent_type)
            message_type: Type of message
            content: Message content
            metadata: Optional metadata
            attachments: Optional file attachments
            
        Returns:
            Created message or None if session not found
        """
        conversation = self.get_conversation(session_id)
        if not conversation:
            logger.warning(f"Conversation session not found: {session_id}")
            return None
        
        message = ConversationMessage(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            sender=sender,
            message_type=message_type,
            content=content,
            metadata=metadata or {},
            attachments=attachments or []
        )
        
        conversation.messages.append(message)
        conversation.updated_at = datetime.now()
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=conversation.user_id,
            action="message_added",
            resource_type="conversation",
            resource_id=session_id,
            details={
                "message_id": message.message_id,
                "sender": sender,
                "message_type": message_type,
                "content_length": len(content)
            }
        )
        
        logger.debug(f"Added message to conversation {session_id}: {message.message_id}")
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
        """
        Add user feedback to a conversation.
        
        Args:
            session_id: Session ID
            feedback_type: Type of feedback
            content: Feedback content
            target_agent: Optional target agent
            priority: Feedback priority
            user_id: Optional user ID
            
        Returns:
            Created feedback or None if session not found
        """
        conversation = self.get_conversation(session_id)
        if not conversation:
            logger.warning(f"Conversation session not found: {session_id}")
            return None
        
        feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            session_id=session_id,
            timestamp=datetime.now(),
            feedback_type=feedback_type,
            content=content,
            target_agent=target_agent,
            priority=priority
        )
        
        conversation.feedback_history.append(feedback)
        conversation.updated_at = datetime.now()
        
        # Add to processing queue
        self.feedback_queue.append(feedback)
        self.stats["total_feedback"] += 1
        self.stats["pending_feedback"] += 1
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=user_id or conversation.user_id,
            action="feedback_added",
            resource_type="feedback",
            resource_id=feedback.feedback_id,
            details={
                "feedback_type": feedback_type,
                "target_agent": target_agent,
                "priority": priority,
                "content_length": len(content)
            }
        )
        
        logger.info(f"Added feedback to conversation {session_id}: {feedback.feedback_id}")
        return feedback
    
    def process_feedback(
        self, 
        feedback_id: str,
        processor: str,
        status: FeedbackStatus,
        result: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Process user feedback.
        
        Args:
            feedback_id: Feedback ID to process
            processor: Name of the processor (agent or system)
            status: Processing status
            result: Optional processing result
            
        Returns:
            True if feedback was found and processed
        """
        # Find feedback in all conversations
        feedback = None
        conversation = None
        
        for conv in self.active_conversations.values():
            for fb in conv.feedback_history:
                if fb.feedback_id == feedback_id:
                    feedback = fb
                    conversation = conv
                    break
            if feedback:
                break
        
        if not feedback:
            logger.warning(f"Feedback not found: {feedback_id}")
            return False
        
        # Update feedback status
        feedback.status = status
        feedback.processed_by = processor
        feedback.processed_at = datetime.now()
        if result:
            feedback.metadata.update(result)
        
        # Update conversation
        conversation.updated_at = datetime.now()
        
        # Update statistics
        if status in [FeedbackStatus.APPROVED, FeedbackStatus.REJECTED, FeedbackStatus.IMPLEMENTED]:
            self.stats["pending_feedback"] = max(0, self.stats["pending_feedback"] - 1)
        
        # Add audit entry
        self._add_audit_entry(
            session_id=feedback.session_id,
            user_id=conversation.user_id,
            action="feedback_processed",
            resource_type="feedback",
            resource_id=feedback_id,
            details={
                "processor": processor,
                "status": status.value,
                "result": result
            }
        )
        
        logger.info(f"Processed feedback {feedback_id}: {status.value}")
        return True
    
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
        """
        Create a knowledge update request.
        
        Args:
            session_id: Session ID
            update_type: Type of knowledge update
            target_agent: Target agent for the update
            content: Update content
            source_feedback: Optional source feedback ID
            approval_required: Whether approval is required
            user_id: Optional user ID
            
        Returns:
            Created knowledge update or None if session not found
        """
        conversation = self.get_conversation(session_id)
        if not conversation:
            logger.warning(f"Conversation session not found: {session_id}")
            return None
        
        knowledge_update = KnowledgeUpdate(
            update_id=str(uuid.uuid4()),
            session_id=session_id,
            timestamp=datetime.now(),
            update_type=update_type,
            target_agent=target_agent,
            content=content,
            source_feedback=source_feedback,
            approval_required=approval_required
        )
        
        conversation.knowledge_updates.append(knowledge_update)
        conversation.updated_at = datetime.now()
        
        # Add to approval queue if required
        if approval_required:
            self.knowledge_update_queue.append(knowledge_update)
            self.stats["pending_knowledge_updates"] += 1
        
        self.stats["total_knowledge_updates"] += 1
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=user_id or conversation.user_id,
            action="knowledge_update_created",
            resource_type="knowledge_update",
            resource_id=knowledge_update.update_id,
            details={
                "update_type": update_type.value,
                "target_agent": target_agent,
                "approval_required": approval_required,
                "content_length": len(content)
            }
        )
        
        logger.info(f"Created knowledge update {knowledge_update.update_id} for agent {target_agent}")
        return knowledge_update
    
    def approve_knowledge_update(
        self,
        update_id: str,
        approver: str,
        comments: Optional[str] = None
    ) -> bool:
        """
        Approve a knowledge update.
        
        Args:
            update_id: Knowledge update ID
            approver: Name of the approver
            comments: Optional approval comments
            
        Returns:
            True if update was found and approved
        """
        # Find knowledge update in all conversations
        knowledge_update = None
        conversation = None
        
        for conv in self.active_conversations.values():
            for ku in conv.knowledge_updates:
                if ku.update_id == update_id:
                    knowledge_update = ku
                    conversation = conv
                    break
            if knowledge_update:
                break
        
        if not knowledge_update:
            logger.warning(f"Knowledge update not found: {update_id}")
            return False
        
        # Update knowledge update
        knowledge_update.status = FeedbackStatus.APPROVED
        knowledge_update.approved_by = approver
        knowledge_update.approved_at = datetime.now()
        if comments:
            knowledge_update.metadata["approval_comments"] = comments
        
        # Update conversation
        conversation.updated_at = datetime.now()
        
        # Update statistics
        self.stats["pending_knowledge_updates"] = max(0, self.stats["pending_knowledge_updates"] - 1)
        
        # Add audit entry
        self._add_audit_entry(
            session_id=knowledge_update.session_id,
            user_id=conversation.user_id,
            action="knowledge_update_approved",
            resource_type="knowledge_update",
            resource_id=update_id,
            details={
                "approver": approver,
                "comments": comments
            }
        )
        
        logger.info(f"Approved knowledge update {update_id} by {approver}")
        return True
    
    def implement_knowledge_update(
        self,
        update_id: str,
        implementer: str,
        implementation_details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Mark a knowledge update as implemented.
        
        Args:
            update_id: Knowledge update ID
            implementer: Name of the implementer
            implementation_details: Optional implementation details
            
        Returns:
            True if update was found and marked as implemented
        """
        # Find knowledge update in all conversations
        knowledge_update = None
        conversation = None
        
        for conv in self.active_conversations.values():
            for ku in conv.knowledge_updates:
                if ku.update_id == update_id:
                    knowledge_update = ku
                    conversation = conv
                    break
            if knowledge_update:
                break
        
        if not knowledge_update:
            logger.warning(f"Knowledge update not found: {update_id}")
            return False
        
        # Update knowledge update
        knowledge_update.status = FeedbackStatus.IMPLEMENTED
        knowledge_update.implemented_at = datetime.now()
        if implementation_details:
            knowledge_update.metadata["implementation_details"] = implementation_details
        
        # Update conversation
        conversation.updated_at = datetime.now()
        
        # Add audit entry
        self._add_audit_entry(
            session_id=knowledge_update.session_id,
            user_id=conversation.user_id,
            action="knowledge_update_implemented",
            resource_type="knowledge_update",
            resource_id=update_id,
            details={
                "implementer": implementer,
                "implementation_details": implementation_details
            }
        )
        
        logger.info(f"Implemented knowledge update {update_id} by {implementer}")
        return True
    
    def get_conversation_history(
        self, 
        session_id: str, 
        limit: Optional[int] = None,
        message_types: Optional[List[str]] = None
    ) -> List[ConversationMessage]:
        """Get conversation history with optional filtering"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return []
        
        messages = conversation.messages
        
        # Filter by message type
        if message_types:
            messages = [msg for msg in messages if msg.message_type in message_types]
        
        # Apply limit
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def get_feedback_summary(self, session_id: str) -> Dict[str, Any]:
        """Get feedback summary for a conversation"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return {}
        
        feedback_by_type = {}
        feedback_by_status = {}
        
        for feedback in conversation.feedback_history:
            # Count by type
            feedback_type = feedback.feedback_type
            feedback_by_type[feedback_type] = feedback_by_type.get(feedback_type, 0) + 1
            
            # Count by status
            status = feedback.status.value
            feedback_by_status[status] = feedback_by_status.get(status, 0) + 1
        
        return {
            "total_feedback": len(conversation.feedback_history),
            "feedback_by_type": feedback_by_type,
            "feedback_by_status": feedback_by_status,
            "pending_feedback": len([f for f in conversation.feedback_history if f.status == FeedbackStatus.PENDING])
        }
    
    def get_knowledge_update_summary(self, session_id: str) -> Dict[str, Any]:
        """Get knowledge update summary for a conversation"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return {}
        
        updates_by_type = {}
        updates_by_status = {}
        
        for update in conversation.knowledge_updates:
            # Count by type
            update_type = update.update_type.value
            updates_by_type[update_type] = updates_by_type.get(update_type, 0) + 1
            
            # Count by status
            status = update.status.value
            updates_by_status[status] = updates_by_status.get(status, 0) + 1
        
        return {
            "total_updates": len(conversation.knowledge_updates),
            "updates_by_type": updates_by_type,
            "updates_by_status": updates_by_status,
            "pending_updates": len([u for u in conversation.knowledge_updates if u.status == FeedbackStatus.PENDING])
        }
    
    def get_audit_trail(
        self, 
        session_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        action_types: Optional[List[str]] = None
    ) -> List[AuditEntry]:
        """Get audit trail with optional filtering"""
        entries = self.audit_trail
        
        # Filter by session
        if session_id:
            entries = [entry for entry in entries if entry.session_id == session_id]
        
        # Filter by time range
        if start_time:
            entries = [entry for entry in entries if entry.timestamp >= start_time]
        if end_time:
            entries = [entry for entry in entries if entry.timestamp <= end_time]
        
        # Filter by action type
        if action_types:
            entries = [entry for entry in entries if entry.action in action_types]
        
        return entries
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        return {
            **self.stats,
            "conversation_stats": {
                "total_conversations": len(self.active_conversations),
                "conversations_by_status": self._get_conversations_by_status(),
                "average_messages_per_conversation": self._get_average_messages_per_conversation(),
                "average_feedback_per_conversation": self._get_average_feedback_per_conversation()
            },
            "feedback_stats": {
                "total_feedback": len(self.feedback_queue),
                "feedback_by_type": self._get_feedback_by_type(),
                "feedback_by_status": self._get_feedback_by_status()
            },
            "knowledge_update_stats": {
                "total_updates": len(self.knowledge_update_queue),
                "updates_by_type": self._get_knowledge_updates_by_type(),
                "updates_by_status": self._get_knowledge_updates_by_status()
            },
            "audit_stats": {
                "total_audit_entries": len(self.audit_trail),
                "audit_entries_by_action": self._get_audit_entries_by_action()
            }
        }
    
    def archive_conversation(self, session_id: str) -> bool:
        """Archive a conversation session"""
        conversation = self.get_conversation(session_id)
        if not conversation:
            return False
        
        conversation.status = ConversationStatus.ARCHIVED
        conversation.updated_at = datetime.now()
        
        # Remove from active conversations
        del self.active_conversations[session_id]
        self.stats["active_conversations"] = max(0, self.stats["active_conversations"] - 1)
        
        # Save to archive
        self._save_conversation_to_archive(conversation)
        
        # Add audit entry
        self._add_audit_entry(
            session_id=session_id,
            user_id=conversation.user_id,
            action="conversation_archived",
            resource_type="conversation",
            resource_id=session_id
        )
        
        logger.info(f"Archived conversation session: {session_id}")
        return True
    
    def _add_audit_entry(
        self,
        session_id: str,
        user_id: Optional[str],
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Add an audit trail entry"""
        entry = AuditEntry(
            entry_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            session_id=session_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {}
        )
        
        self.audit_trail.append(entry)
        
        # Keep audit trail manageable (last 10000 entries)
        if len(self.audit_trail) > 10000:
            self.audit_trail = self.audit_trail[-10000:]
    
    def _get_conversations_by_status(self) -> Dict[str, int]:
        """Get conversation count by status"""
        status_counts = {}
        for conversation in self.active_conversations.values():
            status = conversation.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _get_average_messages_per_conversation(self) -> float:
        """Calculate average messages per conversation"""
        if not self.active_conversations:
            return 0.0
        
        total_messages = sum(len(conv.messages) for conv in self.active_conversations.values())
        return total_messages / len(self.active_conversations)
    
    def _get_average_feedback_per_conversation(self) -> float:
        """Calculate average feedback per conversation"""
        if not self.active_conversations:
            return 0.0
        
        total_feedback = sum(len(conv.feedback_history) for conv in self.active_conversations.values())
        return total_feedback / len(self.active_conversations)
    
    def _get_feedback_by_type(self) -> Dict[str, int]:
        """Get feedback count by type"""
        type_counts = {}
        for conversation in self.active_conversations.values():
            for feedback in conversation.feedback_history:
                feedback_type = feedback.feedback_type
                type_counts[feedback_type] = type_counts.get(feedback_type, 0) + 1
        return type_counts
    
    def _get_feedback_by_status(self) -> Dict[str, int]:
        """Get feedback count by status"""
        status_counts = {}
        for conversation in self.active_conversations.values():
            for feedback in conversation.feedback_history:
                status = feedback.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _get_knowledge_updates_by_type(self) -> Dict[str, int]:
        """Get knowledge update count by type"""
        type_counts = {}
        for conversation in self.active_conversations.values():
            for update in conversation.knowledge_updates:
                update_type = update.update_type.value
                type_counts[update_type] = type_counts.get(update_type, 0) + 1
        return type_counts
    
    def _get_knowledge_updates_by_status(self) -> Dict[str, int]:
        """Get knowledge update count by status"""
        status_counts = {}
        for conversation in self.active_conversations.values():
            for update in conversation.knowledge_updates:
                status = update.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _get_audit_entries_by_action(self) -> Dict[str, int]:
        """Get audit entry count by action"""
        action_counts = {}
        for entry in self.audit_trail:
            action = entry.action
            action_counts[action] = action_counts.get(action, 0) + 1
        return action_counts
    
    def _save_conversation_to_archive(self, conversation: ConversationSession):
        """Save conversation to archive"""
        archive_file = self.storage_path / "archived_conversations" / f"{conversation.session_id}.json"
        archive_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        archive_data = {
            "session_id": conversation.session_id,
            "user_id": conversation.user_id,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "status": conversation.status.value,
            "title": conversation.title,
            "description": conversation.description,
            "tags": conversation.tags,
            "metadata": conversation.metadata,
            "messages": [
                {
                    "message_id": msg.message_id,
                    "timestamp": msg.timestamp.isoformat(),
                    "sender": msg.sender,
                    "message_type": msg.message_type,
                    "content": msg.content,
                    "metadata": msg.metadata,
                    "attachments": msg.attachments
                }
                for msg in conversation.messages
            ],
            "feedback_history": [
                {
                    "feedback_id": fb.feedback_id,
                    "session_id": fb.session_id,
                    "timestamp": fb.timestamp.isoformat(),
                    "feedback_type": fb.feedback_type,
                    "content": fb.content,
                    "target_agent": fb.target_agent,
                    "priority": fb.priority,
                    "status": fb.status.value,
                    "processed_by": fb.processed_by,
                    "processed_at": fb.processed_at.isoformat() if fb.processed_at else None,
                    "metadata": fb.metadata
                }
                for fb in conversation.feedback_history
            ],
            "knowledge_updates": [
                {
                    "update_id": ku.update_id,
                    "session_id": ku.session_id,
                    "timestamp": ku.timestamp.isoformat(),
                    "update_type": ku.update_type.value,
                    "target_agent": ku.target_agent,
                    "content": ku.content,
                    "source_feedback": ku.source_feedback,
                    "approval_required": ku.approval_required,
                    "status": ku.status.value,
                    "approved_by": ku.approved_by,
                    "approved_at": ku.approved_at.isoformat() if ku.approved_at else None,
                    "implemented_at": ku.implemented_at.isoformat() if ku.implemented_at else None,
                    "metadata": ku.metadata
                }
                for ku in conversation.knowledge_updates
            ],
            "audit_entries": [
                {
                    "entry_id": entry.entry_id,
                    "timestamp": entry.timestamp.isoformat(),
                    "session_id": entry.session_id,
                    "user_id": entry.user_id,
                    "action": entry.action,
                    "resource_type": entry.resource_type,
                    "resource_id": entry.resource_id,
                    "details": entry.details,
                    "ip_address": entry.ip_address,
                    "user_agent": entry.user_agent
                }
                for entry in conversation.audit_entries
            ]
        }
        
        with open(archive_file, 'w') as f:
            json.dump(archive_data, f, indent=2)
    
    def _load_existing_data(self):
        """Load existing conversation data from storage"""
        # This would load existing conversations from storage
        # For now, we'll start with empty state
        logger.info("Initialized conversation manager with empty state")


# Global conversation manager instance
conversation_manager = ConversationManager()


def get_conversation_manager() -> ConversationManager:
    """Get the global conversation manager"""
    return conversation_manager


# Export main classes and functions
__all__ = [
    "ConversationManager",
    "ConversationSession",
    "ConversationMessage",
    "UserFeedback",
    "KnowledgeUpdate",
    "AuditEntry",
    "ConversationStatus",
    "FeedbackStatus",
    "KnowledgeUpdateType",
    "conversation_manager",
    "get_conversation_manager"
] 