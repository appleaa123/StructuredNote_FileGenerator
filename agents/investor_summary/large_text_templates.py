"""
Large Text Templates for ISM Agent

🎯 THIS IS WHERE YOU CUSTOMIZE YOUR LARGE TEXT CHUNKS

INSTRUCTIONS:
1. Find the template sections below (marked with ⭐ CUSTOMIZE THIS ⭐)
2. Replace the example text with your exact content
3. Keep the [PLACEHOLDER] variables - they'll be replaced automatically
4. Test your changes using the functions at the bottom

AVAILABLE PLACEHOLDERS:
[Note Title] - The full, official name of the structured note, including the series and currency
[Maturity Date]] - The final maturity date of the note
[Document Date] - The date the investor summary document is created
[Pricing Supplement Number] - The unique number assigned to the pricing supplement
[Pricing Supplement Date] - The date the pricing supplement was issued
[Underlying Asset Type] - The heading for the asset section. Use "Reference Portfolio and Reference Companies" for baskets of stocks or "Index" for index-linked notes.
[Underlying Asset Description] - A detailed description of the underlying asset. For a basket, describe the portfolio, number of companies, weighting, and list the companies. For an index, provide the full index name and a brief description.
[Underlying Asset Name] - The short name of the asset, used in sentences
[levels/prices] - Use "levels" for an index and "prices" for a stock basket.
[Closing Level/Price Name] - The term for the asset's value on a given day (e.g., "Closing Portfolio Price", "Closing Index Level").
[Autocall Level/Price Name] - The term for the autocall trigger value (e.g., "Autocall Price", "Autocall Level").
[First Call Date] - The earliest date the note can be automatically called (e.g., "January 29, 2026").
[Additional Return Percentage] - The participation rate in any upside beyond the fixed return (e.g., "5.00%").
[Return Calculation Metric Name] - The name of the return calculation (e.g., "Price Return", "Index Return").
[Valuation Date 1-6] - The specific dates for each autocall valuation.
[Fixed Return 1-6] - The cumulative fixed return percentage for each corresponding valuation date.
[Final Fixed Return] - The cumulative fixed return percentage for the final valuation date.
[Autocall Level/Price Term] - The heading for this term. Use "Autocall Price" or "Autocall Level".
[Autocall Level/Price Description] - The full description of how the autocall trigger is determined (e.g., "100.00% of the Initial Portfolio Price").
[Return Calculation Metric Term] - The heading for this term. Use "Price Return" or "Index Return".
[Contingent Principal Protection Percentage]: The percentage of protection provided (e.g., "20.00%", "30.00%").
[Final Level/Price Name] - The term for the asset's value at maturity (e.g., "Final Portfolio Price", "Final Index Level").
[Barrier Level/Price Name] - The term for the protection barrier (e.g., "Barrier Price", "Barrier Level").
[Barrier Percentage] - The percentage of the initial value that defines the barrier (e.g., "80.00%", "70.00%").
[Initial Level/Price Name] - The term for the starting value of the asset (e.g., "Initial Portfolio Price", "Initial Index Level").
[Barrier Level/Price Term] - The heading for this term. Use "Barrier Price" or "Barrier Level".
[Fundserv Code] - The note's Fundserv code (e.g., "SSP5525").
[Available Until Date] - The last day to purchase the note (e.g., "January 23, 2025").
[Issue Date] - The date the note is issued (e.g., "January 29, 2025").
[Term] - The full term of the note if not called early (e.g., "7 years").
[CUSIP Code] - The CUSIP number for the note (e.g., "06418YJF6").
[Initial Valuation Date] - The date the initial value of the underlying asset is recorded.
[Final Valuation Date] - The date the final value of the underlying asset is recorded for maturity calculation.
[Fees and Expenses Description] - A paragraph detailing the selling concession fees and any independent agent fees. This can vary significantly between notes.
[Independent Agent Name] - The name of the firm acting as the independent agent (e.g., "Desjardins Securities Inc.", "Wellington-Altus Private Wealth Inc.").
[Asset Manager Name] - The name of the asset manager (e.g., "Bank of Nova Scotia").
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: EXECUTIVE SUMMARY TEMPLATES ⭐
# =============================================================================

# 🔧 RETAIL INVESTOR EXECUTIVE SUMMARY
# ⭐ REPLACE THIS ENTIRE TEXT with your own executive summary for retail investors ⭐
EXECUTIVE_SUMMARY_RETAIL = """
[Note Title]
Principal at Risk Notes - Due [Maturity Date]
[Document Date]

The Bank of Nova Scotia short form base shelf prospectus dated March 4, 2024, a prospectus supplement thereto dated March 5, 2024 and pricing supplement No. [Pricing Supplement Number] (the "pricing supplement") thereto dated [Pricing Supplement Date] (collectively, the "Prospectus") have been filed with the securities regulatory authorities in each of the provinces and territories of Canada. A copy of the Prospectus and any amendments or supplements thereto that have been filed are required to be delivered with this document. The Prospectus and any amendments or supplements thereto contain important information relating to the securities described in this document. This document does not provide full disclosure of all material facts relating to the securities offered and investors should read the Prospectus, and any amendments or supplements thereto, for disclosure of those facts, especially risk factors relating to the securities offered, before making an investment decision. A copy of the short form base shelf prospectus, the prospectus supplement and the pricing supplement can also be obtained at www.sedarplus.ca. Unless the context otherwise requires, terms not otherwise defined herein will have the meaning ascribed thereto in the Prospectus.
Linked to [Asset Manager Name]
Contingent Coupon Payments of up to [Final Fixed Return]
Quarterly autocall at [Additional Return Percentage]
[Contingent Principal Protection Percentage] Contingent Principal Protection at Maturity
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: KEY TERMS TEMPLATES ⭐
# =============================================================================
# 💼 KEY TERMS  
# ⭐ REPLACE THIS ENTIRE TEXT with your own executive summary for institutional investors ⭐

KEY_TERMS = """
Issuer
The Bank of Nova Scotia (the "Bank").

[Underlying Asset Type]
[Underlying Asset Description]

Autocall
The Notes will be automatically called (i.e., redeemed) by the Bank if the [Closing Level/Price Name] on any Autocall Valuation Date is greater than or equal to the [Autocall Level/Price Name]. If the Notes are called, holders will receive both the Principal Amount and a Variable Return for the applicable Autocall Valuation Date. The Notes are callable on an annual basis and cannot be automatically called prior to [First Call Date]. If the [Closing Level/Price Name] on any Autocall Valuation Date is not greater than or equal to the applicable [Autocall Level/Price Name], the Notes will not be automatically called by the Bank and the Variable Return will not be paid to holders in respect of such Autocall Valuation Date.

Potential Variable Return
The Variable Return, if any, applicable to each respective Valuation Date will be calculated using the following formula:

Principal Amount x (Fixed Return + Additional Return)

The Additional Return, if any, is equal to [Additional Return Percentage] of the amount by which the [Return Calculation Metric Name] on the applicable Valuation Date exceeds the applicable Fixed Return, calculated using the formula below:

[Additional Return Percentage] x ([Return Calculation Metric Name] - Fixed Return)

If the [Return Calculation Metric Name] on the applicable Valuation Date is equal to or less than the applicable Fixed Return, no Additional Return will be paid on the Notes.

The Fixed Return used in the calculation of the Variable Return, if any, and the calculation of the Additional Return, if any, for each Valuation Date will be as follows:
AUTOCALL PAYMENT SCHEDULE
┌────────────────────────┬──────────────────────────────────┬──────────────────┐
│ Valuation Date         │ Autocall Level                   │ Fixed Return     │
├────────────────────────┼──────────────────────────────────┼──────────────────┤
│ [Valuation Date 1]     │ [Autocall Level/Price Description] │ [Fixed Return 1] │
│ [Valuation Date 2]     │ [Autocall Level/Price Description] │ [Fixed Return 2] │
│ [Valuation Date 3]     │ [Autocall Level/Price Description] │ [Fixed Return 3] │
│ [Valuation Date 4]     │ [Autocall Level/Price Description] │ [Fixed Return 4] │
│ [Valuation Date 5]     │ [Autocall Level/Price Description] │ [Fixed Return 5] │
│ [Valuation Date 6]     │ [Autocall Level/Price Description] │ [Fixed Return 6] │
│ Final Valuation Date   │ [Autocall Level/Price Description] │ [Final Fixed Return] │
└────────────────────────┴──────────────────────────────────┴──────────────────┘

Contingent Principal Protection
[Contingent Principal Protection Percentage] contingent principal protection. The Notes provide contingent principal protection at maturity if the [Final Level/Price Name] on the Final Valuation Date is greater than or equal to the [Barrier Level/Price Name] (which is [Barrier Percentage] of the [Initial Level/Price Name]). If the [Final Level/Price Name] on the Final Valuation Date is less than the [Barrier Level/Price Name], a holder of the Notes will be fully exposed to any negative performance of the [Underlying Asset Name], meaning that substantially all of such holder's investment may be lost (subject to a minimum principal repayment of $1.00 per Note).

KEY TERMS SUMMARY
┌───────────────────┬─────────────────────────────┐
│ Fundserv          │ [Fundserv Code]             │
│ Available Until   │ [Available Until Date]      │
│ Issue Date        │ [Issue Date]                │
│ Term to Maturity  │ [Term] (if not called)      │
└───────────────────┴─────────────────────────────┘

CONTACT INFORMATION
┌────────────────────────────────────────┬──────────────────┐
│ Sales and Marketing                    │ 1-866-416-7891   │
│ Fundserv Customer Service for Advisors │ 1-833-594-3143   │
└────────────────────────────────────────┴──────────────────┘
"""

# 📋 ADDITIONAL KEY TERMS
# ⭐ REPLACE THIS ENTIRE TEXT with your own detailed product explanation ⭐
ADDITIONAL_KEY_TERMS = """

Principal Amount
$100.00 per Note.

Minimum Investment
$5,000 (50 Notes).

CUSIP
[CUSIP Code]

Fundserv Code
[Fundserv Code]

Initial Valuation Date
[Initial Valuation Date] (the "Initial Valuation Date"), provided that if such day is not an Exchange Business Day then the Initial Valuation Date will be the first succeeding day that is an Exchange Business Day, subject to the occurrence of any special circumstances (see "Special Circumstances" in the pricing supplement).

Final Valuation Date
[Final Valuation Date] (the "Final Valuation Date"), provided that if such day is not an Exchange Business Day then the Final Valuation Date will be the immediately preceding Exchange Business Day, subject to the Notes being automatically called and the occurrence of any special circumstances (see "Special Circumstances" in the pricing supplement).

Valuation Dates, Payment Dates and Call Dates
The specific Valuation Dates, Payment Dates and Call Dates for the Notes will be as indicated in the table below, subject to the occurrence of any special circumstances (see "Special Circumstances" in the pricing supplement) and the Notes being automatically called by the Bank. The Notes are callable on an annual basis and cannot be automatically called by the Bank prior to [First Call Date].

VALUATION AND PAYMENT SCHEDULE
┌──────────────────────────────────────────┬──────────────────────────────────┐
│ Valuation Date                           │ Payment Date/Call Date           │
├──────────────────────────────────────────┼──────────────────────────────────┤
│ [Valuation Date 1]                       │ [Payment Date 1]                 │
│ [Valuation Date 2]                       │ [Payment Date 2]                 │
│ [Valuation Date 3]                       │ [Payment Date 3]                 │
│ [Valuation Date 4]                       │ [Payment Date 4]                 │
│ [Valuation Date 5]                       │ [Payment Date 5]                 │
│ [Valuation Date 6]                       │ [Payment Date 6]                 │
│ [Final Valuation Date] (Final Valuation Date) │ [Maturity Date] (Maturity Date)    │
└──────────────────────────────────────────┴──────────────────────────────────┘

Each of the Valuation Dates (other than the Final Valuation Date) is an "Autocall Valuation Date". Unless the Notes are automatically called by the Bank prior to maturity, the Maturity Date is the last Payment Date. If the Notes are automatically called (i.e., redeemed) by the Bank on any Call Date prior to the Maturity Date, the Notes will be cancelled, all amounts due shall be paid to holders on the applicable Payment Date and holders will not be entitled to receive any subsequent payments in respect of the Notes.

If an Autocall Valuation Date is not an Exchange Business Day then the Autocall Valuation Date will be the immediately preceding Exchange Business Day, subject to the occurrence of any special circumstances (see "Special Circumstances" in the pricing supplement). If a Payment Date, a Call Date or the Maturity Date is not a Business Day then the related payment the Bank is obligated to make on such day, if any, will be paid to the holder on the immediately following Business Day, subject to the occurrence of any special circumstances (see "Special Circumstances" in the pricing supplement), and no interest shall be paid in respect of such delay.

Maturity Redemption Amount
Holders of record will be entitled to an amount payable per Note if the Notes are automatically called by the Bank, or at maturity, as the case may be (in each case, the "Maturity Redemption Amount") as calculated by the Calculation Agent in accordance with the applicable formula below:

If the [Closing Level/Price Name] on an Autocall Valuation Date or the [Final Level/Price Name] on the Final Valuation Date is greater than or equal to the applicable [Autocall Level/Price Name], the Maturity Redemption Amount will equal:
Principal Amount + Variable Return

If the [Final Level/Price Name] on the Final Valuation Date is less than the [Autocall Level/Price Name] but greater than or equal to the [Barrier Level/Price Name], the Maturity Redemption Amount will equal:
Principal Amount

If the [Final Level/Price Name] on the Final Valuation Date is less than the [Barrier Level/Price Name], the Maturity Redemption Amount will equal:
Principal Amount + (Principal Amount x [Return Calculation Metric Name])

The Maturity Redemption Amount will be substantially less than the Principal Amount invested by an investor if the [Final Level/Price Name] on the Final Valuation Date is less than the [Barrier Level/Price Name]. The Maturity Redemption Amount will be subject to a minimum principal repayment of $1.00 per Note.

[Autocall Level/Price Term]
[Autocall Level/Price Description]

[Barrier Level/Price Term]
[Barrier Percentage] of the [Initial Level/Price Name].

[Return Calculation Metric Term]
The [Return Calculation Metric Name] is an amount expressed as a percentage (which can be zero, positive or negative) calculated by the Calculation Agent in accordance with the following formula:
([Final Level/Price Name] - [Initial Level/Price Name]) / [Initial Level/Price Name]

Listing and Secondary Market
The Notes will not be listed on any exchange or marketplace. Scotia Capital Inc. will use reasonable efforts under normal market conditions to provide a daily secondary market for the sale of the Notes but reserves the right to elect not to do so at any time in the future, in its sole and absolute discretion, without prior notice to holders.

Early Trading Charge
[Include this section if applicable]

EARLY TRADING CHARGE SCHEDULE
┌───────────────────────────┬────────────────────────────────────────┐
│ If Sold Within            │ Early Trading Charge (% of Principal Amount) │
├───────────────────────────┼────────────────────────────────────────┤
│ 0-90 days of Issue Date   │ [Early Trading Charge 0-90 Days]       │
│ 91-180 days of Issue Date │ [Early Trading Charge 91-180 Days]     │
│ Thereafter                │ Nil                                    │
└───────────────────────────┴────────────────────────────────────────┘

Eligibility for Investment
Eligible for RRSPs, RRIFs, RESPs, RDSPs, DPSPs, TFSAs and FHSAs.

Fees and Expenses
[Fees and Expenses Description]
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: SCENARIOS TEMPLATES ⭐
# =============================================================================

# 📊 DETAILED MARKET SCENARIOS
# ⭐ REPLACE THIS ENTIRE TEXT with your own scenario analysis and market projections ⭐
HYPOTHETICAL_EXAMPLES = """
EYPOTHETICAL EXAMPLES

The following hypothetical examples show how the Variable Return and Maturity Redemption Amount would be calculated and determined based on certain
hypothetical values and assumptions that are set out below. These examples are for illustrative purposes only and should not be construed as an estimate or
forecast of the performance of the Index or the return that an investor might realize on the Notes. The return on the Notes will be calculated based on the
performance of the Index, which reflects the gross total return performance of the Target Index as reduced by the Adjusted Return Factor. Certain dollar amounts
are rounded to the nearest whole cent and “$” refers to the relevant currency for the specific hypothetical dollar amounts and hypothetical prices that the context
requires.

Example #1 - The Notes are not automatically called as the Closing Index Level on each Autocall Valuation Date is less than the Autocall Level. The Final Index
Level on the Final Valuation Date is less than the Barrier Level and no Variable Return is payable.

Example #2 - The Notes are not automatically called as the Closing Index Level on each Autocall Valuation Date is less than the Autocall Level. The Final Index
Level on the Final Valuation Date is less than the Autocall Level, but greater than or equal to the Barrier Level and no Variable Return is payable.

Example #3 - The Notes are not automatically called as the Closing Index Level on each Autocall Valuation Date is less than the Autocall Level. The Final Index
Level on the Final Valuation Date is greater than or equal to the Autocall Level and a Variable Return is payable consisting of a Fixed Return only. No
Additional Return is payable as the Index Return is less than or equal to the Fixed Return.

Example #4 - The Notes are not automatically called on the 2026 or 2027 Autocall Valuation Dates as the Closing Index Level is less than the Autocall Level.
The Notes are automatically called on the 2028 Autocall Valuation Date as the Closing Index Level is greater than or equal to the Autocall Level and a Variable
Return is payable consisting of a Fixed Return and an Additional Return as the Index Return is greater than the Fixed Return.

Example #5 - The Notes are automatically called on the 2026 Autocall Valuation Date as the Closing Index Level is greater than or equal to the Autocall Level
and a Variable Return is payable consisting of a Fixed Return only. No Additional Return is payable as the Index Return is less than the Fixed Return.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: DISCLAIMER TEMPLATES ⭐
# =============================================================================

# 📜 COMPREHENSIVE LEGAL DISCLAIMERS
# ⭐ REPLACE THIS ENTIRE TEXT with your own legal disclaimers and regulatory notices ⭐
# ⚠️ IMPORTANT: Make sure to include all required regulatory language for your jurisdiction
DISCLAIMER = """
DISCLAIMER
No securities regulatory authority has in any way passed upon the merits of the securities referred to herein and any representation to the contrary is an offence. The Notes are not principal protected (subject to a minimum principal repayment of $1.00 per Note) and an investor may receive substantially less than the original principal amount at maturity. A person should reach a decision to invest in the Notes only after carefully considering, with his or her investment, legal, accounting, tax and other advisors, the suitability of the Notes in light of his or her investment objectives and the information set out in the Prospectus. The Bank, the Calculation Agent, Scotia Capital Inc. and [Independent Agent Name] make no recommendation as to the suitability of the Notes for investment by any particular person. The Notes have not been, and will not be, registered under the United States Securities Act of 1933, as amended (the "1933 Act"), or any State securities laws and, subject to certain exceptions, may not be offered for sale, sold or delivered, directly or indirectly, in the United States, its territories or possessions or to or for the account or benefit of U.S. persons within the meaning of Regulation S under the 1933 Act. In addition, the Notes may not be offered or sold to residents of any jurisdiction or country in Europe. "Scotiabank" and "Scotiabank Global Banking and Markets" are registered trademarks of The Bank of Nova Scotia. Scotia Capital Inc. is a wholly-owned subsidiary of The Bank of Nova Scotia.

Amounts paid to holders of the Notes will depend on the performance of the underlying interests. Unless otherwise specified in the Prospectus, the Bank does not guarantee that any of the principal amount of the Notes will be paid, or guarantee that any return will be paid on the Notes, at or prior to maturity (in each case, subject to a minimum principal repayment of $1.00 per Note). Purchasers could lose substantially all of their investment in the Notes. The Notes are not appropriate investments for persons who do not understand the risks associated with structured products or derivatives. A purchaser of the Notes will be exposed to fluctuations and changes in the [levels/prices] of the [Underlying Asset Name] to which the Notes are linked. The [Underlying Asset Name] [levels/prices] may be volatile and an investment linked to [Underlying Asset Name] [levels/prices] may also be volatile. Purchasers should read carefully the "Risk Factors" sections in the Prospectus.

The Notes will not constitute deposits under the Canada Deposit Insurance Corporation Act or under any other deposit insurance regime. The Notes have not been rated and will not be insured by the Canada Deposit Insurance Corporation or any other entity and therefore the payments to investors will be dependent upon the financial health and creditworthiness of the Bank.

Scotia Capital Inc. is a wholly owned subsidiary of the Bank. Consequently, the Bank is a related and connected issuer of Scotia Capital Inc. within the meaning of applicable securities legislation. See "Plan of Distribution" in the Prospectus.

The information contained herein, while obtained from sources believed to be reliable, is not guaranteed as to its accuracy or completeness.

[Use the following section for notes linked to a basket of shares]

THE REFERENCE COMPANIES AND THE REFERENCE SHARES
All information regarding the Reference Shares and the Reference Companies contained herein has been derived from publicly available sources and its accuracy cannot be guaranteed. The Notes are not in any way sponsored, endorsed, sold or promoted by the Reference Companies.

All information in the pricing supplement relating to the Reference Companies including the Reference Shares is derived from publicly available sources and is presented in the pricing supplement in summary form.

The return payable on the Notes is linked to the price performance of the Reference Shares of the Reference Companies. Accordingly, certain risk factors applicable to investors who invest directly in the Reference Shares are also applicable to an investment in the Notes to the extent that such risk factors could adversely affect the performance of the Reference Shares. Prospective investors are urged to conduct their own independent investigation of the Reference Companies prior to making any investment decision with respect to the Notes. The Bank is not affiliated with the Reference Companies and has not performed any due diligence investigation or review of the Reference Companies.

An investment in the Notes does not represent a direct or indirect investment in the Reference Shares or the Reference Companies and investors do not have an ownership or any other interest (including voting rights or the right to receive any dividends, distributions or other income or amounts accruing or paid thereon) in respect of such Reference Shares. Past performance of the Reference Companies or the Reference Shares is not indicative of future returns.

[Use the following section for notes linked to an index]

INDEX SPONSOR
The Index Sponsor and the Bank have entered into a non-exclusive license agreement providing for the license to the Bank, in exchange for a fee, of the right to use the Index and the Target Index, which are owned, calculated, administered and published by the Index Sponsor, in connection with the Notes.

The license agreement between the Index Sponsor and the Bank provides that the following language must be set forth herein:

The Notes are not sponsored, promoted, sold or supported in any other manner by the Index Sponsor nor does the Index Sponsor offer any express or implicit guarantee or assurance, either with regard to the results of using the Index, the Target Index and/or the trade marks of the Index and Target Index or the applicable "Index Price" (as defined in the license agreement) in respect of the Index and Target Index at any time or in any other respect. The Index and Target Index are calculated and published by the Index Sponsor. The Index Sponsor uses its best efforts to ensure that the Index and Target Index are calculated correctly. Irrespective of its obligations towards the Bank, the Index Sponsor has no obligation to point out errors in the Index and Target Index to third parties including but not limited to investors and/or financial intermediaries of the Notes. Neither publication of the Index and Target Index by the Index Sponsor nor the licensing of the Index and Target Index or the trade marks of the Index and Target Index for the purpose of use in connection with the Notes constitutes a recommendation by the Index Sponsor to invest capital in the Notes nor does it in any way represent an assurance or opinion of the Index Sponsor with regard to any investment in the Notes.

TRADEMARK NOTICE
T™ Trademark of The Bank of Nova Scotia, used under license (where applicable). Scotiabank is a marketing name for the global corporate and investment banking and capital markets businesses of The Bank of Nova Scotia and certain of its affiliates in the countries where they operate including Scotia Capital Inc. (Member-Canadian Investor Protection Fund and regulated by the Canadian Investment Regulatory Organization). Important legal information may be accessed at https://www.gbm.scotiabank.com/en/legal.html. Products and services described are available only by Scotiabank licensed entities in jurisdictions where permitted by law. This information is not directed to or intended for use by any person resident or located in any country where its distribution is contrary to its laws. Not all products and services are offered in all jurisdictions.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: ADD YOUR OWN VARIABLES AND PLACEHOLDERS ⭐
# =============================================================================

# 🔧 ADD YOUR CUSTOM PLACEHOLDERS HERE
# Add any additional placeholders you need for your templates
CUSTOM_PLACEHOLDERS = {
    # ⭐ ADD YOUR COMPANY-SPECIFIC PLACEHOLDERS ⭐
    "YOUR_COMPANY_NAME": "[YOUR_COMPANY_NAME]",      # Replace with your actual company name
    "YOUR_REGULATOR": "[YOUR_REGULATOR]",            # Replace with your regulator (e.g., "FCA", "SEC")
    "YOUR_PHONE": "[YOUR_PHONE]",                    # Replace with your contact phone
    "YOUR_EMAIL": "[YOUR_EMAIL]",                    # Replace with your contact email
    "YOUR_WEBSITE": "[YOUR_WEBSITE]",                # Replace with your website URL
    
    # ⭐ ADD YOUR PRODUCT-SPECIFIC PLACEHOLDERS ⭐
    "ISSUER_RATING": "[ISSUER_RATING]",              # Credit rating (e.g., "A+", "AA-")
    "ASSET_DESCRIPTION": "[ASSET_DESCRIPTION]",      # Detailed asset description
    "SELECTION_RATIONALE": "[SELECTION_RATIONALE]",  # Why this asset was chosen
    "MARKET_EXPOSURE": "[MARKET_EXPOSURE]",          # Type of market exposure
    "INDEX_SPONSOR": "[INDEX_SPONSOR]",              # Index sponsor
    "TRADEMARK_NOTICE": "[TRADEMARK_NOTICE]",        # Trademark notice
    
    # ⭐ ADD YOUR RISK-SPECIFIC PLACEHOLDERS ⭐
    "VOLATILITY_RANGE": "[VOLATILITY_RANGE]",        # Historical volatility range
    "STRESS_LOSS_PERCENTAGE": "[STRESS_LOSS_PERCENTAGE]",  # Loss in stress scenarios
    "BREACH_FREQUENCY": "[BREACH_FREQUENCY]",        # How often barriers are breached
    "PROBABILITY_ESTIMATE": "[PROBABILITY_ESTIMATE]", # Risk probability estimates
    "RISK_LEVEL": "[RISK_LEVEL]",                    # Risk level
    "OPTIMISTIC_PROBABILITY": "[OPTIMISTIC_PROBABILITY]", # Optimistic probability
    "BASE_CASE_PROBABILITY": "[BASE_CASE_PROBABILITY]", # Base case probability
    "STRESS_PROBABILITY": "[STRESS_PROBABILITY]",      # Stress probability
    "SEVERE_PROBABILITY": "[SEVERE_PROBABILITY]",      # Severe probability
    "HISTORICAL_FREQUENCY_STRONG": "[HISTORICAL_FREQUENCY_STRONG]", # Historical frequency strong
    
    # ⭐ ADD YOUR OWN CUSTOM PLACEHOLDERS HERE ⭐
    # "CUSTOM_FIELD_1": "[CUSTOM_FIELD_1]",
    # "CUSTOM_FIELD_2": "[CUSTOM_FIELD_2]",
}

# 📝 CUSTOM TEMPLATE SECTIONS
# ⭐ ADD YOUR OWN TEMPLATE SECTIONS HERE ⭐

# Example: Add your own custom section
YOUR_CUSTOM_SECTION_TEMPLATE = """
⭐ REPLACE THIS with your own custom section text ⭐

This is where you can add any additional sections you need:
- Special product features
- Company-specific information  
- Additional risk warnings
- Custom regulatory requirements
- Your own branded content

Use [PLACEHOLDERS] as needed and they'll be replaced automatically.
"""

# =============================================================================
# USAGE FUNCTIONS
# =============================================================================

def get_template(template_name: str, audience: str = "retail") -> str:
    """
    Get a specific template for a given audience.
    
    Args:
        template_name: Name of the template (e.g., 'executive_summary', 'risk_section')
        audience: Target audience ('retail', 'institutional', 'comprehensive')
    
    Returns:
        Template string with placeholders
    """
    
    templates = {
        "executive_summary": {
            "retail": EXECUTIVE_SUMMARY_RETAIL,
            "institutional": EXECUTIVE_SUMMARY_RETAIL  # Use retail for now, can be customized
        },
        "key_terms": {
            "detailed": KEY_TERMS
        },
        "additional_key_terms": {
            "detailed": ADDITIONAL_KEY_TERMS
        },
        "scenarios": {
            "detailed": HYPOTHETICAL_EXAMPLES
        },
        "disclaimer": {
            "comprehensive": DISCLAIMER
        }
    }
    
    if template_name in templates:
        if audience in templates[template_name]:
            return templates[template_name][audience]
        else:
            # Return first available template if audience not found
            return list(templates[template_name].values())[0]
    
    raise ValueError(f"Template '{template_name}' not found")


def customize_template(template: str, variables: dict) -> str:
    """
    Replace placeholders in template with actual values.
    
    Args:
        template: Template string with [PLACEHOLDER] variables
        variables: Dictionary mapping placeholder names to values
    
    Returns:
        Template with placeholders replaced
    """
    
    customized = template
    
    for placeholder, value in variables.items():
        # Handle both [PLACEHOLDER] and PLACEHOLDER formats
        placeholder_patterns = [
            f"[{placeholder}]",
            f"[{placeholder.upper()}]", 
            placeholder,
            placeholder.upper()
        ]
        
        for pattern in placeholder_patterns:
            customized = customized.replace(pattern, str(value))
    
    return customized


def create_complete_document_from_templates(product_data: dict, audience: str = "retail") -> dict:
    """
    Create a complete document using large text templates.
    
    Args:
        product_data: Dictionary with product information and variables
        audience: Target audience for template selection
    
    Returns:
        Dictionary with all document sections
    """
    
    # Get templates
    executive_summary = get_template("executive_summary", audience)
    key_terms = get_template("key_terms", "detailed")
    additional_key_terms = get_template("additional_key_terms", "detailed")
    scenarios = get_template("scenarios", "detailed")
    disclaimer = get_template("disclaimer", "comprehensive")
    
    # Customize with product data
    document = {
        "executive_summary": customize_template(executive_summary, product_data),
        "key_terms": customize_template(key_terms, product_data),
        "additional_key_terms": customize_template(additional_key_terms, product_data),
        "scenarios": customize_template(scenarios, product_data),
        "disclaimer": customize_template(disclaimer, product_data)
    }
    
    return document


# =============================================================================
# ⭐ TESTING YOUR CUSTOMIZATIONS ⭐
# =============================================================================

def test_your_templates():
    """
    Test your customized templates with sample data.
    
    ⭐ MODIFY THE SAMPLE DATA BELOW to match your actual product information ⭐
    """
    # Bank of Nova Scotia S&P 500 Autocallable Note test data
    your_sample_data = {
        # ===== DOCUMENT HEADER =====
        "Note Title": "S&P 500 Index Autocallable Notes - Series 2025",
        "Maturity Date": "January 29, 2032",
        "Document Date": "January 15, 2025",
        "Pricing Supplement Number": "PS-2025-001",
        "Pricing Supplement Date": "January 29, 2025",
        
        # ===== UNDERLYING ASSET =====
        "Underlying Asset Type": "Index",
        "Underlying Asset Description": "The S&P 500 Index, a broad market index representing large-cap U.S. equities with strong historical performance and liquidity characteristics.",
        "Underlying Asset Name": "S&P 500 Index",
        "levels/prices": "levels",
        "Closing Level/Price Name": "Closing Index Level",
        "Autocall Level/Price Name": "Autocall Level",
        "Final Level/Price Name": "Final Index Level",
        "Barrier Level/Price Name": "Barrier Level",
        "Initial Level/Price Name": "Initial Index Level",
        
        # ===== PRODUCT TERMS =====
        "First Call Date": "January 29, 2026",
        "Additional Return Percentage": "5.00%",
        "Return Calculation Metric Name": "Index Return",
        "Contingent Principal Protection Percentage": "30.00%",
        "Barrier Percentage": "70.00%",
        "Final Fixed Return": "59.50%",
        
        # ===== AUTOCALL SCHEDULE =====
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
        
        # ===== PRODUCT DETAILS =====
        "Fundserv Code": "SSP2501",
        "Available Until Date": "January 22, 2025",
        "Issue Date": "January 29, 2025",
        "Term": "7 years",
        "CUSIP Code": "06418YJF6",
        "Initial Valuation Date": "January 29, 2025",
        "Final Valuation Date": "January 29, 2032",
        
        # ===== FEES AND PARTIES =====
        "Fees and Expenses Description": "The selling concession to be paid by the Bank to Scotia Capital Inc. will be 2.50% of the Principal Amount per Note. An independent agent fee of 1.25% of the Principal Amount per Note will be paid to the Independent Agent.",
        "Independent Agent Name": "Scotia Capital Inc.",
        "Asset Manager Name": "Bank of Nova Scotia",
        
        # ===== SCOTIA COMPANY INFORMATION =====
        "YOUR_COMPANY_NAME": "The Bank of Nova Scotia",
        "YOUR_REGULATOR": "Canadian Securities Regulators",
        "YOUR_PHONE": "1-866-416-7891",
        "YOUR_EMAIL": "structured.products@scotiabank.com",
        "YOUR_WEBSITE": "www.gbm.scotiabank.com",
        
        # ===== LEGACY VARIABLES =====
        "PRODUCT_NAME": "S&P 500 Index Autocallable Notes",
        "UNDERLYING_ASSET": "S&P 500 Index",
        "DOLLAR_AMOUNT": "$100,000",
        "PERCENTAGE": "8.5",
        "TIME_PERIOD": "7 years",
        "BARRIER_PERCENTAGE": "70",
        "ISSUER_NAME": "The Bank of Nova Scotia",
        "RISK_LEVEL": "HIGH",
        "REGULATOR": "Canadian Securities Regulators",
        "COMPANY_NAME": "The Bank of Nova Scotia",
    }
    
    # Create document from your customized templates
    document = create_complete_document_from_templates(your_sample_data, "retail")
    
    print("🧪 Testing Your Bank of Nova Scotia Customized Templates")
    print("=" * 60)
    print(f"✅ Executive summary: {len(document['executive_summary'])} characters")
    print(f"✅ Key terms: {len(document['key_terms'])} characters")
    print(f"✅ Additional key terms: {len(document['additional_key_terms'])} characters")
    print(f"✅ Scenarios: {len(document['scenarios'])} characters")
    print(f"✅ Disclaimer: {len(document['disclaimer'])} characters")
    print("\n📄 Preview of Executive Summary:")
    print(document['executive_summary'][:200] + "...")
    print("\n✅ Bank of Nova Scotia templates ready for ISM agent!")
    
    return document

# Example usage and testing
if __name__ == "__main__":
    print("🎯 Large Text Templates - Customization Test")
    print("=" * 60)
    
    # Test the templates
    document = test_your_templates()
    
    print("\n💡 Next Steps:")
    print("1. Customize the template text in the sections marked with ⭐")
    print("2. Update your sample data in test_your_templates()")
    print("3. Run this file again to test: python large_text_templates.py")
    print("4. Use with ISM agent once satisfied with your templates")