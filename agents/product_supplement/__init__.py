"""
PDS (Prospectus Supplement) Agent for generating prospectus supplement documents.

This module provides specialized functionality for creating prospectus
supplements that reference base shelf prospectus documents and add
specific structured note details.
"""

from .agent import PDSAgent
from .models import PDSInput, PDSOutput, PDSAgentDeps
from .config import PDSConfig
from .large_text_agent import LargeTextPDSAgent

__all__ = [
    "PDSAgent",
    "PDSInput",
    "PDSOutput",
    "PDSAgentDeps",
    "PDSConfig",
    "LargeTextPDSAgent",
]