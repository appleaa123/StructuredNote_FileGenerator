"""
PRS (Pricing Supplement) Agent for generating pricing supplement documents.

This module provides specialized functionality for creating pricing
supplements that contain final pricing and terms, referencing the
base shelf prospectus.
"""

from .agent import PRSAgent
from .models import PRSInput, PRSOutput, PRSAgentDeps
from .config import PRSConfig
from .large_text_agent import LargeTextPRSAgent
from .document_generator import PRSDocumentGenerator
 
__all__ = [
    "PRSAgent",
    "PRSInput", 
    "PRSOutput",
    "PRSAgentDeps",
    "PRSConfig",
    "LargeTextPRSAgent",
    "PRSDocumentGenerator",
]