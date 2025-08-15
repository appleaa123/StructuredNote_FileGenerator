"""
Large Text Agent Wrapper for BSP Agent

This module provides backward compatibility for the BSP large text agent,
following the same pattern as the ISM agent implementation.
"""

from typing import Optional, Dict, Any
from agents.base_shelf_prospectus.large_text_integration import LargeTextBSPAgent as LargeTextBSPAgentCompat

# Backward compatibility alias
LargeTextBSPAgent = LargeTextBSPAgentCompat

# Export the main class for backward compatibility
__all__ = ["LargeTextBSPAgent"] 