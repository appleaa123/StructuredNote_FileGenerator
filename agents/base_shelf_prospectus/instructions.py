"""
Instructions and prompts for the BSP (Base Shelf Prospectus) agent.

This module contains comprehensive instructions for generating base shelf prospectus
documents for structured notes programs, following regulatory requirements and
best practices for legal document generation.
"""

from typing import Dict, List


class BSPInstructions:
    """
    Contains all instruction templates and prompts for the BSP agent.
    
    Provides comprehensive guidance for generating base shelf prospectus documents
    that meet regulatory requirements and serve as the foundation for multiple
    structured note issuances.
    """
    
    def get_base_instructions(self) -> str:
        """Base system instructions for BSP agent"""
        return """
        You are a specialized financial document generator focused on creating Base Shelf Prospectus 
        documents for structured notes programs. Your role is to create comprehensive legal documents 
        that serve as the foundation for multiple structured note issuances.

        CRITICAL REQUIREMENTS:
        1. LEGAL ACCURACY: Ensure all legal information is precise and compliant with regulatory requirements
        2. COMPREHENSIVE COVERAGE: Include all required sections for shelf registration
        3. REGULATORY COMPLIANCE: Meet all SEC and relevant regulatory requirements
        4. CLARITY: Make complex legal concepts accessible to institutional readers
        5. CONSISTENCY: Maintain consistent terminology and structure throughout
        6. COMPLETENESS: Include all mandatory disclosures and risk factors
        7. PROFESSIONAL TONE: Use formal, professional language appropriate for legal documents

        DOCUMENT STRUCTURE REQUIREMENTS:
        - Cover Page: Program title, issuer information, shelf amount, key dates
        - Executive Summary: High-level program overview and key terms
        - Issuer Information: Comprehensive business description and financial condition
        - Program Overview: Detailed program structure and capabilities
        - Risk Factors: Comprehensive risk disclosure section
        - Legal Terms: Legal structure and regulatory framework
        - Use of Proceeds: How proceeds will be used
        - Regulatory Disclosures: Required regulatory information
        - Additional Sections: Any program-specific sections

        Always use the available tools to retrieve relevant legal templates, regulatory 
        requirements, and issuer information before generating content.
        """
    
    def get_legal_compliance_guidelines(self) -> str:
        """Get guidelines for legal compliance and regulatory requirements"""
        return """
        LEGAL COMPLIANCE REQUIREMENTS:
        
        1. SEC COMPLIANCE:
           - Include all required SEC disclosures
           - Follow Regulation S-K requirements
           - Include proper risk factor disclosure
           - Maintain accurate financial information
        
        2. REGULATORY DISCLOSURES:
           - Material information disclosure
           - Risk factor identification
           - Legal structure description
           - Regulatory jurisdiction compliance
        
        3. MANDATORY SECTIONS:
           - Cover page with program details
           - Issuer business description
           - Program structure and terms
           - Comprehensive risk factors
           - Legal terms and conditions
           - Use of proceeds
           - Regulatory framework
        
        4. LANGUAGE REQUIREMENTS:
           - Formal legal language
           - Precise terminology
           - Clear risk disclosure
           - Professional tone throughout
        """
    
    def get_program_structure_guidelines(self) -> str:
        """Get guidelines for describing program structure and capabilities"""
        return """
        PROGRAM STRUCTURE REQUIREMENTS:
        
        1. PROGRAM OVERVIEW:
           - Clear description of program purpose
           - Shelf registration details
           - Issuance authority and limits
           - Program duration and renewal
        
        2. NOTE TYPES:
           - Autocallable notes
           - Barrier notes
           - Reverse convertible notes
           - Other structured products
           - Custom note types
        
        3. DISTRIBUTION METHODS:
           - Broker-dealer networks
           - Private placements
           - Direct institutional sales
           - Retail distribution channels
        
        4. REGULATORY FRAMEWORK:
           - Securities law compliance
           - Regulatory jurisdiction
           - Ongoing disclosure requirements
           - Compliance monitoring
        """
    
    def get_risk_factor_guidelines(self) -> str:
        """Get guidelines for comprehensive risk factor disclosure"""
        return """
        RISK FACTOR REQUIREMENTS:
        
        1. MARKET RISKS:
           - General market risk
           - Interest rate risk
           - Currency risk
           - Volatility risk
        
        2. CREDIT RISKS:
           - Issuer credit risk
           - Counterparty risk
           - Credit rating changes
           - Default risk
        
        3. PRODUCT-SPECIFIC RISKS:
           - Structured product complexity
           - Underlying asset risk
           - Liquidity risk
           - Early termination risk
        
        4. REGULATORY RISKS:
           - Regulatory changes
           - Compliance risk
           - Legal framework changes
           - Jurisdictional risk
        
        5. OPERATIONAL RISKS:
           - Technology risk
           - Operational risk
           - Settlement risk
           - Documentation risk
        """
    
    def get_issuer_information_guidelines(self) -> str:
        """Get guidelines for comprehensive issuer information"""
        return """
        ISSUER INFORMATION REQUIREMENTS:
        
        1. BUSINESS DESCRIPTION:
           - Company overview
           - Business segments
           - Market position
           - Competitive advantages
        
        2. FINANCIAL CONDITION:
           - Financial highlights
           - Key financial metrics
           - Credit ratings
           - Financial strength
        
        3. REGULATORY STATUS:
           - Regulatory licenses
           - Compliance record
           - Regulatory oversight
           - Legal structure
        
        4. MANAGEMENT:
           - Key personnel
           - Experience and qualifications
           - Governance structure
           - Risk management
        """
    
    def get_formatting_guidelines(self) -> Dict[str, str]:
        """Get specific formatting requirements for BSP documents"""
        return {
            "document_title": "Format: '[Program Name] - Base Shelf Prospectus'",
            "cover_page": "Include: Program name, issuer, shelf amount, key dates, regulatory information",
            "executive_summary": "3-4 paragraphs: Program overview, key terms, regulatory framework, risk summary",
            "issuer_information": "Comprehensive business description with financial highlights and regulatory status",
            "program_overview": "Detailed program structure, note types, distribution methods, regulatory framework",
            "risk_factors": "Comprehensive risk disclosure with clear categorization and detailed explanations",
            "legal_terms": "Legal structure, regulatory compliance, governing law, dispute resolution",
            "use_of_proceeds": "Clear description of how proceeds will be used with specific categories",
            "regulatory_disclosures": "Required regulatory information, compliance status, ongoing obligations"
        }
    
    def get_regulatory_templates(self) -> Dict[str, str]:
        """Get regulatory templates for different jurisdictions"""
        return {
            "SEC": {
                "disclaimer": "This prospectus contains important information about the program. No securities regulatory authority has passed upon the merits of the securities.",
                "risk_warning": "Investing in structured notes involves substantial risk of loss. Past performance does not guarantee future results.",
                "compliance_notice": "This program complies with all applicable SEC regulations and ongoing disclosure requirements."
            },
            "Canada": {
                "disclaimer": "This prospectus contains important information about the program. No securities regulatory authority has passed upon the merits of the securities.",
                "risk_warning": "Investing in structured notes involves substantial risk of loss. Past performance does not guarantee future results.",
                "compliance_notice": "This program complies with all applicable Canadian securities laws and ongoing disclosure requirements."
            },
            "EU": {
                "disclaimer": "This prospectus contains important information about the program. No securities regulatory authority has passed upon the merits of the securities.",
                "risk_warning": "Investing in structured notes involves substantial risk of loss. Past performance does not guarantee future results.",
                "compliance_notice": "This program complies with all applicable EU regulations and ongoing disclosure requirements."
            }
        }
    
    def get_program_type_instructions(self, program_type: str) -> str:
        """Get program-specific instructions based on program type"""
        instructions = {
            "general": """
            GENERAL STRUCTURED NOTES PROGRAM:
            
            This program allows for the issuance of various types of structured notes including:
            - Autocallable notes with periodic observation dates
            - Barrier notes with contingent protection
            - Reverse convertible notes with enhanced yield
            - Custom structured products tailored to specific needs
            
            The program provides flexibility to issue notes with different underlying assets,
            risk profiles, and return structures to meet diverse investor needs.
            """,
            
            "autocallable_focused": """
            AUTOCALLABLE-FOCUSED PROGRAM:
            
            This program specializes in autocallable structured notes with features including:
            - Periodic autocall observation dates
            - Contingent coupon payments
            - Principal protection at maturity
            - Enhanced yield potential
            
            Notes may be called early if the underlying asset performs well, providing
            investors with potential early returns and income generation.
            """,
            
            "barrier_focused": """
            BARRIER-FOCUSED PROGRAM:
            
            This program specializes in barrier-structured notes with features including:
            - Contingent principal protection
            - Downside participation
            - Enhanced yield potential
            - Risk-defined payoffs
            
            Notes provide protection against moderate declines while offering enhanced
            yield potential compared to traditional fixed income products.
            """,
            
            "institutional": """
            INSTITUTIONAL-FOCUSED PROGRAM:
            
            This program is designed for institutional investors with features including:
            - Large denomination notes
            - Custom structured solutions
            - Institutional distribution channels
            - Sophisticated risk management
            
            The program provides institutional investors with access to structured
            products tailored to their specific investment objectives and constraints.
            """
        }
        
        return instructions.get(program_type, instructions["general"])
    
    def get_audience_specific_instructions(self, audience: str) -> str:
        """Get audience-specific instructions for BSP documents"""
        instructions = {
            "institutional": """
            INSTITUTIONAL AUDIENCE REQUIREMENTS:
            
            - Technical depth: Advanced financial and legal concepts
            - Regulatory focus: Detailed regulatory compliance information
            - Risk metrics: Comprehensive risk analysis and quantification
            - Legal detail: Detailed legal terms and conditions
            - Professional language: Formal, technical language appropriate for professionals
            """,
            
            "retail": """
            RETAIL AUDIENCE REQUIREMENTS:
            
            - Simplified language: Clear, accessible explanations
            - Basic education: Include fundamental concepts
            - Practical implications: Focus on investor impact
            - Risk warnings: Prominent risk disclosure
            - Professional but accessible: Clear language while maintaining legal accuracy
            """,
            
            "regulatory": """
            REGULATORY AUDIENCE REQUIREMENTS:
            
            - Compliance focus: Detailed regulatory compliance information
            - Legal accuracy: Precise legal language and citations
            - Regulatory framework: Comprehensive regulatory context
            - Documentation: Complete legal and regulatory documentation
            - Formal language: Strict legal and regulatory language
            """
        }
        
        return instructions.get(audience, instructions["institutional"])
    
    def get_section_formatting_requirements(self) -> Dict[str, str]:
        """Get detailed formatting requirements for each section"""
        return {
            "document_title": "Format: '[Program Name] - Base Shelf Prospectus'. Must be clear and professional.",
            "cover_page": "Include program name, issuer, shelf amount, key dates, regulatory information in structured format.",
            "executive_summary": "3-4 paragraphs: (1) Program overview and purpose, (2) Key terms and structure, (3) Regulatory framework, (4) Risk summary.",
            "issuer_information": "Comprehensive business description with financial highlights, regulatory status, and management information.",
            "program_overview": "Detailed program structure, note types, distribution methods, regulatory framework, and operational details.",
            "risk_factors": "Comprehensive risk disclosure with clear categorization: Market, Credit, Product-specific, Regulatory, Operational risks.",
            "legal_terms": "Legal structure, regulatory compliance, governing law, dispute resolution, and legal framework.",
            "use_of_proceeds": "Clear description of how proceeds will be used with specific categories and percentages where applicable.",
            "regulatory_disclosures": "Required regulatory information, compliance status, ongoing obligations, and regulatory framework."
        }
    
    def get_mandatory_compliance_text(self, jurisdiction: str) -> Dict[str, str]:
        """Get mandatory compliance text for different jurisdictions"""
        compliance_text = {
            "SEC": {
                "disclaimer": "This prospectus contains important information about the program. No securities regulatory authority has passed upon the merits of the securities.",
                "risk_warning": "Investing in structured notes involves substantial risk of loss. Past performance does not guarantee future results.",
                "compliance_notice": "This program complies with all applicable SEC regulations and ongoing disclosure requirements.",
                "legal_notice": "This document does not constitute an offer to sell or a solicitation of an offer to buy any securities."
            },
            "Canada": {
                "disclaimer": "This prospectus contains important information about the program. No securities regulatory authority has passed upon the merits of the securities.",
                "risk_warning": "Investing in structured notes involves substantial risk of loss. Past performance does not guarantee future results.",
                "compliance_notice": "This program complies with all applicable Canadian securities laws and ongoing disclosure requirements.",
                "legal_notice": "This document does not constitute an offer to sell or a solicitation of an offer to buy any securities."
            },
            "EU": {
                "disclaimer": "This prospectus contains important information about the program. No securities regulatory authority has passed upon the merits of the securities.",
                "risk_warning": "Investing in structured notes involves substantial risk of loss. Past performance does not guarantee future results.",
                "compliance_notice": "This program complies with all applicable EU regulations and ongoing disclosure requirements.",
                "legal_notice": "This document does not constitute an offer to sell or a solicitation of an offer to buy any securities."
            }
        }
        
        return compliance_text.get(jurisdiction, compliance_text["SEC"])