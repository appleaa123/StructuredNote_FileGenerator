"""
PRS (Pricing Supplement) Agent implementation using Pydantic AI framework.
"""

from typing import Optional
from datetime import datetime
from pydantic_ai import Agent, RunContext
from lightrag import LightRAG, QueryParam

from core.base_agent import BaseFinancialAgent
from core.knowledge_updater import KnowledgeUpdater
from .models import PRSInput, PRSOutput, PRSAgentDeps
from .instructions import PRSInstructions
from .config import PRSConfig


class PRSAgent(BaseFinancialAgent[PRSInput, PRSOutput, PRSAgentDeps]):
    """
    PRS (Pricing Supplement) Agent specialized in generating pricing supplement 
    documents with final pricing and terms using Pydantic AI framework.
    """
    
    def __init__(
        self, 
        knowledge_base_path: str = "knowledge_bases/prs_kb/",
        model_name: str = "openai:gpt-4o-mini",
        config: Optional[PRSConfig] = None
    ):
        """
        Initialize the PRS agent.
        
        Args:
            knowledge_base_path: Path to PRS knowledge base
            model_name: LLM model to use for generation
            config: PRS-specific configuration
        """
        self.prs_config = config or PRSConfig.get_default_config()
        self.instructions = PRSInstructions()
        
        super().__init__(
            agent_type="prs",
            knowledge_base_path=knowledge_base_path,
            model_name=model_name,
            agent_config=self.prs_config.model_dump()
        )
    
    def _create_agent(self) -> Agent[PRSAgentDeps, PRSOutput]:
        """Create and configure the Pydantic AI agent for PRS"""
        agent = Agent(
            model=self.model_name,
            deps_type=PRSAgentDeps,
            output_type=PRSOutput,
            instructions=self.get_system_instructions()
        )
        return agent
    
    def _register_agent_tools(self):
        """Register PRS-specific tools for document generation"""
        
        @self.agent.tool
        async def retrieve_base_prospectus(
            ctx: RunContext[PRSAgentDeps], 
            reference: str,
            section_keywords: str = "summary risk factors pricing"
        ) -> str:
            """
            Retrieve relevant sections from the base shelf prospectus referenced by this pricing supplement.
            """
            try:
                query = f"base prospectus {reference} {section_keywords} key sections"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=8))
                return f"**Base Prospectus Content:**\n{result}"
            except Exception as e:
                return f"Error retrieving base prospectus: {str(e)}"

        @self.agent.tool
        async def retrieve_pricing_methodology(
            ctx: RunContext[PRSAgentDeps], 
            product_type: str,
            underlying_asset: str
        ) -> str:
            """
            Retrieve pricing methodology examples and language.
            """
            try:
                query = f"{product_type} pricing methodology {underlying_asset} examples disclosure"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=10))
                return f"**Pricing Methodology:**\n{result}"
            except Exception as e:
                return f"Error retrieving pricing methodology: {str(e)}"

        @self.agent.tool
        async def retrieve_market_data(
            ctx: RunContext[PRSAgentDeps], 
            underlying_asset: str,
            pricing_date: str
        ) -> str:
            """
            Retrieve market data context used at pricing time.
            """
            try:
                query = f"{underlying_asset} market data around {pricing_date} pricing context"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Market Data at Pricing:**\n{result}"
            except Exception as e:
                return f"Error retrieving market data: {str(e)}"

        @self.agent.tool
        async def retrieve_regulatory_pricing_disclosures(
            ctx: RunContext[PRSAgentDeps], 
            jurisdiction: str = "Canada"
        ) -> str:
            """
            Retrieve regulatory notices and mandatory pricing disclosures.
            """
            try:
                query = f"regulatory pricing disclosures {jurisdiction} pricing supplement mandatory language"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=5))
                return f"**Regulatory Pricing Disclosures:**\n{result}"
            except Exception as e:
                return f"Error retrieving regulatory disclosures: {str(e)}"

        @self.agent.tool
        async def retrieve_final_terms_templates(
            ctx: RunContext[PRSAgentDeps],
            product_type: str,
            audience: str = "institutional"
        ) -> str:
            """
            Retrieve templates/snippets for final terms section and tabular presentation.
            """
            try:
                query = f"{product_type} pricing supplement final terms table template {audience}"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=8))
                return f"**Final Terms Templates:**\n{result}"
            except Exception as e:
                return f"Error retrieving final terms templates: {str(e)}"

        @self.agent.tool
        async def retrieve_estimated_value_language(
            ctx: RunContext[PRSAgentDeps],
            jurisdiction: str = "Canada"
        ) -> str:
            """
            Retrieve standard language for estimated value disclosures at issuance.
            """
            try:
                query = f"{jurisdiction} pricing supplement estimated value disclosure standard language"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Estimated Value Language:**\n{result}"
            except Exception as e:
                return f"Error retrieving estimated value language: {str(e)}"

        @self.agent.tool
        async def retrieve_distribution_and_fees_templates(
            ctx: RunContext[PRSAgentDeps],
            jurisdiction: str = "Canada"
        ) -> str:
            """
            Retrieve templates for distribution, selling restrictions, denominations, and fees breakdowns.
            """
            try:
                query = f"{jurisdiction} pricing supplement distribution selling restrictions denominations fees templates"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Distribution & Fees Templates:**\n{result}"
            except Exception as e:
                return f"Error retrieving distribution and fees templates: {str(e)}"
    
    def get_system_instructions(self) -> str:
        """Get PRS-specific system instructions"""
        return self.instructions.get_base_instructions()
    
    async def _create_dependencies(self, lightrag: LightRAG, input_data: PRSInput) -> PRSAgentDeps:
        """Create PRS-specific dependencies"""
        return PRSAgentDeps(
            lightrag=lightrag,
            agent_type=self.agent_type,
            input_data=input_data,
            config=self.prs_config.model_dump()
        )
    
    def _format_user_prompt(self, input_data: PRSInput) -> str:
        """Format the user prompt for PRS document generation"""
        return f"""
        Generate a comprehensive Pricing Supplement for the following issuance. This document must
        present final terms, pricing methodology, market data at pricing, settlement instructions,
        and regulatory notices, and must cross-reference the Base Prospectus.

        ## Reference Documents
        - Base Prospectus: {input_data.base_prospectus_reference}
        - Supplement Reference: {input_data.supplement_reference or 'Not applicable'}

        ## Final Pricing Information
        - Final Issue Price: {input_data.final_issue_price:.2f}% of principal
        - Final Principal Amount: {input_data.final_principal_amount:,.2f} {input_data.currency}
        - Currency: {input_data.currency}

        ## Final Dates
        - Pricing Date: {input_data.pricing_date.strftime('%B %d, %Y')}
        - Issue Date: {input_data.issue_date.strftime('%B %d, %Y')}
        - Maturity Date: {input_data.maturity_date.strftime('%B %d, %Y')}
        - Settlement Date: {input_data.settlement_date.strftime('%B %d, %Y')}

        ## Final Terms
        - Final Coupon Rate: {input_data.final_coupon_rate if input_data.final_coupon_rate is not None else 'N/A'}
        - Final Barrier Level: {input_data.final_barrier_level if input_data.final_barrier_level is not None else 'N/A'}
        - Underlying Initial Level: {input_data.underlying_initial_level if input_data.underlying_initial_level is not None else 'TBD'}

        ## Market Data at Pricing
        - Underlying Price at Pricing: {input_data.underlying_price_at_pricing if input_data.underlying_price_at_pricing is not None else 'TBD'}
        - Market Conditions: {input_data.market_conditions or 'Standard conditions'}
        - Implied Volatility: {input_data.volatility_at_pricing if input_data.volatility_at_pricing is not None else 'TBD'}

        ## Distribution & Fees
        - Distribution Method: {input_data.distribution_method}
        - Minimum Denomination: {input_data.minimum_denomination:,.2f}
        - Agent Discount: {input_data.agent_discount if input_data.agent_discount is not None else 'N/A'}
        - Estimated Value: {input_data.estimated_value if input_data.estimated_value is not None else 'TBD'}

        ## REQUIRED TOOL USAGE
        1. retrieve_base_prospectus(reference, section_keywords="summary risk factors pricing")
        2. retrieve_pricing_methodology(product_type="{input_data.distribution_method}", underlying_asset="{input_data.currency}")  # NOTE: If product_type is needed, pass correct type instead of distribution
        3. retrieve_market_data(underlying_asset="{input_data.distribution_method}", pricing_date="{input_data.pricing_date.strftime('%Y-%m-%d')}")  # NOTE: Replace placeholders with real underlying asset symbol/name
        4. retrieve_regulatory_pricing_disclosures(jurisdiction="Canada")

        ## OUTPUT REQUIREMENTS
        Return a complete PRSOutput including: document_title, pricing_summary, document_references,
        final_terms_summary, final_terms_table, pricing_methodology, estimated_value_explanation,
        settlement_instructions, delivery_procedures, distribution_information, market_data_at_pricing,
        fees_and_expenses, regulatory_notices, contact_information, additional_sections, document_version,
        pricing_timestamp, and generation_date. Use formal, precise disclosure language.

        Generation Date: {datetime.now().strftime('%Y-%m-%d')}
        """

    async def propose_knowledge_update(self, feedback: str) -> str:
        """
        Propose an update to the PRS knowledge base.
        """
        from core.rag_manager import rag_manager
        updater = KnowledgeUpdater(rag_manager)
        parsed_request = updater.parse_update_request({
            "action": "insert",
            "domain": self.agent_type,
            "content": feedback,
        })
        return updater.create_update_plan(parsed_request)

    async def apply_knowledge_update(self, update_plan: dict):
        """
        Apply an update to the PRS knowledge base.
        """
        from core.rag_manager import rag_manager
        updater = KnowledgeUpdater(rag_manager)
        await updater.apply_update(update_plan)