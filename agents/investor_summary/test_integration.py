#!/usr/bin/env python3
"""
Integration Test for ISM Agent with Large Text Templates

This script tests that all ISM agent components work together correctly
with the large text templates and proper variable handling.
"""

import asyncio
import json
from datetime import date
from pathlib import Path

# Import ISM components
from agents.investor_summary import ISMAgent, ISMInput, LargeTextISMAgent
from agents.investor_summary.large_text_templates import test_your_templates


async def test_basic_ism_agent():
    """Test basic ISM agent functionality"""
    print("🧪 Test 1: Basic ISM Agent")
    print("-" * 40)
    
    try:
        # Create ISM agent
        agent = ISMAgent(use_large_text_templates=True)
        print("✅ ISM agent created successfully")
        
        # Create sample input
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
        print("✅ Sample input data created")
        
        # Test large text template generation
        document = await agent.generate_document_with_large_text_templates(
            input_data=input_data,
            audience="retail"
        )
        
        print("✅ Large text template generation successful")
        print(f"📄 Generated {len(document)} sections:")
        for section, content in document.items():
            word_count = len(content.split())
            print(f"   {section}: {word_count} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic ISM agent test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_large_text_ism_agent():
    """Test LargeTextISMAgent functionality"""
    print("\n🧪 Test 2: Large Text ISM Agent")
    print("-" * 40)
    
    try:
        # Create LargeTextISMAgent
        agent = LargeTextISMAgent()
        print("✅ LargeTextISMAgent created successfully")
        
        # Create sample input
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
        
        # Test document generation
        document = await agent.generate_document_with_large_templates(
            input_data=input_data,
            audience="retail"
        )
        
        print("✅ LargeTextISMAgent document generation successful")
        print(f"📄 Generated {len(document)} sections:")
        for section, content in document.items():
            word_count = len(content.split())
            print(f"   {section}: {word_count} words")
        
        # Test template variables extraction
        variables = agent.get_template_variables(input_data)
        print(f"✅ Template variables extracted: {len(variables)} variables")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in LargeTextISMAgent test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_large_text_templates():
    """Test large text templates directly"""
    print("\n🧪 Test 3: Large Text Templates")
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


async def test_document_saving():
    """Test document saving functionality"""
    print("\n🧪 Test 4: Document Saving")
    print("-" * 40)
    
    try:
        # Create agent and generate document
        agent = LargeTextISMAgent()
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
        
        document = await agent.generate_document_with_large_templates(
            input_data=input_data,
            audience="retail"
        )
        
        # Save document
        output_dir = Path("generated_documents/ism")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "integration_test_document.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(document, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Document saved to: {output_file}")
        print(f"📄 File size: {output_file.stat().st_size} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in document saving test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all integration tests"""
    print("🚀 ISM Agent Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Basic ISM Agent", test_basic_ism_agent),
        ("Large Text ISM Agent", test_large_text_ism_agent),
        ("Large Text Templates", lambda: test_large_text_templates()),
        ("Document Saving", test_document_saving),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
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
        print("🎉 All tests passed! ISM agent is working perfectly!")
        print("\n💡 Next steps:")
        print("   1. Use ISMAgent or LargeTextISMAgent in your applications")
        print("   2. Customize templates in large_text_templates.py")
        print("   3. Test with different product configurations")
        print("   4. Generate documents for your specific use cases")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\n🔧 Common fixes:")
        print("   1. Ensure all dependencies are installed")
        print("   2. Check API keys and configuration")
        print("   3. Verify template customizations")
        print("   4. Review error messages for specific issues")


if __name__ == "__main__":
    asyncio.run(main()) 