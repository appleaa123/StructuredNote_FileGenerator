"""
Base agent class for all financial document generation agents.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Optional, Dict, Type
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from lightrag import LightRAG

from .rag_manager import rag_manager
from .config import global_config


# Type variables for generic agent typing
InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel)
DepsType = TypeVar('DepsType', bound=BaseModel)


class BaseFinancialAgentDeps(BaseModel):
    """
    Base dependencies for all financial agents.
    
    This model defines the common dependencies that all financial document
    agents require, including LightRAG access and agent identification.
    """
    # Allow Any here to enable easy mocking in tests without requiring a real LightRAG instance
    lightrag: Any
    agent_type: str
    config: Optional[Dict[str, Any]] = None
    
    class Config:
        arbitrary_types_allowed = True


class BaseFinancialAgent(ABC, Generic[InputType, OutputType, DepsType]):
    """
    Abstract base class for all financial document agents using Pydantic AI framework.
    
    This class provides the common infrastructure for:
    - LightRAG integration and knowledge retrieval
    - Pydantic AI agent management and tool registration
    - Document generation workflows
    - Error handling and validation
    - Standardized input/output processing
    
    All specialized agents (ISM, BSP, PDS, PRS) should inherit from this class
    and implement the required abstract methods.
    """
    
    def __init__(
        self, 
        agent_type: str, 
        knowledge_base_path: str,
        model_name: str = None,
        agent_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the base financial agent.
        
        Args:
            agent_type: Identifier for the agent type (e.g., 'ism', 'bsp')
            knowledge_base_path: Path to the agent's LightRAG knowledge base
            model_name: LLM model to use (defaults to global config)
            agent_config: Agent-specific configuration overrides
        """
        self.agent_type = agent_type
        self.knowledge_base_path = knowledge_base_path
        self.model_name = model_name or global_config.default_model
        self.agent_config = agent_config or {}
        
        # Initialize the Pydantic AI agent
        self.agent = self._create_agent()
        
        # Register tools after agent creation
        self._register_base_tools()
        self._register_agent_tools()
    
    @abstractmethod
    def _create_agent(self) -> Agent[DepsType, OutputType]:
        """
        Create and configure the Pydantic AI agent.
        
        This method must be implemented by each specialized agent to:
        - Define the agent with appropriate model and types
        - Set system instructions/prompts
        - Configure any agent-specific settings
        
        Returns:
            Configured Pydantic AI agent instance
        """
        pass
    
    @abstractmethod
    def _register_agent_tools(self):
        """
        Register agent-specific tools.
        
        This method should be implemented by each specialized agent to
        register tools that are specific to that agent's domain and
        document generation requirements.
        """
        pass
    
    @abstractmethod
    def get_system_instructions(self) -> str:
        """
        Get agent-specific system instructions.
        
        Returns:
            System instructions/prompts for the agent
        """
        pass
    
    @abstractmethod
    async def _create_dependencies(self, lightrag: LightRAG, input_data: InputType) -> DepsType:
        """
        Create agent-specific dependencies.
        
        Args:
            lightrag: Initialized LightRAG instance
            input_data: Input data for document generation
            
        Returns:
            Agent-specific dependencies object
        """
        pass
    
    @abstractmethod
    def _format_user_prompt(self, input_data: InputType) -> str:
        """
        Format the user prompt based on input data.
        
        Args:
            input_data: Input data for document generation
            
        Returns:
            Formatted prompt string for the LLM
        """
        pass

    @abstractmethod
    async def propose_knowledge_update(self, feedback: str) -> str:
        """
        Propose an update to the knowledge base based on user feedback.
        
        Args:
            feedback: User feedback on generated content
            
        Returns:
            A human-readable plan for the proposed update
        """
        pass

    @abstractmethod
    async def apply_knowledge_update(self, update_plan: Dict[str, Any]):
        """
        Apply an update to the knowledge base.
        
        Args:
            update_plan: The update plan to be executed
        """
        pass
    
    def _register_base_tools(self):
        """
        Register common tools available to all agents.
        
        These tools provide basic functionality that all agents can use,
        such as general knowledge retrieval and cross-domain searches.
        """
        
        @self.agent.tool
        async def retrieve_knowledge(
            ctx: RunContext[DepsType], 
            query: str,
            mode: str = "mix",
            top_k: int = 5
        ) -> str:
            """
            Retrieve knowledge from the agent's domain-specific knowledge base.
            
            Args:
                ctx: The run context containing dependencies
                query: Search query for retrieving relevant information
                mode: Query mode ("mix", "local", "global")
                top_k: Number of top results to return
                
            Returns:
                Retrieved knowledge content
            """
            try:
                result = await rag_manager.query_domain(
                    domain=ctx.deps.agent_type,
                    query=query,
                    mode=mode,
                    top_k=top_k
                )
                return result
            except Exception as e:
                return f"Error retrieving knowledge: {str(e)}"
        
        @self.agent.tool
        async def cross_reference_search(
            ctx: RunContext[DepsType],
            query: str,
            domains: Optional[list] = None,
            mode: str = "mix"
        ) -> str:
            """
            Search across multiple knowledge domains for cross-references.
            
            Args:
                ctx: The run context containing dependencies
                query: Search query
                domains: List of domains to search (defaults to all available)
                mode: Query mode for each domain
                
            Returns:
                Cross-referenced search results
            """
            try:
                if domains is None:
                    domains = rag_manager.list_domains()
                
                # Remove current domain to avoid duplication
                domains = [d for d in domains if d != ctx.deps.agent_type]
                
                if not domains:
                    return "No other domains available for cross-reference search."
                
                results = await rag_manager.cross_domain_query(
                    domains=domains,
                    query=query,
                    mode=mode
                )
                
                # Format results for readability
                formatted_results = []
                for domain, result in results.items():
                    if domain != "error":
                        formatted_results.append(f"**{domain.upper()} Domain:**\n{result}\n")
                
                return "\n".join(formatted_results) if formatted_results else "No relevant cross-references found."
                
            except Exception as e:
                return f"Error in cross-reference search: {str(e)}"
    
    async def initialize_lightrag(self) -> LightRAG:
        """
        Initialize LightRAG instance for this agent.
        
        Returns:
            Initialized LightRAG instance
        """
        return await rag_manager.initialize_rag_instance(
            domain=self.agent_type
        )
    
    async def generate_document(self, input_data: InputType) -> OutputType:
        """
        Generate document using the Pydantic AI agent.
        
        This is the main entry point for document generation. It:
        1. Initializes the LightRAG system
        2. Creates agent dependencies
        3. Formats the user prompt
        4. Runs the Pydantic AI agent
        5. Returns the structured output
        
        Args:
            input_data: Input parameters for document generation
            
        Returns:
            Generated document content as structured output
        """
        try:
            # Initialize LightRAG
            lightrag = await self.initialize_lightrag()
            
            # Create dependencies
            deps = await self._create_dependencies(lightrag, input_data)
            
            # Format user prompt
            user_prompt = self._format_user_prompt(input_data)
            
            # Run the agent
            result = await self.agent.run(user_prompt, deps=deps)

            # Support multiple pydantic_ai return shapes across versions
            if hasattr(result, "data") and result.data is not None:  # legacy
                return result.data  # type: ignore[no-any-return]
            if hasattr(result, "output") and getattr(result, "output") is not None:
                return getattr(result, "output")  # type: ignore[no-any-return]
            # Fallback: try common attribute names before giving up
            for attr in ("result", "final", "value"):
                if hasattr(result, attr) and getattr(result, attr) is not None:
                    return getattr(result, attr)  # type: ignore[no-any-return]
            raise RuntimeError("Agent returned no usable output (missing data/output)")
            
        except Exception as e:
            raise RuntimeError(f"Error generating document with {self.agent_type} agent: {str(e)}")
    
    async def generate_document_with_history(
        self, 
        input_data: InputType,
        message_history: Optional[list] = None
    ) -> OutputType:
        """
        Generate document with conversation history.
        
        Args:
            input_data: Input parameters for document generation
            message_history: Previous conversation messages
            
        Returns:
            Generated document content as structured output
        """
        try:
            # Initialize LightRAG
            lightrag = await self.initialize_lightrag()
            
            # Create dependencies
            deps = await self._create_dependencies(lightrag, input_data)
            
            # Format user prompt
            user_prompt = self._format_user_prompt(input_data)
            
            # Run the agent with message history
            result = await self.agent.run(
                user_prompt, 
                deps=deps,
                message_history=message_history or []
            )

            if hasattr(result, "data") and result.data is not None:
                return result.data  # type: ignore[no-any-return]
            if hasattr(result, "output") and getattr(result, "output") is not None:
                return getattr(result, "output")  # type: ignore[no-any-return]
            for attr in ("result", "final", "value"):
                if hasattr(result, attr) and getattr(result, attr) is not None:
                    return getattr(result, attr)  # type: ignore[no-any-return]
            raise RuntimeError("Agent returned no usable output (missing data/output)")
            
        except Exception as e:
            raise RuntimeError(f"Error generating document with history using {self.agent_type} agent: {str(e)}")
    
    async def validate_input(self, input_data: InputType) -> bool:
        """
        Validate input data for the agent.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Basic Pydantic validation is automatic
            # Agents can override this for additional validation
            return True
        except Exception:
            return False
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the agent.
        
        Returns:
            Dictionary containing agent metadata
        """
        return {
            "agent_type": self.agent_type,
            "model_name": self.model_name,
            "knowledge_base_path": self.knowledge_base_path,
            "config": self.agent_config
        }