"""
Core framework components for the multi-agent financial document generation system.

This module provides the foundational classes and utilities for building
specialized financial document agents using Pydantic AI and LightRAG.
"""

from .base_agent import BaseFinancialAgent, BaseFinancialAgentDeps
from .rag_manager import RAGManager
from .config import GlobalConfig

__all__ = [
    "BaseFinancialAgent",
    "BaseFinancialAgentDeps", 
    "RAGManager",
    "GlobalConfig"
]