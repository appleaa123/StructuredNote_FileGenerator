"""
Minimal Test Suite for BSP Agent

This module provides comprehensive testing for the BSP agent functionality,
including large text templates, variable substitution, and document generation.
"""

import asyncio
import json
import os
import sys
from datetime import date

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from agents.base_shelf_prospectus import BSPAgent, BSPInput, LargeTextBSPAgent
from agents.base_shelf_prospectus.large_text_templates import (
    get_template,
    customize_template,
    create_complete_document_from_templates
)


def test_large_text_templates():
    """Test large text templates functionality"""
    print("🔍 Running: Large Text Templates")
    
    try:
        # Test template retrieval for canonical BSP sections
        cover_page = get_template("cover_page_disclosures", "institutional")
        fls = get_template("forward_looking_statements", "institutional")
        dir_docs = get_template("documents_incorporated_by_reference", "institutional")
        notes_desc = get_template("description_of_the_notes", "institutional")
        pod = get_template("plan_of_distribution", "institutional")
        risks = get_template("risk_factors", "institutional")
        uop = get_template("use_of_proceeds", "institutional")
        statutory = get_template("purchasers_statutory_rights", "institutional")
        cert_bank = get_template("certificate_of_the_bank", "institutional")
        cert_dealers = get_template("certificate_of_the_dealers", "institutional")

        # Verify templates are not empty
        assert len(cover_page) > 0, "Cover page template is empty"
        assert len(fls) > 0, "Forward-looking statements template is empty"
        assert len(dir_docs) > 0, "Documents incorporated by reference template is empty"
        assert len(notes_desc) > 0, "Description of the notes template is empty"
        assert len(pod) > 0, "Plan of distribution template is empty"
        assert len(risks) > 0, "Risk factors template is empty"
        assert len(uop) > 0, "Use of proceeds template is empty"
        assert len(statutory) > 0, "Purchaser's statutory rights template is empty"
        assert len(cert_bank) > 0, "Certificate of the Bank template is empty"
        assert len(cert_dealers) > 0, "Certificate of the Dealers template is empty"

        print("✅ Large text templates test successful")

        # Count words in each section
        sections = {
            "cover_page_disclosures": len(cover_page.split()),
            "forward_looking_statements": len(fls.split()),
            "documents_incorporated_by_reference": len(dir_docs.split()),
            "description_of_the_notes": len(notes_desc.split()),
            "plan_of_distribution": len(pod.split()),
            "risk_factors": len(risks.split()),
            "use_of_proceeds": len(uop.split()),
            "purchasers_statutory_rights": len(statutory.split()),
            "certificate_of_the_bank": len(cert_bank.split()),
            "certificate_of_the_dealers": len(cert_dealers.split()),
        }

        print("📄 Generated canonical BSP sections:")
        for section, word_count in sections.items():
            print(f"   {section}: {word_count} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Large text templates test failed: {str(e)}")
        return False


def test_template_variable_substitution():
    """Test template variable substitution"""
    print("🔍 Running: Template Variable Substitution")
    
    try:
        # Sample BSP data
        sample_data = {
            "Program Name": "Structured Notes Program 2025",
            "Issuer": "Your Financial Institution Ltd",
            "Guarantor": "Not applicable",
            "Shelf Amount": "1,000,000,000",
            "Currency": "USD",
            "Regulatory Jurisdiction": "SEC",
            "Business Description": "Financial services including structured products and investment banking",
            "Document Date": "January 15, 2025",
            "Generation Date": "2025-01-15",
            "Note Types": "Autocallable notes, Barrier notes, Reverse convertible notes",
            "Distribution Methods": "Broker-dealer networks, Private placements, Direct institutional sales",
            "Additional Features": "Standard program features apply",
            "Regulatory Framework": "Compliant with SEC regulations",
            "Compliance Status": "Fully compliant with all applicable regulations",
            "Contact Phone": "1-800-STRUCTURED",
            "Contact Email": "structuredproducts@issuer.com",
            "Contact Website": "www.issuer.com/structuredproducts",
            "Legal Department": "legal@issuer.com",
            "Compliance Department": "compliance@issuer.com",
            "Document Version": "1.0",
            "Document Type": "Base Shelf Prospectus",
            "Document Status": "Draft for Review",
            "Market Risk Level": "High",
            "Credit Risk Level": "Medium",
            "Liquidity Risk Level": "Medium",
            "Regulatory Risk Level": "Low",
            "Operational Risk Level": "Low",
            "Maximum Note Size": "100,000,000 USD",
            "Minimum Note Size": "1,000,000 USD",
            "Shelf Period": "3 years from effective date",
            "Renewal Process": "Subject to regulatory approval and market conditions",
            "Primary Distribution": "Institutional investors and qualified purchasers",
            "Secondary Distribution": "Broker-dealer networks and private placements",
            "Retail Distribution": "Limited to accredited investors and qualified purchasers",
            "SEC Compliance": "Full compliance with Regulation S-K and other applicable regulations",
            "Ongoing Disclosures": "Quarterly and annual reports as required by applicable regulations",
            "Material Events": "Immediate disclosure of material events affecting the program",
            "Governing Law": "New York law",
            "Dispute Resolution": "Arbitration in accordance with FINRA rules",
            "Jurisdiction": "Federal and state courts in New York",
            "Primary Use": "General corporate purposes including funding structured products",
            "Secondary Use": "Hedging activities and risk management",
            "Tertiary Use": "Working capital and other business purposes",
            "Risk Management Framework": "Comprehensive risk management policies and procedures",
            "Credit Risk Management": "Regular credit assessments and monitoring",
            "Market Risk Management": "Dynamic hedging strategies and position limits",
            "Operational Risk Management": "Robust internal controls and monitoring systems"
        }
        
        # Test variable substitution on a canonical BSP section
        template_to_check = get_template("cover_page_disclosures", "institutional")
        customized_summary = customize_template(template_to_check, sample_data)
        
        # Verify substitution worked
        assert "[Program Name]" not in customized_summary, "Variable substitution failed for Program Name"
        assert "[Issuer]" not in customized_summary, "Variable substitution failed for Issuer"
        assert "[Shelf Amount]" not in customized_summary, "Variable substitution failed for Shelf Amount"
        assert "[Currency]" not in customized_summary, "Variable substitution failed for Currency"
        
        # Verify values were substituted
        assert "Structured Notes Program 2025" in customized_summary, "Program name not substituted"
        assert "Your Financial Institution Ltd" in customized_summary, "Issuer not substituted"
        assert "1,000,000,000" in customized_summary, "Shelf amount not substituted"
        assert "USD" in customized_summary, "Currency not substituted"
        
        print("✅ Template variable substitution successful")
        return True
        
    except Exception as e:
        print(f"❌ Template variable substitution test failed: {str(e)}")
        return False


def test_document_saving():
    """Test document saving functionality"""
    print("🔍 Running: Document Saving")
    
    try:
        # Create sample data
        sample_data = {
            "Program Name": "Structured Notes Program 2025",
            "Issuer": "Your Financial Institution Ltd",
            "Guarantor": "Not applicable",
            "Shelf Amount": "1,000,000,000",
            "Currency": "USD",
            "Regulatory Jurisdiction": "SEC",
            "Business Description": "Financial services including structured products and investment banking",
            "Document Date": "January 15, 2025",
            "Generation Date": "2025-01-15",
            "Note Types": "Autocallable notes, Barrier notes, Reverse convertible notes",
            "Distribution Methods": "Broker-dealer networks, Private placements, Direct institutional sales",
            "Additional Features": "Standard program features apply",
            "Regulatory Framework": "Compliant with SEC regulations",
            "Compliance Status": "Fully compliant with all applicable regulations",
            "Contact Phone": "1-800-STRUCTURED",
            "Contact Email": "structuredproducts@issuer.com",
            "Contact Website": "www.issuer.com/structuredproducts",
            "Legal Department": "legal@issuer.com",
            "Compliance Department": "compliance@issuer.com",
            "Document Version": "1.0",
            "Document Type": "Base Shelf Prospectus",
            "Document Status": "Draft for Review",
            "Market Risk Level": "High",
            "Credit Risk Level": "Medium",
            "Liquidity Risk Level": "Medium",
            "Regulatory Risk Level": "Low",
            "Operational Risk Level": "Low",
            "Maximum Note Size": "100,000,000 USD",
            "Minimum Note Size": "1,000,000 USD",
            "Shelf Period": "3 years from effective date",
            "Renewal Process": "Subject to regulatory approval and market conditions",
            "Primary Distribution": "Institutional investors and qualified purchasers",
            "Secondary Distribution": "Broker-dealer networks and private placements",
            "Retail Distribution": "Limited to accredited investors and qualified purchasers",
            "SEC Compliance": "Full compliance with Regulation S-K and other applicable regulations",
            "Ongoing Disclosures": "Quarterly and annual reports as required by applicable regulations",
            "Material Events": "Immediate disclosure of material events affecting the program",
            "Governing Law": "New York law",
            "Dispute Resolution": "Arbitration in accordance with FINRA rules",
            "Jurisdiction": "Federal and state courts in New York",
            "Primary Use": "General corporate purposes including funding structured products",
            "Secondary Use": "Hedging activities and risk management",
            "Tertiary Use": "Working capital and other business purposes",
            "Risk Management Framework": "Comprehensive risk management policies and procedures",
            "Credit Risk Management": "Regular credit assessments and monitoring",
            "Market Risk Management": "Dynamic hedging strategies and position limits",
            "Operational Risk Management": "Robust internal controls and monitoring systems"
        }
        
        # Generate document
        document = create_complete_document_from_templates(sample_data, "institutional")
        
        # Ensure output directory exists
        os.makedirs("generated_documents/bsp", exist_ok=True)
        
        # Save JSON document
        json_filename = "generated_documents/bsp/minimal_test_document.json"
        with open(json_filename, 'w') as f:
            json.dump(document, f, indent=2)
        
        # Save text document
        text_filename = "generated_documents/bsp/minimal_test_document.txt"
        with open(text_filename, 'w') as f:
            f.write("BSP Base Shelf Prospectus Document\n")
            f.write("=" * 50 + "\n\n")
            
            for section_name, content in document.items():
                f.write(f"{section_name.upper().replace('_', ' ')}\n")
                f.write("-" * 30 + "\n")
                f.write(content)
                f.write("\n\n")
        
        # Verify files were created
        assert os.path.exists(json_filename), f"JSON file not created: {json_filename}"
        assert os.path.exists(text_filename), f"Text file not created: {text_filename}"
        
        # Verify file sizes
        json_size = os.path.getsize(json_filename)
        text_size = os.path.getsize(text_filename)
        
        assert json_size > 0, "JSON file is empty"
        assert text_size > 0, "Text file is empty"
        
        print(f"✅ Document saved to: {json_filename}")
        print(f"✅ Text document saved to: {text_filename}")
        print(f"📊 JSON file size: {json_size} bytes")
        print(f"📊 Text file size: {text_size} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Document saving test failed: {str(e)}")
        return False


def test_bsp_input_creation():
    """Test BSP input model creation"""
    print("🔍 Running: BSP Input Creation")
    
    try:
        # Create sample BSP input
        bsp_input = BSPInput(
            issuer="Your Financial Institution Ltd",
            guarantor=None,
            program_name="Structured Notes Program 2025",
            shelf_amount=1000000000.0,
            currency="USD",
            regulatory_jurisdiction="SEC",
            sec_registration="333-123456",
            legal_structure="Delaware corporation",
            business_description="Financial services including structured products and investment banking",
            financial_condition="Strong financial condition with excellent credit ratings",
            note_types=["autocallable", "barrier", "reverse convertible"],
            distribution_methods=["broker-dealer", "private placement", "direct institutional"],
            additional_features={
                "custom_notes": True,
                "hedging_program": "Comprehensive hedging program",
                "risk_management": "Advanced risk management framework"
            }
        )
        
        # Verify input creation
        assert bsp_input.issuer == "Your Financial Institution Ltd"
        assert bsp_input.program_name == "Structured Notes Program 2025"
        assert bsp_input.shelf_amount == 1000000000.0
        assert bsp_input.currency == "USD"
        assert bsp_input.regulatory_jurisdiction == "SEC"
        assert len(bsp_input.note_types) == 3
        assert len(bsp_input.distribution_methods) == 3
        assert bsp_input.additional_features is not None
        
        print("✅ BSP input creation successful")
        print(f"📋 Created input for: {bsp_input.program_name}")
        print(f"💰 Shelf amount: {bsp_input.shelf_amount:,.0f} {bsp_input.currency}")
        print(f"📝 Note types: {', '.join(bsp_input.note_types)}")
        
        return True
        
    except Exception as e:
        print(f"❌ BSP input creation test failed: {str(e)}")
        return False


def main():
    """Run all BSP tests"""
    print("🚀 BSP Large Text Templates Minimal Tests")
    print("=" * 60)
    print()
    
    # Run tests
    tests = [
        test_large_text_templates,
        test_template_variable_substitution,
        test_document_saving,
        test_bsp_input_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
    
    print()
    print("=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if passed == total:
        print(f"✅ PASS {passed}/{total} tests")
        print("🎉 All tests passed! BSP large text templates are working perfectly!")
    else:
        print(f"❌ FAIL {passed}/{total} tests")
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total


if __name__ == "__main__":
    main()
