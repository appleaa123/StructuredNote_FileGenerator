"""
Large Text Templates for PRS Agent

🎯 THIS IS WHERE YOU CUSTOMIZE YOUR PRS LARGE TEXT CHUNKS

INSTRUCTIONS:
1. Find the template sections below (marked with ⭐ CUSTOMIZE THIS ⭐)
2. Replace the example text with your exact content
3. Keep the [PLACEHOLDER] variables - they'll be replaced automatically
4. Test your changes using the functions at the bottom

AVAILABLE PLACEHOLDERS:
[Pricing Supplement Number] - The unique identification number for the pricing supplement. Format: 4-digit number.
[Pricing Supplement Date] - The date the pricing supplement is issued. Format: Month Day, Year.
[Note Name] - The specific brand or marketing name of the note series. Format: Text (e.g., BNS Canadian Insurance (AR) Index Autocallable Notes).
[Series Number] - The specific series identifier for the notes. Format: Alphanumeric (e.g., 109F, 452F, 5, 105).
[Currency Code] - The three-letter currency code for the offering. Format: CAD or USD.
[Currency Symbol] - The symbol for the currency of the offering. Format: $ or US$.
[Maximum Offering Size in Dollars] - The total principal amount of the offering. Format: Number with commas (e.g., 30,000,000).
[Maximum Number of Notes] - The total number of notes being offered. Format: Number with commas (e.g., 300,000).
[Maturity Date] - The date on which the notes are due to be repaid. Format: Month Day, Year.
[Asset Type] - The type of underlying asset the notes are linked to. Format: Equity or Index.
[Underlying Asset Name] - The specific name of the Index or Reference Portfolio. Format: Text (e.g., Solactive Canada Insurance 220 AR Index or "the Reference Portfolio").
[Target Asset(s) Name] - The name of the underlying target index or a list of the underlying reference shares. Format: Text or a list of company names.
[Synthetic Dividend] - The value of the synthetic dividend reduction for Adjusted Return (AR) Index notes. Format: Number (e.g., 220, 27, 115).
[Autocall Level/Price details] - The specific trigger level or price for an automatic call, which can vary by date. Format: Percentage and description (e.g., 100.00% of the Initial Index Level).
[First Possible Call Date] - The earliest date the notes can be automatically called. Format: Month Day, Year.
[Barrier/Buffer Level Percentage] - The downside protection threshold percentage. Format: Percentage (e.g., 60.00%, 70.00%, 80.00%).
[Initial Level/Price] - The term used for the starting value of the underlying asset. Format: "Initial Index Level" or "Initial Portfolio Price".
[Downside Risk Description] - A brief statement describing the investor's exposure to loss if the barrier is breached. Format: Text.
[Minimum Number of Notes] - The minimum quantity of notes for a subscription. Format: Number (e.g., 50).
[Fee per Note] - The selling concession or fee paid to investment dealers per note. Format: Dollar value (e.g., $3.00, $0.00).
[Agent Fee Cap per Note] - The maximum fee per note payable to the independent agent. Format: Dollar value (e.g., $0.15).
[Agent Fee Cap Percentage] - The maximum fee as a percentage of the principal payable to the independent agent. Format: Percentage (e.g., 0.15%).
[Independent Agent Name] - The full legal name of the firm acting as the independent agent. Format: Text (e.g., Wellington-Altus Private Wealth Inc.).
[Estimated Value per Note] - The bank's estimated value of a single note on the pricing date. Format: Dollar value (e.g., 96.20).
[Lead Investment Dealer] - The primary dealer for the offering. Format: Scotia Capital Inc.
[Co-Investment Dealer] - The secondary dealer or independent agent participating in the offering. Format: Full legal name.
[Issue Date] - The date on which the notes will be formally issued. Format: Month Day, Year.
[CUSIP Number] - The unique 9-character alphanumeric code identifying the security. Format: Alphanumeric (e.g., 06418YKC1).
[Fundserv Code] - The unique code used for processing through the Fundserv network. Format: Alphanumeric (e.g., SSP5542).
[Initial Valuation Date] - The date on which the initial level of the underlying asset is determined. Format: Month Day, Year.
[Final Valuation Date] - The date on which the final level of the underlying asset is determined for maturity calculation. Format: Month Day, Year.
[Table of Valuation, Payment, and Call Dates] - A formatted table outlining the schedule of valuation, payment, and call dates for the life of the note.
[Additional Return Formula] - The specific formula used to calculate the "Additional Return" portion of the Variable Return. Format: Mathematical expression.
[Table of Fixed Returns for each Valuation Date] - A formatted table specifying the fixed return percentage for each valuation period.
[Buffer Percentage] - The percentage of principal protected from loss in a buffer note. Format: Percentage (e.g., 20.00%).
[Buffered Return Adjuster] - The multiplier for calculating downside exposure below the buffer level. Format: Number (e.g., 1.25).
[Table of Early Trading Charges] - A formatted table outlining the charges for selling the note before a specified period.
[Table of Reference Shares and Weights] - A formatted table listing the underlying securities and their respective weights in a Reference Portfolio.
[Index Launch Date] - The date the primary index was launched. Format: Month Day, Year.
[Target Index Launch Date] - The date the target index was launched. Format: Month Day, Year.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Regulatory and Offering Disclaimers⭐
# =============================================================================

# 🔧 Regulatory and Offering Disclaimers
# ⭐ This is the standard set of legal disclaimers that appears on the first page of every pricing supplement. It clarifies the scope of the offering and regulatory status. ⭐


REGULATORY_AND_OFFERING_DISCLAIMERS = """
Regulatory and Offering Disclaimers

Pricing Supplement No. [Pricing Supplement Number] to the Short Form Base Shelf Prospectus dated March 4, 2024 and the Prospectus Supplement thereto dated March 5, 2024.

No securities regulatory authority has expressed an opinion about these securities and it is an offence to claim otherwise.

This pricing supplement together with the short form base shelf prospectus dated March 4, 2024 and the prospectus supplement dated March 5, 2024 to which it relates, as amended or supplemented, and each document incorporated by reference into such prospectus, constitutes a public offering of these securities only in those jurisdictions where they may be lawfully offered for sale and therein only by persons permitted to sell such securities.

The securities to be issued hereunder have not been, and will not be, registered under the United States Securities Act of 1933, as amended and, subject to certain exceptions, may not be offered, sold or delivered, directly or indirectly, in the United States of America or for the account or benefit of U.S. persons.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Offering Overview ⭐
# =============================================================================
# 💼 Offering Overview
# ⭐ This is the introductory paragraph on the first page that provides a high-level summary of the note offering, its linkage, and its key features like the autocall and barrier conditions. ⭐

Offering_Overview = """
Offering Overview

The Bank of Nova Scotia (the "Bank") is offering up to [Currency Symbol][Maximum Offering Size in Dollars] [Note Name], Series [Series Number] ([Currency Code]) (the "Notes").

The Notes are principal at risk notes that offer a return linked to the [Underlying Asset Name]. Whether there is a return on the Notes through the Variable Return and whether the Principal Amount is returned at maturity is based on the performance of the [Index/Reference Portfolio]. The return on the Notes will not reflect the total return that an investor would receive if such investor owned the securities included in the [Target Asset(s) Name].

The Notes will be automatically called (i.e., redeemed) by the Bank if the [Closing Index Level/Closing Portfolio Price] on any Autocall Valuation Date is greater than or equal to the [Autocall Level/Price details]. If the Notes are called, holders will receive both the Principal Amount and a Variable Return for the applicable Autocall Valuation Date. The Notes are callable on an annual basis and cannot be automatically called prior to [First Possible Call Date].

If the Notes are not automatically called by the Bank, and the [Final Index Level/Final Portfolio Price] on the Final Valuation Date is greater than or equal to the Autocall Level, holders will receive both the Principal Amount and a Variable Return. If the Notes are not automatically called by the Bank, the Notes provide contingent principal protection at maturity if the [Final Index Level/Final Portfolio Price] on the Final Valuation Date is greater than or equal to the [Barrier Level/Barrier Price] (which is [Barrier/Buffer Level Percentage]% of the [Initial Level/Price]). If the [Final Index Level/Final Portfolio Price] on the Final Valuation Date is less than the Barrier Level, [Downside Risk Description], meaning that substantially all of such holder's investment may be lost (subject to a minimum principal repayment of [Currency Symbol]1.00 per Note).
"""

# 📋 General Risks and Guarantees
# ⭐ This section, found on the first page, states that the notes are not insured deposits and that there are no guarantees of return or principal repayment. ⭐
General_Risks_and_Guarantees = """
General Risks and Guarantees

The Notes will not constitute deposits insured under the Canada Deposit Insurance Corporation Act or under any other deposit insurance regime.

An investment in the Notes involves risks. The Notes are not designed to be alternatives to fixed income or money market instruments. The Notes are only appropriate investments for persons who understand the risks associated with structured products and derivatives. The Notes are considered to be "specified derivatives" under applicable Canadian securities laws.

None of the Bank, the Investment Dealers or any of their respective affiliates, or any other person guarantees that investors in the Notes will receive an amount equal to their original investment (subject to a minimum principal repayment of [Currency Symbol]1.00 per Note), or guarantees that any return will be paid on the Notes, at or prior to maturity. The Maturity Redemption Amount will depend on the performance of the [Index/Reference Portfolio]. An investor could lose substantially all of his or her investment in the Notes (subject to a minimum principal repayment of [Currency Symbol]1.00 per Note). See "Risk Factors".
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Prospectus and Capitalized Terms ⭐
# =============================================================================
# 📊 Prospectus and Capitalized Terms
# ⭐ This section explains that the pricing supplement is part of a larger set of documents that constitute the full prospectus and defines where to find capitalized terms. ⭐

Prospectus_and_Capitalized_Terms = """
Prospectus and Capitalized Terms

The Notes described in this pricing supplement will be issued under the Bank's senior (principal at risk) note program and will be direct senior unsecured and unsubordinated debt securities. The Notes are described in three separate documents: (1) the base shelf prospectus, (2) the product supplement, and (3) this pricing supplement which contains the specific terms (including pricing information) about the Notes being offered, all of which, collectively, constitute the "prospectus" in respect of such Notes. Each of these documents should be read and considered carefully before a purchaser makes an investment decision in respect of the Notes. A copy of the prospectus for the Notes will be posted at www.scotianotes.com. Any capitalized terms used in this pricing supplement and not defined herein have the meaning ascribed to them in the product supplement or the base shelf prospectus, as the case may be.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Documents Incorporated by Reference ⭐
# =============================================================================
# ⚖️ Documents Incorporated by Reference
# ⭐ This is a standard legal clause that incorporates this pricing supplement and other filed documents into the base shelf prospectus, and explains how subsequent documents can modify or supersede prior statements. ⭐

Documents_Incorporated_by_Reference = """
Documents Incorporated by Reference

This pricing supplement is deemed to be incorporated by reference into the base shelf prospectus solely for the purpose of the Notes issued hereunder. Other documents are also incorporated or deemed to be incorporated by reference into the base shelf prospectus and reference should be made to the base shelf prospectus for full particulars. Any statement contained or contemplated in a document incorporated or deemed to be incorporated by reference in the base shelf prospectus or in this pricing supplement will be deemed to be modified or superseded for purposes of this pricing supplement to the extent that a statement contained herein or in any other subsequently filed document which also is or is deemed to be incorporated by reference in the base shelf prospectus or in this pricing supplement modifies or supersedes such statement. The modifying or superseding statement need not state that it has modified or superseded a prior statement or include any other information set forth in the document that it modifies or supersedes. The making of a modifying or superseding statement will not be deemed an admission for any purpose that the modified or superseded statement, when made, constituted a misrepresentation, an untrue statement of a material fact or an omission to state a material fact that is required to be stated or that is necessary to make a statement not misleading in light of the circumstances in which it was made. Any statement so modified or superseded will not be deemed, except as so modified or superseded, to constitute a part of this pricing supplement.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Deferred Payment ⭐
# =============================================================================
# ⚖️ Deferred Payment
# ⭐ This clause addresses compliance with the Criminal Code (Canada) regarding interest rate limits, stating that payments may be deferred to avoid exceeding the criminal rate.

Deferred_Payment = """
Deferred Payment
The following disclosure supersedes in its entirety the disclosure under "Deferred Payment" set forth at page 16 in the base shelf prospectus, and is deemed to be incorporated by reference into the base shelf prospectus. Under the Criminal Code (Canada), a lender is prohibited from entering into an agreement or arrangement to receive interest at an annual percentage rate of interest, calculated in accordance with generally accepted actuarial practices and principles, exceeding 35% of the credit advanced under the agreement or arrangement. This prohibition may not apply, depending on the amount of the credit advanced and, in certain circumstances, the annual percentage rate of interest received by the lender/investor on such credit advanced. The Bank will not, to the extent permitted by law, voluntarily claim the benefits of any laws concerning usurious rates of interest. If not permitted by law to do so, when any payment is to be made by the Bank to a holder of the Notes, payment of a portion of such amount may be deferred to ensure compliance with such laws, if applicable.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Forward-looking Statements ⭐
# =============================================================================
# ⚖️ Forward-looking Statements
# ⭐ This is a lengthy, standard "safe harbor" statement required under securities laws. It cautions readers about forward-looking statements and the various risks and uncertainties that could cause actual results to differ. The text is boilerplate and does not change between documents.

Forward_looking_Statements = """
Forward-looking Statements
From time to time, the Bank's public communications include oral or written forward-looking statements. Statements of this type are included in this document, and may be included in other filings with Canadian securities regulators or the U.S. Securities and Exchange Commission (the "SEC"), or in other communications. In addition, representatives of the Bank may include forward-looking statements orally to analysts, investors, the media and others. All such statements are made pursuant to the "safe harbor" provisions of the U.S. Private Securities Litigation Reform Act of 1995 and any applicable Canadian securities legislation. Forward-looking statements may include, but are not limited to, statements made in this document, the Management's Discussion and Analysis in the Bank's 2024 Annual Report under the headings "Outlook" and in other statements regarding the Bank's objectives, strategies to achieve those objectives, the regulatory environment in which the Bank operates, anticipated financial results, and the outlook for the Bank's businesses and for the Canadian, U.S. and global economies. Such statements are typically identified by words or phrases such as "believe," "expect," "aim," "achieve," "foresee," "forecast," "anticipate," "intend," "estimate," "outlook," "seek," "schedule," "plan," "goal," "strive," "target," "project," "commit," "objective," and similar expressions of future or conditional verbs, such as "will," "may," "should," "would," "might," "can" and "could" and positive and negative variations thereof. By their very nature, forward-looking statements require the Bank to make assumptions and are subject to inherent risks and uncertainties, which give rise to the possibility that the Bank's predictions, forecasts, projections, expectations or conclusions will not prove to be accurate, that the Bank's assumptions may not be correct and that the Bank's financial performance objectives, vision and strategic goals will not be achieved. The Bank cautions readers not to place undue reliance on these statements as a number of risk factors, many of which are beyond the Bank's control and effects of which can be difficult to predict, could cause the Bank's actual results to differ materially from the expectations, targets, estimates or intentions expressed in such forward-looking statements.

...[This section continues with a detailed list of risk factors, which is identical across all documents]...

Any forward-looking statements contained in the 2024 Annual Report represent the views of management only as of the date thereof and are presented for the purpose of assisting the Bank's shareholders and analysts in understanding the Bank's financial position, objectives and priorities, and anticipated financial performance as at and for the periods ended on the dates presented, and may not be appropriate for other purposes. Except as required by law, the Bank does not undertake to update any forward-looking statements, whether written or oral, that may be made from time to time by or on its behalf. Additional information relating to the Bank, including the Bank's Annual Information Form, can be located on the SEDAR+ website at www.sedarplus.ca and on the EDGAR section of the SEC's website at www.sec.gov.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Suitability for Investment ⭐
# =============================================================================
# ⚖️ Suitability for Investment
# This section provides guidance on the type of investor for whom the notes may be suitable. The introductory sentence and the closing sentence are standard, while the bullet points are customized to reflect the specific features of the note.

Suitability_for_Investment = """
Suitability for Investment
Investors should independently determine, with their own advisors, whether an investment in the Notes is suitable for them having regard to their own investment objectives and expectations and the risk factors described under "Risk Factors" in this pricing supplement, the base shelf prospectus and the product supplement.

The Notes may be suitable for investors:
- [Customized bullet point regarding investment strategy]
- [Customized bullet point regarding risk/return profile and linkage to equity markets]
- [Customized bullet point regarding understanding the underlying asset and lack of direct ownership]
- [Customized bullet point regarding point-to-point measurement and foregoing dividends]
- [Customized bullet point regarding investment horizon and autocall risk]
- [Customized bullet point regarding risk of loss below the barrier/buffer]
- [Customized bullet point regarding credit risk]
- who have carefully considered the risks associated with an investment in the Notes; and
- willing to assume the credit risk of the Bank.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Appendix C: Certain Canadian Federal Income Tax Considerations ⭐
# =============================================================================
# ⚖️ Appendix C: Certain Canadian Federal Income Tax Considerations
# ⭐  This is a standard legal opinion from the Bank's counsel regarding the tax implications for a specific type of Canadian investor. This entire section is boilerplate and does not change between notes of the same currency.

Appendix_C_Certain_Canadian_Federal_Income_Tax_Considerations = """
Appendix C: Certain Canadian Federal Income Tax Considerations

In the opinion of Stikeman Elliott LLP, counsel to the Bank, the following is, as of the date hereof, a summary of the principal Canadian federal income tax considerations generally applicable to the acquisition, holding and disposition of the Notes by an investor who purchases the Notes at the time of their issuance. This summary is applicable only to an investor who, for the purposes of the Income Tax Act (Canada) (the "Act") and at all relevant times, is an individual (other than a trust), is or is deemed to be resident in Canada, deals at arm's length with the Bank and the Investment Dealers, is not affiliated with the Bank and holds the Notes as capital property (a "Resident Initial Investor").

...[This section continues with several paragraphs of detailed tax information which is identical across all documents of the same currency]...

Investors should consult their own tax advisors for advice with respect to the income tax consequences of an investment in the Notes, based on their particular circumstances.
"""

# =============================================================================
# ⭐ TEMPLATE MANAGEMENT FUNCTIONS ⭐
# =============================================================================

from typing import Dict, List


def list_canonical_section_keys() -> List[str]:
    """
    Return the canonical section keys exposed by this module.
    These keys are the stable identifiers that other components should use.
    """
    return [
        "regulatory_and_offering_disclaimers",
        "offering_overview",
        "general_risks_and_guarantees",
        "prospectus_and_capitalized_terms",
        "documents_incorporated_by_reference",
        "deferred_payment",
        "forward_looking_statements",
        "suitability_for_investment",
        "appendix_c_certain_canadian_federal_income_tax_considerations",
    ]


def get_template(template_name: str, audience: str = "retail") -> str:
    """
    Get a canonical template by name.

    Supported canonical names are provided by list_canonical_section_keys().
    The audience parameter is accepted for API compatibility.
    """
    canonical_templates: Dict[str, str] = {
        "regulatory_and_offering_disclaimers": REGULATORY_AND_OFFERING_DISCLAIMERS,
        "offering_overview": Offering_Overview,
        "general_risks_and_guarantees": General_Risks_and_Guarantees,
        "prospectus_and_capitalized_terms": Prospectus_and_Capitalized_Terms,
        "documents_incorporated_by_reference": Documents_Incorporated_by_Reference,
        "deferred_payment": Deferred_Payment,
        "forward_looking_statements": Forward_looking_Statements,
        "suitability_for_investment": Suitability_for_Investment,
        "appendix_c_certain_canadian_federal_income_tax_considerations": Appendix_C_Certain_Canadian_Federal_Income_Tax_Considerations,
    }

    return canonical_templates.get(template_name, "Template not found.")


def customize_template(template: str, variables: dict) -> str:
    """
    Customize template with variables.
    
    Args:
        template: Template content
        variables: Variables to substitute
        
    Returns:
        Customized template
    """
    customized = template
    for placeholder, value in variables.items():
        placeholder_key = f"[{placeholder}]"
        if placeholder_key in customized:
            customized = customized.replace(placeholder_key, str(value))
    return customized


def create_complete_document_from_templates(product_data: dict, audience: str = "retail") -> dict:
    """
    Create a complete document using canonical large text templates.

    Args:
        product_data: Variables to substitute into templates. Keys must match
                      placeholders exactly as used in the customized sections.
        audience: Accepted for API compatibility.

    Returns:
        Dict[str, str]: Canonical section key -> customized content
    """
    # Pull canonical templates
    sections = {key: get_template(key, audience) for key in list_canonical_section_keys()}

    # Perform variable substitution without altering the original templates
    document = {key: customize_template(template, product_data) for key, template in sections.items()}

    return document


# =============================================================================
# ⭐ TESTING YOUR CUSTOMIZATIONS ⭐
# =============================================================================

def test_your_templates():
    """
    Test your customized templates with sample data.
    
    ⭐ MODIFY THE SAMPLE DATA BELOW to match your actual pricing information ⭐
    """
    # Sample PRS test data
    your_sample_data = {
        # Provide only a minimal subset; unresolved placeholders are okay for this quick test
        "Pricing Supplement Number": "0123",
        "Pricing Supplement Date": "January 29, 2025",
        "Note Name": "Canadian Insurance (AR) Index Autocallable Notes",
        "Series Number": "2025-1",
        "Currency Code": "USD",
        "Currency Symbol": "US$",
        "Maximum Offering Size in Dollars": "100,000,000",
        "Underlying Asset Name": "Solactive Canada Insurance 220 AR Index",
        "Target Asset(s) Name": "Solactive Canada Insurance 220 AR Index",
        "Autocall Level/Price details": "100.00% of the Initial Index Level",
        "First Possible Call Date": "January 31, 2026",
        "Barrier/Buffer Level Percentage": "70.00%",
        "Initial Level/Price": "Initial Index Level",
        "Downside Risk Description": "the holder will be fully exposed to the decline in the Index",
        "Independent Agent Name": "Wellington-Altus Private Wealth Inc.",
        "Estimated Value per Note": "96.20",
        "Lead Investment Dealer": "Scotia Capital Inc.",
        "Issue Date": "January 31, 2025",
        "Final Valuation Date": "January 28, 2032",
    }
    
    print("🧪 Testing PRS Large Text Templates")
    print("=" * 50)
    
    # Test template generation
    document = create_complete_document_from_templates(your_sample_data, "retail")
    
    print("✅ Templates generated successfully!")
    for key in list_canonical_section_keys():
        print(f"📄 {key}: {len(document[key])} characters")
    
    return document


if __name__ == "__main__":
    test_your_templates() 