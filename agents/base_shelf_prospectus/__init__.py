"""
BSP (Base Shelf Prospectus) Agent for generating base shelf prospectus documents.

This module provides specialized functionality for creating comprehensive legal
documents that serve as the foundation for multiple structured note issuances.
"""

from .agent import BSPAgent
from .models import BSPInput, BSPOutput, BSPAgentDeps
from .config import BSPConfig
from .large_text_integration import LargeTextBSPAgent, create_large_text_bsp_agent
from .large_text_agent import LargeTextBSPAgent as LargeTextBSPAgentCompat

__all__ = [
    "BSPAgent",
    "BSPInput", 
    "BSPOutput",
    "BSPAgentDeps",
    "BSPConfig",
    "LargeTextBSPAgent",
    "create_large_text_bsp_agent",
    "LargeTextBSPAgentCompat"
]