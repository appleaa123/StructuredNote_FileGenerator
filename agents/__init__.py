"""
Agent implementations for specialized financial document generation.

This package contains all the specialized agents for different document types:
- ISM: Investor Summary documents  
- BSP: Base Shelf Prospectus documents
- PDS: Prospectus Supplement documents
- PRS: Pricing Supplement documents

Each agent is designed to handle specific document types with specialized
capabilities for financial document generation, compliance checking, and
knowledge management.
"""

import asyncio
from typing import Dict, List, Optional, Any, Type
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from .investor_summary import ISMAgent

from .base_shelf_prospectus import BSPAgent
from .product_supplement import PDSAgent
from .pricing_supplement import PRSAgent


class AgentStatus(Enum):
    """Status of agent implementations"""
    AVAILABLE = "available"      # Fully implemented and ready
    SHELL = "shell"             # Basic structure, needs implementation
    DEVELOPMENT = "development"  # In development
    DEPRECATED = "deprecated"   # No longer maintained


class AgentCapability(Enum):
    """Capabilities that agents can have"""
    DOCUMENT_GENERATION = "document_generation"
    TEMPLATE_RETRIEVAL = "template_retrieval"
    COMPLIANCE_CHECK = "compliance_check"
    KNOWLEDGE_UPDATE = "knowledge_update"
    CROSS_REFERENCE = "cross_reference"
    MULTI_AGENT_COORDINATION = "multi_agent_coordination"


@dataclass
class AgentMetadata:
    """Metadata for agent registration"""
    agent_type: str
    class_name: str
    description: str
    status: AgentStatus
    capabilities: List[AgentCapability]
    version: str
    last_updated: datetime
    health_status: str = "unknown"
    dependencies: List[str] = None
    config_schema: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class AgentRegistry:
    """
    Registry for managing all available agents.
    
    This class provides:
    - Agent discovery and registration
    - Capability-based agent selection
    - Health monitoring and status tracking
    - Factory pattern for agent creation
    - Metadata management
    """
    
    def __init__(self):
        """Initialize the agent registry"""
        self._agents: Dict[str, AgentMetadata] = {}
        self._agent_classes: Dict[str, Type] = {}
        self._initialize_registry()
    
    def _initialize_registry(self):
        """Initialize the registry with all available agents"""
        # Register Investor Summary Agent
        self.register_agent(
            agent_type="investor_summary",
            class_name="ISMAgent",
            description="Investor Summary Agent - Generates investor-friendly summary documents for structured products",
            status=AgentStatus.AVAILABLE,
            capabilities=[
                AgentCapability.DOCUMENT_GENERATION,
                AgentCapability.TEMPLATE_RETRIEVAL,
                AgentCapability.COMPLIANCE_CHECK,
                AgentCapability.KNOWLEDGE_UPDATE
            ],
            version="1.0.0",
            last_updated=datetime.now(),
            health_status="healthy",
            dependencies=["pydantic-ai", "lightrag", "openai"],
            config_schema={
                "model_name": "openai:gpt-4o-mini",
                "knowledge_base_path": "knowledge_bases/investor_summary_kb/",
                "max_tokens": 4000,
                "temperature": 0.7
            }
        )
        
        # Register Base Shelf Prospectus Agent
        self.register_agent(
            agent_type="base_shelf_prospectus",
            class_name="BSPAgent",
            description="Base Shelf Prospectus Agent - Generates base shelf prospectus documents for structured product programs",
            status=AgentStatus.AVAILABLE,
            capabilities=[
                AgentCapability.DOCUMENT_GENERATION,
                AgentCapability.TEMPLATE_RETRIEVAL,
                AgentCapability.COMPLIANCE_CHECK,
                AgentCapability.KNOWLEDGE_UPDATE
            ],
            version="1.0.0",
            last_updated=datetime.now(),
            health_status="healthy",
            dependencies=["pydantic-ai", "lightrag", "openai"],
            config_schema={
                "model_name": "openai:gpt-4o-mini",
                "knowledge_base_path": "knowledge_bases/base_shelf_prospectus_kb/",
                "max_tokens": 4000,
                "temperature": 0.7
            }
        )
        
        # Register Product Supplement Agent
        self.register_agent(
            agent_type="product_supplement",
            class_name="PDSAgent",
            description="Product Supplement Agent - Generates product supplement documents for specific offerings",
            status=AgentStatus.AVAILABLE,
            capabilities=[
                AgentCapability.DOCUMENT_GENERATION,
                AgentCapability.TEMPLATE_RETRIEVAL,
                AgentCapability.COMPLIANCE_CHECK,
                AgentCapability.KNOWLEDGE_UPDATE
            ],
            version="1.0.0",
            last_updated=datetime.now(),
            health_status="healthy",
            dependencies=["pydantic-ai", "lightrag", "openai"],
            config_schema={
                "model_name": "openai:gpt-4o-mini",
                "knowledge_base_path": "knowledge_bases/product_supplement_kb/",
                "max_tokens": 4000,
                "temperature": 0.7
            }
        )
        
        # Register Pricing Supplement Agent
        self.register_agent(
            agent_type="pricing_supplement",
            class_name="PRSAgent",
            description="Pricing Supplement Agent - Generates pricing supplement documents with specific product terms",
            status=AgentStatus.AVAILABLE,
            capabilities=[
                AgentCapability.DOCUMENT_GENERATION,
                AgentCapability.TEMPLATE_RETRIEVAL,
                AgentCapability.COMPLIANCE_CHECK,
                AgentCapability.KNOWLEDGE_UPDATE
            ],
            version="1.0.0",
            last_updated=datetime.now(),
            health_status="healthy",
            dependencies=["pydantic-ai", "lightrag", "openai"],
            config_schema={
                "model_name": "openai:gpt-4o-mini",
                "knowledge_base_path": "knowledge_bases/pricing_supplement_kb/",
                "max_tokens": 4000,
                "temperature": 0.7
            }
        )
        
        # Register agent classes (support both old and new names for backward compatibility)
        self._agent_classes = {
            "ism": ISMAgent,
            "investor_summary": ISMAgent,
            "bsp": BSPAgent,
            "base_shelf_prospectus": BSPAgent,
            "pds": PDSAgent,
            "product_supplement": PDSAgent,
            "prs": PRSAgent,
            "pricing_supplement": PRSAgent
        }
    
    def register_agent(
        self,
        agent_type: str,
        class_name: str,
        description: str,
        status: AgentStatus,
        capabilities: List[AgentCapability],
        version: str,
        last_updated: datetime,
        health_status: str = "unknown",
        dependencies: List[str] = None,
        config_schema: Optional[Dict[str, Any]] = None
    ):
        """Register an agent in the registry"""
        metadata = AgentMetadata(
            agent_type=agent_type,
            class_name=class_name,
            description=description,
            status=status,
            capabilities=capabilities,
            version=version,
            last_updated=last_updated,
            health_status=health_status,
            dependencies=dependencies or [],
            config_schema=config_schema
        )
        
        self._agents[agent_type] = metadata
    
    def get_agent_metadata(self, agent_type: str) -> Optional[AgentMetadata]:
        """Get metadata for a specific agent"""
        # Backward compatibility mapping
        agent_name_mapping = {
            "ism": "investor_summary",
            "bsp": "base_shelf_prospectus",
            "pds": "product_supplement",
            "prs": "pricing_supplement"
        }
        
        # Map old names to new names
        mapped_agent_type = agent_name_mapping.get(agent_type, agent_type)
        
        return self._agents.get(mapped_agent_type)
    
    def get_all_agents(self) -> Dict[str, AgentMetadata]:
        """Get all registered agents"""
        return self._agents.copy()
    
    def get_agents_by_capability(self, capability: AgentCapability) -> List[AgentMetadata]:
        """Get all agents that have a specific capability"""
        return [
            metadata for metadata in self._agents.values()
            if capability in metadata.capabilities
        ]
    
    def get_agents_by_status(self, status: AgentStatus) -> List[AgentMetadata]:
        """Get all agents with a specific status"""
        return [
            metadata for metadata in self._agents.values()
            if metadata.status == status
        ]
    
    def get_agent_class(self, agent_type: str) -> Optional[Type]:
        """Get the class for a specific agent type"""
        return self._agent_classes.get(agent_type)
    
    def create_agent(self, agent_type: str, **kwargs) -> Optional[Any]:
        """Create an instance of a specific agent"""
        agent_class = self.get_agent_class(agent_type)
        if agent_class is None:
            return None
        
        try:
            return agent_class(**kwargs)
        except Exception as e:
            print(f"Error creating agent {agent_type}: {e}")
            return None
    
    def get_agent_status_summary(self) -> Dict[str, Any]:
        """Get a summary of all agent statuses"""
        summary = {
            "total_agents": len(self._agents),
            "available_agents": len(self.get_agents_by_status(AgentStatus.AVAILABLE)),
            "shell_agents": len(self.get_agents_by_status(AgentStatus.SHELL)),
            "development_agents": len(self.get_agents_by_status(AgentStatus.DEVELOPMENT)),
            "agents_by_type": {}
        }
        
        for agent_type, metadata in self._agents.items():
            summary["agents_by_type"][agent_type] = {
                "status": metadata.status.value,
                "health": metadata.health_status,
                "capabilities": [cap.value for cap in metadata.capabilities],
                "version": metadata.version,
                "last_updated": metadata.last_updated.isoformat()
            }
        
        return summary
    
    def update_agent_health(self, agent_type: str, health_status: str):
        """Update the health status of an agent"""
        if agent_type in self._agents:
            self._agents[agent_type].health_status = health_status
            self._agents[agent_type].last_updated = datetime.now()
    
    def check_agent_health(self, agent_type: str) -> Dict[str, Any]:
        """Check the health of a specific agent"""
        metadata = self.get_agent_metadata(agent_type)
        if not metadata:
            return {"status": "not_found", "error": f"Agent {agent_type} not found"}
        
        # Try to create an instance to test health
        try:
            agent_instance = self.create_agent(agent_type)
            if agent_instance:
                health_status = "healthy"
                error = None
            else:
                health_status = "unhealthy"
                error = "Failed to create agent instance"
        except Exception as e:
            health_status = "unhealthy"
            error = str(e)
        
        # Update health status
        self.update_agent_health(agent_type, health_status)
        
        return {
            "agent_type": agent_type,
            "status": health_status,
            "error": error,
            "capabilities": [cap.value for cap in metadata.capabilities],
            "version": metadata.version,
            "last_updated": metadata.last_updated.isoformat()
        }


# Global registry instance
agent_registry = AgentRegistry()


def get_agent_registry() -> AgentRegistry:
    """Get the global agent registry"""
    return agent_registry


def get_agent_metadata(agent_type: str) -> Optional[AgentMetadata]:
    """Get metadata for a specific agent"""
    return agent_registry.get_agent_metadata(agent_type)


def get_all_agents() -> Dict[str, AgentMetadata]:
    """Get all registered agents"""
    return agent_registry.get_all_agents()


def create_agent(agent_type: str, **kwargs) -> Optional[Any]:
    """Create an instance of a specific agent"""
    return agent_registry.create_agent(agent_type, **kwargs)


def get_agents_by_capability(capability: AgentCapability) -> List[AgentMetadata]:
    """Get all agents that have a specific capability"""
    return agent_registry.get_agents_by_capability(capability)


def get_agent_status_summary() -> Dict[str, Any]:
    """Get a summary of all agent statuses"""
    return agent_registry.get_agent_status_summary()


# Export all agent classes for backward compatibility
__all__ = [
    "ISMAgent",
    "BSPAgent", 
    "PDSAgent",
    "PRSAgent",
    "AgentRegistry",
    "AgentMetadata",
    "AgentStatus",
    "AgentCapability",
    "agent_registry",
    "get_agent_registry",
    "get_agent_metadata",
    "get_all_agents",
    "create_agent",
    "get_agents_by_capability",
    "get_agent_status_summary"
]