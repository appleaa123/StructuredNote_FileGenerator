"""
ISM (Investor Summary) Agent implementation using Pydantic AI framework.
"""

from typing import Optional
from datetime import datetime
from pydantic_ai import Agent, RunContext
from lightrag import LightRAG, QueryParam

from core.base_agent import BaseFinancialAgent
from core.knowledge_updater import KnowledgeUpdater
from .models import ISMInput, ISMOutput, ISMAgentDeps
from .instructions import ISMInstructions
from .config import ISMConfig

# Import large text templates
try:
    from .large_text_templates import (
        get_template, 
        create_complete_document_from_templates,
        customize_template
    )
    LARGE_TEXT_AVAILABLE = True
except ImportError:
    LARGE_TEXT_AVAILABLE = False
    print("⚠️  Large text templates not available, using standard ISM agent")


class ISMAgent(BaseFinancialAgent[ISMInput, ISMOutput, ISMAgentDeps]):
    """
    ISM (Investor Summary) Agent specialized in generating investor-friendly 
    summary documents for structured notes using Pydantic AI framework.
    
    This agent transforms complex financial products into clear, accessible
    summaries that help investors understand what they're investing in,
    the potential returns, and associated risks.
    
    Key capabilities:
    - Generate comprehensive investor summaries
    - Retrieve product-specific templates and examples
    - Create scenario analyses with concrete examples
    - Explain risks in plain language
    - Ensure regulatory compliance
    - Customize content for different investor audiences
    - Use large text templates for professional formatting
    """
    
    def __init__(
        self, 
        knowledge_base_path: str = "knowledge_bases/ism_kb/",
        model_name: str = "openai:gpt-4o-mini",
        config: Optional[ISMConfig] = None,
        use_large_text_templates: bool = True
    ):
        """
        Initialize the ISM agent.
        
        Args:
            knowledge_base_path: Path to ISM knowledge base
            model_name: LLM model to use for generation
            config: ISM-specific configuration
            use_large_text_templates: Whether to use large text templates (default: True)
        """
        self.ism_config = config or ISMConfig.get_default_config()
        self.instructions = ISMInstructions()
        self.use_large_text_templates = use_large_text_templates and LARGE_TEXT_AVAILABLE
        
        if self.use_large_text_templates:
            print("✅ ISM agent configured to use large text templates")
        else:
            print("⚠️  ISM agent using standard templates")
        
        super().__init__(
            agent_type="ism",
            knowledge_base_path=knowledge_base_path,
            model_name=model_name,
            agent_config=self.ism_config.model_dump()
        )
    
    def _create_agent(self) -> Agent[ISMAgentDeps, ISMOutput]:
        """Create and configure the Pydantic AI agent for ISM"""
        agent = Agent(
            model=self.model_name,
            deps_type=ISMAgentDeps,
            output_type=ISMOutput,
            instructions=self.get_system_instructions()
        )
        
        return agent
    
    def _register_agent_tools(self):
        """Register ISM-specific tools for document generation"""
        
        @self.agent.tool
        async def retrieve_investor_templates(
            ctx: RunContext[ISMAgentDeps], 
            query: str,
            product_type: Optional[str] = None
        ) -> str:
            """
            Retrieve investor summary templates and examples from the knowledge base.
            
            Args:
                ctx: The run context containing dependencies
                query: Search query for relevant templates
                product_type: Specific product type to focus on
                
            Returns:
                Retrieved template content and examples
            """
            try:
                # Enhance query with product type if provided
                if product_type:
                    enhanced_query = f"investor summary template {product_type} {query}"
                else:
                    enhanced_query = f"investor summary template {query}"
                
                result = await ctx.deps.lightrag.aquery(
                    enhanced_query,
                    param=QueryParam(mode="mix", top_k=8)
                )
                
                return f"**Template Information:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving templates: {str(e)}"
        
        @self.agent.tool
        async def retrieve_product_information(
            ctx: RunContext[ISMAgentDeps], 
            product_type: str,
            underlying_asset: str,
            specific_features: Optional[str] = None
        ) -> str:
            """
            Retrieve detailed product information and similar examples.
            
            Args:
                ctx: The run context containing dependencies
                product_type: Type of structured product (e.g., autocallable, barrier)
                underlying_asset: The underlying asset
                specific_features: Specific product features to focus on
                
            Returns:
                Product information and comparable examples
            """
            try:
                # Build comprehensive query
                query_parts = [product_type, "structured note", underlying_asset]
                if specific_features:
                    query_parts.append(specific_features)
                
                query = " ".join(query_parts) + " investor information examples"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=10)
                )
                
                return f"**Product Information:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving product information: {str(e)}"
        
        @self.agent.tool
        async def retrieve_risk_explanations(
            ctx: RunContext[ISMAgentDeps], 
            risk_categories: str,
            investor_audience: str = "retail_investors"
        ) -> str:
            """
            Retrieve risk explanations tailored to the investor audience.
            
            Args:
                ctx: The run context containing dependencies
                risk_categories: Categories of risks to explain
                investor_audience: Target investor audience for language level
                
            Returns:
                Risk explanations in appropriate language
            """
            try:
                query = f"risk explanation {risk_categories} {investor_audience} plain language examples"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=8)
                )
                
                return f"**Risk Information:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving risk explanations: {str(e)}"
        
        @self.agent.tool
        async def retrieve_scenario_examples(
            ctx: RunContext[ISMAgentDeps],
            product_type: str,
            underlying_asset: str,
            market_conditions: Optional[str] = None
        ) -> str:
            """
            Retrieve scenario analysis examples and historical performance data.
            
            Args:
                ctx: The run context containing dependencies
                product_type: Type of structured product
                underlying_asset: The underlying asset
                market_conditions: Specific market conditions to analyze
                
            Returns:
                Scenario examples and historical context
            """
            try:
                query_parts = [product_type, underlying_asset, "scenario analysis", "performance examples"]
                if market_conditions:
                    query_parts.append(market_conditions)
                
                query = " ".join(query_parts)
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=6)
                )
                
                return f"**Scenario Examples:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving scenario examples: {str(e)}"
        
        @self.agent.tool
        async def retrieve_regulatory_content(
            ctx: RunContext[ISMAgentDeps], 
            jurisdiction: str,
            document_type: str = "investor_summary"
        ) -> str:
            """
            Retrieve regulatory requirements and standard disclosures.
            
            Args:
                ctx: The run context containing dependencies
                jurisdiction: Regulatory jurisdiction (US, EU, UK, etc.)
                document_type: Type of document for specific requirements
                
            Returns:
                Regulatory content and required disclosures
            """
            try:
                query = f"regulatory disclosure {jurisdiction} {document_type} requirements mandatory language"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=5)
                )
                
                return f"**Regulatory Requirements:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving regulatory content: {str(e)}"
        
        @self.agent.tool
        async def retrieve_comparable_products(
            ctx: RunContext[ISMAgentDeps],
            product_type: str,
            issuer: Optional[str] = None,
            time_period: str = "recent"
        ) -> str:
            """
            Retrieve information about comparable products for context and benchmarking.
            
            Args:
                ctx: The run context containing dependencies
                product_type: Type of product to compare
                issuer: Specific issuer to focus on (optional)
                time_period: Time period for comparisons
                
            Returns:
                Information about comparable products
            """
            try:
                query_parts = [product_type, "comparable products", time_period]
                if issuer:
                    query_parts.append(issuer)
                
                query = " ".join(query_parts) + " market examples"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=6)
                )
                
                return f"**Comparable Products:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving comparable products: {str(e)}"
    
    def get_system_instructions(self) -> str:
        """Get ISM-specific system instructions"""
        base_instructions = self.instructions.get_base_instructions()
        
        # Add audience-specific instructions if available
        if hasattr(self.ism_config, 'target_audience'):
            audience_instructions = self.instructions.get_audience_specific_instructions(
                self.ism_config.target_audience
            )
            return f"{base_instructions}\n\n{audience_instructions}"
        
        return base_instructions
    
    async def _create_dependencies(self, lightrag: LightRAG, input_data: ISMInput) -> ISMAgentDeps:
        """Create ISM-specific dependencies"""
        return ISMAgentDeps(
            lightrag=lightrag,
            agent_type=self.agent_type,
            input_data=input_data,
            config=self.ism_config.model_dump()
        )
    
    def _format_user_prompt(self, input_data: ISMInput) -> str:
        """Format the user prompt for ISM document generation"""
        
        # Get product-specific instructions
        product_instructions = self.instructions.get_product_type_instructions(input_data.product_type)
        
        # Get audience-specific instructions
        audience_instructions = self.instructions.get_audience_specific_instructions(input_data.target_audience)
        
        # Calculate investment period
        investment_period = (input_data.maturity_date - input_data.issue_date).days / 365.25
        
        # Build comprehensive prompt
        prompt = f"""
        Generate a comprehensive Investor Summary document for the following structured note.
        
        ## Product Details:
        - **Product Name**: {input_data.product_name}
        - **Issuer**: {input_data.issuer}
        - **Product Type**: {input_data.product_type}
        - **Underlying Asset**: {input_data.underlying_asset}
        - **Currency**: {input_data.currency}
        - **Principal Amount**: {input_data.principal_amount:,.2f} {input_data.currency}
        - **Issue Date**: {input_data.issue_date}
        - **Maturity Date**: {input_data.maturity_date}
        - **Investment Period**: {investment_period:.1f} years
        
        ## Product Structure:
        """
        
        # Add product-specific details
        if input_data.coupon_rate:
            prompt += f"- **Coupon Rate**: {input_data.coupon_rate}% per annum\n"
        
        if input_data.barrier_level:
            prompt += f"- **Barrier Level**: {input_data.barrier_level}%\n"
        
        if input_data.autocall_barrier:
            prompt += f"- **Autocall Barrier**: {input_data.autocall_barrier}%\n"
        
        if input_data.protection_level:
            prompt += f"- **Protection Level**: {input_data.protection_level}%\n"
        
        if input_data.memory_feature is not None:
            prompt += f"- **Memory Feature**: {'Yes' if input_data.memory_feature else 'No'}\n"
        
        # Add investor information
        prompt += f"""
        
        ## Investor Profile:
        - **Target Audience**: {input_data.target_audience}
        - **Risk Tolerance**: {input_data.risk_tolerance}
        - **Investment Objective**: {input_data.investment_objective}
        - **Regulatory Jurisdiction**: {input_data.regulatory_jurisdiction}
        - **Distribution Method**: {input_data.distribution_method}
        """
        
        if input_data.minimum_investment:
            prompt += f"- **Minimum Investment**: {input_data.minimum_investment:,.2f} {input_data.currency}\n"
        
        # Add market context if available
        if input_data.market_outlook:
            prompt += f"- **Market Outlook**: {input_data.market_outlook}\n"
        
        if input_data.volatility_level:
            prompt += f"- **Expected Volatility**: {input_data.volatility_level}\n"
        
        # Add additional features if any
        if input_data.additional_features:
            prompt += f"- **Additional Features**: {input_data.additional_features}\n"
        
        # Get section-specific formatting requirements
        section_requirements = self.instructions.get_section_formatting_requirements()
        mandatory_compliance = self.instructions.get_mandatory_compliance_text(input_data.regulatory_jurisdiction)
        
        # Add specific instructions
        prompt += f"""
        
        ## Generation Instructions:
        
        {product_instructions}
        
        {audience_instructions}
        
        ## CRITICAL FORMATTING REQUIREMENTS:
        
        **Document Title Format:**
        {section_requirements['document_title']}
        
        **Executive Summary Structure:**
        {section_requirements['executive_summary']}
        
        **Key Features Format:**
        {section_requirements['key_features']}
        
        **Risk Level Format:**
        {section_requirements['risk_level_indicator']}
        
        **Risk List Format:**
        {section_requirements['key_risks']}
        
        **Return Scenarios Format:**
        {section_requirements['potential_returns']}
        
        **Mandatory Compliance Text (MUST include exactly):**
        """
        
        for key, text in mandatory_compliance.items():
            prompt += f"- {key}: {text}\n"
        
        prompt += f"""
        
        ## Required Tools Usage:
        
        Before generating the document, please use the available tools to:
        
        1. **retrieve_investor_templates**: Get templates for {input_data.product_type} investor summaries
        2. **retrieve_product_information**: Get detailed information about {input_data.product_type} products with {input_data.underlying_asset}
        3. **retrieve_risk_explanations**: Get risk explanations appropriate for {input_data.target_audience}
        4. **retrieve_scenario_examples**: Get scenario analysis examples for this product type
        5. **retrieve_regulatory_content**: Get regulatory requirements for {input_data.regulatory_jurisdiction}
        6. **retrieve_comparable_products**: Get information about similar products for context
        
        ## Output Requirements:
        
        Generate a complete ISMOutput with all required fields populated. The document MUST:
        - Follow ALL formatting requirements specified above EXACTLY
        - Include ALL mandatory compliance text word-for-word
        - Use specific numerical examples with the investment amount ${input_data.principal_amount:,.2f} {input_data.currency}
        - Calculate actual dollar returns for all scenarios
        - Format all dates as "Month DD, YYYY" 
        - Include exactly 3 bullet points for key features
        - Include exactly 4 risks starting with "Risk:"
        - End sections with "In summary," where specified
        
        **VERIFICATION CHECKLIST:**
        Before submitting, verify that:
        ✓ Document title follows exact format
        ✓ Executive summary has exactly 3 paragraphs
        ✓ Key features has exactly 3 bullet points (15-25 words each)
        ✓ Risk level follows "Risk Level: [LEVEL] - [explanation]" format
        ✓ All 4 risks start with "Risk:"
        ✓ All mandatory compliance phrases are included word-for-word
        ✓ Dollar amounts are calculated using ${input_data.principal_amount:,.2f}
        ✓ All dates use "Month DD, YYYY" format
        
        **Generation Date**: {datetime.now().strftime('%Y-%m-%d')}
        """
        
        return prompt
    
    def _prepare_large_text_variables(self, input_data: ISMInput) -> dict:
        """Prepare variables for large text templates from ISM input data"""
        from datetime import datetime
        
        # Calculate term and dates
        term_years = ((input_data.maturity_date - input_data.issue_date).days / 365.25)
        
        # Generate valuation dates (annually for autocall)
        valuation_dates = []
        for i in range(1, min(7, int(term_years) + 1)):
            from datetime import date
            val_date = date(input_data.issue_date.year + i, input_data.issue_date.month, input_data.issue_date.day)
            valuation_dates.append(val_date.strftime("%B %d, %Y"))
        
        # Prepare variables for large text templates
        variables = {
            # Document header
            "Note Title": f"{input_data.product_name} - Series {datetime.now().strftime('%Y')}",
            "Maturity Date": input_data.maturity_date.strftime("%B %d, %Y"),
            "Document Date": datetime.now().strftime("%B %d, %Y"),
            "Pricing Supplement Number": f"PS-{datetime.now().strftime('%Y')}-{hash(input_data.product_name) % 1000:03d}",
            "Pricing Supplement Date": input_data.issue_date.strftime("%B %d, %Y"),
            
            # Underlying asset
            "Underlying Asset Type": "Index" if "index" in input_data.underlying_asset.lower() else "Reference Portfolio and Reference Companies",
            "Underlying Asset Description": f"The {input_data.underlying_asset}, a broad market index representing large-cap U.S. equities with strong historical performance and liquidity characteristics.",
            "Underlying Asset Name": input_data.underlying_asset,
            "levels/prices": "levels" if "index" in input_data.underlying_asset.lower() else "prices",
            "Closing Level/Price Name": f"Closing {'Index Level' if 'index' in input_data.underlying_asset.lower() else 'Portfolio Price'}",
            "Autocall Level/Price Name": f"Autocall {'Level' if 'index' in input_data.underlying_asset.lower() else 'Price'}",
            "Final Level/Price Name": f"Final {'Index Level' if 'index' in input_data.underlying_asset.lower() else 'Portfolio Price'}",
            "Barrier Level/Price Name": f"Barrier {'Level' if 'index' in input_data.underlying_asset.lower() else 'Price'}",
            "Initial Level/Price Name": f"Initial {'Index Level' if 'index' in input_data.underlying_asset.lower() else 'Portfolio Price'}",
            
            # Product terms
            "First Call Date": (input_data.issue_date.replace(year=input_data.issue_date.year + 1)).strftime("%B %d, %Y"),
            "Additional Return Percentage": "5.00%",
            "Return Calculation Metric Name": f"{'Index Return' if 'index' in input_data.underlying_asset.lower() else 'Price Return'}",
            "Contingent Principal Protection Percentage": f"{100 - (input_data.barrier_level or 70):.2f}%",
            "Barrier Percentage": f"{input_data.barrier_level or 70:.2f}%",
            "Final Fixed Return": f"{(input_data.coupon_rate or 8.5) * term_years:.2f}%",
            
            # Autocall schedule
            "Valuation Date 1": valuation_dates[0] if len(valuation_dates) > 0 else "January 29, 2025",
            "Valuation Date 2": valuation_dates[1] if len(valuation_dates) > 1 else "January 29, 2026",
            "Valuation Date 3": valuation_dates[2] if len(valuation_dates) > 2 else "January 29, 2027",
            "Valuation Date 4": valuation_dates[3] if len(valuation_dates) > 3 else "January 29, 2028",
            "Valuation Date 5": valuation_dates[4] if len(valuation_dates) > 4 else "January 29, 2029",
            "Valuation Date 6": valuation_dates[5] if len(valuation_dates) > 5 else "January 29, 2030",
            "Fixed Return 1": f"{(input_data.coupon_rate or 8.5):.2f}%",
            "Fixed Return 2": f"{(input_data.coupon_rate or 8.5) * 2:.2f}%",
            "Fixed Return 3": f"{(input_data.coupon_rate or 8.5) * 3:.2f}%",
            "Fixed Return 4": f"{(input_data.coupon_rate or 8.5) * 4:.2f}%",
            "Fixed Return 5": f"{(input_data.coupon_rate or 8.5) * 5:.2f}%",
            "Fixed Return 6": f"{(input_data.coupon_rate or 8.5) * 6:.2f}%",
            "Autocall Level/Price Description": f"100.00% of the Initial {'Index Level' if 'index' in input_data.underlying_asset.lower() else 'Portfolio Price'}",
            
            # Product details
            "Fundserv Code": f"SSP{datetime.now().strftime('%y')}{hash(input_data.product_name) % 100:02d}",
            "Available Until Date": (input_data.issue_date.replace(day=input_data.issue_date.day - 7)).strftime("%B %d, %Y"),
            "Issue Date": input_data.issue_date.strftime("%B %d, %Y"),
            "Term": f"{term_years:.0f} years",
            "CUSIP Code": f"06418Y{hash(input_data.product_name) % 1000:03d}",
            "Initial Valuation Date": input_data.issue_date.strftime("%B %d, %Y"),
            "Final Valuation Date": input_data.maturity_date.strftime("%B %d, %Y"),
            
            # Fees and parties
            "Fees and Expenses Description": "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 2.50% of the Principal Amount per Note. An independent agent fee of 1.25% of the Principal Amount per Note will be paid to the Independent Agent.",
            "Independent Agent Name": "Scotia Capital Inc.",
            "Asset Manager Name": input_data.issuer,
        }
        
        return variables
    
    async def generate_document_with_large_text_templates(
        self, 
        input_data: ISMInput,
        audience: str = "retail",
        custom_variables: Optional[dict] = None
    ) -> dict:
        """
        Generate document using large text templates.
        
        Args:
            input_data: ISM input data
            audience: Target audience ("retail" or "institutional")
            custom_variables: Additional variables for template substitution
            
        Returns:
            Dictionary with generated document sections using large text templates
        """
        if not self.use_large_text_templates:
            raise ValueError("Large text templates not available. Set use_large_text_templates=True during initialization.")
        
        print(f"🚀 Generating document with large text templates for {audience} audience...")
        
        # Prepare template variables from input data
        template_variables = self._prepare_large_text_variables(input_data)
        
        # Add custom variables if provided
        if custom_variables:
            template_variables.update(custom_variables)
        
        # Generate document using large text templates
        document = create_complete_document_from_templates(template_variables, audience)
        
        print("✅ Document generated successfully using large text templates!")
        return document
    
    async def generate_customized_document(
        self, 
        input_data: ISMInput,
        audience_override: Optional[str] = None,
        config_override: Optional[ISMConfig] = None
    ) -> ISMOutput:
        """
        Generate a document with custom audience or configuration.
        
        Args:
            input_data: Input parameters for document generation
            audience_override: Override the target audience
            config_override: Override the agent configuration
            
        Returns:
            Generated ISM document
        """
        # Create a copy of input data with audience override if provided
        if audience_override:
            input_dict = input_data.model_dump()
            input_dict['target_audience'] = audience_override
            input_data = ISMInput(**input_dict)
        
        # Temporarily update configuration if override provided
        original_config = self.ism_config
        if config_override:
            self.ism_config = config_override
        
        try:
            result = await self.generate_document(input_data)
            return result
        finally:
            # Restore original configuration
            self.ism_config = original_config

    async def propose_knowledge_update(self, feedback: str) -> str:
        """
        Propose an update to the ISM knowledge base.
        """
        # Use unified KnowledgeUpdater interface
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
        Apply an update to the ISM knowledge base.
        """
        from core.rag_manager import rag_manager
        updater = KnowledgeUpdater(rag_manager)
        await updater.apply_update(update_plan)