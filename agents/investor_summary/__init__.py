"""
ISM (Investor Summary) Agent for generating investor-friendly summary documents.

This module provides specialized functionality for creating clear, accessible
investor summaries for structured notes and other financial products.
"""

from .agent import ISMAgent
from .models import ISMInput, ISMOutput, ISMAgentDeps
from .config import ISMConfig
from .large_text_integration import LargeTextISMAgent, create_large_text_ism_agent
from .large_text_agent import LargeTextISMAgent as LargeTextISMAgentCompat

__all__ = [
    "ISMAgent",
    "ISMInput", 
    "ISMOutput",
    "ISMAgentDeps",
    "ISMConfig",
    "LargeTextISMAgent",
    "create_large_text_ism_agent",
    "LargeTextISMAgentCompat"
]