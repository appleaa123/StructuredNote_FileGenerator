"""
Agent Factory - Clean interface for creating and managing agents.

This module provides a factory pattern for creating agents with proper
configuration, error handling, and health monitoring.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Type
from datetime import datetime
from dataclasses import dataclass

from . import AgentRegistry, AgentMetadata, AgentStatus, AgentCapability, agent_registry
from .investor_summary import ISMAgent
from .base_shelf_prospectus import BSPAgent
from .product_supplement import PDSAgent
from .pricing_supplement import PRSAgent

# Import large text agents
from .investor_summary.large_text_agent import LargeTextISMAgent
from .base_shelf_prospectus.large_text_agent import LargeTextBSPAgent
from .product_supplement.large_text_agent import LargeTextPDSAgent
from .pricing_supplement.large_text_agent import LargeTextPRSAgent

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class AgentFactoryConfig:
    """Configuration for agent factory"""
    default_model: str = "openai:gpt-4o-mini"
    default_max_tokens: int = 4000
    default_temperature: float = 0.7
    enable_health_monitoring: bool = True
    auto_retry_on_failure: bool = True
    max_retry_attempts: int = 3


class AgentFactory:
    """
    Factory for creating and managing agent instances.
    
    This class provides:
    - Clean agent creation interface
    - Configuration management
    - Health monitoring
    - Error handling and retry logic
    - Agent lifecycle management
    - Support for both base agents and large text agents
    """
    
    def __init__(self, config: Optional[AgentFactoryConfig] = None):
        """Initialize the agent factory"""
        self.config = config or AgentFactoryConfig()
        self.registry = agent_registry
        self.active_agents: Dict[str, Any] = {}
        self.agent_health_cache: Dict[str, Dict[str, Any]] = {}
        
    def create_agent(
        self, 
        agent_type: str, 
        config_overrides: Optional[Dict[str, Any]] = None,
        enable_monitoring: bool = True
    ) -> Optional[Any]:
        """
        Create an agent instance with proper configuration.
        
        Args:
            agent_type: Type of agent to create (investor_summary, base_shelf_prospectus, product_supplement, pricing_supplement)
            config_overrides: Optional configuration overrides
            enable_monitoring: Whether to enable health monitoring
            
        Returns:
            Agent instance or None if creation fails
        """
        try:
            # Backward compatibility mapping
            agent_name_mapping = {
                "ism": "investor_summary",
                "bsp": "base_shelf_prospectus",
                "pds": "product_supplement",
                "prs": "pricing_supplement"
            }
            
            # Map old names to new names
            mapped_agent_type = agent_name_mapping.get(agent_type, agent_type)
            
            # Get agent metadata
            metadata = self.registry.get_agent_metadata(mapped_agent_type)
            if not metadata:
                logger.error(f"Agent type {agent_type} (mapped to {mapped_agent_type}) not found in registry")
                return None
            
            # Check agent status
            if metadata.status == AgentStatus.DEPRECATED:
                logger.warning(f"Agent {agent_type} is deprecated")
            elif metadata.status == AgentStatus.SHELL:
                logger.warning(f"Agent {agent_type} is a shell implementation")
            
            # Prepare configuration
            config = self._prepare_agent_config(agent_type, config_overrides)
            
            # Create agent instance
            agent = self._create_agent_instance(mapped_agent_type, config)
            if not agent:
                return None
            
            # Register for monitoring if enabled
            if enable_monitoring:
                self.active_agents[agent_type] = {
                    "instance": agent,
                    "created_at": datetime.now(),
                    "config": config,
                    "health_status": "unknown"
                }
            
            return agent
            
        except Exception as e:
            logger.error(f"Error creating agent {agent_type}: {e}")
            return None
    
    def create_large_text_agent(
        self, 
        agent_type: str, 
        config_overrides: Optional[Dict[str, Any]] = None,
        enable_monitoring: bool = True
    ) -> Optional[Any]:
        """
        Create a large text agent instance with proper configuration.
        
        Args:
            agent_type: Type of agent to create (ism, bsp, pds, prs)
            config_overrides: Optional configuration overrides
            enable_monitoring: Whether to enable health monitoring
            
        Returns:
            Large text agent instance or None if creation fails
        """
        try:
            # Get agent metadata
            metadata = self.registry.get_agent_metadata(agent_type)
            if not metadata:
                logger.error(f"Agent type {agent_type} not found in registry")
                return None
            
            # Check agent status
            if metadata.status == AgentStatus.DEPRECATED:
                logger.warning(f"Agent {agent_type} is deprecated")
            elif metadata.status == AgentStatus.SHELL:
                logger.warning(f"Agent {agent_type} is a shell implementation")
            
            # Prepare configuration
            config = self._prepare_agent_config(agent_type, config_overrides)
            
            # Create base agent first
            base_agent = self._create_agent_instance(agent_type, config)
            if not base_agent:
                return None
            
            # Create large text agent wrapper
            large_text_agent = self._create_large_text_agent_instance(agent_type, base_agent, config)
            if not large_text_agent:
                return None
            
            # Register for monitoring if enabled
            if enable_monitoring:
                self.active_agents[f"{agent_type}_large_text"] = {
                    "instance": large_text_agent,
                    "created_at": datetime.now(),
                    "config": config,
                    "health_status": "unknown"
                }
            
            return large_text_agent
            
        except Exception as e:
            logger.error(f"Error creating large text agent {agent_type}: {e}")
            return None
    
    def create_agent_with_retry(
        self, 
        agent_type: str, 
        config_overrides: Optional[Dict[str, Any]] = None,
        max_attempts: Optional[int] = None
    ) -> Optional[Any]:
        """
        Create an agent with retry logic.
        
        Args:
            agent_type: Type of agent to create
            config_overrides: Optional configuration overrides
            max_attempts: Maximum retry attempts (uses factory default if None)
            
        Returns:
            Agent instance or None if all attempts fail
        """
        max_attempts = max_attempts or self.config.max_retry_attempts
        
        for attempt in range(max_attempts):
            try:
                agent = self.create_agent(agent_type, config_overrides)
                if agent:
                    logger.info(f"Successfully created agent {agent_type} on attempt {attempt + 1}")
                    return agent
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for agent {agent_type}: {e}")
                
                if attempt < max_attempts - 1:
                    logger.info(f"Retrying agent creation for {agent_type}...")
                    asyncio.sleep(1)  # Brief delay before retry
        
        logger.error(f"Failed to create agent {agent_type} after {max_attempts} attempts")
        return None
    
    def create_agents_by_capability(
        self, 
        capability: AgentCapability,
        config_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create all agents with a specific capability.
        
        Args:
            capability: Capability to filter by
            config_overrides: Optional configuration overrides
            
        Returns:
            Dictionary of created agents
        """
        agents = {}
        matching_agents = self.registry.get_agents_by_capability(capability)
        
        for metadata in matching_agents:
            agent_type = metadata.agent_type
            agent = self.create_agent(agent_type, config_overrides)
            if agent:
                agents[agent_type] = agent
        
        return agents
    
    def get_agent_health(self, agent_type: str) -> Dict[str, Any]:
        """
        Get health information for a specific agent.
        
        Args:
            agent_type: Type of agent to check
            
        Returns:
            Health information dictionary
        """
        if agent_type not in self.active_agents:
            return {
                "status": "not_found",
                "message": f"Agent {agent_type} not found in active agents"
            }
        
        agent_info = self.active_agents[agent_type]
        
        try:
            # Basic health check - try to access agent attributes
            agent = agent_info["instance"]
            health_status = "healthy"
            
            # Check if agent has required attributes
            if hasattr(agent, 'agent_type'):
                agent_type_check = agent.agent_type
            else:
                health_status = "warning"
                agent_type_check = "unknown"
            
            return {
                "status": health_status,
                "agent_type": agent_type_check,
                "created_at": agent_info["created_at"].isoformat(),
                "config": agent_info["config"],
                "health_status": agent_info["health_status"]
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "agent_type": agent_type
            }
    
    def get_all_agent_health(self) -> Dict[str, Dict[str, Any]]:
        """
        Get health information for all active agents.
        
        Returns:
            Dictionary of health information for all agents
        """
        health_info = {}
        
        for agent_type in self.active_agents:
            health_info[agent_type] = self.get_agent_health(agent_type)
        
        return health_info
    
    def cleanup_agent(self, agent_type: str) -> bool:
        """
        Clean up a specific agent.
        
        Args:
            agent_type: Type of agent to clean up
            
        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            if agent_type in self.active_agents:
                # Perform any cleanup needed for the agent
                agent_info = self.active_agents[agent_type]
                agent = agent_info["instance"]
                
                # Call cleanup method if it exists
                if hasattr(agent, 'cleanup'):
                    agent.cleanup()
                
                # Remove from active agents
                del self.active_agents[agent_type]
                
                logger.info(f"Successfully cleaned up agent {agent_type}")
                return True
            else:
                logger.warning(f"Agent {agent_type} not found in active agents")
                return False
                
        except Exception as e:
            logger.error(f"Error cleaning up agent {agent_type}: {e}")
            return False
    
    def cleanup_all_agents(self) -> Dict[str, bool]:
        """
        Clean up all active agents.
        
        Returns:
            Dictionary of cleanup results for each agent
        """
        results = {}
        
        for agent_type in list(self.active_agents.keys()):
            results[agent_type] = self.cleanup_agent(agent_type)
        
        return results
    
    def get_active_agents(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all active agents.
        
        Returns:
            Dictionary of active agent information
        """
        return self.active_agents.copy()
    
    def _prepare_agent_config(
        self, 
        agent_type: str, 
        config_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Prepare configuration for agent creation"""
        # Get default config from registry
        metadata = self.registry.get_agent_metadata(agent_type)
        default_config = metadata.config_schema or {}
        
        # Apply factory defaults
        config = {
            "model_name": self.config.default_model,
            "max_tokens": self.config.default_max_tokens,
            "temperature": self.config.default_temperature,
            **default_config
        }
        
        # Apply overrides
        if config_overrides:
            config.update(config_overrides)
        
        return config
    
    def _create_agent_instance(self, agent_type: str, config: Dict[str, Any]) -> Optional[Any]:
        """Create the actual agent instance"""
        try:
            if agent_type == "ism" or agent_type == "investor_summary":
                return ISMAgent(
                    knowledge_base_path=config.get("knowledge_base_path", "knowledge_bases/investor_summary_kb/"),
                    model_name=config.get("model_name", self.config.default_model)
                )
            elif agent_type == "bsp" or agent_type == "base_shelf_prospectus":
                return BSPAgent(
                    knowledge_base_path=config.get("knowledge_base_path", "knowledge_bases/base_shelf_prospectus_kb/"),
                    model_name=config.get("model_name", self.config.default_model)
                )
            elif agent_type == "pds" or agent_type == "product_supplement":
                return PDSAgent(
                    knowledge_base_path=config.get("knowledge_base_path", "knowledge_bases/product_supplement_kb/"),
                    model_name=config.get("model_name", self.config.default_model)
                )
            elif agent_type == "prs" or agent_type == "pricing_supplement":
                return PRSAgent(
                    knowledge_base_path=config.get("knowledge_base_path", "knowledge_bases/pricing_supplement_kb/"),
                    model_name=config.get("model_name", self.config.default_model)
                )
            else:
                logger.error(f"Unknown agent type: {agent_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating agent instance for {agent_type}: {e}")
            return None
    
    def _create_large_text_agent_instance(self, agent_type: str, base_agent: Any, config: Dict[str, Any]) -> Optional[Any]:
        """Create the actual large text agent instance"""
        try:
            if agent_type == "ism" or agent_type == "investor_summary":
                return LargeTextISMAgent(base_agent, config)
            elif agent_type == "bsp" or agent_type == "base_shelf_prospectus":
                return LargeTextBSPAgent(base_agent, config)
            elif agent_type == "pds" or agent_type == "product_supplement":
                return LargeTextPDSAgent(base_agent, config)
            elif agent_type == "prs" or agent_type == "pricing_supplement":
                return LargeTextPRSAgent(base_agent, config)
            else:
                logger.error(f"Unknown agent type for large text agent: {agent_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating large text agent instance for {agent_type}: {e}")
            return None


# Global factory instance
agent_factory = AgentFactory()


def get_agent_factory() -> AgentFactory:
    """Get the global agent factory"""
    return agent_factory


def create_agent_with_factory(
    agent_type: str, 
    config_overrides: Optional[Dict[str, Any]] = None
) -> Optional[Any]:
    """Create an agent using the global factory"""
    return agent_factory.create_agent(agent_type, config_overrides)


def create_large_text_agent_with_factory(
    agent_type: str, 
    config_overrides: Optional[Dict[str, Any]] = None
) -> Optional[Any]:
    """Create a large text agent using the global factory"""
    return agent_factory.create_large_text_agent(agent_type, config_overrides)


def create_agents_by_capability(
    capability: AgentCapability,
    config_overrides: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create all agents with a specific capability"""
    return agent_factory.create_agents_by_capability(capability, config_overrides)


def get_agent_health(agent_type: str) -> Dict[str, Any]:
    """Get health information for a specific agent"""
    return agent_factory.get_agent_health(agent_type)


def get_all_agent_health() -> Dict[str, Dict[str, Any]]:
    """Get health information for all agents"""
    return agent_factory.get_all_agent_health()


# Export factory functions
__all__ = [
    "AgentFactory",
    "AgentFactoryConfig",
    "agent_factory",
    "get_agent_factory",
    "create_agent_with_factory",
    "create_large_text_agent_with_factory",
    "create_agents_by_capability",
    "get_agent_health",
    "get_all_agent_health"
] 