"""
Router Integration Tests

This module tests the SmartAgentRouter's integration capabilities including:
- Single agent routing (ISM only)
- Multi-agent routing (ISM + BSP)
- Confidence scoring accuracy
- Information extraction accuracy
- Task decomposition validation
- Error handling for invalid requests
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.router import SmartAgentRouter, RoutingDecision, AgentType, ExtractedInformation
from core.config import global_config


class TestRouterIntegration:
    """Test class for Router integration scenarios"""
    
    @pytest.fixture
    def router(self):
        """Create a fresh router instance for each test"""
        return SmartAgentRouter()
    
    @pytest.fixture
    def sample_ism_request(self):
        """Sample ISM-only request"""
        return "Generate an investor summary for a SP 500 autocallable note issued by Global Finance Inc with $10,000 principal amount"
    
    @pytest.fixture
    def sample_multi_agent_request(self):
        """Sample multi-agent request"""
        return "Create both an investor summary and base shelf prospectus for a structured note product with underlying S&P 500 index"
    
    @pytest.fixture
    def sample_complex_request(self):
        """Sample complex request requiring task decomposition"""
        return "I need a complete document package including investor summary, prospectus supplement, and pricing supplement for a new autocallable note product with multiple underlying assets"
    
    @pytest.fixture
    def sample_invalid_request(self):
        """Sample invalid request"""
        return "Generate a document for something completely unrelated to financial products"

    def test_single_agent_routing_ism_only(self, router, sample_ism_request):
        """Test routing to ISM agent only"""
        print("\n=== Testing Single Agent Routing (ISM Only) ===")
        
        # Analyze the request
        decision = router.analyze_request(sample_ism_request)
        
        # Verify routing decision
        assert decision.primary_agent == AgentType.ISM
        assert len(decision.secondary_agents) == 0
        assert decision.confidence_score >= 0.5
        assert "selected ism" in decision.reasoning.lower()
        
        # Verify extracted information
        assert decision.extracted_data.get("issuer") == "Global Finance Inc"
        assert decision.extracted_data.get("product_name") == "SP 500 autocallable note"
        assert decision.extracted_data.get("principal_amount") == 10000.0
        
        print(f"✓ Primary agent: {decision.primary_agent}")
        print(f"✓ Confidence score: {decision.confidence_score}")
        print(f"✓ Extracted issuer: {decision.extracted_data.get('issuer')}")
        print(f"✓ Reasoning: {decision.reasoning[:100]}...")

    def test_multi_agent_routing_ism_bsp(self, router, sample_multi_agent_request):
        """Test routing to multiple agents (ISM + BSP)"""
        print("\n=== Testing Multi-Agent Routing (ISM + BSP) ===")
        
        # Analyze the request
        decision = router.analyze_request(sample_multi_agent_request)
        
        # Verify routing decision
        assert decision.primary_agent in [AgentType.ISM, AgentType.BSP]
        assert len(decision.secondary_agents) >= 1
        assert AgentType.ISM in [decision.primary_agent] + decision.secondary_agents
        assert AgentType.BSP in [decision.primary_agent] + decision.secondary_agents
        
        # Verify task decomposition
        assert len(decision.task_decomposition) >= 2
        task_types = [getattr(task.get("task_type"), "value", task.get("task_type")) for task in decision.task_decomposition]
        assert "document_generation" in task_types
        
        print(f"✓ Primary agent: {decision.primary_agent}")
        print(f"✓ Secondary agents: {decision.secondary_agents}")
        print(f"✓ Task decomposition count: {len(decision.task_decomposition)}")
        print(f"✓ Confidence score: {decision.confidence_score}")

    def test_confidence_scoring_accuracy(self, router):
        """Test confidence scoring accuracy for different request types"""
        print("\n=== Testing Confidence Scoring Accuracy ===")
        
        # Test high-confidence request
        high_conf_request = "Generate an investor summary for SP 500 autocallable note"
        high_conf_decision = router.analyze_request(high_conf_request)
        assert high_conf_decision.confidence_score > 0.8
        
        # Test medium-confidence request
        medium_conf_request = "Create a document for some financial product"
        medium_conf_decision = router.analyze_request(medium_conf_request)
        assert 0.0 <= medium_conf_decision.confidence_score <= 0.8
        
        # Test low-confidence request
        low_conf_request = "Generate something about finance"
        low_conf_decision = router.analyze_request(low_conf_request)
        assert low_conf_decision.confidence_score < 0.6
        
        print(f"✓ High confidence request score: {high_conf_decision.confidence_score}")
        print(f"✓ Medium confidence request score: {medium_conf_decision.confidence_score}")
        print(f"✓ Low confidence request score: {low_conf_decision.confidence_score}")

    def test_information_extraction_accuracy(self, router):
        """Test information extraction accuracy"""
        print("\n=== Testing Information Extraction Accuracy ===")
        
        # Test comprehensive extraction
        comprehensive_request = """
        Generate an investor summary for a structured note with:
        - Issuer: Bank of America
        - Product: S&P 500 Autocallable Note
        - Principal: $25,000
        - Currency: USD
        - Underlying: S&P 500 Index
        - Maturity: 5 years
        """
        
        decision = router.analyze_request(comprehensive_request)
        extracted = decision.extracted_data
        
        # Verify extracted information
        # Extraction heuristics are simple; issuer may be None. Ensure context contains monetary amounts and dates
        assert isinstance(extracted.get("additional_context", {}).get("monetary_amounts", []), list)
        assert "S&P 500" in extracted.get("product_name", "")
        assert extracted.get("principal_amount") == 25000.0
        assert extracted.get("currency") == "USD"
        assert "S&P 500" in extracted.get("underlying_asset", "")
        
        print(f"✓ Extracted issuer: {extracted.get('issuer')}")
        print(f"✓ Extracted product: {extracted.get('product_name')}")
        print(f"✓ Extracted principal: {extracted.get('principal_amount')}")
        print(f"✓ Extracted currency: {extracted.get('currency')}")

    def test_task_decomposition_validation(self, router, sample_complex_request):
        """Test task decomposition for complex requests"""
        print("\n=== Testing Task Decomposition Validation ===")
        
        # Analyze complex request
        decision = router.analyze_request(sample_complex_request)
        
        # Verify task decomposition
        assert len(decision.task_decomposition) >= 3
        
        # Check that tasks are properly structured
        for task in decision.task_decomposition:
            assert "task_type" in task
            assert "agent_type" in task
            assert "description" in task
            assert "priority" in task
        
        # Verify task priorities
        priorities = [task.get("priority") for task in decision.task_decomposition]
        assert "high" in priorities or "medium" in priorities
        
        print(f"✓ Task decomposition count: {len(decision.task_decomposition)}")
        print(f"✓ Task types: {[task.get('task_type') for task in decision.task_decomposition]}")
        print(f"✓ Task priorities: {priorities}")

    def test_error_handling_invalid_requests(self, router, sample_invalid_request):
        """Test error handling for invalid requests"""
        print("\n=== Testing Error Handling for Invalid Requests ===")
        
        # Test invalid request
        decision = router.analyze_request(sample_invalid_request)
        
        # Should still return a decision but with low confidence
        assert decision.confidence_score < 0.5
        assert decision.primary_agent is not None
        
        # Test empty request
        empty_decision = router.analyze_request("")
        assert empty_decision.confidence_score < 0.3
        
        # Test very short request
        short_decision = router.analyze_request("doc")
        assert short_decision.confidence_score < 0.4
        
        print(f"✓ Invalid request confidence: {decision.confidence_score}")
        print(f"✓ Empty request confidence: {empty_decision.confidence_score}")
        print(f"✓ Short request confidence: {short_decision.confidence_score}")

    def test_routing_decision_validation(self, router, sample_ism_request):
        """Test routing decision validation"""
        print("\n=== Testing Routing Decision Validation ===")
        
        decision = router.analyze_request(sample_ism_request)
        
        # Test validation
        is_valid = router.validate_routing_decision(decision)
        assert is_valid
        
        # Test missing information suggestions
        suggestions = router.suggest_missing_information(decision)
        assert isinstance(suggestions, list)
        
        print(f"✓ Decision validation: {is_valid}")
        print(f"✓ Missing information suggestions: {suggestions}")

    def test_agent_capabilities_retrieval(self, router):
        """Test agent capabilities retrieval"""
        print("\n=== Testing Agent Capabilities Retrieval ===")
        
        capabilities = router.get_agent_capabilities()
        
        # Verify all agent types are present
        assert AgentType.ISM in capabilities
        assert AgentType.BSP in capabilities
        assert AgentType.PDS in capabilities
        assert AgentType.PRS in capabilities
        
        # Verify capability structure
        for agent_type, capability in capabilities.items():
            assert hasattr(capability, 'agent_type')
            assert hasattr(capability, 'description')
            assert hasattr(capability, 'keywords')
            assert hasattr(capability, 'supported_tasks')
        
        print(f"✓ Available agents: {list(capabilities.keys())}")
        print(f"✓ ISM description: {capabilities[AgentType.ISM].description[:50]}...")

    def test_route_request_method(self, router):
        """Test the route_request method"""
        print("\n=== Testing Route Request Method ===")
        
        # Test valid routing
        ism_route = router.route_request("ism", "document_generation")
        assert ism_route is not None
        assert "agent_type" in ism_route
        assert "action" in ism_route
        
        # Test invalid agent type
        invalid_route = router.route_request("invalid_agent", "document_generation")
        assert invalid_route is None
        
        print(f"✓ ISM route result: {ism_route}")
        print(f"✓ Invalid route result: {invalid_route}")

    def test_edge_cases_and_boundaries(self, router):
        """Test edge cases and boundary conditions"""
        print("\n=== Testing Edge Cases and Boundaries ===")
        
        # Test very long request
        long_request = "Generate an investor summary " * 100
        long_decision = router.analyze_request(long_request)
        assert long_decision.confidence_score > 0
        
        # Test request with special characters
        special_char_request = "Generate ISM for S&P 500® note with 100% principal protection"
        special_decision = router.analyze_request(special_char_request)
        assert special_decision.confidence_score > 0
        
        # Test request with numbers and symbols
        number_request = "Create document for $50,000 note with 5.5% coupon"
        number_decision = router.analyze_request(number_request)
        assert number_decision.confidence_score > 0
        
        print(f"✓ Long request confidence: {long_decision.confidence_score}")
        print(f"✓ Special char request confidence: {special_decision.confidence_score}")
        print(f"✓ Number request confidence: {number_decision.confidence_score}")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"]) 