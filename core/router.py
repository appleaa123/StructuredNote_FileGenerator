"""
Smart Agent Router for analyzing user requests and routing to appropriate sub-agents.

This module provides intelligent routing capabilities to:
- Analyze user requests to detect which agents are needed
- Extract key information required for document generation
- Decompose complex tasks into sub-tasks for different agents
- Route tasks to the appropriate specialized agents
- Handle multi-agent workflows and coordination
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field  # type: ignore

from .config import global_config

# Configure logging
logging.basicConfig(level=global_config.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Enumeration of available agent types"""
    INVESTOR_SUMMARY = "investor_summary"  # Investor Summary
    BASE_SHELF_PROSPECTUS = "base_shelf_prospectus"  # Base Shelf Prospectus
    PRODUCT_SUPPLEMENT = "product_supplement"  # Product Supplement
    PRICING_SUPPLEMENT = "pricing_supplement"  # Pricing Supplement


class TaskType(Enum):
    """Enumeration of task types that can be performed"""
    DOCUMENT_GENERATION = "document_generation"
    KNOWLEDGE_UPDATE = "knowledge_update"
    DOCUMENT_REVIEW = "document_review"
    CROSS_REFERENCE = "cross_reference"
    TEMPLATE_RETRIEVAL = "template_retrieval"
    COMPLIANCE_CHECK = "compliance_check"


@dataclass
class AgentCapability:
    """Represents the capabilities of a specific agent"""
    agent_type: AgentType
    input_model: type
    output_model: type
    description: str
    keywords: List[str]
    required_fields: List[str]
    optional_fields: List[str]
    supported_tasks: List[TaskType]


@dataclass
class RoutingDecision:
    """Represents a routing decision for a task"""
    primary_agent: AgentType
    secondary_agents: List[AgentType]
    extracted_data: Dict[str, Any]
    confidence_score: float
    reasoning: str
    task_decomposition: List[Dict[str, Any]]


@dataclass
class ExtractedInformation:
    """Represents information extracted from user requests"""
    issuer: Optional[str] = None
    product_name: Optional[str] = None
    underlying_asset: Optional[str] = None
    currency: Optional[str] = None
    principal_amount: Optional[float] = None
    product_type: Optional[str] = None
    regulatory_jurisdiction: Optional[str] = None
    target_audience: Optional[str] = None
    document_type: Optional[str] = None
    # PDS-specific fields (aligned with PDSInput)
    base_prospectus_reference: Optional[str] = None
    base_prospectus_date: Optional[str] = None
    note_series: Optional[str] = None
    note_description: Optional[str] = None
    issue_price: Optional[str] = None
    issue_date: Optional[str] = None
    maturity_date: Optional[str] = None
    pricing_date: Optional[str] = None
    barrier_level: Optional[str] = None
    coupon_structure: Optional[str] = None
    calculation_methodology: Optional[str] = None
    underlying_performance: Optional[str] = None
    # PRS-specific fields (aligned with PRSInput)
    final_issue_price: Optional[str] = None
    final_principal_amount: Optional[str] = None
    settlement_date: Optional[str] = None
    final_coupon_rate: Optional[str] = None
    final_barrier_level: Optional[str] = None
    underlying_initial_level: Optional[str] = None
    underlying_price_at_pricing: Optional[str] = None
    market_conditions: Optional[str] = None
    volatility_at_pricing: Optional[str] = None
    distribution_method: Optional[str] = None
    minimum_denomination: Optional[str] = None
    agent_discount: Optional[str] = None
    estimated_value: Optional[str] = None
    supplement_reference: Optional[str] = None
    additional_context: Dict[str, Any] = None


class SmartAgentRouter:
    """
    Intelligent router that analyzes user requests and routes to appropriate sub-agents.
    
    This class provides:
    - Request analysis and agent detection
    - Key information extraction from natural language
    - Task decomposition for complex requests
    - Routing decisions with confidence scoring
    - Support for multi-agent workflows
    """
    
    def __init__(self):
        """Initialize the SmartAgentRouter with agent capabilities"""
        self.agent_capabilities = self._initialize_agent_capabilities()
        self.keyword_patterns = self._build_keyword_patterns()
        self.extraction_patterns = self._build_extraction_patterns()
        
    def _initialize_agent_capabilities(self) -> Dict[AgentType, AgentCapability]:
        """Initialize the capabilities of all available agents"""
        capabilities = {
            AgentType.INVESTOR_SUMMARY: AgentCapability(
                agent_type=AgentType.INVESTOR_SUMMARY,
                input_model=None,  # set below
                output_model=None,  # set below
                description="Generates investor-friendly summary documents for structured products",
                keywords=[
                    "investor summary", "investor friendly", "summary document", "retail investor",
                    "autocallable", "structured note", "investment summary", "product summary",
                    "investor guide", "product overview", "investment overview"
                ],
                required_fields=[
                    "issuer", "product_name", "underlying_asset", "currency", "principal_amount",
                    "product_type", "regulatory_jurisdiction"
                ],
                optional_fields=[
                    "barrier_level", "coupon_rate", "protection_level", "autocall_barrier",
                    "target_audience", "risk_tolerance", "investment_objective"
                ],
                supported_tasks=[
                    TaskType.DOCUMENT_GENERATION,
                    TaskType.TEMPLATE_RETRIEVAL,
                    TaskType.COMPLIANCE_CHECK
                ]
            ),
            AgentType.BASE_SHELF_PROSPECTUS: AgentCapability(
                agent_type=AgentType.BASE_SHELF_PROSPECTUS,
                input_model=None,
                output_model=None,
                description="Generates base shelf prospectus documents for structured product programs",
                keywords=[
                    "base shelf prospectus", "shelf prospectus", "prospectus", "shelf program",
                    "shelf amount", "program prospectus", "base prospectus", "shelf filing"
                ],
                required_fields=[
                    "issuer", "program_name", "shelf_amount", "currency", "regulatory_jurisdiction"
                ],
                optional_fields=[
                    "program_description", "shelf_period", "filing_date", "effective_date"
                ],
                supported_tasks=[
                    TaskType.DOCUMENT_GENERATION,
                    TaskType.COMPLIANCE_CHECK
                ]
            ),
            AgentType.PRODUCT_SUPPLEMENT: AgentCapability(
                agent_type=AgentType.PRODUCT_SUPPLEMENT,
                input_model=None,
                output_model=None,
                description="Generates product supplement documents for specific offerings",
                keywords=[
                    "product supplement", "supplement", "offering document", "supplemental prospectus",
                    "offering prospectus", "supplemental filing", "offering supplement"
                ],
                required_fields=[
                    "base_prospectus_reference",
                    "base_prospectus_date",
                    "note_series",
                    "note_description",
                    "underlying_asset",
                    "principal_amount",
                    "issue_price",
                    "currency",
                    "issue_date",
                    "maturity_date",
                    "product_type",
                    "calculation_methodology",
                ],
                optional_fields=[
                    "pricing_date",
                    "barrier_level",
                    "coupon_structure",
                    "underlying_performance",
                    "additional_terms",
                ],
                supported_tasks=[
                    TaskType.DOCUMENT_GENERATION,
                    TaskType.COMPLIANCE_CHECK
                ]
            ),
            AgentType.PRICING_SUPPLEMENT: AgentCapability(
                agent_type=AgentType.PRICING_SUPPLEMENT,
                input_model=None,
                output_model=None,
                description="Generates pricing supplement documents with specific product terms",
                keywords=[
                    "pricing supplement", "pricing terms", "product terms", "pricing document",
                    "final terms", "pricing sheet", "term sheet", "pricing supplement"
                ],
                required_fields=[
                    "base_prospectus_reference",
                    "final_issue_price",
                    "final_principal_amount",
                    "currency",
                    "pricing_date",
                    "issue_date",
                    "maturity_date",
                    "settlement_date",
                    "distribution_method",
                    "minimum_denomination",
                ],
                optional_fields=[
                    "supplement_reference",
                    "final_coupon_rate",
                    "final_barrier_level",
                    "underlying_initial_level",
                    "underlying_price_at_pricing",
                    "market_conditions",
                    "volatility_at_pricing",
                    "agent_discount",
                    "estimated_value",
                    "additional_terms",
                ],
                supported_tasks=[
                    TaskType.DOCUMENT_GENERATION,
                    TaskType.COMPLIANCE_CHECK
                ]
            )
        }

        # Bind real Pydantic models for stronger validation and introspection
        try:
            from agents.investor_summary.models import ISMInput, ISMOutput
            from agents.base_shelf_prospectus.models import BSPInput, BSPOutput
            from agents.product_supplement.models import PDSInput, PDSOutput
            from agents.pricing_supplement.models import PRSInput, PRSOutput
            capabilities[AgentType.INVESTOR_SUMMARY].input_model = ISMInput
            capabilities[AgentType.INVESTOR_SUMMARY].output_model = ISMOutput
            capabilities[AgentType.BASE_SHELF_PROSPECTUS].input_model = BSPInput
            capabilities[AgentType.BASE_SHELF_PROSPECTUS].output_model = BSPOutput
            capabilities[AgentType.PRODUCT_SUPPLEMENT].input_model = PDSInput
            capabilities[AgentType.PRODUCT_SUPPLEMENT].output_model = PDSOutput
            capabilities[AgentType.PRICING_SUPPLEMENT].input_model = PRSInput
            capabilities[AgentType.PRICING_SUPPLEMENT].output_model = PRSOutput
        except Exception:
            # Keep defaults if imports fail; avoids hard dependency at import time
            pass

        return capabilities
    
    def _build_keyword_patterns(self) -> Dict[str, List[str]]:
        """Build keyword patterns for agent detection"""
        patterns = {}
        for agent_type, capability in self.agent_capabilities.items():
            patterns[agent_type.value] = capability.keywords
        return patterns
    
    def _build_extraction_patterns(self) -> Dict[str, re.Pattern]:
        """Build regex patterns for information extraction"""
        return {
            "issuer": re.compile(r"(?:by|from|issued by|company|firm|bank)\s+([A-Za-z\s&.,]+?)(?:\s+(?:on|with|for|program|note|security|autocallable|barrier|prospectus|supplement|pricing|shelf|offering|product|amount|jurisdiction|currency|million|billion|thousand|USD|EUR|GBP|CAD|AUD|JPY|\$|%|on the|with \$|for \$|program|note|security|autocallable|barrier|prospectus|supplement|pricing|shelf|offering|product|amount|jurisdiction|currency|million|billion|thousand|USD|EUR|GBP|CAD|AUD|JPY|\$|%|on the|with \$|for \$))", re.IGNORECASE),
            "product_name": re.compile(r"(?:product|note|security|investment|program|offering)\s*(?:name|title)?\s*[:\-]?\s*([A-Za-z0-9\s&.,\-]+?)(?:\s+(?:on|with|for|program|note|security|autocallable|barrier|prospectus|supplement|pricing|shelf|offering|product|amount|jurisdiction|currency|million|billion|thousand|USD|EUR|GBP|CAD|AUD|JPY|\$|%|on the|with \$|for \$|program|note|security|autocallable|barrier|prospectus|supplement|pricing|shelf|offering|product|amount|jurisdiction|currency|million|billion|thousand|USD|EUR|GBP|CAD|AUD|JPY|\$|%|on the|with \$|for \$))", re.IGNORECASE),
            "underlying_asset": re.compile(r"(?:on|underlying|asset|index|reference)\s+(?:the\s+)?([A-Za-z0-9\s&.,]+?)(?:\s+(?:with|for|program|note|security|autocallable|barrier|prospectus|supplement|pricing|shelf|offering|product|amount|jurisdiction|currency|million|billion|thousand|USD|EUR|GBP|CAD|AUD|JPY|\$|%|with \$|for \$))", re.IGNORECASE),
            "currency": re.compile(r"(?:currency|denomination|USD|EUR|GBP|CAD|AUD|JPY)\s*[:\-]?\s*(USD|EUR|GBP|CAD|AUD|JPY)", re.IGNORECASE),
            "principal_amount": re.compile(r"\$?([0-9,]+(?:\.\d{2})?)\s*(?:million|billion|thousand)?\s*(USD|EUR|GBP|CAD|AUD|JPY)?", re.IGNORECASE),
            "product_type": re.compile(r"(?:type|structure|autocallable|barrier|reverse convertible|step-up|memory)\s*[:\-]?\s*(autocallable|barrier|reverse convertible|step-up|memory)", re.IGNORECASE),
            "regulatory_jurisdiction": re.compile(r"(?:jurisdiction|regulatory|compliance|US|EU|UK|Canada|Australia|Japan)\s*[:\-]?\s*(US|EU|UK|Canada|Australia|Japan)", re.IGNORECASE),
            "target_audience": re.compile(r"(?:audience|investor|target|retail|institutional|accredited|qualified)\s*[:\-]?\s*(retail|institutional|accredited|qualified)", re.IGNORECASE),
            "document_type": re.compile(r"(?:document|documentation|report|summary|prospectus|supplement|pricing)\s*[:\-]?\s*(summary|prospectus|supplement|pricing)", re.IGNORECASE),
            # PDS-specific fields aligned to PDSInput
            "base_prospectus_reference": re.compile(r"(?:base\s*(?:shelf\s*)?prospectus(?:\s*reference)?|base\s*prospectus)\s*[:\-]?\s*([A-Za-z0-9\s,&().\-]+)", re.IGNORECASE),
            "base_prospectus_date": re.compile(r"(?:base\s*(?:shelf\s*)?prospectus\s*date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s+\d{1,2},\s*\d{4})", re.IGNORECASE),
            "note_series": re.compile(r"(?:note\s*series|series)\s*[:\-]?\s*([A-Za-z0-9\-\s]+)", re.IGNORECASE),
            "note_description": re.compile(r"(?:note\s*description|description)\s*[:\-]?\s*([A-Za-z0-9\s,&().\-]+)", re.IGNORECASE),
            "issue_price": re.compile(r"(?:issue\s*price)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)\s*%", re.IGNORECASE),
            "issue_date": re.compile(r"(?:issue\s*date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s+\d{1,2},\s*\d{4})", re.IGNORECASE),
            "maturity_date": re.compile(r"(?:maturity\s*date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s+\d{1,2},\s*\d{4})", re.IGNORECASE),
            "pricing_date": re.compile(r"(?:pricing\s*date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s+\d{1,2},\s*\d{4})", re.IGNORECASE),
            "barrier_level": re.compile(r"(?:barrier\s*(?:level)?)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)\s*%", re.IGNORECASE),
            "coupon_structure": re.compile(r"(?:coupon\s*(?:structure|payment\s*structure))\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
            "calculation_methodology": re.compile(r"(?:calculation\s*methodology)\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
            "underlying_performance": re.compile(r"(?:underlying\s*performance|performance\s*measure)\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
            # PRS-specific fields aligned to PRSInput
            "final_issue_price": re.compile(r"(?:final\s*issue\s*price)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)\s*%", re.IGNORECASE),
            "final_principal_amount": re.compile(r"(?:final\s*principal\s*amount)\s*[:\-]?\s*\$?([0-9,]+(?:\.[0-9]+)?)", re.IGNORECASE),
            "settlement_date": re.compile(r"(?:settlement\s*date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s+\d{1,2},\s*\d{4})", re.IGNORECASE),
            "final_coupon_rate": re.compile(r"(?:final\s*coupon\s*rate)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)\s*%", re.IGNORECASE),
            "final_barrier_level": re.compile(r"(?:final\s*barrier\s*level)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)\s*%", re.IGNORECASE),
            "underlying_initial_level": re.compile(r"(?:underlying\s*initial\s*level)\s*[:\-]?\s*([0-9,]+(?:\.[0-9]+)?)", re.IGNORECASE),
            "underlying_price_at_pricing": re.compile(r"(?:underlying\s*price\s*at\s*pricing)\s*[:\-]?\s*([0-9,]+(?:\.[0-9]+)?)", re.IGNORECASE),
            "market_conditions": re.compile(r"(?:market\s*conditions)\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
            "volatility_at_pricing": re.compile(r"(?:volatility\s*at\s*pricing|implied\s*volatility)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
            "distribution_method": re.compile(r"(?:distribution\s*method)\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
            "minimum_denomination": re.compile(r"(?:minimum\s*denomination)\s*[:\-]?\s*\$?([0-9,]+(?:\.[0-9]+)?)", re.IGNORECASE),
            "agent_discount": re.compile(r"(?:agent\s*discount)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
            "estimated_value": re.compile(r"(?:estimated\s*value)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
            "supplement_reference": re.compile(r"(?:supplement\s*reference)\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
        }
    
    def analyze_request(self, user_request: str) -> RoutingDecision:
        """
        Analyze a user request and determine routing decisions.
        
        Args:
            user_request: The user's natural language request
            
        Returns:
            RoutingDecision with agent assignments and extracted information
        """
        logger.info(f"Analyzing user request: {user_request[:100]}...")
        
        # Extract information from the request
        extracted_info = self._extract_information(user_request)
        
        # Detect which agents are needed
        agent_scores = self._detect_agents(user_request)
        
        # Determine primary and secondary agents
        primary_agent = self._determine_primary_agent(agent_scores)
        secondary_agents = self._determine_secondary_agents(agent_scores, primary_agent)
        
        # Decompose the task
        task_decomposition = self._decompose_task(user_request, primary_agent, secondary_agents)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(agent_scores, extracted_info)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(agent_scores, primary_agent, extracted_info)
        
        return RoutingDecision(
            primary_agent=primary_agent,
            secondary_agents=secondary_agents,
            extracted_data=extracted_info.__dict__,
            confidence_score=confidence_score,
            reasoning=reasoning,
            task_decomposition=task_decomposition
        )
    
    def _extract_information(self, user_request: str) -> ExtractedInformation:
        """Extract key information from the user request"""
        extracted = ExtractedInformation()
        extracted.additional_context = {}
        
        # Apply extraction patterns
        for field_name, pattern in self.extraction_patterns.items():
            match = pattern.search(user_request)
            if match:
                value = match.group(1).strip()
                if hasattr(extracted, field_name):
                    setattr(extracted, field_name, value)
                else:
                    extracted.additional_context[field_name] = value
        
        # Additional context extraction
        extracted.additional_context.update(self._extract_additional_context(user_request))
        
        # Post-process extracted information
        self._post_process_extracted_info(extracted, user_request)
        
        return extracted
    
    def _post_process_extracted_info(self, extracted: ExtractedInformation, user_request: str):
        """Post-process extracted information to improve accuracy"""
        # Clean up issuer names
        if extracted.issuer:
            # Remove common suffixes and clean up
            issuer = extracted.issuer.strip()
            for suffix in [' on', ' with', ' for', ' program', ' note', ' security']:
                if issuer.endswith(suffix):
                    issuer = issuer[:-len(suffix)]
            extracted.issuer = issuer.strip()
        
        # Clean up product names
        if extracted.product_name:
            product = extracted.product_name.strip()
            for suffix in [' on', ' with', ' for', ' program', ' note', ' security']:
                if product.endswith(suffix):
                    product = product[:-len(suffix)]
            extracted.product_name = product.strip()
        
        # Clean up underlying asset
        if extracted.underlying_asset:
            asset = extracted.underlying_asset.strip()
            for suffix in [' with', ' for', ' program', ' note', ' security']:
                if asset.endswith(suffix):
                    asset = asset[:-len(suffix)]
            extracted.underlying_asset = asset.strip()
        
        # Extract currency from principal amount if not already set
        if extracted.principal_amount and not extracted.currency:
            currency_match = re.search(r'(USD|EUR|GBP|CAD|AUD|JPY)', user_request, re.IGNORECASE)
            if currency_match:
                extracted.currency = currency_match.group(1)
        
        # Extract product type if not already set
        if not extracted.product_type:
            for product_type in ['autocallable', 'barrier', 'reverse convertible', 'step-up', 'memory']:
                if product_type.lower() in user_request.lower():
                    extracted.product_type = product_type
                    break
    
    def _extract_additional_context(self, user_request: str) -> Dict[str, Any]:
        """Extract additional context information"""
        context = {}
        
        # Extract dates
        date_pattern = re.compile(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})")
        dates = date_pattern.findall(user_request)
        if dates:
            context["dates"] = dates
        
        # Extract percentages
        percent_pattern = re.compile(r"(\d+(?:\.\d+)?)\s*%")
        percentages = percent_pattern.findall(user_request)
        if percentages:
            context["percentages"] = [float(p) for p in percentages]
        
        # Extract monetary amounts
        money_pattern = re.compile(r"\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)")
        amounts = money_pattern.findall(user_request)
        if amounts:
            context["monetary_amounts"] = [float(a.replace(',', '')) for a in amounts]
        
        return context
    
    def _detect_agents(self, user_request: str) -> Dict[AgentType, float]:
        """Detect which agents are needed based on the request"""
        agent_scores = {agent_type: 0.0 for agent_type in AgentType}
        
        # Convert request to lowercase for matching
        request_lower = user_request.lower()
        
        for agent_type, capability in self.agent_capabilities.items():
            score = 0.0
            
            # Check keyword matches
            for keyword in capability.keywords:
                if keyword.lower() in request_lower:
                    score += 1.0
            
            # Check for exact phrase matches (higher weight)
            for keyword in capability.keywords:
                if f" {keyword.lower()} " in f" {request_lower} ":
                    score += 2.0
            
            # Normalize score
            if capability.keywords:
                agent_scores[agent_type] = score / len(capability.keywords)
        
        return agent_scores
    
    def _determine_primary_agent(self, agent_scores: Dict[AgentType, float]) -> AgentType:
        """Determine the primary agent based on scores"""
        if not agent_scores:
            return AgentType.ISM  # Default fallback
        
        # Find agent with highest score
        primary_agent = max(agent_scores.items(), key=lambda x: x[1])[0]
        
        # If no clear winner, default to INVESTOR_SUMMARY
        if agent_scores[primary_agent] < 0.1:
            return AgentType.INVESTOR_SUMMARY
        
        return primary_agent
    
    def _determine_secondary_agents(
        self, 
        agent_scores: Dict[AgentType, float], 
        primary_agent: AgentType
    ) -> List[AgentType]:
        """Determine secondary agents for multi-agent workflows"""
        secondary_agents = []
        
        for agent_type, score in agent_scores.items():
            if agent_type != primary_agent and score > 0.3:
                secondary_agents.append(agent_type)
        
        return secondary_agents
    
    def _decompose_task(
        self, 
        user_request: str, 
        primary_agent: AgentType,
        secondary_agents: List[AgentType]
    ) -> List[Dict[str, Any]]:
        """Decompose the task into sub-tasks for different agents"""
        tasks = []
        
        # Primary agent task
        primary_capability = self.agent_capabilities[primary_agent]
        tasks.append({
            "agent_type": primary_agent,
            "task_type": TaskType.DOCUMENT_GENERATION,
            "priority": "high",
            "description": f"Generate {primary_capability.description.lower()}",
            "required_fields": primary_capability.required_fields,
            "optional_fields": primary_capability.optional_fields
        })
        
        # Secondary agent tasks
        for agent_type in secondary_agents:
            capability = self.agent_capabilities[agent_type]
            tasks.append({
                "agent_type": agent_type,
                "task_type": TaskType.DOCUMENT_GENERATION,
                "priority": "medium",
                "description": f"Generate {capability.description.lower()}",
                "required_fields": capability.required_fields,
                "optional_fields": capability.optional_fields
            })
        
        return tasks
    
    def _calculate_confidence(
        self, 
        agent_scores: Dict[AgentType, float], 
        extracted_info: ExtractedInformation
    ) -> float:
        """Calculate confidence score for the routing decision"""
        # Base confidence from agent scores
        max_score = max(agent_scores.values()) if agent_scores else 0.0
        base_confidence = min(max_score * 2, 1.0)  # Scale to 0-1
        
        # Boost confidence if we extracted key information
        info_boost = 0.0
        if extracted_info.issuer:
            info_boost += 0.1
        if extracted_info.product_name:
            info_boost += 0.1
        if extracted_info.underlying_asset:
            info_boost += 0.1
        if extracted_info.currency:
            info_boost += 0.05
        if extracted_info.principal_amount:
            info_boost += 0.05
        
        confidence = min(base_confidence + info_boost, 1.0)
        return confidence
    
    def _generate_reasoning(
        self, 
        agent_scores: Dict[AgentType, float], 
        primary_agent: AgentType,
        extracted_info: ExtractedInformation
    ) -> str:
        """Generate reasoning for the routing decision"""
        reasoning_parts = []
        
        # Explain primary agent selection
        primary_score = agent_scores.get(primary_agent, 0.0)
        reasoning_parts.append(f"Selected {primary_agent.value.upper()} as primary agent (confidence: {primary_score:.2f})")
        
        # Explain extracted information
        if extracted_info.issuer:
            reasoning_parts.append(f"Detected issuer: {extracted_info.issuer}")
        if extracted_info.product_name:
            reasoning_parts.append(f"Detected product: {extracted_info.product_name}")
        if extracted_info.underlying_asset:
            reasoning_parts.append(f"Detected underlying: {extracted_info.underlying_asset}")
        
        # Explain secondary agents if any
        secondary_agents = [agent for agent, score in agent_scores.items() 
                          if agent != primary_agent and score > 0.3]
        if secondary_agents:
            reasoning_parts.append(f"Additional agents needed: {', '.join([a.value.upper() for a in secondary_agents])}")
        
        return ". ".join(reasoning_parts)
    
    def get_agent_capabilities(self) -> Dict[AgentType, AgentCapability]:
        """Get the capabilities of all available agents"""
        return self.agent_capabilities
    
    def validate_routing_decision(self, decision: RoutingDecision) -> bool:
        """Validate that a routing decision is complete and coherent"""
        if not decision.primary_agent:
            return False
        
        if decision.confidence_score < 0.1:
            return False
        
        # Check if required fields are available for primary agent
        primary_capability = self.agent_capabilities[decision.primary_agent]
        extracted_data = decision.extracted_data
        
        # Basic validation - ensure at least one required field for the chosen agent is present
        required = primary_capability.required_fields
        present_fields = sum(1 for field in required if extracted_data.get(field))
        
        return present_fields >= 1
    
    def suggest_missing_information(self, decision: RoutingDecision) -> List[str]:
        """Suggest what information might be missing for the routing decision"""
        suggestions = []
        primary_capability = self.agent_capabilities[decision.primary_agent]
        extracted_data = decision.extracted_data
        
        for field in primary_capability.required_fields:
            if not extracted_data.get(field):
                suggestions.append(f"Missing required field: {field}")
        
        return suggestions
    
    def route_request(self, agent_type: str, action: str) -> Optional[Dict[str, Any]]:
        """
        Route a request to a specific agent and action.
        
        Args:
            agent_type: Type of agent to route to (ism, bsp, pds, prs)
            action: Action to perform (generate_document, etc.)
            
        Returns:
            Routing information or None if routing failed
        """
        try:
            # Validate agent type
            if agent_type not in [agent.value for agent in AgentType]:
                logger.warning(f"Unknown agent type: {agent_type}")
                return None
            
            # Get agent capability
            agent_enum = AgentType(agent_type)
            capability = self.agent_capabilities[agent_enum]
            
            # Check if action is supported
            if action == "generate_document" and TaskType.DOCUMENT_GENERATION in capability.supported_tasks:
                return {
                    "agent_type": agent_type,
                    "action": action,
                    "capability": capability,
                    "status": "routed",
                    "supported": True
                }
            else:
                logger.warning(f"Action {action} not supported by agent {agent_type}")
                return {
                    "agent_type": agent_type,
                    "action": action,
                    "capability": capability,
                    "status": "unsupported_action",
                    "supported": False
                }
                
        except Exception as e:
            logger.error(f"Error routing request to {agent_type}: {e}")
            return None


# Global router instance
smart_router = SmartAgentRouter() 