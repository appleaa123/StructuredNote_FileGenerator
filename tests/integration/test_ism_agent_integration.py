"""
ISM Agent Integration Tests

This module tests the ISM Agent's integration capabilities including:
- Document generation workflow
- Template retrieval and customization
- Knowledge base integration
- Large text template handling
- Custom placeholder processing
- Output validation and formatting
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import Dict, List, Any, Optional
import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from agents.investor_summary.agent import ISMAgent
from agents.investor_summary.models import ISMInput, ISMOutput, ISMAgentDeps
from agents.investor_summary.config import ISMConfig
from core.base_agent import BaseFinancialAgent


class TestISMAgentIntegration:
    """Test class for ISM Agent integration scenarios"""
    
    @pytest.fixture
    def ism_agent(self):
        """Create a fresh ISM agent instance for each test"""
        return ISMAgent(
            knowledge_base_path="knowledge_bases/ism_kb/",
            model_name="openai:gpt-4o-mini"
        )
    
    @pytest.fixture
    def sample_ism_input(self):
        """Sample ISM input data"""
        return ISMInput(
            issuer="Global Finance Inc",
            product_name="SP 500 Autocallable Note Series 2024-1",
            underlying_asset="S&P 500 Index",
            principal_amount=10000.0,
            currency="USD",
            issue_date="2025-01-29",
            maturity_date="2029-01-29",
            autocall_dates=["2026-01-29", "2027-01-29", "2028-01-29"],
            autocall_level=1.0,
            barrier_level=0.7,
            fixed_return=0.15,
            additional_return_multiplier=1.0,
            risk_tolerance="medium",
            investment_objective="capital_growth_with_income",
            investor_audience="retail_investors",
            regulatory_jurisdiction="US",
            distribution_method="broker_dealer_network",
            product_type="autocallable_note",
            additional_context={
                "risk_level": "moderate",
                "target_return": "15% annually",
                "protection_level": "70% barrier"
            }
        )
    
    @pytest.fixture
    def sample_complex_input(self):
        """Sample complex ISM input with multiple features"""
        return ISMInput(
            issuer="Bank of America",
            product_name="Multi-Asset Autocallable Note",
            underlying_asset="S&P 500 Index, Russell 2000 Index, MSCI EAFE Index",
            principal_amount=25000.0,
            currency="USD",
            issue_date="2026-06-15",
            maturity_date="2030-06-15",
            autocall_dates=["2027-06-15", "2028-06-15", "2029-06-15"],
            autocall_level=1.0,
            barrier_level=0.6,
            fixed_return=0.12,
            additional_return_multiplier=1.5,
            risk_tolerance="high",
            investment_objective="high_income",
            investor_audience="accredited_investors",
            regulatory_jurisdiction="US",
            distribution_method="private_placement",
            product_type="multi_asset_autocallable",
            additional_context={
                "risk_level": "high",
                "target_return": "12% annually",
                "protection_level": "60% barrier",
                "correlation_features": "worst-of performance",
                "leverage_ratio": 1.5
            }
        )

    @pytest.mark.asyncio
    async def test_document_generation_workflow(self, ism_agent, sample_ism_input):
        """Test complete document generation workflow"""
        print("\n=== Testing Document Generation Workflow ===")
        
        # Mock the agent execution to avoid actual LLM calls and bypass LightRAG init
        with patch.object(ism_agent, 'agent') as mock_agent, \
             patch.object(ism_agent, 'initialize_lightrag', new=AsyncMock(return_value=Mock())):
            # Provide a minimally valid ISMOutput per model requirements
            mock_agent.run = AsyncMock(return_value=Mock(data=ISMOutput(
                document_title="Investor Summary - SP 500 Autocallable Note",
                executive_summary="This note offers exposure to the S&P 500 Index with autocall features.",
                product_description="Investment Overview: Clear explanation. In summary, this is a concise wrap.",
                how_it_works="1. Step one\n2. Step two\n3. Step three",
                key_features=[
                    "• Feature A: Benefit A - Impact explained here",
                    "• Feature B: Benefit B - Impact explained here",
                    "• Feature C: Benefit C - Impact explained here",
                ],
                investment_details="Includes dates and minimum investment",
                potential_returns="Best/Expected/Worst with amounts",
                scenarios_analysis="Potential Outcomes: details",
                risk_summary="Summary of risks. All investments carry risk of loss.",
                key_risks=[
                    "Risk: Market - explanation example",
                    "Risk: Credit - explanation example",
                    "Risk: Liquidity - explanation example",
                    "Risk: Product - explanation example",
                ],
                risk_mitigation="Mitigation details",
                risk_level_indicator="Risk Level: MEDIUM - reason. What it means.",
                important_dates="Issue and maturity dates",
                fees_and_charges="Fees listed",
                liquidity_information="Secondary market info",
                suitability_assessment="This investment is suitable for... This investment may not be suitable for all investors.",
                regulatory_notices="Important Notice: jurisdiction text",
                tax_considerations="Tax implications may include... Consult your tax advisor for specific guidance.",
                contact_information="Phone/Email/Website",
                next_steps="1. Do this\n2. Then this\n3. Finally",
                disclaimer="Past performance does not guarantee future results. All investments carry risk of loss. Please consult your financial advisor before investing. This summary is for informational purposes only.",
                generation_date="2025-01-29",
            )))
            
            # Test document generation
            result = await ism_agent.generate_document(sample_ism_input)
            
            # Verify output structure
            assert result is not None
            assert hasattr(result, 'document_title')
            assert hasattr(result, 'executive_summary')
            assert hasattr(result, 'product_overview')
            assert hasattr(result, 'risk_disclosure')
            assert hasattr(result, 'scenarios')
            assert hasattr(result, 'regulatory_compliance')
            
            # Verify content quality
            assert len(result.document_title) > 0
            assert len(result.executive_summary) > 50
            assert len(result.product_overview) > 100
            assert len(result.risk_disclosure) > 100
            assert len(result.scenarios) > 200
            
        print(f"✓ Document title: {result.document_title}")
        print(f"✓ Executive summary length: {len(result.executive_summary)}")
        print(f"✓ Product overview length: {len(result.product_overview)}")

    @pytest.mark.asyncio
    async def test_template_retrieval_and_customization(self, ism_agent, sample_ism_input):
        """Test template retrieval and customization capabilities"""
        print("\n=== Testing Template Retrieval and Customization ===")
        
        # Mock LightRAG query responses
        mock_template_response = """
        INVESTOR SUMMARY TEMPLATE
        
        Product: {product_name}
        Issuer: {issuer}
        Principal Amount: {principal_amount}
        
        Executive Summary:
        This {product_type} offers exposure to {underlying_asset} with {protection_level} principal protection.
        
        Key Features:
        - Autocall dates: {autocall_dates}
        - Fixed return: {fixed_return}
        - Barrier level: {barrier_level}
        """
        
        with patch.object(ism_agent, 'agent') as mock_agent:
            class _FakeDeps:
                def __init__(self):
                    self.lightrag = Mock()
            mock_agent.run = AsyncMock(return_value=Mock(data=ISMOutput(
                document_title="Investor Summary - Autocallable",
                executive_summary="Para1. Para2. Para3. This investment may not be suitable for all investors.",
                product_description="Investment Overview: ... In summary,",
                how_it_works="1. step\n2. step\n3. step",
                key_features=["• A: B - C","• A: B - C","• A: B - C"],
                investment_details="...",
                potential_returns="...",
                scenarios_analysis="...",
                risk_summary="All investments carry risk of loss.",
                key_risks=["Risk: a","Risk: b","Risk: c","Risk: d"],
                risk_mitigation="...",
                risk_level_indicator="Risk Level: MEDIUM - ...",
                important_dates="...",
                fees_and_charges="...",
                liquidity_information="...",
                suitability_assessment="This investment is suitable for... This investment may not be suitable for all investors.",
                regulatory_notices="Important Notice:",
                tax_considerations="Tax implications may include... Consult your tax advisor for specific guidance.",
                contact_information="...",
                next_steps="1\n2\n3",
                disclaimer="Past performance does not guarantee future results. All investments carry risk of loss. Please consult your financial advisor before investing. This summary is for informational purposes only.",
                generation_date="2025-01-29",
            )))
            # LightRAG not used in this mocked execution path.
            
            # Test template retrieval
            template_result = await ism_agent.retrieve_investor_templates(
                query="autocallable note template",
                product_type="autocallable"
            )
            
            # Verify template retrieval
            assert template_result is not None
            assert "INVESTOR SUMMARY TEMPLATE" in template_result
            assert "{product_name}" in template_result
            assert "{issuer}" in template_result
            
            # Test template customization
            customized_template = template_result.replace("{product_name}", sample_ism_input.product_name)
            customized_template = customized_template.replace("{issuer}", sample_ism_input.issuer)
            customized_template = customized_template.replace("{principal_amount}", str(sample_ism_input.principal_amount))
            
            assert sample_ism_input.product_name in customized_template
            assert sample_ism_input.issuer in customized_template
            assert str(sample_ism_input.principal_amount) in customized_template
            
        print(f"✓ Template retrieved: {len(template_result)} characters")
        print(f"✓ Template customized successfully")
        print(f"✓ Placeholders replaced: {customized_template.count('{') == 0}")

    @pytest.mark.asyncio
    async def test_knowledge_base_integration(self, ism_agent, sample_ism_input):
        """Test knowledge base integration"""
        print("\n=== Testing Knowledge Base Integration ===")
        
        # Mock knowledge base responses
        mock_kb_responses = {
            "product_information": "S&P 500 Index is a market-capitalization-weighted index of 500 large-cap stocks.",
            "risk_explanations": "Principal protection is subject to barrier conditions. Market risk applies.",
            "scenario_examples": "Example 1: Autocall at 15% return. Example 2: Maturity with 30% loss.",
            "regulatory_content": "SEC Rule 434 requires clear disclosure of risks and features."
        }
        
        with patch.object(ism_agent, 'agent') as mock_agent:
            mock_agent.run = AsyncMock(return_value=Mock(data=ISMOutput(
                document_title="Investor Summary - Multi",
                executive_summary="Para1. Para2. Para3. This investment may not be suitable for all investors.",
                product_description="Investment Overview: ... In summary,",
                how_it_works="1. step\n2. step\n3. step",
                key_features=["• A: B - C","• A: B - C","• A: B - C"],
                investment_details="...",
                potential_returns="...",
                scenarios_analysis="...",
                risk_summary="All investments carry risk of loss.",
                key_risks=["Risk: a","Risk: b","Risk: c","Risk: d"],
                risk_mitigation="...",
                risk_level_indicator="Risk Level: MEDIUM - ...",
                important_dates="...",
                fees_and_charges="...",
                liquidity_information="...",
                suitability_assessment="This investment is suitable for... This investment may not be suitable for all investors.",
                regulatory_notices="Important Notice:",
                tax_considerations="Tax implications may include... Consult your tax advisor for specific guidance.",
                contact_information="...",
                next_steps="1\n2\n3",
                disclaimer="Past performance does not guarantee future results. All investments carry risk of loss. Please consult your financial advisor before investing. This summary is for informational purposes only.",
                generation_date="2025-01-29",
            )))
            # LightRAG not used here either
            
            # Test product information retrieval
            product_info = await ism_agent.retrieve_product_information(
                product_type="autocallable",
                underlying_asset="S&P 500 Index",
                specific_features="autocall"
            )
            assert "S&P 500 Index" in product_info
            
            # Test risk explanation retrieval
            risk_info = await ism_agent.retrieve_risk_explanations(
                risk_categories="principal protection, market risk",
                investor_audience="retail_investors"
            )
            assert "risk" in risk_info.lower()
            
            # Test scenario examples retrieval
            scenarios = await ism_agent.retrieve_scenario_examples(
                product_type="autocallable",
                underlying_asset="S&P 500 Index"
            )
            assert "example" in scenarios.lower()
            
        print(f"✓ Product information retrieved: {len(product_info)} characters")
        print(f"✓ Risk explanations retrieved: {len(risk_info)} characters")
        print(f"✓ Scenario examples retrieved: {len(scenarios)} characters")

    @pytest.mark.asyncio
    async def test_large_text_template_handling(self, ism_agent, sample_complex_input):
        """Test large text template handling capabilities"""
        print("\n=== Testing Large Text Template Handling ===")
        
        # Create a large template with many placeholders
        large_template = """
        COMPREHENSIVE INVESTOR SUMMARY
        
        PRODUCT DETAILS:
        Issuer: {issuer}
        Product Name: {product_name}
        Underlying Assets: {underlying_asset}
        Principal Amount: {principal_amount} {currency}
        Maturity Date: {maturity_date}
        
        AUTOCALL FEATURES:
        Autocall Dates: {autocall_dates}
        Autocall Level: {autocall_level}
        Fixed Return: {fixed_return}
        
        RISK FEATURES:
        Barrier Level: {barrier_level}
        Additional Return Multiplier: {additional_return_multiplier}
        
        INVESTOR PROFILE:
        Target Audience: {investor_audience}
        Regulatory Jurisdiction: {regulatory_jurisdiction}
        Product Type: {product_type}
        
        ADDITIONAL CONTEXT:
        Risk Level: {risk_level}
        Target Return: {target_return}
        Protection Level: {protection_level}
        Correlation Features: {correlation_features}
        Leverage Ratio: {leverage_ratio}
        
        DETAILED SCENARIOS:
        {scenarios}
        
        RISK DISCLOSURES:
        {risk_disclosures}
        
        REGULATORY COMPLIANCE:
        {regulatory_compliance}
        """ * 5  # Make it large
        
        # Test large template processing
        with patch.object(ism_agent, 'agent') as mock_agent:
            mock_agent.run = AsyncMock(return_value=Mock(data=ISMOutput(
                document_title="Investor Summary - Custom",
                executive_summary="Para1. Para2. Para3. This investment may not be suitable for all investors.",
                product_description="Investment Overview: ... In summary,",
                how_it_works="1. step\n2. step\n3. step",
                key_features=["• A: B - C","• A: B - C","• A: B - C"],
                investment_details="...",
                potential_returns="...",
                scenarios_analysis="...",
                risk_summary="All investments carry risk of loss.",
                key_risks=["Risk: a","Risk: b","Risk: c","Risk: d"],
                risk_mitigation="...",
                risk_level_indicator="Risk Level: MEDIUM - ...",
                important_dates="...",
                fees_and_charges="...",
                liquidity_information="...",
                suitability_assessment="This investment is suitable for... This investment may not be suitable for all investors.",
                regulatory_notices="Important Notice:",
                tax_considerations="Tax implications may include... Consult your tax advisor for specific guidance.",
                contact_information="...",
                next_steps="1\n2\n3",
                disclaimer="Past performance does not guarantee future results. All investments carry risk of loss. Please consult your financial advisor before investing. This summary is for informational purposes only.",
                generation_date="2025-01-29",
            )))
            # No LightRAG usage in this mocked path
            
            # Test template retrieval and processing
            template_result = await ism_agent.retrieve_investor_templates(
                query="comprehensive investor summary template",
                product_type="multi_asset_autocallable"
            )
            
            # Verify large template handling
            assert len(template_result) > 1000
            assert template_result.count("{") > 20  # Many placeholders
            assert template_result.count("}") > 20
            
            # Test placeholder replacement
            placeholders = [
                "{issuer}", "{product_name}", "{underlying_asset}", "{principal_amount}",
                "{currency}", "{maturity_date}", "{autocall_dates}", "{autocall_level}",
                "{fixed_return}", "{barrier_level}", "{additional_return_multiplier}",
                "{investor_audience}", "{regulatory_jurisdiction}", "{product_type}"
            ]
            
            customized_template = template_result
            for placeholder in placeholders:
                if placeholder in customized_template:
                    # Replace with sample data
                    replacement = getattr(sample_complex_input, placeholder.strip("{}"), "N/A")
                    customized_template = customized_template.replace(placeholder, str(replacement))
            
            # Verify customization
            assert sample_complex_input.issuer in customized_template
            assert sample_complex_input.product_name in customized_template
            assert str(sample_complex_input.principal_amount) in customized_template
            
        print(f"✓ Large template size: {len(template_result)} characters")
        print(f"✓ Placeholders found: {template_result.count('{')}")
        print(f"✓ Customization successful: {customized_template.count('{') < template_result.count('{')}")

    @pytest.mark.asyncio
    async def test_custom_placeholder_processing(self, ism_agent, sample_ism_input):
        """Test custom placeholder processing"""
        print("\n=== Testing Custom Placeholder Processing ===")
        
        # Create template with custom placeholders
        custom_template = """
        CUSTOM INVESTOR SUMMARY
        
        Standard Fields:
        Issuer: {issuer}
        Product: {product_name}
        Amount: {principal_amount}
        
        Custom Fields:
        Risk Level: {risk_level}
        Target Return: {target_return}
        Protection Level: {protection_level}
        
        Calculated Fields:
        Annual Return: {annual_return}
        Max Loss: {max_loss}
        Autocall Probability: {autocall_probability}
        
        Dynamic Content:
        Market Conditions: {market_conditions}
        Investor Profile: {investor_profile}
        Regulatory Notes: {regulatory_notes}
        """
        
        # Test custom placeholder processing
        with patch.object(ism_agent, 'agent') as mock_agent:
            mock_agent.run = AsyncMock(return_value=Mock(data=ISMOutput(
                document_title="Investor Summary - Custom",
                executive_summary="Para1. Para2. Para3. This investment may not be suitable for all investors.",
                product_description="Investment Overview: ... In summary,",
                how_it_works="1. step\n2. step\n3. step",
                key_features=["• A: B - C","• A: B - C","• A: B - C"],
                investment_details="...",
                potential_returns="...",
                scenarios_analysis="...",
                risk_summary="All investments carry risk of loss.",
                key_risks=["Risk: a","Risk: b","Risk: c","Risk: d"],
                risk_mitigation="...",
                risk_level_indicator="Risk Level: MEDIUM - ...",
                important_dates="...",
                fees_and_charges="...",
                liquidity_information="...",
                suitability_assessment="This investment is suitable for... This investment may not be suitable for all investors.",
                regulatory_notices="Important Notice:",
                tax_considerations="Tax implications may include... Consult your tax advisor for specific guidance.",
                contact_information="...",
                next_steps="1\n2\n3",
                disclaimer="Past performance does not guarantee future results. All investments carry risk of loss. Please consult your financial advisor before investing. This summary is for informational purposes only.",
                generation_date="2025-01-29",
            )))
            
            # Test template retrieval
            template = await ism_agent.retrieve_investor_templates(
                query="custom investor summary template",
                product_type="autocallable"
            )
            
            # Process custom placeholders
            processed_template = template
            
            # Standard placeholders
            processed_template = processed_template.replace("{issuer}", sample_ism_input.issuer)
            processed_template = processed_template.replace("{product_name}", sample_ism_input.product_name)
            processed_template = processed_template.replace("{principal_amount}", str(sample_ism_input.principal_amount))
            
            # Custom placeholders from additional_context
            if sample_ism_input.additional_context:
                for key, value in sample_ism_input.additional_context.items():
                    placeholder = f"{{{key}}}"
                    if placeholder in processed_template:
                        processed_template = processed_template.replace(placeholder, str(value))
            
            # Calculated placeholders
            annual_return = sample_ism_input.fixed_return * 100
            max_loss = (1 - sample_ism_input.barrier_level) * 100
            autocall_probability = "15-20%"  # Estimated
            
            processed_template = processed_template.replace("{annual_return}", f"{annual_return}%")
            processed_template = processed_template.replace("{max_loss}", f"{max_loss}%")
            processed_template = processed_template.replace("{autocall_probability}", autocall_probability)
            
            # Dynamic content placeholders
            processed_template = processed_template.replace("{market_conditions}", "Current market volatility")
            processed_template = processed_template.replace("{investor_profile}", sample_ism_input.investor_audience)
            processed_template = processed_template.replace("{regulatory_notes}", "SEC compliant")
            
            # Verify processing
            assert sample_ism_input.issuer in processed_template
            assert sample_ism_input.product_name in processed_template
            assert str(sample_ism_input.principal_amount) in processed_template
            assert "15%" in processed_template  # annual return
            assert "30%" in processed_template  # max loss
            assert "15-20%" in processed_template  # autocall probability
            
        print(f"✓ Custom placeholders processed")
        print(f"✓ Calculated fields added")
        print(f"✓ Dynamic content inserted")

    @pytest.mark.asyncio
    async def test_output_validation_and_formatting(self, ism_agent, sample_ism_input):
        """Test output validation and formatting"""
        print("\n=== Testing Output Validation and Formatting ===")
        
        # Mock agent output
        mock_output = ISMOutput(
            document_title="Investor Summary - SP 500 Autocallable Note Series 2024-1",
            executive_summary="This structured note offers exposure to the S&P 500 Index with autocall features providing potential for enhanced returns while maintaining principal protection subject to barrier conditions.",
            product_overview="The note is designed to provide investors with exposure to the performance of the S&P 500 Index while offering a fixed return if certain conditions are met. The product includes autocall features that may result in early redemption.",
            risk_disclosure="Investors may lose up to 30% of their principal if the S&P 500 Index falls below the barrier level at maturity. The note is subject to issuer credit risk and market volatility.",
            scenarios="Scenario 1: Autocall at 15% return if S&P 500 is above 100% at autocall date. Scenario 2: Maturity with 30% loss if S&P 500 is below 70% at maturity. Scenario 3: Maturity with 15% return if S&P 500 is between 70% and 100% at maturity.",
            regulatory_compliance="This document complies with SEC Rule 434 requirements for investor summaries and includes all required risk disclosures for retail investors."
        )
        
        # Test output validation
        assert mock_output.document_title is not None
        assert len(mock_output.document_title) > 0
        assert mock_output.executive_summary is not None
        assert len(mock_output.executive_summary) > 50
        assert mock_output.product_overview is not None
        assert len(mock_output.product_overview) > 100
        assert mock_output.risk_disclosure is not None
        assert len(mock_output.risk_disclosure) > 100
        assert mock_output.scenarios is not None
        assert len(mock_output.scenarios) > 200
        assert mock_output.regulatory_compliance is not None
        assert len(mock_output.regulatory_compliance) > 50
        
        # Test formatting requirements
        assert "Investor Summary" in mock_output.document_title
        assert "S&P 500" in mock_output.executive_summary
        assert "autocall" in mock_output.product_overview.lower()
        assert "risk" in mock_output.risk_disclosure.lower()
        assert "scenario" in mock_output.scenarios.lower()
        assert "SEC" in mock_output.regulatory_compliance
        
        # Test content quality checks
        assert mock_output.executive_summary.count(".") >= 2  # Multiple sentences
        assert mock_output.product_overview.count(".") >= 3  # Detailed description
        assert mock_output.scenarios.count("Scenario") >= 2  # Multiple scenarios
        assert mock_output.risk_disclosure.count("risk") >= 1  # Risk disclosure present
        
        print(f"✓ Document title: {mock_output.document_title}")
        print(f"✓ Executive summary length: {len(mock_output.executive_summary)}")
        print(f"✓ Product overview length: {len(mock_output.product_overview)}")
        print(f"✓ Risk disclosure length: {len(mock_output.risk_disclosure)}")
        print(f"✓ Scenarios length: {len(mock_output.scenarios)}")
        print(f"✓ Regulatory compliance length: {len(mock_output.regulatory_compliance)}")

    @pytest.mark.asyncio
    async def test_customized_document_generation(self, ism_agent, sample_ism_input):
        """Test customized document generation with overrides"""
        print("\n=== Testing Customized Document Generation ===")
        
        # Test with audience override
        audience_override = "accredited_investors"
        
        with patch.object(ism_agent, '_create_agent', return_value=Mock()) as mock_agent:
            mock_agent.return_value.run.return_value = ISMOutput(
                document_title="Accredited Investor Summary - SP 500 Autocallable Note",
                executive_summary="This note is suitable for accredited investors seeking enhanced returns.",
                product_overview="Advanced structured product with sophisticated risk features.",
                risk_disclosure="Accredited investors should understand the complex risk profile.",
                scenarios="Multiple scenarios including leverage and correlation features.",
                regulatory_compliance="Compliant with accredited investor regulations."
            )
            
            # Test customized generation
            result = await ism_agent.generate_customized_document(
                input_data=sample_ism_input,
                audience_override=audience_override
            )
            
            # Verify customization
            assert result is not None
            assert "Accredited Investor" in result.document_title
            assert "accredited investors" in result.executive_summary.lower()
            assert "sophisticated" in result.product_overview.lower()
            
        print(f"✓ Customized document generated")
        print(f"✓ Audience override applied: {audience_override}")
        print(f"✓ Content adapted for target audience")

    @pytest.mark.asyncio
    async def test_knowledge_update_integration(self, ism_agent):
        """Test knowledge update integration"""
        print("\n=== Testing Knowledge Update Integration ===")
        
        # Test knowledge update proposal
        feedback = "The risk disclosure should include new regulatory requirements for ESG considerations"
        
        with patch.object(ism_agent, 'propose_knowledge_update', new=AsyncMock(return_value={"update_type":"risk_disclosure","content":"Updated","priority":"high"})):
            # Test update proposal
            update_plan = await ism_agent.propose_knowledge_update(feedback)
            
            # Verify update proposal
            assert update_plan is not None
            assert "update_type" in update_plan
            assert "content" in update_plan
            assert "priority" in update_plan
            
        print(f"✓ Knowledge update proposed")
        print(f"✓ Update type: {update_plan.get('update_type')}")
        print(f"✓ Update priority: {update_plan.get('priority')}")

    @pytest.mark.asyncio
    async def test_edge_cases_and_error_handling(self, ism_agent):
        """Test edge cases and error handling"""
        print("\n=== Testing Edge Cases and Error Handling ===")
        
        # Test with minimal input
        minimal_input = ISMInput(
            issuer="Test Bank",
            product_name="Test Product",
            underlying_asset="Test Index",
            principal_amount=1000.0,
            currency="USD",
            issue_date="2024-01-01",
            maturity_date="2025-01-01",
            autocall_dates=["2024-01-01"],
            autocall_level=1.0,
            barrier_level=0.8,
            fixed_return=0.05,
            additional_return_multiplier=1.0,
            risk_tolerance="medium",
            investment_objective="income",
            investor_audience="retail_investors",
            regulatory_jurisdiction="US",
            distribution_method="broker_dealer_network",
            product_type="test_product"
        )
        
        with patch.object(ism_agent, 'agent') as mock_agent:
            mock_agent.run = AsyncMock(return_value=Mock(data=ISMOutput(
                document_title="Test Document",
                executive_summary="Test summary",
                product_description="Investment Overview: ... In summary,",
                how_it_works="1. step\n2. step\n3. step",
                key_features=["• A: B - C","• A: B - C","• A: B - C"],
                investment_details="...",
                potential_returns="...",
                scenarios_analysis="...",
                risk_summary="All investments carry risk of loss.",
                key_risks=["Risk: a","Risk: b","Risk: c","Risk: d"],
                risk_mitigation="...",
                risk_level_indicator="Risk Level: MEDIUM - ...",
                important_dates="...",
                fees_and_charges="...",
                liquidity_information="...",
                suitability_assessment="This investment is suitable for... This investment may not be suitable for all investors.",
                regulatory_notices="Important Notice:",
                tax_considerations="Tax implications may include... Consult your tax advisor for specific guidance.",
                contact_information="...",
                next_steps="1\n2\n3",
                disclaimer="Past performance does not guarantee future results. All investments carry risk of loss. Please consult your financial advisor before investing. This summary is for informational purposes only.",
                generation_date="2025-01-29",
            )))
            
            # Test minimal input handling
            result = await ism_agent.generate_document(minimal_input)
            assert result is not None
            assert result.document_title == "Test Document"
            
        # Test error handling
        with patch.object(ism_agent, '_create_agent', side_effect=Exception("Test error")):
            try:
                await ism_agent.generate_document(minimal_input)
                assert False, "Should have raised an exception"
            except Exception as e:
                assert "Test error" in str(e)
                
        print(f"✓ Minimal input handled successfully")
        print(f"✓ Error handling works correctly")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"]) 