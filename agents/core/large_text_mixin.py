"""
Base Large Text Agent Mixin - Unified implementation for all agents.

This mixin provides a consistent interface for template-based document generation
across all financial document agents (ISM, BSP, PDS, PRS).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TypeVar, Generic, Type
from datetime import datetime
from pydantic import BaseModel

# Generic types for different agent models
InputT = TypeVar('InputT', bound=BaseModel)
OutputT = TypeVar('OutputT', bound=BaseModel)


class LargeTextAgentMixin(ABC, Generic[InputT, OutputT]):
    """
    Unified mixin for large text template integration across all agents.
    
    This provides a consistent interface for:
    - Template-based document generation
    - Dictionary output for customers
    - Pydantic model output for testing/validation
    - Field mapping and extraction
    """
    
    def __init__(self, base_agent, config=None):
        """Initialize with base agent and configuration"""
        self.base_agent = base_agent
        self.config = config
        self.agent_type = self._get_agent_type()
    
    @abstractmethod
    def _get_agent_type(self) -> str:
        """Return agent type (ism, bsp, pds, prs)"""
        pass
    
    @abstractmethod
    def _get_template_module(self):
        """Return the template module for this agent"""
        pass
    
    @abstractmethod
    def _get_output_model(self) -> Type[OutputT]:
        """Return the Pydantic output model class"""
        pass
    
    @abstractmethod
    def _get_input_model(self) -> Type[InputT]:
        """Return the Pydantic input model class"""
        pass
    
    async def generate_document_with_large_templates(
        self, 
        input_data: InputT,
        audience: str = "retail",
        custom_variables: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """
        Generate document using large text templates.
        
        Args:
            input_data: Agent-specific input data
            audience: Target audience ("retail" or "institutional")
            custom_variables: Additional variables for template substitution
            
        Returns:
            Dictionary with generated document sections using templates
        """
        print(f"🚀 Generating {self.agent_type.upper()} document with large text templates for {audience} audience...")
        
        # Prepare template variables from input data
        template_variables = self._prepare_template_variables(input_data, custom_variables)
        
        # Get template module
        template_module = self._get_template_module()
        
        # Generate document using templates
        document = template_module.create_complete_document_from_templates(template_variables, audience)
        
        print(f"✅ {self.agent_type.upper()} document generated successfully using large text templates!")
        return document
    
    async def generate_document_for_testing(
        self, 
        input_data: InputT,
        audience: str = "retail",
        custom_variables: Optional[Dict[str, str]] = None
    ) -> OutputT:
        """
        Generate document for testing - returns Pydantic model.
        
        Args:
            input_data: Agent-specific input data
            audience: Target audience
            custom_variables: Additional variables
            
        Returns:
            Pydantic output model for testing and validation
        """
        # Generate dictionary first
        document_dict = await self.generate_document_with_large_templates(
            input_data, audience, custom_variables
        )
        
        # Convert to Pydantic model
        return self._convert_dict_to_output_model(document_dict, input_data)
    
    def _prepare_template_variables(
        self, 
        input_data: InputT, 
        custom_variables: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """
        Convert input data to template variables.
        
        This is the main customization point for each agent.
        """
        # Base variables common to all agents
        variables = {
            "Document Date": datetime.now().strftime("%B %d, %Y"),
            "Generation Date": datetime.now().strftime('%Y-%m-%d'),
            "Document Version": "1.0",
        }
        
        # Add agent-specific variables
        variables.update(self._extract_agent_specific_variables(input_data))
        
        # Add custom variables if provided
        if custom_variables:
            variables.update(custom_variables)
        
        return variables
    
    @abstractmethod
    def _extract_agent_specific_variables(self, input_data: InputT) -> Dict[str, str]:
        """
        Extract agent-specific variables from input data.
        
        This is where each agent customizes the variable extraction.
        """
        pass
    
    def _convert_dict_to_output_model(self, doc_dict: Dict[str, str], input_data: InputT) -> OutputT:
        """
        Convert template dictionary to Pydantic output model.
        
        This provides a unified conversion interface.
        """
        output_model_class = self._get_output_model()
        
        # Create mapping from dictionary to model fields
        field_mapping = self._create_field_mapping(doc_dict, input_data)
        
        # Create and return the output model
        return output_model_class(**field_mapping)
    
    @abstractmethod
    def _create_field_mapping(self, doc_dict: Dict[str, str], input_data: InputT) -> Dict[str, Any]:
        """
        Create field mapping from template dictionary to output model.
        
        This is where each agent defines how template sections map to model fields.
        """
        pass
    
    def _extract_text_field(self, doc_dict: Dict[str, str], key: str, default: str = "") -> str:
        """Helper to extract text fields from template dictionary"""
        return doc_dict.get(key, default)
    
    def _extract_list_field(self, doc_dict: Dict[str, str], key: str) -> list:
        """Helper to extract list fields from template dictionary"""
        content = doc_dict.get(key, "")
        # Parse content into list (implementation varies by agent)
        return self._parse_content_to_list(content)
    
    def _parse_content_to_list(self, content: str) -> list:
        """Parse template content into structured list"""
        # Default implementation - can be overridden by specific agents
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return [line for line in lines if line.startswith('•') or line.startswith('-')]
    
    def _extract_section_content(self, doc_dict: Dict[str, str], section_key: str, default: str = "") -> str:
        """Extract content from a specific section"""
        return doc_dict.get(section_key, default)
    
    def _create_default_field(self, input_data: InputT, field_name: str, default_value: str = "") -> str:
        """Create a default field value based on input data"""
        # This can be overridden by specific agents for custom field creation
        return default_value 