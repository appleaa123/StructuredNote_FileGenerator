"""
ISM Agent Customization Examples

This file shows you exactly where and how to customize the ISM agent's output format,
wording, and structure to match your specific requirements.

CUSTOMIZATION METHODS:
1. Direct configuration in code (shown below)
2. Upload a sample document template (see upload_template_example)
3. Modify the instructions.py file directly
4. Create custom configuration objects

Choose the method that works best for your workflow.
"""

import asyncio
from datetime import date
from typing import Dict, Any, List
from pathlib import Path

# Import ISM components
from agents.investor_summary import ISMAgent, ISMInput, ISMConfig
from agents.investor_summary.instructions import ISMInstructions
from agents.investor_summary.document_generator import ISMDocumentGenerator


# =============================================================================
# METHOD 1: DIRECT CODE CUSTOMIZATION
# =============================================================================

def create_custom_ism_config_with_your_format():
    """
    MAIN CUSTOMIZATION METHOD: Define your exact format requirements here.
    
    This is where you input your specific document format, wording, and structure.
    Replace the examples below with your actual requirements.
    """
    
    # YOUR CUSTOM FORMAT TEMPLATES
    your_custom_templates = {
        "document_title_template": {
            "format": "[Product Name] - Investor Information Document",  # ← CHANGE THIS
            "max_length": "100",  # ← CHANGE THIS
            "example": "S&P 500 Linked Note - Investor Information Document"
        },
        "risk_level_template": {
            "format": "Investment Risk: [HIGH/MEDIUM/LOW] | [explanation]",  # ← CHANGE THIS
            "sentence_1": "Risk level determined by market exposure",
            "sentence_2": "Potential for significant gains or losses"
        },
        "bullet_point_template": {
            "format": "→ [Feature Name]: [Description] ([Impact])",  # ← CHANGE THIS
            "word_count": "20-30 words",  # ← CHANGE THIS
            "focus": "clear benefits and risks"
        },
        "scenario_template": {
            "best_case": "Optimistic scenario: [condition] → [X]% gain (${amount})",  # ← CHANGE THIS
            "expected_case": "Base case: [condition] → [Y]% return (${amount})",  # ← CHANGE THIS
            "worst_case": "Risk scenario: [condition] → [Z]% loss (${amount})"  # ← CHANGE THIS
        }
    }
    
    # YOUR MANDATORY PHRASES (these MUST appear exactly as written)
    your_mandatory_phrases = {
        "risk_warnings": [
            "Capital at risk - you may lose some or all of your investment",  # ← CHANGE THIS
            "Past performance is not a guide to future performance",  # ← CHANGE THIS
            "The value of investments can go down as well as up"  # ← CHANGE THIS
        ],
        "suitability_notices": [
            "This product may not be suitable for all investors",  # ← CHANGE THIS
            "Please ensure you understand the risks before investing"  # ← CHANGE THIS
        ],
        "advice_disclaimers": [
            "Seek independent financial advice if you are unsure",  # ← CHANGE THIS
            "This is not personal investment advice",  # ← CHANGE THIS
            "This document is for information purposes only"  # ← CHANGE THIS
        ],
        "section_endings": [
            "To summarize:",  # ← CHANGE THIS (replaces "In summary,")
        ],
        # ADD YOUR OWN CUSTOM CATEGORIES
        "your_company_disclaimers": [
            "This document is issued by [Your Company Name]",  # ← ADD YOUR COMPANY INFO
            "Regulated by [Your Regulator]",  # ← ADD YOUR REGULATORY INFO
            "For more information visit [your-website.com]"  # ← ADD YOUR WEBSITE
        ]
    }
    
    # YOUR STRUCTURE REQUIREMENTS
    your_structure_requirements = {
        "executive_summary": {
            "paragraph_count": 4,  # ← CHANGE THIS (was 3)
            "paragraph_1": "Investment name and type",
            "paragraph_2": "Key mechanism and underlying asset",
            "paragraph_3": "Target returns and main risks",
            "paragraph_4": "Suitability and next steps",  # ← ADDED NEW PARAGRAPH
            "mandatory_ending": "This product may not be suitable for all investors."
        },
        "key_features": {
            "bullet_count": 5,  # ← CHANGE THIS (was 3)
            "words_per_bullet": {"min": 20, "max": 30},  # ← CHANGE THIS
            "format": "→ [Feature Name]: [Description] ([Impact])"
        },
        "key_risks": {
            "risk_count": 6,  # ← CHANGE THIS (was 4)
            "words_per_risk": {"min": 20, "max": 35},  # ← CHANGE THIS
            "required_types": [
                "market_risk", 
                "credit_risk", 
                "liquidity_risk", 
                "product_specific_risk",
                "currency_risk",  # ← ADDED NEW RISK TYPE
                "regulatory_risk"  # ← ADDED NEW RISK TYPE
            ]
        }
    }
    
    # CREATE CUSTOM CONFIGURATION
    custom_config = ISMConfig.create_custom_format_config(
        custom_templates=your_custom_templates,
        custom_phrases=your_mandatory_phrases,
        custom_structure=your_structure_requirements
    )
    
    # ADDITIONAL CONFIGURATION OPTIONS
    custom_config.target_reading_level = "grade_12"  # ← CHANGE THIS
    custom_config.max_document_length = 8000  # ← CHANGE THIS
    custom_config.tone = "formal_professional"  # ← CHANGE THIS
    custom_config.technical_level = "moderate"  # ← CHANGE THIS
    
    return custom_config


# =============================================================================
# METHOD 2: SAMPLE DOCUMENT TEMPLATE UPLOAD
# =============================================================================

def upload_and_parse_template_document(template_file_path: str):
    """
    Upload a sample document and extract format requirements from it.
    
    Args:
        template_file_path: Path to your sample document (.docx, .pdf, or .txt)
    
    Usage:
        1. Create a sample document with your desired format
        2. Save it as a file
        3. Call this function with the file path
        4. The function will extract format patterns and create a config
    """
    
    # This is a template - you would implement actual file parsing
    print(f"Analyzing template document: {template_file_path}")
    
    # EXAMPLE: If you upload a document with this structure:
    template_analysis = {
        "detected_title_format": "Investment Summary: [Product] ([Asset])",
        "detected_risk_format": "Risk Rating: [LEVEL] - [explanation]",
        "detected_bullet_style": "• [item]",
        "detected_mandatory_phrases": [
            "This investment carries significant risk",
            "Consult your advisor before investing"
        ],
        "detected_section_order": [
            "Executive Summary",
            "Product Overview", 
            "Investment Details",
            "Risk Information",
            "Important Information"
        ]
    }
    
    # Convert analysis to configuration
    extracted_config = ISMConfig()
    
    # Apply detected patterns
    extracted_config.format_templates["document_title_template"]["format"] = template_analysis["detected_title_format"]
    extracted_config.mandatory_phrases["risk_warnings"] = template_analysis["detected_mandatory_phrases"]
    
    return extracted_config


# =============================================================================
# METHOD 3: CUSTOM INSTRUCTIONS CLASS
# =============================================================================

class YourCustomISMInstructions(ISMInstructions):
    """
    Extend the base instructions with your specific requirements.
    This gives you complete control over the agent's behavior.
    """
    
    def get_base_instructions(self) -> str:
        """Override with your custom instructions"""
        return """
        You are creating investor summary documents with the following EXACT requirements:
        
        ## YOUR CUSTOM FORMAT RULES:
        
        **Document Structure:**
        1. Title: Must use format "Investment Summary: [Product] ([Underlying])"
        2. Executive Summary: Exactly 4 paragraphs, each 2-3 sentences
        3. Key Features: Exactly 5 bullet points using "→" symbol
        4. Risk Assessment: Must include 6 specific risk categories
        5. Financial Projections: 3 scenarios with probability estimates
        
        **Mandatory Language:**
        - All risk statements must start with "Risk:"
        - All scenarios must include probability percentages
        - Every section must end with a summary sentence
        - Must use "Capital at risk" instead of "investment risk"
        
        **Formatting Standards:**
        - Use British English spelling (e.g., "realise" not "realize")
        - All percentages rounded to 1 decimal place
        - Currency amounts with commas (e.g., £100,000)
        - Dates in DD/MM/YYYY format
        
        **YOUR COMPANY SPECIFIC REQUIREMENTS:**
        - Include company logo placeholder: [LOGO]
        - Include regulatory reference: "Authorised by [Regulator]"
        - Include risk scale: "Risk Level 1-10: [X]"
        - Include contact details in footer
        
        ## ADD YOUR SPECIFIC INSTRUCTIONS HERE:
        [Replace this section with your detailed requirements]
        """
    
    def get_your_custom_section_requirements(self) -> Dict[str, str]:
        """Define requirements for each section"""
        return {
            "executive_summary": """
            Paragraph 1: What is this investment? (25-30 words)
            Paragraph 2: How does it work? (30-35 words) 
            Paragraph 3: What are the returns? (25-30 words)
            Paragraph 4: Who is it for? (20-25 words)
            Must end with: "Capital at risk. Seek advice if unsure."
            """,
            
            "key_features": """
            → Feature 1: [Investment mechanism] (highlight main benefit)
            → Feature 2: [Return potential] (specific percentage or range)
            → Feature 3: [Risk protection] (what safeguards exist)
            → Feature 4: [Liquidity terms] (when can you exit)
            → Feature 5: [Costs and fees] (transparent fee disclosure)
            Each bullet: 25-30 words exactly.
            """,
            
            "risk_assessment": """
            Risk Level: [1-10 scale] - [one sentence explanation]
            
            Risk: Market Risk - [specific to underlying asset]
            Risk: Credit Risk - [issuer-specific concerns]
            Risk: Liquidity Risk - [exit limitations]
            Risk: Product Risk - [structure-specific risks]
            Risk: Currency Risk - [if applicable]
            Risk: Regulatory Risk - [regulatory changes]
            
            Each risk: 20-30 words with concrete example.
            """
        }


# =============================================================================
# METHOD 4: RUNTIME CUSTOMIZATION
# =============================================================================

async def generate_document_with_runtime_customization():
    """
    Show how to customize the agent at runtime with specific requirements.
    """
    
    # Create base configuration
    config = ISMConfig.get_default_config()
    
    # RUNTIME CUSTOMIZATION: Modify specific aspects
    config = config.customize_format_template(
        "document_title_template",
        {
            "format": "INVESTMENT FACT SHEET: [Product Name]",  # ← YOUR FORMAT
            "max_length": "60",
            "style": "uppercase_headers"
        }
    )
    
    # Add your mandatory phrases
    config = config.add_mandatory_phrase(
        "risk_warnings", 
        "This product is not covered by the Financial Services Compensation Scheme"  # ← YOUR PHRASE
    )
    
    # Create agent with custom configuration
    agent = ISMAgent(config=config)
    
    # You can also use custom instructions
    agent.instructions = YourCustomISMInstructions()
    
    # Create input data
    input_data = ISMInput(
        issuer="Your Bank Name",
        product_name="FTSE 100 Autocallable Note",
        underlying_asset="FTSE 100 Index",
        currency="GBP",
        principal_amount=50000.00,
        issue_date=date(2024, 3, 1),
        maturity_date=date(2029, 3, 1),
        product_type="autocallable",
        barrier_level=65.0,
        coupon_rate=7.5,
        autocall_barrier=100.0,
        target_audience="high_net_worth",
        risk_tolerance="medium",
        investment_objective="income_generation",
        regulatory_jurisdiction="UK",
        distribution_method="private_banking"
    )
    
    # Generate document
    result = await agent.generate_document(input_data)
    
    return result


# =============================================================================
# METHOD 5: CONFIGURATION FROM EXTERNAL FILE
# =============================================================================

def load_format_from_json_file(config_file_path: str) -> ISMConfig:
    """
    Load format requirements from a JSON configuration file.
    
    Create a JSON file with your format requirements like this:
    
    {
        "document_title_format": "[Product] Investment Summary - [Date]",
        "mandatory_phrases": {
            "risk_warnings": ["Your custom risk warning here"],
            "disclaimers": ["Your custom disclaimer here"]
        },
        "structure_requirements": {
            "executive_summary_paragraphs": 3,
            "key_features_count": 4,
            "risk_count": 5
        },
        "company_information": {
            "name": "Your Company Ltd",
            "regulator": "FCA",
            "website": "www.yourcompany.com",
            "phone": "+44 20 1234 5678"
        }
    }
    """
    
    import json
    
    # Load your configuration file
    with open(config_file_path, 'r') as f:
        your_config_data = json.load(f)
    
    # Convert to ISM configuration
    config = ISMConfig()
    
    # Apply your settings
    if "document_title_format" in your_config_data:
        config.format_templates["document_title_template"]["format"] = your_config_data["document_title_format"]
    
    if "mandatory_phrases" in your_config_data:
        for category, phrases in your_config_data["mandatory_phrases"].items():
            config.mandatory_phrases[category] = phrases
    
    # Add company-specific information
    if "company_information" in your_config_data:
        company_info = your_config_data["company_information"]
        config.mandatory_phrases["company_info"] = [
            f"Issued by {company_info['name']}",
            f"Regulated by {company_info['regulator']}",
            f"Contact: {company_info['phone']}",
            f"Website: {company_info['website']}"
        ]
    
    return config


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

async def example_1_basic_customization():
    """Example 1: Basic format customization"""
    
    print("=== Example 1: Basic Customization ===")
    
    # Create custom configuration
    config = create_custom_ism_config_with_your_format()
    
    # Create agent
    agent = ISMAgent(config=config)
    
    # Create sample input
    input_data = ISMInput(
        issuer="Example Bank",
        product_name="S&P 500 Auto-Call Note",
        underlying_asset="S&P 500 Index",
        currency="USD",
        principal_amount=100000.00,
        issue_date=date(2024, 6, 1),
        maturity_date=date(2027, 6, 1),
        product_type="autocallable",
        barrier_level=60.0,
        coupon_rate=8.0,
        risk_tolerance="medium",
        investment_objective="capital_growth",
        regulatory_jurisdiction="US",
        distribution_method="private_placement"
    )
    
    # Generate document
    result = await agent.generate_document(input_data)
    
    print(f"Document title: {result.document_title}")
    print(f"Risk level: {result.risk_level_indicator}")
    print(f"Key features count: {len(result.key_features)}")
    
    return result


async def example_2_document_generation():
    """Example 2: Generate actual document file"""
    
    print("=== Example 2: Document Generation ===")
    
    # Use runtime customization
    result = await generate_document_with_runtime_customization()
    
    # Create document generator
    doc_generator = ISMDocumentGenerator()
    
    # Generate DOCX file
    input_data = ISMInput(
        issuer="Your Bank",
        product_name="Custom Product",
        underlying_asset="FTSE 100",
        currency="GBP",
        principal_amount=50000,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
        product_type="autocallable",
        risk_tolerance="medium",
        investment_objective="income",
        regulatory_jurisdiction="UK",
        distribution_method="retail"
    )
    
    # Create document
    file_path = doc_generator.create_docx_document(
        ism_output=result,
        input_data=input_data,
        filename="custom_formatted_document.docx"
    )
    
    print(f"Document saved to: {file_path}")
    
    return file_path


def example_3_json_configuration():
    """Example 3: Load configuration from JSON file"""
    
    print("=== Example 3: JSON Configuration ===")
    
    # Create sample JSON configuration
    sample_config = {
        "document_title_format": "INVESTMENT FACTSHEET: [Product] ([Asset])",
        "mandatory_phrases": {
            "risk_warnings": [
                "Capital at risk - you may lose money",
                "Past performance does not predict future returns"
            ],
            "company_disclaimers": [
                "This document is issued by Your Company Ltd",
                "Authorised and regulated by the FCA"
            ]
        },
        "structure_requirements": {
            "executive_summary_paragraphs": 4,
            "key_features_count": 5,
            "risk_count": 6
        },
        "company_information": {
            "name": "Your Investment Company Ltd",
            "regulator": "Financial Conduct Authority",
            "website": "www.yourinvestments.com",
            "phone": "+44 20 1234 5678"
        }
    }
    
    # Save to file (you would create this file with your actual settings)
    import json
    config_file = "your_ism_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    # Load configuration
    config = load_format_from_json_file(config_file)
    
    print("Configuration loaded successfully!")
    print(f"Document title format: {config.format_templates['document_title_template']['format']}")
    print(f"Risk warnings: {config.mandatory_phrases['risk_warnings']}")
    
    return config


# =============================================================================
# HOW TO USE THIS FILE
# =============================================================================

if __name__ == "__main__":
    print("""
    ISM AGENT CUSTOMIZATION GUIDE
    =============================
    
    To customize your ISM agent output:
    
    1. DIRECT CUSTOMIZATION (Recommended):
       - Edit the create_custom_ism_config_with_your_format() function above
       - Replace all the example templates with your exact requirements
       - Run: python ism_customization_examples.py
    
    2. JSON FILE CONFIGURATION:
       - Create a JSON file with your format requirements
       - Use the load_format_from_json_file() function
       - Easier to maintain and share
    
    3. UPLOAD SAMPLE DOCUMENT:
       - Create a sample document with your desired format
       - Use upload_and_parse_template_document() to extract patterns
       - Best for complex formatting requirements
    
    4. CUSTOM INSTRUCTIONS CLASS:
       - Extend YourCustomISMInstructions class
       - Complete control over agent behavior
       - Best for advanced customization
    
    Choose the method that works best for your needs!
    """)
    
    # Run examples
    async def run_examples():
        # Example 1: Basic customization
        result1 = await example_1_basic_customization()
        
        # Example 2: Generate document
        file_path = await example_2_document_generation()
        
        # Example 3: JSON configuration
        config3 = example_3_json_configuration()
        
        print("\nAll examples completed successfully!")
        print(f"Check the generated document at: {file_path}")
    
    # Uncomment to run examples
    # asyncio.run(run_examples())