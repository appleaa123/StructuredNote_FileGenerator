"""
Large Text Agent for ISM

This module provides the LargeTextISMAgent class for backward compatibility.
The main implementation is now in large_text_integration.py.
"""

from .large_text_integration import LargeTextISMAgent, create_large_text_ism_agent

# Re-export for backward compatibility
__all__ = ['LargeTextISMAgent', 'create_large_text_ism_agent'] 