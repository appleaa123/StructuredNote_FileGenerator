"""
BSP (Base Shelf Prospectus) Agent implementation using Pydantic AI framework.

This agent generates comprehensive base shelf prospectus documents for structured
notes programs, following regulatory requirements and best practices for legal
document generation.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic_ai import Agent, RunContext
from lightrag import LightRAG, QueryParam

from core.base_agent import BaseFinancialAgent
from core.knowledge_updater import KnowledgeUpdater
from .models import BSPInput, BSPOutput, BSPAgentDeps
from .instructions import BSPInstructions
from .config import BSPConfig

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
    print("⚠️  Large text templates not available, using standard BSP agent")


class BSPAgent(BaseFinancialAgent[BSPInput, BSPOutput, BSPAgentDeps]):
    """
    BSP (Base Shelf Prospectus) Agent specialized in generating base shelf prospectus 
    documents for structured notes programs using Pydantic AI framework.
    
    This agent creates comprehensive legal documents that serve as the foundation
    for multiple structured note issuances, ensuring regulatory compliance and
    professional standards.
    
    Key capabilities:
    - Generate comprehensive base shelf prospectus documents
    - Retrieve legal templates and regulatory requirements
    - Create detailed program descriptions and risk factors
    - Ensure regulatory compliance across jurisdictions
    - Customize content for different audiences
    - Use large text templates for professional formatting
    """
    
    def __init__(
        self, 
        knowledge_base_path: str = "knowledge_bases/bsp_kb/",
        model_name: str = "openai:gpt-4o-mini",
        config: Optional[BSPConfig] = None,
        use_large_text_templates: bool = True
    ):
        """
        Initialize the BSP agent.
        
        Args:
            knowledge_base_path: Path to BSP knowledge base
            model_name: LLM model to use for generation
            config: BSP-specific configuration
            use_large_text_templates: Whether to use large text templates (default: True)
        """
        self.bsp_config = config or BSPConfig.get_default_config()
        self.instructions = BSPInstructions()
        self.use_large_text_templates = use_large_text_templates and LARGE_TEXT_AVAILABLE
        
        if self.use_large_text_templates:
            print("✅ BSP agent configured to use large text templates")
        else:
            print("⚠️  BSP agent using standard templates")
        
        super().__init__(
            agent_type="bsp",
            knowledge_base_path=knowledge_base_path,
            model_name=model_name,
            agent_config=self.bsp_config.model_dump()
        )
    
    def _create_agent(self) -> Agent[BSPAgentDeps, BSPOutput]:
        """Create and configure the Pydantic AI agent for BSP"""
        agent = Agent(
            model=self.model_name,
            deps_type=BSPAgentDeps,
            output_type=BSPOutput,
            instructions=self.get_system_instructions()
        )
        
        return agent
    
    def _register_agent_tools(self):
        """Register BSP-specific tools for document generation"""
        
        @self.agent.tool
        async def retrieve_legal_templates(
            ctx: RunContext[BSPAgentDeps], 
            query: str,
            jurisdiction: Optional[str] = None
        ) -> str:
            """
            Retrieve legal templates and regulatory requirements from the knowledge base.
            
            Args:
                ctx: The run context containing dependencies
                query: Search query for relevant templates
                jurisdiction: Specific jurisdiction to focus on
                
            Returns:
                Retrieved legal template content and requirements
            """
            try:
                # Enhance query with jurisdiction if provided
                if jurisdiction:
                    enhanced_query = f"legal template {jurisdiction} {query}"
                else:
                    enhanced_query = f"legal template {query}"
                
                result = await ctx.deps.lightrag.aquery(
                    enhanced_query,
                    param=QueryParam(mode="mix", top_k=8)
                )
                
                return f"**Legal Template Information:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving legal templates: {str(e)}"
        
        @self.agent.tool
        async def retrieve_regulatory_requirements(
            ctx: RunContext[BSPAgentDeps], 
            jurisdiction: str,
            document_type: str = "base_shelf_prospectus"
        ) -> str:
            """
            Retrieve regulatory requirements and compliance information.
            
            Args:
                ctx: The run context containing dependencies
                jurisdiction: Regulatory jurisdiction (SEC, Canada, EU, etc.)
                document_type: Type of document for specific requirements
                
            Returns:
                Regulatory requirements and compliance information
            """
            try:
                query = f"regulatory requirements {jurisdiction} {document_type} compliance"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=10)
                )
                
                return f"**Regulatory Requirements:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving regulatory requirements: {str(e)}"
        
        @self.agent.tool
        async def retrieve_issuer_information(
            ctx: RunContext[BSPAgentDeps], 
            issuer_type: str,
            business_sector: Optional[str] = None
        ) -> str:
            """
            Retrieve issuer information and business descriptions.
            
            Args:
                ctx: The run context containing dependencies
                issuer_type: Type of issuer (bank, financial institution, etc.)
                business_sector: Specific business sector to focus on
                
            Returns:
                Issuer information and business descriptions
            """
            try:
                query_parts = [issuer_type, "business description", "financial institution"]
                if business_sector:
                    query_parts.append(business_sector)
                
                query = " ".join(query_parts) + " issuer information"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=8)
                )
                
                return f"**Issuer Information:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving issuer information: {str(e)}"
        
        @self.agent.tool
        async def retrieve_program_structure_examples(
            ctx: RunContext[BSPAgentDeps],
            program_type: str,
            note_types: Optional[str] = None
        ) -> str:
            """
            Retrieve program structure examples and templates.
            
            Args:
                ctx: The run context containing dependencies
                program_type: Type of structured notes program
                note_types: Specific note types to focus on
                
            Returns:
                Program structure examples and templates
            """
            try:
                query_parts = [program_type, "structured notes program", "shelf registration"]
                if note_types:
                    query_parts.append(note_types)
                
                query = " ".join(query_parts) + " program structure examples"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=6)
                )
                
                return f"**Program Structure Examples:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving program structure examples: {str(e)}"
        
        @self.agent.tool
        async def retrieve_risk_factor_templates(
            ctx: RunContext[BSPAgentDeps], 
            risk_categories: str,
            jurisdiction: str = "SEC"
        ) -> str:
            """
            Retrieve risk factor templates and examples.
            
            Args:
                ctx: The run context containing dependencies
                risk_categories: Categories of risks to include
                jurisdiction: Regulatory jurisdiction for compliance
                
            Returns:
                Risk factor templates and examples
            """
            try:
                query = f"risk factors {risk_categories} {jurisdiction} legal templates"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=8)
                )
                
                return f"**Risk Factor Templates:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving risk factor templates: {str(e)}"
        
        @self.agent.tool
        async def retrieve_legal_terms_examples(
            ctx: RunContext[BSPAgentDeps],
            legal_area: str,
            jurisdiction: Optional[str] = None
        ) -> str:
            """
            Retrieve legal terms and conditions examples.
            
            Args:
                ctx: The run context containing dependencies
                legal_area: Specific legal area (securities, corporate, etc.)
                jurisdiction: Regulatory jurisdiction (optional)
                
            Returns:
                Legal terms and conditions examples
            """
            try:
                query_parts = [legal_area, "legal terms", "conditions"]
                if jurisdiction:
                    query_parts.append(jurisdiction)
                
                query = " ".join(query_parts) + " examples templates"
                
                result = await ctx.deps.lightrag.aquery(
                    query,
                    param=QueryParam(mode="mix", top_k=6)
                )
                
                return f"**Legal Terms Examples:**\n{result}"
                
            except Exception as e:
                return f"Error retrieving legal terms examples: {str(e)}"

        @self.agent.tool
        async def retrieve_dealer_agreements(
            ctx: RunContext[BSPAgentDeps],
            jurisdiction: str = "Canada",
            focus: str = "dealer agreement terms"
        ) -> str:
            """
            Retrieve dealer/underwriting agreement examples and standard clauses.
            """
            try:
                query = f"{jurisdiction} {focus} base shelf prospectus underwriting syndicate provisions"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Dealer/Underwriting Agreements:**\n{result}"
            except Exception as e:
                return f"Error retrieving dealer agreements: {str(e)}"

        @self.agent.tool
        async def retrieve_use_of_proceeds_examples(
            ctx: RunContext[BSPAgentDeps],
            issuer: Optional[str] = None,
            sector: Optional[str] = None
        ) -> str:
            """
            Retrieve standard 'Use of Proceeds' language and examples.
            """
            try:
                parts = ["use of proceeds", "base shelf prospectus", "structured notes"]
                if issuer:
                    parts.append(issuer)
                if sector:
                    parts.append(sector)
                query = " ".join(parts)
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=6))
                return f"**Use of Proceeds Examples:**\n{result}"
            except Exception as e:
                return f"Error retrieving use of proceeds: {str(e)}"

        @self.agent.tool
        async def retrieve_shelf_program_requirements(
            ctx: RunContext[BSPAgentDeps],
            jurisdiction: str = "SEC",
            duration_years: int = 3
        ) -> str:
            """
            Retrieve shelf registration program requirements and duration/renewal standards.
            """
            try:
                query = f"{jurisdiction} shelf registration program requirements duration {duration_years} renewal disclosure"
                result = await ctx.deps.lightrag.aquery(query, param=QueryParam(mode="mix", top_k=5))
                return f"**Shelf Program Requirements:**\n{result}"
            except Exception as e:
                return f"Error retrieving shelf program requirements: {str(e)}"
    
    def get_system_instructions(self) -> str:
        """Get BSP-specific system instructions"""
        base_instructions = self.instructions.get_base_instructions()
        
        # Add legal compliance guidelines
        legal_guidelines = self.instructions.get_legal_compliance_guidelines()
        
        return f"{base_instructions}\n\n{legal_guidelines}"
    
    async def _create_dependencies(self, lightrag: LightRAG, input_data: BSPInput) -> BSPAgentDeps:
        """Create BSP-specific dependencies"""
        return BSPAgentDeps(
            lightrag=lightrag,
            agent_type=self.agent_type,
            input_data=input_data,
            config=self.bsp_config.model_dump()
        )
    
    def _format_user_prompt(self, input_data: BSPInput) -> str:
        """Format the user prompt for BSP document generation"""
        
        # Get program-specific instructions
        program_instructions = self.instructions.get_program_type_instructions("general")
        
        # Get audience-specific instructions (default to institutional for BSP)
        audience_instructions = self.instructions.get_audience_specific_instructions("institutional")
        
        # Build comprehensive prompt
        prompt = f"""
        Generate a comprehensive Base Shelf Prospectus document for the following structured notes program.
        
        ## Program Details:
        - **Program Name**: {input_data.program_name}
        - **Issuer**: {input_data.issuer}
        - **Guarantor**: {input_data.guarantor or 'Not applicable'}
        - **Shelf Amount**: {input_data.shelf_amount:,.2f} {input_data.currency}
        - **Currency**: {input_data.currency}
        - **Regulatory Jurisdiction**: {input_data.regulatory_jurisdiction}
        - **Legal Structure**: {input_data.legal_structure}
        
        ## Business Information:
        - **Business Description**: {input_data.business_description}
        - **Financial Condition**: {input_data.financial_condition or 'Available upon request'}
        - **SEC Registration**: {input_data.sec_registration or 'Not applicable'}
        
        ## Program Structure:
        - **Note Types**: {', '.join(input_data.note_types)}
        - **Distribution Methods**: {', '.join(input_data.distribution_methods)}
        """
        
        # Add additional features if any
        if input_data.additional_features:
            prompt += f"- **Additional Features**: {input_data.additional_features}\n"
        
        # Get section-specific formatting requirements
        section_requirements = self.instructions.get_section_formatting_requirements()
        mandatory_compliance = self.instructions.get_mandatory_compliance_text(input_data.regulatory_jurisdiction)
        
        # Add specific instructions
        prompt += f"""
        
        ## Generation Instructions:
        
        {program_instructions}
        
        {audience_instructions}
        
        ## CRITICAL FORMATTING REQUIREMENTS:
        
        **Document Title Format:**
        {section_requirements['document_title']}
        
        **Cover Page Structure:**
        {section_requirements['cover_page']}
        
        **Executive Summary Structure:**
        {section_requirements['executive_summary']}
        
        **Issuer Information Format:**
        {section_requirements['issuer_information']}
        
        **Program Overview Format:**
        {section_requirements['program_overview']}
        
        **Risk Factors Format:**
        {section_requirements['risk_factors']}
        
        **Legal Terms Format:**
        {section_requirements['legal_terms']}
        
        **Use of Proceeds Format:**
        {section_requirements['use_of_proceeds']}
        
        **Regulatory Disclosures Format:**
        {section_requirements['regulatory_disclosures']}
        
        **Mandatory Compliance Text (MUST include exactly):**
        """
        
        for key, text in mandatory_compliance.items():
            prompt += f"- {key}: {text}\n"
        
        prompt += f"""
        
        ## Required Tools Usage:
        
        Before generating the document, please use the available tools to:
        
        1. **retrieve_legal_templates**: Get legal templates for {input_data.regulatory_jurisdiction} base shelf prospectus
        2. **retrieve_regulatory_requirements**: Get regulatory requirements for {input_data.regulatory_jurisdiction}
        3. **retrieve_issuer_information**: Get issuer information for {input_data.issuer}
        4. **retrieve_program_structure_examples**: Get program structure examples for structured notes
        5. **retrieve_risk_factor_templates**: Get risk factor templates for {input_data.regulatory_jurisdiction}
        6. **retrieve_legal_terms_examples**: Get legal terms examples for securities law
        
        ## Output Requirements:
        
        Generate a complete BSPOutput with all required fields populated. The document MUST:
        - Follow ALL formatting requirements specified above EXACTLY
        - Include ALL mandatory compliance text word-for-word
        - Use professional legal language throughout
        - Include comprehensive risk factor disclosure
        - Format all amounts with proper currency notation
        - Include detailed program structure and capabilities
        - Maintain regulatory compliance for {input_data.regulatory_jurisdiction}
        
        **VERIFICATION CHECKLIST:**
        Before submitting, verify that:
        ✓ Document title follows exact format
        ✓ Cover page includes all required information
        ✓ Executive summary has exactly 3-4 paragraphs
        ✓ Issuer information is comprehensive and accurate
        ✓ Program overview includes all note types and distribution methods
        ✓ Risk factors are comprehensive and properly categorized
        ✓ Legal terms are complete and jurisdiction-appropriate
        ✓ Use of proceeds is clearly described
        ✓ All mandatory compliance phrases are included word-for-word
        ✓ Professional legal language is used throughout
        
        **Generation Date**: {datetime.now().strftime('%Y-%m-%d')}
        """
        
        return prompt
    
    def _prepare_large_text_variables(self, input_data: BSPInput) -> dict:
        """Prepare variables for large text templates from BSP input data"""
        from datetime import datetime
        
        # Generate program codes
        import hashlib
        program_string = f"{input_data.program_name}_{input_data.issuer}"
        hash_object = hashlib.md5(program_string.encode())
        program_code = f"BSP-{hash_object.hexdigest()[:6].upper()}"
        
        registration_string = f"{input_data.program_name}_{input_data.issuer}_{input_data.shelf_amount}"
        hash_object = hashlib.md5(registration_string.encode())
        shelf_registration_number = f"SR-{hash_object.hexdigest()[:8].upper()}"
        
        # Prepare variables for large text templates
        variables = {
            # Document header
            "Program Name": input_data.program_name,
            "Issuer": input_data.issuer,
            "Guarantor": input_data.guarantor or "Not applicable",
            "Shelf Amount": f"{input_data.shelf_amount:,.0f}",
            "Currency": input_data.currency,
            "Regulatory Jurisdiction": input_data.regulatory_jurisdiction,
            "Document Date": datetime.now().strftime("%B %d, %Y"),
            "Generation Date": datetime.now().strftime("%Y-%m-%d"),
            
            # Program details
            "Program Code": program_code,
            "Shelf Registration Number": shelf_registration_number,
            "Program Duration": "3 years",
            "Legal Structure": input_data.legal_structure,
            "SEC Registration": input_data.sec_registration or "Not applicable",
            
            # Business information
            "Business Description": input_data.business_description,
            "Financial Condition": input_data.financial_condition or "Available upon request",
            
            # Note types and distribution
            "Note Types": ", ".join(input_data.note_types),
            "Distribution Methods": ", ".join(input_data.distribution_methods),
            
            # Additional features
            "Additional Features": self._format_additional_features(input_data.additional_features),
            
            # Regulatory information
            "Regulatory Framework": f"Compliant with {input_data.regulatory_jurisdiction} regulations",
            "Compliance Status": "Fully compliant with all applicable regulations",
            
            # Contact information (defaults)
            "Contact Phone": "1-800-STRUCTURED",
            "Contact Email": "structuredproducts@issuer.com",
            "Contact Website": "www.issuer.com/structuredproducts",
            "Legal Department": "legal@issuer.com",
            "Compliance Department": "compliance@issuer.com",
            
            # Document metadata
            "Document Version": "1.0",
            "Document Type": "Base Shelf Prospectus",
            "Document Status": "Draft for Review",
            
            # Risk categories
            "Market Risk Level": "High",
            "Credit Risk Level": "Medium",
            "Liquidity Risk Level": "Medium",
            "Regulatory Risk Level": "Low",
            "Operational Risk Level": "Low",
            
            # Program capabilities
            "Maximum Note Size": f"{input_data.shelf_amount * 0.1:,.0f} {input_data.currency}",
            "Minimum Note Size": f"{input_data.shelf_amount * 0.001:,.0f} {input_data.currency}",
            "Shelf Period": "3 years from effective date",
            "Renewal Process": "Subject to regulatory approval and market conditions",
            
            # Distribution channels
            "Primary Distribution": "Institutional investors and qualified purchasers",
            "Secondary Distribution": "Broker-dealer networks and private placements",
            "Retail Distribution": "Limited to accredited investors and qualified purchasers",
            
            # Regulatory compliance
            "SEC Compliance": "Full compliance with Regulation S-K and other applicable regulations",
            "Ongoing Disclosures": "Quarterly and annual reports as required by applicable regulations",
            "Material Events": "Immediate disclosure of material events affecting the program",
            
            # Legal framework
            "Governing Law": "New York law",
            "Dispute Resolution": "Arbitration in accordance with FINRA rules",
            "Jurisdiction": "Federal and state courts in New York",
            
            # Use of proceeds
            "Primary Use": "General corporate purposes including funding structured products",
            "Secondary Use": "Hedging activities and risk management",
            "Tertiary Use": "Working capital and other business purposes",
            
            # Risk management
            "Risk Management Framework": "Comprehensive risk management policies and procedures",
            "Credit Risk Management": "Regular credit assessments and monitoring",
            "Market Risk Management": "Dynamic hedging strategies and position limits",
            "Operational Risk Management": "Robust internal controls and monitoring systems"
        }

        # Map to new BSP template placeholders with sensible defaults
        variables.update({
            # Dates and formalities
            "Date of Prospectus": variables.get("Document Date", datetime.now().strftime("%B %d, %Y")),
            "Dealer Agreement Date": variables.get("Document Date", datetime.now().strftime("%B %d, %Y")),

            # Parties and signatories
            "List of Investment Dealers": "To be determined and disclosed in applicable pricing supplement",
            "Directors Resident Outside of Canada": "None",
            "Bank Legal Counsel": "To be determined",
            "Dealers Legal Counsel": "To be determined",

            # Tranche-specific placeholders
            "Specific Designation of Notes": f"{input_data.program_name} Notes",
            "Aggregate Principal Amount": "See applicable product or pricing supplement",
            "Maturity Date": "See applicable product or pricing supplement",
            "Offering Price": "See applicable product or pricing supplement",
            "Variable Return Formula": "As described in the applicable product or pricing supplement",
            "Underlying Interests": "As described in the applicable product or pricing supplement",
            "Minimum Principal Repayment": "0% unless otherwise specified in the applicable supplement",
        })
        
        return variables
    
    def _format_additional_features(self, additional_features: Optional[Dict[str, Any]]) -> str:
        """Format additional features for template use"""
        if not additional_features:
            return "Standard program features apply"
        
        features = []
        for key, value in additional_features.items():
            if isinstance(value, (list, tuple)):
                features.append(f"{key}: {', '.join(map(str, value))}")
            else:
                features.append(f"{key}: {value}")
        
        return "; ".join(features)
    
    async def generate_document_with_large_text_templates(
        self, 
        input_data: BSPInput,
        audience: str = "institutional",
        custom_variables: Optional[dict] = None
    ) -> dict:
        """
        Generate document using large text templates.
        
        Args:
            input_data: BSP input data
            audience: Target audience ("institutional", "retail", or "regulatory")
            custom_variables: Additional variables for template substitution
            
        Returns:
            Dictionary with generated document sections using large text templates
        """
        if not self.use_large_text_templates:
            raise ValueError("Large text templates not available. Set use_large_text_templates=True during initialization.")
        
        print(f"🚀 Generating BSP document with large text templates for {audience} audience...")
        
        # Prepare template variables from input data
        template_variables = self._prepare_large_text_variables(input_data)
        
        # Add custom variables if provided
        if custom_variables:
            template_variables.update(custom_variables)
        
        # Generate document using large text templates
        document = create_complete_document_from_templates(template_variables, audience)
        
        print("✅ BSP document generated successfully using large text templates!")
        return document
    
    async def generate_customized_document(
        self, 
        input_data: BSPInput,
        audience_override: Optional[str] = None,
        config_override: Optional[BSPConfig] = None
    ) -> BSPOutput:
        """
        Generate a document with custom audience or configuration.
        
        Args:
            input_data: Input parameters for document generation
            audience_override: Override the target audience
            config_override: Override the agent configuration
            
        Returns:
            Generated BSP document
        """
        # Temporarily update configuration if override provided
        original_config = self.bsp_config
        if config_override:
            self.bsp_config = config_override
        
        try:
            result = await self.generate_document(input_data)
            return result
        finally:
            # Restore original configuration
            self.bsp_config = original_config

    async def propose_knowledge_update(self, feedback: str) -> str:
        """
        Propose an update to the BSP knowledge base.
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
        Apply an update to the BSP knowledge base.
        """
        from core.rag_manager import rag_manager
        updater = KnowledgeUpdater(rag_manager)
        await updater.apply_update(update_plan)