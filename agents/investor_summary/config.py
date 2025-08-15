"""
Configuration settings for the ISM (Investor Summary) agent.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class ISMConfig(BaseModel):
    """
    Configuration settings specific to the ISM agent.
    
    This configuration controls various aspects of ISM document generation
    including content preferences, formatting options, and compliance settings.
    """
    
    # Document Generation Settings
    max_document_length: int = Field(default=6000, description="Maximum document length in words")
    target_reading_level: str = Field(default="grade_10", description="Target reading level for content")
    include_executive_summary: bool = Field(default=True, description="Whether to include executive summary")
    include_scenarios: bool = Field(default=True, description="Whether to include scenario analysis")
    include_risk_matrix: bool = Field(default=True, description="Whether to include risk assessment matrix")
    
    # Content Preferences
    use_bullet_points: bool = Field(default=True, description="Use bullet points for key features")
    include_examples: bool = Field(default=True, description="Include concrete numerical examples")
    include_analogies: bool = Field(default=True, description="Use analogies for complex concepts")
    emphasize_risks: bool = Field(default=True, description="Emphasize risk information prominently")
    
    # Language and Style Settings
    tone: str = Field(default="professional_friendly", description="Overall tone of the document")
    technical_level: str = Field(default="accessible", description="Level of technical detail")
    sentence_length_target: int = Field(default=20, description="Target maximum sentence length")
    paragraph_length_target: int = Field(default=4, description="Target maximum sentences per paragraph")
    
    # Regulatory and Compliance Settings
    include_disclaimers: bool = Field(default=True, description="Include regulatory disclaimers")
    include_regulatory_warnings: bool = Field(default=True, description="Include mandatory warnings")
    include_suitability_assessment: bool = Field(default=True, description="Include investor suitability section")
    include_tax_considerations: bool = Field(default=True, description="Include basic tax information")
    
    # Output Format Settings
    output_format: str = Field(default="structured", description="Output format: structured, narrative, or hybrid")
    include_table_of_contents: bool = Field(default=False, description="Include table of contents")
    include_glossary: bool = Field(default=True, description="Include glossary of terms")
    include_contact_info: bool = Field(default=True, description="Include contact information section")
    
    # Risk Assessment Settings
    risk_categories: List[str] = Field(
        default=["market_risk", "credit_risk", "liquidity_risk", "product_specific_risk"],
        description="Categories of risk to assess"
    )
    risk_scoring_method: str = Field(default="qualitative", description="Risk scoring approach")
    include_risk_timeline: bool = Field(default=True, description="Include risk timeline analysis")
    
    # Scenario Analysis Settings
    scenario_types: List[str] = Field(
        default=["optimistic", "base_case", "stress", "extreme"],
        description="Types of scenarios to include"
    )
    include_historical_context: bool = Field(default=True, description="Include historical performance context")
    scenario_probability_estimates: bool = Field(default=True, description="Include probability estimates")
    
    # Audience-Specific Settings
    audience_customization: Dict[str, Dict[str, Any]] = Field(
        default={
            "retail_investors": {
                "simplify_language": True,
                "include_basic_education": True,
                "emphasize_practical_implications": True,
                "detailed_risk_warnings": True
            },
            "high_net_worth": {
                "technical_depth": "moderate",
                "portfolio_context": True,
                "tax_optimization_focus": True,
                "alternative_comparisons": True
            },
            "institutional": {
                "technical_depth": "advanced",
                "regulatory_focus": True,
                "risk_metrics": "comprehensive",
                "benchmark_comparisons": True
            }
        },
        description="Audience-specific customization settings"
    )
    
    # Knowledge Retrieval Settings
    knowledge_retrieval: Dict[str, Any] = Field(
        default={
            "max_query_results": 10,
            "query_modes": ["mix", "local", "global"],
            "relevance_threshold": 0.7,
            "cross_reference_domains": ["bsp", "pds", "prs"],
            "template_priority": ["product_specific", "general", "regulatory"]
        },
        description="Settings for knowledge base queries"
    )
    
    # Quality Control Settings
    quality_checks: Dict[str, bool] = Field(
        default={
            "fact_verification": True,
            "consistency_check": True,
            "completeness_check": True,
            "readability_check": True,
            "compliance_check": True
        },
        description="Quality control checks to perform"
    )
    
    # Custom Format Templates
    format_templates: Dict[str, Dict[str, str]] = Field(
        default={
            "document_title_template": {
                "format": "[Product Type] Investment Summary - [Underlying Asset]",
                "max_length": "80",
                "example": "Autocallable Investment Summary - S&P 500 Index"
            },
            "risk_level_template": {
                "format": "Risk Level: [HIGH/MEDIUM/LOW] - [2-sentence explanation]",
                "sentence_1": "Explains why this risk level",
                "sentence_2": "Explains what this means for investor"
            },
            "bullet_point_template": {
                "format": "• [Feature]: [Benefit] - [Impact explanation]",
                "word_count": "15-25 words",
                "focus": "investor benefits"
            },
            "risk_item_template": {
                "format": "Risk: [Risk Name] - [Plain language explanation with example]",
                "word_count": "15-30 words",
                "required_count": "4"
            },
            "scenario_template": {
                "best_case": "[Condition] could result in [X]% return ([dollar amount])",
                "expected_case": "[Condition] would likely result in [Y]% return ([dollar amount])",
                "worst_case": "[Condition] could result in [Z]% loss ([dollar amount])"
            }
        },
        description="Customizable format templates for document sections"
    )
    
    # Mandatory Wording Requirements
    mandatory_phrases: Dict[str, List[str]] = Field(
        default={
            "risk_warnings": [
                "All investments carry risk of loss",
                "You may lose some or all of your investment",
                "Past performance does not guarantee future results"
            ],
            "suitability_notices": [
                "This investment may not be suitable for all investors",
                "Please consider your investment objectives, risk tolerance, and financial situation"
            ],
            "advice_disclaimers": [
                "Please consult your financial advisor before investing",
                "This document does not constitute investment advice",
                "This summary is for informational purposes only"
            ],
            "section_endings": [
                "In summary,",  # Required at end of certain sections
            ]
        },
        description="Mandatory phrases that must appear exactly as specified"
    )
    
    # Word Count and Structure Requirements
    structure_requirements: Dict[str, Dict[str, Any]] = Field(
        default={
            "executive_summary": {
                "paragraph_count": 3,
                "paragraph_1": "What this investment is (1-2 sentences)",
                "paragraph_2": "How it works and key terms (2-3 sentences)",
                "paragraph_3": "Target investors and main risks (2-3 sentences)",
                "mandatory_ending": "This investment may not be suitable for all investors."
            },
            "key_features": {
                "bullet_count": 3,
                "words_per_bullet": {"min": 15, "max": 25},
                "format": "• [Feature]: [Benefit] - [Impact explanation]"
            },
            "key_risks": {
                "risk_count": 4,
                "words_per_risk": {"min": 15, "max": 30},
                "required_types": ["market_risk", "credit_risk", "liquidity_risk", "product_specific_risk"]
            },
            "potential_returns": {
                "scenario_count": 3,
                "scenario_types": ["best_case", "expected_case", "worst_case"],
                "include_dollar_amounts": True,
                "include_probabilities": True
            }
        },
        description="Detailed structure requirements for each section"
    )
    
    @classmethod
    def get_default_config(cls) -> "ISMConfig":
        """Get default configuration for ISM agent"""
        return cls()
    
    @classmethod
    def get_retail_optimized_config(cls) -> "ISMConfig":
        """Get configuration optimized for retail investors"""
        config = cls()
        config.target_reading_level = "grade_8"
        config.include_analogies = True
        config.emphasize_risks = True
        config.include_basic_education = True
        config.technical_level = "basic"
        return config
    
    @classmethod
    def get_institutional_optimized_config(cls) -> "ISMConfig":
        """Get configuration optimized for institutional investors"""
        config = cls()
        config.target_reading_level = "graduate"
        config.technical_level = "advanced"
        config.include_risk_matrix = True
        config.scenario_probability_estimates = True
        config.include_regulatory_warnings = True
        return config
    
    def customize_for_audience(self, audience: str) -> "ISMConfig":
        """
        Customize configuration for a specific audience.
        
        Args:
            audience: Target audience type
            
        Returns:
            Customized configuration
        """
        if audience in self.audience_customization:
            customizations = self.audience_customization[audience]
            
            # Create a copy of current config
            config_dict = self.model_dump()
            
            # Apply customizations
            for key, value in customizations.items():
                if key in config_dict:
                    config_dict[key] = value
            
            return ISMConfig(**config_dict)
        
        return self
    
    def get_retrieval_settings(self) -> Dict[str, Any]:
        """Get settings for knowledge retrieval operations"""
        return self.knowledge_retrieval
    
    def get_quality_settings(self) -> Dict[str, bool]:
        """Get quality control settings"""
        return self.quality_checks
    
    def validate_settings(self) -> bool:
        """
        Validate configuration settings for consistency.
        
        Returns:
            True if configuration is valid
        """
        # Check reading level consistency
        reading_levels = ["elementary", "grade_8", "grade_10", "grade_12", "college", "graduate"]
        if self.target_reading_level not in reading_levels:
            return False
        
        # Check technical level consistency
        tech_levels = ["basic", "accessible", "moderate", "advanced"]
        if self.technical_level not in tech_levels:
            return False
        
        # Check output format
        output_formats = ["structured", "narrative", "hybrid"]
        if self.output_format not in output_formats:
            return False
        
        return True
    
    def get_format_templates(self) -> Dict[str, Dict[str, str]]:
        """Get format templates for document sections"""
        return self.format_templates
    
    def get_mandatory_phrases(self) -> Dict[str, List[str]]:
        """Get mandatory phrases that must appear in documents"""
        return self.mandatory_phrases
    
    def get_structure_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get structure requirements for document sections"""
        return self.structure_requirements
    
    def customize_format_template(self, section: str, new_format: Dict[str, str]) -> "ISMConfig":
        """
        Customize format template for a specific section.
        
        Args:
            section: Section name to customize
            new_format: New format template
            
        Returns:
            Updated configuration
        """
        config_dict = self.model_dump()
        if section in config_dict["format_templates"]:
            config_dict["format_templates"][section].update(new_format)
        else:
            config_dict["format_templates"][section] = new_format
        
        return ISMConfig(**config_dict)
    
    def add_mandatory_phrase(self, category: str, phrase: str) -> "ISMConfig":
        """
        Add a mandatory phrase to a category.
        
        Args:
            category: Category to add phrase to
            phrase: Phrase to add
            
        Returns:
            Updated configuration
        """
        config_dict = self.model_dump()
        if category in config_dict["mandatory_phrases"]:
            config_dict["mandatory_phrases"][category].append(phrase)
        else:
            config_dict["mandatory_phrases"][category] = [phrase]
        
        return ISMConfig(**config_dict)
    
    @classmethod
    def create_custom_format_config(
        cls,
        custom_templates: Optional[Dict[str, Dict[str, str]]] = None,
        custom_phrases: Optional[Dict[str, List[str]]] = None,
        custom_structure: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> "ISMConfig":
        """
        Create a configuration with custom format requirements.
        
        Args:
            custom_templates: Custom format templates
            custom_phrases: Custom mandatory phrases
            custom_structure: Custom structure requirements
            
        Returns:
            Custom configuration
        """
        config = cls()
        
        if custom_templates:
            config.format_templates.update(custom_templates)
        
        if custom_phrases:
            for category, phrases in custom_phrases.items():
                if category in config.mandatory_phrases:
                    config.mandatory_phrases[category].extend(phrases)
                else:
                    config.mandatory_phrases[category] = phrases
        
        if custom_structure:
            config.structure_requirements.update(custom_structure)
        
        return config