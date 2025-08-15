import os
import asyncio
from datetime import date

from dotenv import load_dotenv

from agents.investor_summary import ISMAgent
from agents.investor_summary.models import ISMInput


async def run_example() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set. Please add it to your .env or environment.")
        return

    ism_agent = ISMAgent()

    input_data = ISMInput(
        issuer="Global Finance Inc.",
        product_name="S&P 500 Autocallable Note",
        underlying_asset="S&P 500 Index",
        currency="USD",
        principal_amount=100000.00,
        issue_date=date(2024, 8, 1),
        maturity_date=date(2029, 8, 1),
        product_type="autocallable",
        barrier_level=60.0,
        coupon_rate=8.5,
        target_audience="retail_investors",
        risk_tolerance="medium",
        investment_objective="capital_growth_with_income",
        regulatory_jurisdiction="US",
        distribution_method="broker_dealer_network",
    )

    result = await ism_agent.generate_document(input_data)
    print("\n✅ ISM document generated. Key fields:")
    print(f"document_title: {result.document_title}")
    print(f"executive_summary: {result.executive_summary[:120]}...")


if __name__ == "__main__":
    asyncio.run(run_example())


