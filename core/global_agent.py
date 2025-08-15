"""
GlobalAgent - The orchestration layer for multi-agent financial document generation.

This module provides the GlobalAgent class that acts as the user-facing "brain"
for the entire framework, coordinating multiple specialized agents and handling
user feedback and workflow management.

Key Features:
- Intelligent request routing to appropriate agents
- Multi-agent workflow coordination
- User feedback processing and agent updates
- Conversation state management
- Result aggregation and presentation
- Session management and cleanup
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .router import SmartAgentRouter, RoutingDecision
from .conversation_manager import (
    ConversationManager as RealConversationManager,
    ConversationSession as CMConversationSession,
    UserFeedback,
    KnowledgeUpdate,
    FeedbackStatus,
    KnowledgeUpdateType,
    get_conversation_manager,
)
from .config import global_config
from agents.factory import (
    create_agent_with_factory,
    create_large_text_agent_with_factory,
)
from agents import get_agent_status_summary, get_agent_registry

# Configure logging
logging.basicConfig(level=global_config.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FeedbackType(Enum):
    """Types of user feedback that can be processed"""
    APPROVAL = "approval"
    REJECTION = "rejection"
    CONTENT_UPDATE = "content_update"
    KNOWLEDGE_UPDATE = "knowledge_update"
    CLARIFICATION_REQUEST = "clarification_request"


class ConversationState(Enum):
    """States of a conversation session"""
    INITIALIZED = "initialized"
    PROCESSING = "processing"
    AWAITING_FEEDBACK = "awaiting_feedback"
    UPDATING = "updating"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class AgentResult:
    """Result from a single agent execution"""
    agent_type: str
    success: bool
    processing_time: float
    output: Optional[Any] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GlobalAgentResponse:
    """Response from the GlobalAgent"""
    success: bool
    message: str
    session_id: str
    conversation_state: ConversationState
    primary_result: Optional[AgentResult] = None
    secondary_results: List[AgentResult] = field(default_factory=list)
    aggregated_content: Dict[str, Any] = field(default_factory=dict)
    next_actions: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    reasoning: str = ""


@dataclass
class ConversationSession:
    """Represents a conversation session with the GlobalAgent"""
    session_id: str
    user_request: str
    routing_decision: RoutingDecision
    conversation_state: ConversationState
    created_at: datetime
    updated_at: datetime
    message_history: List[Dict[str, Any]] = field(default_factory=list)
    agent_results: Dict[str, AgentResult] = field(default_factory=dict)
    feedback_history: List[Dict[str, Any]] = field(default_factory=list)


class GlobalAgent:
    """
    GlobalAgent - The orchestration layer for multi-agent financial document generation.
    
    This class provides:
    - Intelligent request routing and analysis
    - Multi-agent workflow coordination
    - User feedback processing and agent updates
    - Conversation state management
    - Result aggregation and presentation
    - Session management and cleanup
    """
    
    def __init__(self, action=None, config=None):
        """Initialize the GlobalAgent with routing and agent management"""
        self.router = SmartAgentRouter()
        self.sessions: Dict[str, ConversationSession] = {}
        self.agent_registry = self._initialize_agent_registry()
        # Use the shared ConversationManager with full functionality
        self.conversation_manager = get_conversation_manager()
        # Note: get_conversation_manager() call removed as it was causing issues
        
    def _initialize_agent_registry(self) -> Dict[str, Any]:
        """Initialize the registry of available agents from the centralized AgentRegistry"""
        summary = get_agent_status_summary()
        agents_info = summary.get("agents_by_type", {})
        # Normalize to the legacy shape used by get_agent_status()
        normalized: Dict[str, Any] = {}
        for agent_type, meta in agents_info.items():
            normalized[agent_type] = {
                "class": None,  # dynamically imported or created via factory
                "description": get_agent_registry().get_agent_metadata(agent_type).description if get_agent_registry().get_agent_metadata(agent_type) else agent_type,
                "capabilities": get_agent_registry().get_agent_metadata(agent_type).capabilities if get_agent_registry().get_agent_metadata(agent_type) else [],
                "status": meta.get("status", "unknown"),
                "health": meta.get("health", "unknown"),
                "last_updated": meta.get("last_updated", datetime.now().isoformat()),
                "config_schema": (get_agent_registry().get_agent_metadata(agent_type).config_schema if get_agent_registry().get_agent_metadata(agent_type) else None),
            }
        return normalized
    
    async def process_request(
        self,
        user_request: str,
        session_id: Optional[str] = None,
        agents: Optional[List[str]] = None,
        run_all: bool = False,
        use_large_text_templates: Optional[bool] = None,
        render_docx: Optional[bool] = None,
        audience: Optional[str] = None,
        filename: Optional[str] = None,
        title: Optional[str] = None,
        enforce_placeholder_validation: Optional[bool] = None,
        custom_variables: Optional[Dict[str, Any]] = None,
    ) -> GlobalAgentResponse:
        """
        Process a user request through the GlobalAgent orchestration.
        
        Args:
            user_request: The user's natural language request
            session_id: Optional session ID for conversation continuity
            agents: Optional explicit list of agent types to execute (e.g., ["ism", "bsp"]).
                When provided, this overrides automatic routing and executes exactly these agents
                in the provided order. The first item is treated as the primary agent.
            run_all: If True (and agents is None), execute all available agents for document
                generation. The automatically selected primary agent runs first, followed by all
                other available agents as secondary.
            
        Returns:
            GlobalAgentResponse with results and next actions
        """
        logger.info(f"Processing request: {user_request[:100]}...")
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        try:
            # Analyze the request using the router
            routing_decision = self.router.analyze_request(user_request)
            
            # Create or update session
            session = self._get_or_create_session(session_id, user_request, routing_decision)
            
            # Update session state
            session.conversation_state = ConversationState.PROCESSING
            session.updated_at = datetime.now()
            
            # Decide which agents to execute based on explicit selection, run_all flag, or router
            selected_agent_names: List[str]

            if agents is not None and len(agents) > 0:
                # Normalize and validate explicit agent list
                provided = [a.strip().lower() for a in agents if a and isinstance(a, str)]
                valid_agent_names = {a.value for a in self.router.get_agent_capabilities().keys()}
                filtered = [a for a in provided if a in valid_agent_names]
                if not filtered:
                    raise ValueError(
                        f"No valid agents provided. Valid options: {sorted(valid_agent_names)}"
                    )
                selected_agent_names = filtered
            elif run_all:
                # Run all available agents; primary first, then the rest
                all_agents = [a.value for a in self.router.get_agent_capabilities().keys()]
                primary_name = routing_decision.primary_agent.value
                selected_agent_names = [primary_name] + [a for a in all_agents if a != primary_name]
            else:
                # Default: primary + router-selected secondary agents
                primary_name = routing_decision.primary_agent.value
                selected_agent_names = [primary_name] + [a.value for a in routing_decision.secondary_agents]

            # Execute agents in order; first is primary, rest are secondary
            primary_agent_name = selected_agent_names[0]
            primary_result = await self._execute_agent(
                primary_agent_name,
                self._merge_request_overrides(
                    routing_decision.extracted_data,
                    use_large_text_templates,
                    render_docx,
                    audience,
                    filename,
                    title,
                    enforce_placeholder_validation,
                    custom_variables,
                ),
                session_id,
            )

            secondary_results: List[AgentResult] = []
            for secondary_name in selected_agent_names[1:]:
                result = await self._execute_agent(
                    secondary_name,
                    self._merge_request_overrides(
                        routing_decision.extracted_data,
                        use_large_text_templates,
                        render_docx,
                        audience,
                        filename,
                        title,
                        enforce_placeholder_validation,
                        custom_variables,
                    ),
                    session_id,
                )
                secondary_results.append(result)
            
            # Aggregate results
            aggregated_content = self._aggregate_results(primary_result, secondary_results)
            
            # Determine next actions
            next_actions = self._determine_next_actions(
                routing_decision, primary_result, secondary_results
            )
            
            # Update session
            session.agent_results[primary_result.agent_type] = primary_result
            for result in secondary_results:
                session.agent_results[result.agent_type] = result
            session.conversation_state = ConversationState.AWAITING_FEEDBACK
            
            # Create response
            response = GlobalAgentResponse(
                success=primary_result.success,
                message=self._generate_response_message(primary_result, secondary_results),
                session_id=session_id,
                conversation_state=session.conversation_state,
                primary_result=primary_result,
                secondary_results=secondary_results,
                aggregated_content=aggregated_content,
                next_actions=next_actions,
                confidence_score=routing_decision.confidence_score,
                reasoning=routing_decision.reasoning
            )
            
            logger.info(f"Request processed successfully. Session: {session_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return GlobalAgentResponse(
                success=False,
                message=f"Error processing request: {str(e)}",
                session_id=session_id,
                conversation_state=ConversationState.ERROR
            )

    @staticmethod
    def _merge_request_overrides(
        extracted_data: Dict[str, Any],
        use_large_text_templates: Optional[bool],
        render_docx: Optional[bool],
        audience: Optional[str],
        filename: Optional[str],
        title: Optional[str],
        enforce_placeholder_validation: Optional[bool],
        custom_variables: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        # Start with extracted data but drop None values to allow defaults downstream
        merged = {k: v for k, v in (extracted_data or {}).items() if v is not None}
        if use_large_text_templates is not None:
            merged["use_large_text_templates"] = use_large_text_templates
        if render_docx is not None:
            merged["render_docx"] = render_docx
        if audience is not None:
            merged["audience"] = audience
        if filename is not None:
            merged["filename"] = filename
        if title is not None:
            merged["title"] = title
        if enforce_placeholder_validation is not None:
            merged["enforce_placeholder_validation"] = enforce_placeholder_validation
        if custom_variables is not None:
            merged["custom_variables"] = custom_variables
        return merged
    
    async def handle_feedback(
        self, 
        session_id: str, 
        feedback: str, 
        feedback_type: FeedbackType,
        target_agent: Optional[str] = None,
        priority: str = "normal"
    ) -> GlobalAgentResponse:
        """
        Handle user feedback and update agents accordingly.
        
        Args:
            session_id: The session ID to update
            feedback: User feedback content
            feedback_type: Type of feedback provided
            target_agent: Optional target agent for the feedback
            priority: Feedback priority level
            
        Returns:
            GlobalAgentResponse with updated results
        """
        logger.info(f"Handling feedback for session {session_id}: {feedback_type.value}")
        
        # Get conversation from sessions dict (backward compatibility)
        conversation = self.sessions.get(session_id)
        if not conversation:
            return GlobalAgentResponse(
                success=False,
                message=f"Session {session_id} not found",
                session_id=session_id,
                conversation_state=ConversationState.ERROR
            )
        
        # Add feedback to conversation
        user_feedback = self.conversation_manager.add_feedback(
            session_id=session_id,
            feedback_type=feedback_type.value,
            content=feedback,
            target_agent=target_agent,
            priority=priority
        )
        
        if not user_feedback:
            return GlobalAgentResponse(
                success=False,
                message="Failed to add feedback to conversation",
                session_id=session_id,
                conversation_state=ConversationState.ERROR
            )
        
        # Add system message about feedback processing
        self.conversation_manager.add_message(
            session_id=session_id,
            sender="system",
            message_type="feedback_received",
            content=f"Feedback received: {feedback_type.value}",
            metadata={"feedback_id": user_feedback.feedback_id}
        )
        
        try:
            # Process feedback based on type
            if feedback_type == FeedbackType.APPROVAL:
                response = await self._handle_approval(conversation, feedback, user_feedback)
            elif feedback_type == FeedbackType.REJECTION:
                response = await self._handle_rejection(conversation, feedback, user_feedback)
            elif feedback_type == FeedbackType.CONTENT_UPDATE:
                response = await self._handle_content_update(conversation, feedback, user_feedback)
            elif feedback_type == FeedbackType.KNOWLEDGE_UPDATE:
                response = await self._handle_knowledge_update(conversation, feedback, user_feedback)
            elif feedback_type == FeedbackType.CLARIFICATION_REQUEST:
                response = await self._handle_clarification_request(conversation, feedback, user_feedback)
            else:
                response = GlobalAgentResponse(
                    success=False,
                    message=f"Unknown feedback type: {feedback_type}",
                    session_id=session_id,
                    conversation_state=ConversationState.ERROR
                )
            
            # Mark feedback as processed
            self.conversation_manager.process_feedback(
                feedback_id=user_feedback.feedback_id,
                processor="global_agent",
                status=FeedbackStatus.APPROVED if response.success else FeedbackStatus.FAILED,
                result={"response_message": response.message}
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling feedback: {e}")
            
            # Mark feedback as failed
            self.conversation_manager.process_feedback(
                feedback_id=user_feedback.feedback_id,
                processor="global_agent",
                status=FeedbackStatus.FAILED,
                result={"error": str(e)}
            )
            
            return GlobalAgentResponse(
                success=False,
                message=f"Error handling feedback: {str(e)}",
                session_id=session_id,
                conversation_state=ConversationState.ERROR
            )
    
    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get the status of all available agents"""
        return self.agent_registry.copy()
    
    def get_session_info(self, session_id: str) -> Optional[CMConversationSession]:
        """Get information about a specific session"""
        return self.conversation_manager.get_conversation(session_id)
    
    def get_conversation_history(self, session_id: str, limit: Optional[int] = None) -> List[Any]:
        """Get conversation history for a session"""
        # core.conversation_manager.get_conversation_history supports (session_id, limit=None, message_types=None)
        return self.conversation_manager.get_conversation_history(session_id, limit)
    
    def get_feedback_summary(self, session_id: str) -> Dict[str, Any]:
        """Get feedback summary for a session"""
        return self.conversation_manager.get_feedback_summary(session_id)
    
    def get_knowledge_update_summary(self, session_id: str) -> Dict[str, Any]:
        """Get knowledge update summary for a session"""
        return self.conversation_manager.get_knowledge_update_summary(session_id)
    
    def get_audit_trail(self, session_id: Optional[str] = None, hours: int = 24) -> List[Any]:
        """Get audit trail with optional filtering"""
        from datetime import datetime, timedelta
        start_time = datetime.now() - timedelta(hours=hours)
        return self.conversation_manager.get_audit_trail(
            session_id=session_id,
            start_time=start_time
        )
    
    def get_conversation_statistics(self) -> Dict[str, Any]:
        """Get comprehensive conversation statistics"""
        return self.conversation_manager.get_statistics()
    
    def cleanup_session(self, session_id: str) -> bool:
        """Clean up a session and free resources"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleaned up session: {session_id}")
            return True
        return False
    
    def _get_or_create_session(
        self, 
        session_id: str, 
        user_request: str, 
        routing_decision: RoutingDecision
    ) -> CMConversationSession:
        """Get existing session or create a new one"""
        # Check if session exists in sessions dict (backward compatibility)
        if session_id in self.sessions:
            conversation = self.sessions[session_id]
            # Update existing conversation
            conversation.updated_at = datetime.now()
            # Add user request as a message
            self.conversation_manager.add_message(
                session_id=session_id,
                sender="user",
                message_type="request",
                content=user_request,
                metadata={"routing_decision": routing_decision.__dict__}
            )
            return conversation
        else:
            # Create new conversation using conversation manager
            conversation = self.conversation_manager.create_conversation(
                user_id=None,  # Could be passed from request
                title=f"Document Generation Session {session_id[:8]}",
                description="Session for generating financial documents",
                tags=["document_generation", "financial"],
                session_id=session_id,
            )
            
            # Add initial user request
            self.conversation_manager.add_message(
                session_id=session_id,
                sender="user",
                message_type="request",
                content=user_request,
                metadata={"routing_decision": routing_decision.__dict__}
            )
            
            # Store in sessions for backward compatibility
            self.sessions[session_id] = conversation
            return conversation
    
    async def _execute_agent(
        self, 
        agent_type: str, 
        input_data: Dict[str, Any], 
        session_id: str
    ) -> AgentResult:
        """Execute a specific agent with the given input data"""
        start_time = datetime.now()
        
        try:
            # Extract orchestration flags without polluting Pydantic model creation
            use_large_text = bool(input_data.pop("use_large_text_templates", False))
            render_docx = bool(input_data.pop("render_docx", False))
            audience = input_data.pop("audience", None)
            filename = input_data.pop("filename", None)
            title = input_data.pop("title", None)
            enforce_placeholder_validation = bool(input_data.pop("enforce_placeholder_validation", True))
            custom_variables = input_data.pop("custom_variables", None)

            # Create agent via factory (base or large-text wrapper)
            if use_large_text:
                agent = create_large_text_agent_with_factory(agent_type)
            else:
                agent = create_agent_with_factory(agent_type)
            if not agent:
                return AgentResult(
                    agent_type=agent_type,
                    success=False,
                    processing_time=0.0,
                    error_message=f"Agent {agent_type} not available"
                )

            # Prepare input model with scaffolding and capture missing fields
            processed_input, missing_fields = self._prepare_agent_input(agent_type, input_data)

            # Execute based on path
            if use_large_text and render_docx:
                # Prefer convenience DOCX generation if supported
                if hasattr(agent, "generate_docx_with_large_templates"):
                    # All large-text wrappers (including ISM) expose this method now
                    docx_path = await agent.generate_docx_with_large_templates(  # type: ignore[attr-defined]
                        input_data=processed_input,
                        audience=audience or "retail",
                        custom_variables=custom_variables,
                        title=title,
                        filename=filename,
                        enforce_placeholder_validation=enforce_placeholder_validation,
                    )
                    result_output = {"docx_path": docx_path}
                else:
                    # Fallback: generate dict then caller can serialize
                    sections = await agent.generate_document_with_large_templates(  # type: ignore[attr-defined]
                        input_data=processed_input,
                        audience=audience or "retail",
                        custom_variables=custom_variables,
                    )
                    result_output = {"sections": sections}
            elif use_large_text:
                # Generate dictionary sections via large-text path
                sections = await agent.generate_document_with_large_templates(  # type: ignore[attr-defined]
                    input_data=processed_input,
                    audience=audience or "retail",
                    custom_variables=custom_variables,
                )
                result_output = {"sections": sections}
            else:
                # Default LLM path
                result_output = await agent.generate_document(processed_input)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                agent_type=agent_type,
                success=True,
                processing_time=processing_time,
                output=result_output,
                metadata={
                    "agent_impl": type(agent).__name__,
                    "missing_fields": missing_fields or [],
                }
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Error executing agent {agent_type}: {e}")
            
            return AgentResult(
                agent_type=agent_type,
                success=False,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    async def _get_agent_class(self, agent_type: str):
        """Dynamically import and return agent class"""
        try:
            if agent_type == "ism":
                from agents.investor_summary import ISMAgent
                return ISMAgent
            elif agent_type == "bsp":
                from agents.base_shelf_prospectus import BSPAgent
                return BSPAgent
            elif agent_type == "pds":
                from agents.product_supplement import PDSAgent
                return PDSAgent
            elif agent_type == "prs":
                from agents.pricing_supplement import PRSAgent
                return PRSAgent
            else:
                logger.warning(f"Unknown agent type: {agent_type}")
                return None
        except ImportError as e:
            logger.error(f"Failed to import agent {agent_type}: {e}")
            return None
    
    def _prepare_agent_input(self, agent_type: str, input_data: Dict[str, Any]) -> Tuple[Any, List[str]]:
        """Prepare input data for a specific agent type with lightweight scaffolding and missing-field tracking"""
        missing_fields: List[str] = []

        def with_defaults(model_cls, data: Dict[str, Any], default_map: Dict[str, Any]) -> Any:
            # Apply safe defaults only for keys we know and report them as missing
            prepared = dict(data)
            for key, default_val in default_map.items():
                if key not in prepared:
                    missing_fields.append(key)
                    prepared[key] = default_val() if callable(default_val) else default_val
            return model_cls(**prepared)

        def coerce_float(value: Any) -> Optional[float]:
            if value is None:
                return None
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                txt = value.strip().replace(",", "")
                try:
                    return float(txt)
                except Exception:
                    return None
            return None

        if agent_type == "ism":
            from agents.investor_summary.models import ISMInput
            # Provide safe defaults where feasible for E2E doc runs
            defaults = {
                "issuer": "The Bank of Nova Scotia",
                "product_name": "Autocallable Plus Notes",
                "underlying_asset": "Canadian Financials Basket",
                "currency": "CAD",
                "principal_amount": 5000.0,
                "issue_date": datetime.now().date(),
                "maturity_date": (datetime.now().date().replace(year=datetime.now().year + 7)),
                "product_type": "autocallable",
                "target_audience": "retail_investors",
                "risk_tolerance": "medium",
                "investment_objective": "capital_growth_with_income",
                "regulatory_jurisdiction": "Canada",
                "distribution_method": "broker_dealer_network",
            }
            # Coerce numeric fields if present from routing text
            if "principal_amount" in input_data:
                coerced = coerce_float(input_data.get("principal_amount"))
                if coerced is not None:
                    input_data["principal_amount"] = coerced
            return with_defaults(ISMInput, input_data, defaults), missing_fields
        elif agent_type == "bsp":
            from agents.base_shelf_prospectus.models import BSPInput
            defaults = {
                "issuer": "TBD",
                "program_name": "Structured Note Program",
                "shelf_amount": 10000000.0,
                "currency": "USD",
                "regulatory_jurisdiction": "Canada",
                # Additional required fields for BSPInput
                "legal_structure": "Senior unsecured notes",
                "business_description": "Banking and financial services, including structured products",
                "note_types": ["Autocallable notes"],
                "distribution_methods": ["registered investment dealers"],
            }
            return with_defaults(BSPInput, input_data, defaults), missing_fields
        elif agent_type == "pds":
            from agents.product_supplement.models import PDSInput
            from datetime import date, timedelta
            today = date.today()
            defaults = {
                "base_prospectus_reference": "Base Shelf Prospectus",
                "base_prospectus_date": today,
                "note_series": "Series TBD",
                "note_description": "TBD",
                "underlying_asset": "TBD",
                "principal_amount": 100000.0,
                "issue_price": 100.0,
                "currency": "USD",
                "issue_date": today,
                "maturity_date": today + timedelta(days=365*3),
                "product_type": "autocallable",
                "calculation_methodology": "See applicable pricing supplement.",
            }
            if "principal_amount" in input_data:
                coerced = coerce_float(input_data.get("principal_amount"))
                if coerced is not None:
                    input_data["principal_amount"] = coerced
            if "issue_price" in input_data:
                coerced_ip = coerce_float(input_data.get("issue_price"))
                if coerced_ip is not None:
                    input_data["issue_price"] = coerced_ip
            return with_defaults(PDSInput, input_data, defaults), missing_fields
        elif agent_type == "prs":
            from agents.pricing_supplement.models import PRSInput
            from datetime import date, timedelta
            today = date.today()
            defaults = {
                "base_prospectus_reference": "Base Shelf Prospectus",
                "final_issue_price": 100.0,
                "final_principal_amount": 100000.0,
                "currency": "USD",
                "pricing_date": today,
                "issue_date": today,
                "maturity_date": today + timedelta(days=365*3),
                "settlement_date": today + timedelta(days=7),
                "distribution_method": "retail",
                "minimum_denomination": 100,
            }
            if "final_issue_price" in input_data:
                coerced_fip = coerce_float(input_data.get("final_issue_price"))
                if coerced_fip is not None:
                    input_data["final_issue_price"] = coerced_fip
            if "final_principal_amount" in input_data:
                coerced_fpa = coerce_float(input_data.get("final_principal_amount"))
                if coerced_fpa is not None:
                    input_data["final_principal_amount"] = coerced_fpa
            if "minimum_denomination" in input_data:
                coerced_md = coerce_float(input_data.get("minimum_denomination"))
                if coerced_md is not None:
                    input_data["minimum_denomination"] = coerced_md
            return with_defaults(PRSInput, input_data, defaults), missing_fields
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    def _aggregate_results(
        self, 
        primary_result: AgentResult, 
        secondary_results: List[AgentResult]
    ) -> Dict[str, Any]:
        """Aggregate results from multiple agents"""
        aggregated = {
            "total_agents": 1 + len(secondary_results),
            "successful_agents": sum(1 for r in [primary_result] + secondary_results if r.success),
            "primary_agent": primary_result.agent_type,
            "primary_success": primary_result.success,
            "secondary_agents": [r.agent_type for r in secondary_results],
            "all_results": {
                primary_result.agent_type: {
                    "success": primary_result.success,
                    "processing_time": primary_result.processing_time,
                    "error": primary_result.error_message
                }
            }
        }
        
        for result in secondary_results:
            aggregated["all_results"][result.agent_type] = {
                "success": result.success,
                "processing_time": result.processing_time,
                "error": result.error_message
            }
        
        return aggregated
    
    def _determine_next_actions(
        self, 
        routing_decision: RoutingDecision,
        primary_result: AgentResult,
        secondary_results: List[AgentResult]
    ) -> List[str]:
        """Determine next actions based on results"""
        actions = []
        
        if primary_result.success:
            actions.append("Review generated document")
            actions.append("Provide feedback for improvements")
            if secondary_results:
                actions.append("Review secondary documents")
        else:
            actions.append("Check agent availability and configuration")
            actions.append("Verify input data completeness")
        
        # Add agent-specific actions
        if routing_decision.primary_agent.value == "ism":
            actions.append("Customize for specific investor audience")
            actions.append("Add regulatory compliance checks")
        
        return actions
    
    def _generate_response_message(
        self, 
        primary_result: AgentResult, 
        secondary_results: List[AgentResult]
    ) -> str:
        """Generate a user-friendly response message"""
        if primary_result.success:
            message = f"Successfully generated {primary_result.agent_type.upper()} document"
            if secondary_results:
                successful_secondary = sum(1 for r in secondary_results if r.success)
                message += f" and {successful_secondary} additional documents"
            message += ". Please review and provide feedback."
        else:
            message = f"Failed to generate {primary_result.agent_type.upper()} document: {primary_result.error_message}"
        
        return message
    
    async def _handle_approval(self, conversation: ConversationSession, feedback: str, user_feedback: UserFeedback) -> GlobalAgentResponse:
        """Handle user approval feedback"""
        # Add approval message to conversation
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="approval_processed",
            content="Document approved by user",
            metadata={"feedback_id": user_feedback.feedback_id}
        )
        
        return GlobalAgentResponse(
            success=True,
            message="Document approved! The generated document is ready for use.",
            session_id=conversation.session_id,
            conversation_state=ConversationState.COMPLETED,
            next_actions=["Download final document", "Archive session"]
        )
    
    async def _handle_rejection(self, conversation: ConversationSession, feedback: str, user_feedback: UserFeedback) -> GlobalAgentResponse:
        """Handle user rejection feedback"""
        # Add rejection message to conversation
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="rejection_processed",
            content=f"Document rejected: {feedback}",
            metadata={"feedback_id": user_feedback.feedback_id}
        )
        
        # Get the original user request from conversation history
        user_messages = self.conversation_manager.get_conversation_history(
            conversation.session_id, 
            message_types=["request"]
        )
        
        if user_messages:
            original_request = user_messages[-1].content
            updated_request = f"{original_request} [REJECTED: {feedback}]"
        else:
            updated_request = f"Regenerate document [REJECTED: {feedback}]"
        
        # Update routing decision based on feedback
        routing_decision = self.router.analyze_request(updated_request)
        
        # Re-execute primary agent
        primary_result = await self._execute_agent(
            routing_decision.primary_agent.value,
            routing_decision.extracted_data,
            conversation.session_id
        )
        
        # Add regeneration message
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="document_regenerated",
            content="Document regenerated based on rejection feedback",
            metadata={"agent_result": primary_result.__dict__}
        )
        
        return GlobalAgentResponse(
            success=primary_result.success,
            message=f"Document regenerated based on feedback: {feedback}",
            session_id=conversation.session_id,
            conversation_state=ConversationState.AWAITING_FEEDBACK,
            primary_result=primary_result,
            next_actions=["Review updated document", "Provide additional feedback"]
        )
    
    async def _handle_content_update(self, conversation: ConversationSession, feedback: str, user_feedback: UserFeedback) -> GlobalAgentResponse:
        """Handle content update feedback"""
        # Add content update message to conversation
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="content_update_processed",
            content=f"Content update requested: {feedback}",
            metadata={"feedback_id": user_feedback.feedback_id}
        )
        
        # Get the original user request from conversation history
        user_messages = self.conversation_manager.get_conversation_history(
            conversation.session_id, 
            message_types=["request"]
        )
        
        if user_messages:
            original_request = user_messages[-1].content
            updated_request = f"{original_request} [UPDATE: {feedback}]"
        else:
            updated_request = f"Update document [UPDATE: {feedback}]"
        
        routing_decision = self.router.analyze_request(updated_request)
        
        primary_result = await self._execute_agent(
            routing_decision.primary_agent.value,
            routing_decision.extracted_data,
            conversation.session_id
        )
        
        # Add update message
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="document_updated",
            content="Document updated with requested changes",
            metadata={"agent_result": primary_result.__dict__}
        )
        
        return GlobalAgentResponse(
            success=primary_result.success,
            message=f"Document updated with requested changes: {feedback}",
            session_id=conversation.session_id,
            conversation_state=ConversationState.AWAITING_FEEDBACK,
            primary_result=primary_result,
            next_actions=["Review updated content", "Approve or request further changes"]
        )
    
    async def _handle_knowledge_update(self, conversation: ConversationSession, feedback: str, user_feedback: UserFeedback) -> GlobalAgentResponse:
        """Handle knowledge update feedback"""
        # Add knowledge update message to conversation
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="knowledge_update_processed",
            content=f"Knowledge update requested: {feedback}",
            metadata={"feedback_id": user_feedback.feedback_id}
        )
        
        # Create knowledge update request
        knowledge_update = self.conversation_manager.create_knowledge_update(
            session_id=conversation.session_id,
            update_type=KnowledgeUpdateType.PRODUCT_KNOWLEDGE,  # Default type
            target_agent=user_feedback.target_agent or "ism",  # Default to ISM if no target specified
            content=feedback,
            source_feedback=user_feedback.feedback_id
        )
        
        if knowledge_update:
            # Add knowledge update message
            self.conversation_manager.add_message(
                session_id=conversation.session_id,
                sender="system",
                message_type="knowledge_update_created",
                content=f"Knowledge update created: {knowledge_update.update_id}",
                metadata={"knowledge_update_id": knowledge_update.update_id}
            )
        
        return GlobalAgentResponse(
            success=True,
            message=f"Knowledge update request received: {feedback}. This will be processed in the background.",
            session_id=conversation.session_id,
            conversation_state=ConversationState.AWAITING_FEEDBACK,
            next_actions=["Continue with document generation", "Monitor knowledge update progress"]
        )
    
    async def _handle_clarification_request(self, conversation: ConversationSession, feedback: str, user_feedback: UserFeedback) -> GlobalAgentResponse:
        """Handle clarification request feedback"""
        # Add clarification message to conversation
        self.conversation_manager.add_message(
            session_id=conversation.session_id,
            sender="system",
            message_type="clarification_requested",
            content=f"Clarification requested: {feedback}",
            metadata={"feedback_id": user_feedback.feedback_id}
        )
        
        return GlobalAgentResponse(
            success=True,
            message=f"Clarification requested: {feedback}. Please provide additional details.",
            session_id=conversation.session_id,
            conversation_state=ConversationState.AWAITING_FEEDBACK,
            next_actions=["Provide additional information", "Clarify requirements"]
        )


# Global instance for easy access
global_agent = GlobalAgent()