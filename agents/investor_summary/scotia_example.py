#!/usr/bin/env python3
"""
Bank of Nova Scotia ISM Agent Example

This example demonstrates how to use the ISM agent with your customized
Bank of Nova Scotia large text templates to generate structured note documents.

🎯 QUICK START:
1. Ensure your templates are customized in large_text_templates.py
2. Run this script: python scotia_example.py
3. Review the generated documents
4. Modify the product data below for your actual products
"""

import asyncio
from datetime import date
from pathlib import Path

# Import ISM components
from agents.investor_summary import ISMInput, LargeTextISMAgent
from agents.investor_summary.large_text_templates import test_your_templates


async def example_sp500_autocallable():
    """
    Example: S&P 500 Index Autocallable Note
    
    Typical Bank of Nova Scotia retail index-linked product
    """
    print("🚀 Generating S&P 500 Index Autocallable Note")
    print("=" * 60)
    
    # Create the ISM agent with large text templates
    agent = LargeTextISMAgent()
    
    # Define the S&P 500 product details
    input_data = ISMInput(
        issuer="The Bank of Nova Scotia",
        product_name="S&P 500 Index Autocallable Notes - Series 2025A",
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
    
    # Custom variables specific to this product
    custom_variables = {
        "Pricing Supplement Number": "PS-2025-SP500-001",
        "Fundserv Code": "SSP2501",
        "CUSIP Code": "06418YSP5",
        "Independent Agent Name": "Scotia Capital Inc.",
        "Fees and Expenses Description": "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 2.50% of the Principal Amount per Note. No additional independent agent fees apply for retail distribution."
    }
    
    # Generate the complete document
    document = await agent.generate_document_with_large_templates(
        input_data=input_data,
        audience="retail",
        custom_variables=custom_variables
    )
    
    # Save to file
    save_document(document, "scotia_sp500_autocallable.txt")
    
    print("✅ S&P 500 Autocallable Note document generated successfully!")
    return document


async def example_canadian_bank_basket():
    """
    Example: Canadian Bank Basket Autocallable Note
    
    Institutional product featuring Canadian bank stocks
    """
    print("\n🚀 Generating Canadian Bank Basket Autocallable Note")
    print("=" * 60)
    
    agent = LargeTextISMAgent()
    
    # Define the Canadian bank basket product
    input_data = ISMInput(
        issuer="The Bank of Nova Scotia",
        product_name="Canadian Bank Basket Autocallable Notes - Series 2025B",
        underlying_asset="Canadian Banking Sector Portfolio",
        currency="CAD",
        principal_amount=500000.00,
        issue_date=date(2025, 3, 15),
        maturity_date=date(2030, 3, 15),
        product_type="autocallable",
        barrier_level=65.0,
        coupon_rate=7.25,
        risk_tolerance="high",
        investment_objective="yield_enhancement",
        regulatory_jurisdiction="Canada",
        distribution_method="institutional"
    )
    
    # Basket-specific custom variables
    custom_variables = {
        "Underlying Asset Type": "Reference Portfolio and Reference Companies",
        "Underlying Asset Description": "A basket consisting of 5 equally-weighted Canadian bank stocks: Royal Bank of Canada (RY), Toronto-Dominion Bank (TD), Bank of Nova Scotia (BNS), Bank of Montreal (BMO), and Canadian Imperial Bank of Commerce (CM). The portfolio provides exposure to the Canadian banking sector with strong dividend yields and established market positions.",
        "levels/prices": "prices",
        "Closing Level/Price Name": "Closing Portfolio Price",
        "Autocall Level/Price Name": "Autocall Price",
        "Final Level/Price Name": "Final Portfolio Price",
        "Barrier Level/Price Name": "Barrier Price",
        "Initial Level/Price Name": "Initial Portfolio Price",
        "Return Calculation Metric Name": "Price Return",
        "Pricing Supplement Number": "PS-2025-BANKS-001",
        "Fundserv Code": "SSP2502",
        "CUSIP Code": "06418YBK3",
        "Fees and Expenses Description": "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 1.75% of the Principal Amount per Note for institutional distribution. Additional structuring fees of 0.50% apply."
    }
    
    # Generate the document
    document = await agent.generate_document_with_large_templates(
        input_data=input_data,
        audience="retail",  # Using retail template with institutional data
        custom_variables=custom_variables
    )
    
    # Save to file
    save_document(document, "scotia_bank_basket_autocallable.txt")
    
    print("✅ Canadian Bank Basket document generated successfully!")
    return document


async def example_tsx60_note():
    """
    Example: TSX 60 Index Note
    
    Canadian equity index exposure with capital protection
    """
    print("\n🚀 Generating TSX 60 Index Protected Note")
    print("=" * 60)
    
    agent = LargeTextISMAgent()
    
    # Define the TSX 60 product
    input_data = ISMInput(
        issuer="The Bank of Nova Scotia",
        product_name="TSX 60 Index Protected Notes - Series 2025C",
        underlying_asset="S&P/TSX 60 Index",
        currency="CAD",
        principal_amount=250000.00,
        issue_date=date(2025, 6, 1),
        maturity_date=date(2028, 6, 1),
        product_type="autocallable",
        barrier_level=75.0,  # Higher protection
        coupon_rate=6.5,
        risk_tolerance="medium",
        investment_objective="capital_preservation_with_growth",
        regulatory_jurisdiction="Canada",
        distribution_method="private_wealth"
    )
    
    # TSX 60 specific variables
    custom_variables = {
        "Underlying Asset Description": "The S&P/TSX 60 Index, representing the 60 largest and most liquid stocks traded on the Toronto Stock Exchange, providing broad exposure to the Canadian equity market including financials, energy, materials, and technology sectors.",
        "INDEX_SPONSOR": "S&P Dow Jones Indices",
        "Pricing Supplement Number": "PS-2025-TSX60-001",
        "Fundserv Code": "SSP2503",
        "CUSIP Code": "06418YTX6",
        "Contingent Principal Protection Percentage": "25.00%",  # 100% - 75% barrier
        "Additional Return Percentage": "4.00%",  # Lower participation for higher protection
    }
    
    # Generate the document
    document = await agent.generate_document_with_large_templates(
        input_data=input_data,
        audience="retail",
        custom_variables=custom_variables
    )
    
    # Save to file
    save_document(document, "scotia_tsx60_protected.txt")
    
    print("✅ TSX 60 Protected Note document generated successfully!")
    return document


def save_document(document: dict, filename: str):
    """Save generated document to a text file"""
    output_path = Path("generated_documents") / "ism" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
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
    
    print(f"   📁 Document saved to: {output_path}")


def test_templates_first():
    """Test templates before running examples"""
    print("🧪 Testing Bank of Nova Scotia Templates First...")
    print("=" * 60)
    
    try:
        # Test the templates
        document = test_your_templates()
        
        print("✅ Template test completed successfully!")
        print("\n📊 Template Statistics:")
        for section, content in document.items():
            word_count = len(content.split())
            print(f"   {section}: {word_count} words")
        
        return True
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        print("   Please check your template customizations in large_text_templates.py")
        return False


async def main():
    """Main function - run all examples"""
    print("🏦 Bank of Nova Scotia ISM Agent Examples")
    print("📝 Generating Structured Note Documents")
    print("=" * 80)
    
    # First test the templates
    if not test_templates_first():
        print("\n❌ Template testing failed. Please fix templates before continuing.")
        return
    
    print("\n🎯 Now generating sample Bank of Nova Scotia products...")
    
    try:
        # Generate all example documents
        sp500_doc = await example_sp500_autocallable()
        bank_basket_doc = await example_canadian_bank_basket()
        tsx60_doc = await example_tsx60_note()
        
        print("\n" + "=" * 80)
        print("🎉 All Bank of Nova Scotia examples completed successfully!")
        print("\n📁 Generated Documents:")
        print("   1. scotia_sp500_autocallable.txt")
        print("   2. scotia_bank_basket_autocallable.txt") 
        print("   3. scotia_tsx60_protected.txt")
        
        print("\n💡 Next Steps:")
        print("   1. Review the generated documents in generated_documents/ism/")
        print("   2. Customize the product data above for your actual products")
        print("   3. Modify templates in large_text_templates.py as needed")
        print("   4. Use LargeTextISMAgent in your production systems")
        
        print("\n🛠️ Customization Options:")
        print("   • Modify CUSTOM_PLACEHOLDERS in large_text_templates.py")
        print("   • Add YOUR_CUSTOM_SECTION_TEMPLATE for additional content")
        print("   • Update variable mappings in large_text_integration.py")
        print("   • Create new product examples by copying the functions above")
        
    except Exception as e:
        print(f"\n❌ Error generating examples: {e}")
        print("   This might be due to missing API keys or configuration issues")
        print("   Check the error message and your setup")


if __name__ == "__main__":
    print("🚀 Starting Bank of Nova Scotia ISM Agent Examples...")
    asyncio.run(main())