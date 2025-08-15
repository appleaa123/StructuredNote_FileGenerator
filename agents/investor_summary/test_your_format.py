#!/usr/bin/env python3
"""
Quick Format Testing Script for ISM Agent

Use this script to quickly test your format customizations without running
the full document generation process.

Usage:
    python test_your_format.py
"""

import json
import asyncio
from datetime import date
from pathlib import Path

# Import ISM components
from agents.investor_summary import ISMAgent, ISMInput, ISMConfig, LargeTextISMAgent
from agents.investor_summary.ism_customization_examples import create_custom_ism_config_with_your_format


def test_json_config(config_file: str = "sample_format_config.json"):
    """Test configuration loaded from JSON file"""
    print(f"🔍 Testing JSON configuration from: {config_file}")
    
    try:
        # Load JSON config
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        print("✅ JSON file loaded successfully!")
        
        # Display key settings
        print("\n📋 Your Configuration Summary:")
        print(f"   Document Title Format: {config_data.get('document_title_format', 'Not set')}")
        print(f"   Reading Level: {config_data.get('reading_level', 'Not set')}")
        print(f"   Max Length: {config_data.get('max_document_length', 'Not set')} words")
        
        # Display mandatory phrases
        if 'mandatory_phrases' in config_data:
            print("\n📝 Your Mandatory Phrases:")
            for category, phrases in config_data['mandatory_phrases'].items():
                print(f"   {category}:")
                for phrase in phrases:
                    print(f"     - {phrase}")
        
        # Display company info
        if 'company_information' in config_data:
            print("\n🏢 Your Company Information:")
            company = config_data['company_information']
            for key, value in company.items():
                print(f"   {key}: {value}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {config_file}")
        print("   Create this file using the sample_format_config.json template")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_code_config():
    """Test configuration from Python code"""
    print("🔍 Testing Python code configuration...")
    
    try:
        # Load config from code
        config = create_custom_ism_config_with_your_format()
        
        print("✅ Python configuration loaded successfully!")
        
        # Display settings
        print("\n📋 Your Configuration Summary:")
        print(f"   Target Reading Level: {config.target_reading_level}")
        print(f"   Max Document Length: {config.max_document_length} words")
        print(f"   Tone: {config.tone}")
        print(f"   Technical Level: {config.technical_level}")
        
        # Display format templates
        print("\n📐 Your Format Templates:")
        for template_name, template_config in config.format_templates.items():
            print(f"   {template_name}:")
            if isinstance(template_config, dict):
                for key, value in template_config.items():
                    print(f"     {key}: {value}")
        
        # Display mandatory phrases
        print("\n📝 Your Mandatory Phrases:")
        for category, phrases in config.mandatory_phrases.items():
            print(f"   {category}:")
            for phrase in phrases[:3]:  # Show first 3 to avoid clutter
                print(f"     - {phrase}")
            if len(phrases) > 3:
                print(f"     ... and {len(phrases) - 3} more")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in Python configuration: {e}")
        return False


def test_format_application():
    """Test how the format will be applied to actual content"""
    print("\n🧪 Testing Format Application...")
    
    try:
        # Create sample data
        sample_data = {
            "product_type": "Autocallable",
            "underlying_asset": "S&P 500 Index",
            "risk_level": "HIGH",
            "investment_amount": 100000,
            "currency": "USD"
        }
        
        # Load config
        config = create_custom_ism_config_with_your_format()
        
        # Test title format
        title_template = config.format_templates["document_title_template"]["format"]
        sample_title = title_template.replace("[Product Type]", sample_data["product_type"])
        sample_title = sample_title.replace("[Underlying Asset]", sample_data["underlying_asset"])
        
        print(f"📄 Sample Document Title:")
        print(f"   Template: {title_template}")
        print(f"   Result: {sample_title}")
        
        # Test risk level format
        risk_template = config.format_templates["risk_level_template"]["format"]
        sample_risk = risk_template.replace("[HIGH/MEDIUM/LOW]", sample_data["risk_level"])
        sample_risk = sample_risk.replace("[2-sentence explanation]", "This investment has significant market exposure. Your returns will vary with market performance.")
        
        print(f"\n⚠️  Sample Risk Level:")
        print(f"   Template: {risk_template}")
        print(f"   Result: {sample_risk}")
        
        # Test bullet point format
        bullet_template = config.format_templates["bullet_point_template"]["format"]
        sample_bullet = bullet_template.replace("[Feature]", "Automatic Early Redemption")
        sample_bullet = sample_bullet.replace("[Benefit]", "Potential early exit with profits")
        sample_bullet = sample_bullet.replace("[Impact explanation]", "reduces time risk")
        
        print(f"\n• Sample Bullet Point:")
        print(f"   Template: {bullet_template}")
        print(f"   Result: {sample_bullet}")
        
        # Test scenario format
        scenario_template = config.format_templates["scenario_template"]["best_case"]
        sample_scenario = scenario_template.replace("[condition]", "Market rises 20%")
        sample_scenario = sample_scenario.replace("[X]", "15.0")
        sample_scenario = sample_scenario.replace("[dollar amount]", f"${sample_data['investment_amount'] * 1.15:,.0f}")
        
        print(f"\n📈 Sample Best Case Scenario:")
        print(f"   Template: {scenario_template}")
        print(f"   Result: {sample_scenario}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing format application: {e}")
        return False


def test_large_text_templates():
    """Test Bank of Nova Scotia large text templates"""
    print("\n🏦 Testing Bank of Nova Scotia Large Text Templates...")
    
    try:
        # Import large text templates
        from agents.investor_summary.large_text_templates import test_your_templates, create_complete_document_from_templates
        
        # Test the templates directly
        print("   📝 Testing template customizations...")
        document = test_your_templates()
        
        print("\n   ✅ Template test completed successfully!")
        
        # Show template statistics
        print("\n   📊 Your Template Statistics:")
        for section, content in document.items():
            word_count = len(content.split())
            char_count = len(content)
            print(f"     {section}: {word_count} words, {char_count} characters")
        
        # Test sample Bank of Nova Scotia data
        print("\n   🧪 Testing with Bank of Nova Scotia sample data...")
        
        scotia_sample_data = {
            "Note Title": "S&P 500 Index Autocallable Notes - Series 2025",
            "Underlying Asset Name": "S&P 500 Index",
            "Asset Manager Name": "Bank of Nova Scotia",
            "Fundserv Code": "SSP2501",
            "CUSIP Code": "06418YJF6",
            "Independent Agent Name": "Scotia Capital Inc.",
            "YOUR_COMPANY_NAME": "The Bank of Nova Scotia",
            "YOUR_PHONE": "1-866-416-7891",
            "Final Fixed Return": "59.50%",
            "Barrier Percentage": "70.00%",
        }
        
        # Test specific template generation
        scotia_document = create_complete_document_from_templates(scotia_sample_data, "retail")
        
        print("   ✅ Scotia sample data test completed!")
        
        # Check for placeholder replacement
        print("\n   🔍 Checking placeholder replacement:")
        placeholder_issues = []
        for section, content in scotia_document.items():
            if "[" in content and "]" in content:
                # Count unreplaced placeholders
                import re
                placeholders = re.findall(r'\[([^\]]+)\]', content)
                if placeholders:
                    placeholder_issues.extend([(section, p) for p in placeholders])
        
        if placeholder_issues:
            print("   ⚠️  Found unreplaced placeholders:")
            for section, placeholder in placeholder_issues[:10]:  # Show first 10
                print(f"     {section}: [{placeholder}]")
            if len(placeholder_issues) > 10:
                print(f"     ... and {len(placeholder_issues) - 10} more")
        else:
            print("   ✅ All placeholders successfully replaced!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing large text templates: {e}")
        return False


async def test_large_text_integration():
    """Test full integration with Bank of Nova Scotia templates"""
    print("\n🔗 Testing Large Text Template Integration...")
    
    try:
        # Create large text ISM agent
        agent = LargeTextISMAgent()
        
        # Create Scotia sample input
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
        
        print("   ⏳ Generating document with large text templates...")
        
        # Generate document using large text templates
        document = await agent.generate_document_with_large_templates(
            input_data=input_data,
            audience="retail"
        )
        
        print("   ✅ Large text integration test completed!")
        
        # Display results
        print("\n   📄 Generated Document Sections:")
        for section, content in document.items():
            word_count = len(content.split())
            print(f"     {section}: {word_count} words")
            # Show first line preview
            first_line = content.split('\n')[0][:80]
            print(f"       Preview: {first_line}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in large text integration: {e}")
        print(f"   This might be due to missing API keys or network issues")
        return False


async def test_full_generation():
    """Test full document generation with your custom format"""
    print("\n🚀 Testing Full Document Generation...")
    
    try:
        # Create custom config
        config = create_custom_ism_config_with_your_format()
        
        # Create agent
        agent = ISMAgent(config=config)
        
        # Create sample input
        input_data = ISMInput(
            issuer="Test Bank Ltd",
            product_name="S&P 500 Autocallable Note",
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
        
        print("⏳ Generating document (this may take 30-60 seconds)...")
        
        # Generate document
        result = await agent.generate_document(input_data)
        
        print("✅ Document generated successfully!")
        
        # Display key results
        print(f"\n📄 Generated Document Preview:")
        print(f"   Title: {result.document_title}")
        print(f"   Risk Level: {result.risk_level_indicator}")
        print(f"   Key Features Count: {len(result.key_features)}")
        print(f"   Key Risks Count: {len(result.key_risks)}")
        
        # Show first few lines of executive summary
        exec_lines = result.executive_summary.split('\n')[:3]
        print(f"\n📋 Executive Summary Preview:")
        for i, line in enumerate(exec_lines, 1):
            if line.strip():
                print(f"   Para {i}: {line.strip()[:80]}...")
        
        # Show sample features and risks
        print(f"\n• Key Features Preview:")
        for i, feature in enumerate(result.key_features[:2], 1):
            print(f"   {i}. {feature}")
        
        print(f"\n⚠️  Key Risks Preview:")
        for i, risk in enumerate(result.key_risks[:2], 1):
            print(f"   {i}. {risk}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in full generation: {e}")
        print(f"   This might be due to missing API keys or network issues")
        return False


def main():
    """Main testing function"""
    print("🔧 ISM Agent Format Testing Tool")
    print("🏦 Bank of Nova Scotia Large Text Templates")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Bank of Nova Scotia Large Text Templates (Primary)
    print("\n1️⃣  Testing Bank of Nova Scotia Large Text Templates")
    if not test_large_text_templates():
        all_tests_passed = False
    
    # Test 2: Large Text Integration (Optional)
    print("\n2️⃣  Testing Large Text Integration")
    print("⚠️  This test requires API access and may take time.")
    
    user_input = input("Do you want to run the large text integration test? (y/N): ").lower().strip()
    if user_input in ['y', 'yes']:
        try:
            result = asyncio.run(test_large_text_integration())
            if not result:
                all_tests_passed = False
        except Exception as e:
            print(f"❌ Large text integration test failed: {e}")
            all_tests_passed = False
    else:
        print("⏭️  Skipping large text integration test")
    
    # Test 3: JSON Configuration (Legacy)
    print("\n3️⃣  Testing JSON Configuration (Legacy Method)")
    json_path = Path("sample_format_config.json")
    if json_path.exists():
        if not test_json_config():
            all_tests_passed = False
    else:
        print("⚠️  sample_format_config.json not found - skipping JSON test")
    
    # Test 4: Python Code Configuration (Legacy)
    print("\n4️⃣  Testing Python Code Configuration (Legacy Method)")
    try:
        if not test_code_config():
            all_tests_passed = False
    except Exception as e:
        print(f"⚠️  Python config test failed: {e}")
        print("   This is okay if you're only using large text templates")
    
    # Test 5: Format Application (Legacy)
    print("\n5️⃣  Testing Format Application (Legacy Method)")
    try:
        if not test_format_application():
            all_tests_passed = False
    except Exception as e:
        print(f"⚠️  Format application test failed: {e}")
        print("   This is okay if you're only using large text templates")
    
    # Summary
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All tests passed! Your Bank of Nova Scotia templates are ready!")
        print("\n✅ Next steps:")
        print("   1. Run python large_text_integration.py for full examples")
        print("   2. Use LargeTextISMAgent in your production code")
        print("   3. Customize templates further in large_text_templates.py")
        print("   4. Test with different Bank of Nova Scotia products")
    else:
        print("⚠️  Some tests had issues. Check the errors above.")
        print("\n🔧 Common fixes:")
        print("   1. Update placeholders in large_text_templates.py")
        print("   2. Check variable mappings in large_text_integration.py")
        print("   3. Ensure all Bank of Nova Scotia data is properly formatted")
        print("   4. Review template structure and content")
    
    print("\n💡 Bank of Nova Scotia Template Features:")
    print("   ✅ Canadian regulatory compliance language")
    print("   ✅ Scotia Capital Inc. distribution details")
    print("   ✅ Fundserv and CUSIP code integration")
    print("   ✅ Autocall payment schedule tables")
    print("   ✅ RRSPs, RRIFs, TFSAs eligibility")
    print("   ✅ Complete structured note documentation")


if __name__ == "__main__":
    main()