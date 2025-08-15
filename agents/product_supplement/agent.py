"""
PDS (Prospectus Supplement) Agent implementation using Pydantic AI framework.
"""

from typing import Optional
from datetime import datetime
from pydantic_ai import Agent, RunContext
from lightrag import LightRAG, QueryParam

from core.base_agent import BaseFinancialAgent
from core.knowledge_updater import KnowledgeUpdater
from .models import PDSInput, PDSOutput, PDSAgentDeps
from .instructions import PDSInstructions
from .config import PDSConfig


class PDSAgent(BaseFinancialAgent[PDSInput, PDSOutput, PDSAgentDeps]):
    """
    PDS (Prospectus Supplement) Agent specialized in generating prospectus supplement 
    documents for specific structured notes using Pydantic AI framework.
    """
    
    def __init__(
        self, 
        knowledge_base_path: str = "knowledge_bases/pds_kb/",
        model_name: str = "openai:gpt-4o-mini",
        config: Optional[PDSConfig] = None
    ):
        """
        Initialize the PDS agent.
        
        Args:
            knowledge_base_path: Path to PDS knowledge base
            model_name: LLM model to use for generation
            config: PDS-specific configuration
        """
        self.pds_config = config or PDSConfig.get_default_config()
        self.instructions = PDSInstructions()
        
        super().__init__(
            agent_type="pds",
            knowledge_base_path=knowledge_base_path,
            model_name=model_name,
            agent_config=self.pds_config.model_dump()
        )
    
    def _create_agent(self) -> Agent[PDSAgentDeps, PDSOutput]:
        """Create and configure the Pydantic AI agent for PDS"""
        agent = Agent(
            model=self.model_name,
            deps_type=PDSAgentDeps,
            output_type=PDSOutput,
            instructions=self.get_system_instructions()
        )
        return agent
    
    def _register_agent_tools(self):
        """Register PDS-specific tools for document generation"""
        
        @self.agent.tool
        async def retrieve_base_prospectus(
            ctx: RunContext[PDSAgentDeps], 
            reference: str,
            section_keywords: str = "summary"
        ) -> str:
            """
            Retrieve relevant sections from the base shelf prospectus referenced by this supplement.
            
            Args:
                ctx: Run context with dependencies
                reference: Base prospectus reference/title/id
                section_keywords: Keywords to target specific sections
            Returns:
                Extracted base prospectus content
            """
            try:
                query = f"base prospectus {reference} {section_keywords} key sections"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=8))
                return f"**Base Prospectus Content:**\n{result}"
            except Exception as e:
                return f"Error retrieving base prospectus: {str(e)}"

        @self.agent.tool
        async def retrieve_note_specific_terms(
            ctx: RunContext[PDSAgentDeps], 
            product_type: str,
            underlying_asset: str,
            focus: str = "calculation methodology"
        ) -> str:
            """
            Retrieve note-specific terms, structures, and examples from the PDS knowledge base.
            """
            try:
                query = f"{product_type} prospectus supplement {underlying_asset} {focus} terms examples"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=10))
                return f"**Note-Specific Terms:**\n{result}"
            except Exception as e:
                return f"Error retrieving note-specific terms: {str(e)}"

        @self.agent.tool
        async def retrieve_regulatory_requirements(
            ctx: RunContext[PDSAgentDeps], 
            jurisdiction: str,
            document_type: str = "prospectus_supplement"
        ) -> str:
            """
            Retrieve regulatory requirements and mandatory disclosures for the jurisdiction.
            """
            try:
                query = f"regulatory disclosure {jurisdiction} {document_type} requirements mandatory language"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Regulatory Requirements:**\n{result}"
            except Exception as e:
                return f"Error retrieving regulatory requirements: {str(e)}"

        @self.agent.tool
        async def retrieve_risk_factors(
            ctx: RunContext[PDSAgentDeps], 
            product_type: str,
            underlying_asset: str
        ) -> str:
            """
            Retrieve risk factors specific to this prospectus supplement.
            """
            try:
                query = f"risk factors {product_type} supplement {underlying_asset} examples language"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=8))
                return f"**Risk Factors:**\n{result}"
            except Exception as e:
                return f"Error retrieving risk factors: {str(e)}"

        @self.agent.tool
        async def retrieve_supplement_purpose_templates(
            ctx: RunContext[PDSAgentDeps],
            jurisdiction: str = "Canada"
        ) -> str:
            """
            Retrieve concise purpose/relationship-to-base-prospectus templates for supplements.
            """
            try:
                query = f"{jurisdiction} prospectus supplement purpose language relationship to base prospectus template"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Supplement Purpose Templates:**\n{result}"
            except Exception as e:
                return f"Error retrieving supplement purpose templates: {str(e)}"

        @self.agent.tool
        async def retrieve_calculation_agent_determinations(
            ctx: RunContext[PDSAgentDeps],
            product_type: str,
            focus: str = "calculation agent determinations"
        ) -> str:
            """
            Retrieve standard language around calculation agent determinations/adjustments.
            """
            try:
                query = f"{product_type} {focus} prospectus supplement language adjustments methodology"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Calculation Agent Determinations:**\n{result}"
            except Exception as e:
                return f"Error retrieving calculation agent determinations: {str(e)}"

        @self.agent.tool
        async def retrieve_risk_introductions(
            ctx: RunContext[PDSAgentDeps],
            product_type: str,
            jurisdiction: str = "Canada"
        ) -> str:
            """
            Retrieve succinct risk introduction paragraphs appropriate for supplements.
            """
            try:
                query = f"{jurisdiction} {product_type} prospectus supplement risk introduction paragraph examples"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=5))
                return f"**Risk Introductions:**\n{result}"
            except Exception as e:
                return f"Error retrieving risk introductions: {str(e)}"
    
    def get_system_instructions(self) -> str:
        """Get PDS-specific system instructions"""
        return self.instructions.get_base_instructions()
    
    async def _create_dependencies(self, lightrag: LightRAG, input_data: PDSInput) -> PDSAgentDeps:
        """Create PDS-specific dependencies"""
        return PDSAgentDeps(
            lightrag=lightrag,
            agent_type=self.agent_type,
            input_data=input_data,
            config=self.pds_config.model_dump()
        )
    
    def _format_user_prompt(self, input_data: PDSInput) -> str:
        """Format the user prompt for PDS document generation"""
        term_years = (input_data.maturity_date - input_data.issue_date).days / 365.25
        return f"""
        Generate a comprehensive Prospectus Supplement for the following note issuance.

        ## Base Prospectus Reference
        - Reference: {input_data.base_prospectus_reference}
        - Date: {input_data.base_prospectus_date.strftime('%B %d, %Y')}

        ## Note Overview
        - Series: {input_data.note_series}
        - Description: {input_data.note_description}
        - Underlying Asset: {input_data.underlying_asset}
        - Product Type: {input_data.product_type}
        - Currency: {input_data.currency}
        - Principal Amount: {input_data.principal_amount:,.2f} {input_data.currency}
        - Issue Price: {input_data.issue_price:.2f}% of principal
        - Issue Date: {input_data.issue_date.strftime('%B %d, %Y')}
        - Maturity Date: {input_data.maturity_date.strftime('%B %d, %Y')}
        - Term: {term_years:.1f} years

        ## Structure & Calculations
        - Barrier Level: {input_data.barrier_level if input_data.barrier_level is not None else 'N/A'}
        - Coupon Structure: {input_data.coupon_structure or 'N/A'}
        - Calculation Methodology: {input_data.calculation_methodology}
        - Underlying Performance Measure: {input_data.underlying_performance or 'As described'}

        ## Additional Terms
        - {input_data.additional_terms or {}}

        ## REQUIRED TOOL USAGE
        1. retrieve_base_prospectus(reference, section_keywords="summary risk factors offering particulars")
        2. retrieve_note_specific_terms(product_type, underlying_asset, focus="calculation methodology and payment schedule")
        3. retrieve_regulatory_requirements(jurisdiction="Canada", document_type="prospectus_supplement")
        4. retrieve_risk_factors(product_type, underlying_asset)

        ## OUTPUT REQUIREMENTS
        Return a complete PDSOutput that includes: document_title, supplement_cover, base_prospectus_reference,
        supplement_purpose, specific_terms, underlying_description, calculation_methodology, payment_schedule,
        additional_risks, pricing_details, market_information, tax_implications, additional_sections, document_version,
        and generation_date. Ensure legal precision and clear cross-references to the base prospectus.

        Generation Date: {datetime.now().strftime('%Y-%m-%d')}
        """

    async def propose_knowledge_update(self, feedback: str) -> str:
        """
        Propose an update to the PDS knowledge base.
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
        Apply an update to the PDS knowledge base.
        """
        from core.rag_manager import rag_manager
        updater = KnowledgeUpdater(rag_manager)
        await updater.apply_update(update_plan)