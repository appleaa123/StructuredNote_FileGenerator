#!/usr/bin/env python3
"""
Standalone Test for ISM Large Text Templates

This script tests the large text templates and integration components
without requiring the full ISM agent with LightRAG dependencies.
"""

import json
from datetime import date
from pathlib import Path

# Import only the components we need
from agents.investor_summary.models import ISMInput
from agents.investor_summary.large_text_templates import test_your_templates, create_complete_document_from_templates


def test_large_text_templates():
    """Test large text templates directly"""
    print("🧪 Test 1: Large Text Templates")
    print("-" * 40)
    
    try:
        # Test templates
        document = test_your_templates()
        
        print("✅ Large text templates test successful")
        print(f"📄 Generated {len(document)} sections:")
        for section, content in document.items():
            word_count = len(content.split())
            print(f"   {section}: {word_count} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in large text templates test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template_variable_substitution():
    """Test template variable substitution"""
    print("\n🧪 Test 2: Template Variable Substitution")
    print("-" * 40)
    
    try:
        # Create sample data
        sample_data = {
            "Note Title": "S&P 500 Index Autocallable Notes - Series 2025",
            "Maturity Date": "January 29, 2032",
            "Document Date": "January 15, 2025",
            "Pricing Supplement Number": "PS-2025-001",
            "Pricing Supplement Date": "January 29, 2025",
            "Underlying Asset Type": "Index",
            "Underlying Asset Description": "The S&P 500 Index, a broad market index representing large-cap U.S. equities with strong historical performance and liquidity characteristics.",
            "Underlying Asset Name": "S&P 500 Index",
            "levels/prices": "levels",
            "Closing Level/Price Name": "Closing Index Level",
            "Autocall Level/Price Name": "Autocall Level",
            "Final Level/Price Name": "Final Index Level",
            "Barrier Level/Price Name": "Barrier Level",
            "Initial Level/Price Name": "Initial Index Level",
            "First Call Date": "January 29, 2026",
            "Additional Return Percentage": "5.00%",
            "Return Calculation Metric Name": "Index Return",
            "Contingent Principal Protection Percentage": "30.00%",
            "Barrier Percentage": "70.00%",
            "Final Fixed Return": "59.50%",
            "Valuation Date 1": "January 29, 2026",
            "Valuation Date 2": "January 29, 2027",
            "Valuation Date 3": "January 29, 2028",
            "Valuation Date 4": "January 29, 2029",
            "Valuation Date 5": "January 29, 2030",
            "Valuation Date 6": "January 29, 2031",
            "Fixed Return 1": "8.50%",
            "Fixed Return 2": "17.00%",
            "Fixed Return 3": "25.50%",
            "Fixed Return 4": "34.00%",
            "Fixed Return 5": "42.50%",
            "Fixed Return 6": "51.00%",
            "Autocall Level/Price Description": "100.00% of the Initial Index Level",
            "Fundserv Code": "SSP2501",
            "Available Until Date": "January 22, 2025",
            "Issue Date": "January 29, 2025",
            "Term": "7 years",
            "CUSIP Code": "06418YJF6",
            "Initial Valuation Date": "January 29, 2025",
            "Final Valuation Date": "January 29, 2032",
            "Fees and Expenses Description": "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 2.50% of the Principal Amount per Note. No additional independent agent fees apply for retail distribution.",
            "Independent Agent Name": "Scotia Capital Inc.",
            "Asset Manager Name": "Bank of Nova Scotia",
            "YOUR_COMPANY_NAME": "The Bank of Nova Scotia",
            "YOUR_REGULATOR": "Canadian Securities Regulators",
            "YOUR_PHONE": "1-866-416-7891",
            "YOUR_EMAIL": "structured.products@scotiabank.com",
            "YOUR_WEBSITE": "www.gbm.scotiabank.com",
        }
        
        # Generate document using templates
        document = create_complete_document_from_templates(sample_data, "retail")
        
        print("✅ Template variable substitution successful")
        print(f"📄 Generated {len(document)} sections:")
        for section, content in document.items():
            word_count = len(content.split())
            print(f"   {section}: {word_count} words")
        
        # Check for unreplaced placeholders
        placeholder_issues = []
        for section, content in document.items():
            if "[" in content and "]" in content:
                import re
                placeholders = re.findall(r'\[([^\]]+)\]', content)
                if placeholders:
                    placeholder_issues.extend([(section, p) for p in placeholders])
        
        if placeholder_issues:
            print("⚠️  Found unreplaced placeholders:")
            for section, placeholder in placeholder_issues[:10]:
                print(f"     {section}: [{placeholder}]")
            if len(placeholder_issues) > 10:
                print(f"     ... and {len(placeholder_issues) - 10} more")
        else:
            print("✅ All placeholders successfully replaced!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in template variable substitution test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_saving():
    """Test document saving functionality"""
    print("\n🧪 Test 3: Document Saving")
    print("-" * 40)
    
    try:
        # Create sample data
        sample_data = {
            "Note Title": "S&P 500 Index Autocallable Notes - Series 2025",
            "Maturity Date": "January 29, 2032",
            "Document Date": "January 15, 2025",
            "Pricing Supplement Number": "PS-2025-001",
            "Pricing Supplement Date": "January 29, 2025",
            "Underlying Asset Type": "Index",
            "Underlying Asset Description": "The S&P 500 Index, a broad market index representing large-cap U.S. equities with strong historical performance and liquidity characteristics.",
            "Underlying Asset Name": "S&P 500 Index",
            "levels/prices": "levels",
            "Closing Level/Price Name": "Closing Index Level",
            "Autocall Level/Price Name": "Autocall Level",
            "Final Level/Price Name": "Final Index Level",
            "Barrier Level/Price Name": "Barrier Level",
            "Initial Level/Price Name": "Initial Index Level",
            "First Call Date": "January 29, 2026",
            "Additional Return Percentage": "5.00%",
            "Return Calculation Metric Name": "Index Return",
            "Contingent Principal Protection Percentage": "30.00%",
            "Barrier Percentage": "70.00%",
            "Final Fixed Return": "59.50%",
            "Valuation Date 1": "January 29, 2026",
            "Valuation Date 2": "January 29, 2027",
            "Valuation Date 3": "January 29, 2028",
            "Valuation Date 4": "January 29, 2029",
            "Valuation Date 5": "January 29, 2030",
            "Valuation Date 6": "January 29, 2031",
            "Fixed Return 1": "8.50%",
            "Fixed Return 2": "17.00%",
            "Fixed Return 3": "25.50%",
            "Fixed Return 4": "34.00%",
            "Fixed Return 5": "42.50%",
            "Fixed Return 6": "51.00%",
            "Autocall Level/Price Description": "100.00% of the Initial Index Level",
            "Fundserv Code": "SSP2501",
            "Available Until Date": "January 22, 2025",
            "Issue Date": "January 29, 2025",
            "Term": "7 years",
            "CUSIP Code": "06418YJF6",
            "Initial Valuation Date": "January 29, 2025",
            "Final Valuation Date": "January 29, 2032",
            "Fees and Expenses Description": "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 2.50% of the Principal Amount per Note. No additional independent agent fees apply for retail distribution.",
            "Independent Agent Name": "Scotia Capital Inc.",
            "Asset Manager Name": "Bank of Nova Scotia",
            "YOUR_COMPANY_NAME": "The Bank of Nova Scotia",
            "YOUR_REGULATOR": "Canadian Securities Regulators",
            "YOUR_PHONE": "1-866-416-7891",
            "YOUR_EMAIL": "structured.products@scotiabank.com",
            "YOUR_WEBSITE": "www.gbm.scotiabank.com",
        }
        
        # Generate document
        document = create_complete_document_from_templates(sample_data, "retail")
        
        # Save document
        output_dir = Path("generated_documents/ism")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "standalone_test_document.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(document, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Document saved to: {output_file}")
        print(f"📄 File size: {output_file.stat().st_size} bytes")
        
        # Also save as text file for readability
        text_file = output_dir / "standalone_test_document.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("BANK OF NOVA SCOTIA STRUCTURED NOTE DOCUMENT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {date.today().strftime('%B %d, %Y')}\n")
            f.write("=" * 80 + "\n\n")
            
            for section_name, content in document.items():
                f.write(f"\n{'='*60}\n")
                f.write(f"{section_name.upper().replace('_', ' ')}\n")
                f.write(f"{'='*60}\n\n")
                f.write(content)
                f.write("\n\n")
        
        print(f"✅ Text document saved to: {text_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in document saving test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ism_input_creation():
    """Test ISMInput creation"""
    print("\n🧪 Test 4: ISMInput Creation")
    print("-" * 40)
    
    try:
        # Create ISMInput
        input_data = ISMInput(
            issuer="The Bank of Nova Scotia",
            product_name="S&P 500 Index Autocallable Notes",
            underlying_asset="S&P 500 Index",
            currency="CAD",
            principal_amount=100000.00,
            issue_date=date(2025, 1, 29),
            maturity_date=date(2032, 1, 29),
            product_type="autocallable",
            barrier_level=70.0,
            coupon_rate=8.5,
            risk_tolerance="medium",
            investment_objective="income_and_growth",
            regulatory_jurisdiction="Canada",
            distribution_method="retail"
        )
        
        print("✅ ISMInput created successfully")
        print(f"   Issuer: {input_data.issuer}")
        print(f"   Product: {input_data.product_name}")
        print(f"   Asset: {input_data.underlying_asset}")
        print(f"   Amount: {input_data.principal_amount:,.2f} {input_data.currency}")
        print(f"   Term: {((input_data.maturity_date - input_data.issue_date).days / 365.25):.1f} years")
        print(f"   Barrier: {input_data.barrier_level}%")
        print(f"   Coupon: {input_data.coupon_rate}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in ISMInput creation test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all standalone tests"""
    print("🚀 ISM Large Text Templates Standalone Tests")
    print("=" * 60)
    
    tests = [
        ("Large Text Templates", test_large_text_templates),
        ("Template Variable Substitution", test_template_variable_substitution),
        ("Document Saving", test_document_saving),
        ("ISMInput Creation", test_ism_input_creation),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Large text templates are working perfectly!")
        print("\n💡 Next steps:")
        print("   1. Use the large text templates in your applications")
        print("   2. Customize templates in large_text_templates.py")
        print("   3. Test with different product configurations")
        print("   4. Generate documents for your specific use cases")
        print("\n📁 Generated files:")
        print("   - generated_documents/ism/standalone_test_document.json")
        print("   - generated_documents/ism/standalone_test_document.txt")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\n🔧 Common fixes:")
        print("   1. Ensure all dependencies are installed")
        print("   2. Check template customizations")
        print("   3. Verify file permissions for saving")
        print("   4. Review error messages for specific issues")


if __name__ == "__main__":
    main() 