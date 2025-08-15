"""
Large Text Templates for BSP Agent

🎯 THIS IS WHERE YOU CUSTOMIZE YOUR BSP LARGE TEXT CHUNKS

INSTRUCTIONS:
1. Find the template sections below (marked with ⭐ CUSTOMIZE THIS ⭐)
2. Replace the example text with your exact content
3. Keep the [PLACEHOLDER] variables - they'll be replaced automatically
4. Test your changes using the functions at the bottom

AVAILABLE PLACEHOLDERS:
[Date of Prospectus] - The issuance date of the Short Form Base Shelf Prospectus.
[Dealer Agreement Date] - The date of the formal agreement between the Bank and the listed Investment Dealers.
[List of Investment Dealers] - The full legal names of the securities dealers authorized to offer the notes.
[Directors Resident Outside of Canada] - The names of the Bank's directors who are not residents of Canada.
[Bank Legal Counsel] - The law firm representing The Bank of Nova Scotia for the offering.
[Dealers Legal Counsel] - The law firm representing the Investment Dealers for the offering.
[Specific Designation of Notes] - The unique title or series name for a specific tranche of notes.
[Aggregate Principal Amount] - The total value of the notes being offered in a specific tranche.
[Currency] - The currency in which the notes are denominated and payments will be made.
[Maturity Date] - The date on which the principal amount of the notes is due to be repaid.
[Offering Price] - The price at which the notes are initially sold to the public.
[Variable Return Formula] - The specific formula used to calculate interest or variable payments linked to underlying assets.
[Underlying Interests] - A description of the specific financial instruments, indices, or assets to which the notes' performance is linked.
[Minimum Principal Repayment] - The minimum guaranteed percentage or amount of the principal that will be repaid at maturity.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: COVER PAGE DISCLOSURES ⭐
# =============================================================================

# 🔧 COVER PAGE DISCLOSURES
# ⭐ This is the mandatory text for the cover page, containing regulatory warnings, a description of the offering structure, and notices to investors.
Cover_Page_Disclosures = """
Cover Page Disclosures

No securities regulatory authority has expressed an opinion about these securities and it is an offence to claim otherwise. This short form base shelf prospectus has been filed under legislation in each of the provinces and territories of Canada that permits certain information about these securities to be determined after this prospectus has become final and that permits the omission from this prospectus of that information. The legislation requires the delivery to purchasers of a prospectus supplement containing the omitted information within a specified period of time after agreeing to purchase any of these securities. This short form base shelf prospectus has been filed in reliance on an exemption from the preliminary base shelf prospectus requirement for a well-known seasoned issuer. This short form base shelf prospectus constitutes a public offering of these securities only in those jurisdictions where they may be lawfully offered for sale and therein only by persons permitted to sell such securities. The securities to be issued hereunder have not been and will not be registered under the United States Securities Act of 1933, as amended (the 'U.S. Securities Act') and, subject to certain exceptions, may not be offered, sold or delivered, directly or indirectly, in the United States or to or for the account or benefit of U.S. Persons (as defined in Regulation S under the U.S. Securities Act). See 'Plan of Distribution'.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: FORWARD-LOOKING STATEMENTS ⭐
# =============================================================================
# 💼 FORWARD-LOOKING STATEMENTS 
# ⭐ This section is a standard "safe harbor" provision designed to protect the Bank from liability related to projections and other forward-looking information by outlining the inherent risks and uncertainties. ⭐

FORWARD_LOOKING_STATEMENTS = """
Forward-Looking Statements

From time to time, the Bank's public communications include oral or written forward-looking statements. Statements of this type are included in this document, and may be included in other filings with Canadian securities regulators or the U.S. Securities and Exchange Commission, or in other communications. All such statements are made pursuant to the 'safe harbor' provisions of the U.S. Private Securities Litigation Reform Act of 1995 and any applicable Canadian securities legislation. Such statements are typically identified by words or phrases such as 'believe,' 'expect,' 'aim,' 'achieve,' 'foresee,' 'forecast,' 'anticipate,' 'intend,' 'estimate,' 'plan,' 'goal,' and similar expressions of future or conditional verbs, such as 'will,' 'may,' 'should,' 'would,' 'might,' 'can' and 'could'. By their very nature, forward-looking statements require the Bank to make assumptions and are subject to inherent risks and uncertainties, which give rise to the possibility that the Bank's predictions, forecasts, projections, expectations or conclusions will not prove to be accurate. The Bank cautions readers not to place undue reliance on these statements as a number of risk factors, many of which are beyond the Bank's control and effects of which can be difficult to predict, could cause the Bank's actual results to differ materially from the expectations, targets, estimates or intentions expressed in such forward-looking statements. Except as required by law, the Bank does not undertake to update any forward-looking statements, whether written or oral, that may be made from time to time by or on its behalf.
"""

# 📋 DOCUMENTS INCORPORATED BY REFERENCE
# ⭐ This section legally integrates other key public filings into the prospectus, avoiding the need to repeat voluminous information. ⭐
DOCUMENTS_INCORPORATED_BY_REFERENCE = """
Documents Incorporated by Reference

The following documents have been filed with the securities regulatory authorities in each province and territory of Canada and are specifically incorporated by reference into, and form an integral part of, this Prospectus: (a) the Bank's annual information form; (b) the Bank's consolidated financial statements, together with the auditors' report thereon; (c) the Bank's management's discussion and analysis for the year ended October 31; (d) the Bank's unaudited condensed interim consolidated financial statements for the three months ended January 31; (e) the Bank's management's discussion and analysis for the three months ended January 31; and (f) the Bank's notice of annual meeting and management proxy circular. Any documents of the type referred to in the preceding paragraph, any material change reports (excluding confidential material change reports), any business acquisition reports and any other disclosure documents required to be incorporated by reference in this Prospectus, filed by the Bank with a securities regulatory authority in Canada after the date of this Prospectus and prior to the completion or withdrawal of any offering hereunder, will be deemed to be incorporated by reference in this Prospectus.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: DESCRIPTION OF THE NOTES ⭐
# =============================================================================
# 📊 DESCRIPTION OF THE NOTES
# ⭐ This provides a general description of the securities that may be offered. Specific details are left to the pricing/product supplements. ⭐

DESCRIPTION_OF_THE_NOTES = """
Description of the Notes

The Notes will constitute direct senior unsecured and unsubordinated obligations of the Bank and will rank equally with all other present and future direct senior unsecured and unsubordinated indebtedness of the Bank, subject to certain priorities under applicable law. The Notes will not constitute deposits that are insured under the Canada Deposit Insurance Corporation Act or any other deposit insurance regime. A Note of this type provides that the principal amount payable at its maturity, and/or the amount of interest, if any, payable on an interest payment date, will be determined, in whole or in part, by reference to one or more [Underlying Interests]. Purchasers could lose substantially all of their investment in Notes, subject to a minimum repayment of [Minimum Principal Repayment] as may be specified in the applicable product supplement or pricing supplement. Unless otherwise specified in the applicable product supplement or pricing supplement, upon issuance, the Notes will be issued in 'book-entry only' form and will be represented by a fully registered global note. Notes issued in 'book-entry only' form must be purchased, transferred or redeemed through participants in the depository service of CDS Clearing and Depository Services Inc. ('CDS') or its nominee.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: PLAN OF DISTRIBUTION ⭐
# =============================================================================
# ⚖️ PLAN OF DISTRIBUTION
# ⭐ This section outlines how the Notes will be sold to the public. ⭐

PLAN_OF_DISTRIBUTION = """
Plan of Distribution

The Notes will be offered severally by one or more of [List of Investment Dealers] (collectively, the 'Investment Dealers'). Under a dealer agreement dated [Dealer Agreement Date], the Notes may be purchased or offered at various times by any of the Investment Dealers, as agent, dealer, underwriter or principal at prices and commissions to be agreed upon, for sale to the public at prices to be negotiated with purchasers. The Bank may also offer the Notes to purchasers directly, pursuant to applicable law, at prices and terms to be negotiated. Scotia Capital is a wholly-owned subsidiary of the Bank. Consequently, the Bank is a related and connected issuer of Scotia Capital within the meaning of applicable securities legislation. Scotia Capital is expected to be involved in any decision to distribute Notes hereunder and in determining the terms of each particular offering of Notes.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: RISK FACTORS ⭐
# =============================================================================
# ⚖️ RISK FACTORS
# ⭐ This section provides a summary of the principal risks that potential investors should consider. It includes risks related to the Bank's business, the notes themselves, and the underlying assets. ⭐

RISK_FACTORS = """
Risk Factors

An investment in Notes is subject to various risks including those risks inherent in conducting the business of a diversified financial institution. Before deciding whether to invest in Notes, purchasers should consider carefully the risks set out herein and incorporated by reference in this Prospectus (including subsequently filed documents incorporated by reference) and, if applicable, those described in the product supplement and pricing supplement relating to a specific offering of Notes. The Notes will not constitute deposits that are insured under the Canada Deposit Insurance Corporation Act (Canada) (the 'CDIC Act') or any other deposit insurance regime. Therefore, a holder will not be entitled to Canada Deposit Insurance Corporation protection. The obligation to make payments to holders of Notes is an obligation of the Bank. Accordingly, the likelihood that such holders will receive payments owing to them in connection with the Notes will be dependent upon the financial health and creditworthiness of the Bank. Unless otherwise specified in the applicable product supplement or pricing supplement, there may be no market through which the Notes may be sold and holders may not be able to sell the Notes.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: USE OF PROCEEDS ⭐
# =============================================================================
# ⚖️ USE OF PROCEEDS
# ⭐ This is a brief, standard statement explaining what the Bank will do with the money raised from the sale of the notes. ⭐

Use_of_Proceeds = """
Use of Proceeds

Unless otherwise specified in a product supplement or pricing supplement, the net proceeds to the Bank from the sale of Notes will be added to the general funds of the Bank and utilized for general banking purposes.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: PURCHASER'S STATUTORY RIGHTS ⭐
# =============================================================================
# ⚖️ PURCHASER'S STATUTORY RIGHTS
# ⭐ This section is a mandatory disclosure informing investors of their legal rights under securities laws, such as the right of withdrawal and rescission.

Purchaser_s_Statutory_Rights = """
Purchaser's Statutory Rights

Securities legislation in certain of the provinces and territories of Canada provides purchasers with the right to withdraw from an agreement to purchase securities. This right may be exercised within two business days after receipt or deemed receipt of a prospectus and any amendment. In several of the provinces and territories, the securities legislation further provides a purchaser with remedies for rescission or, in some jurisdictions, revisions of the price or damages if the Prospectus and any amendment contains a misrepresentation or is not delivered to the purchaser, provided that the remedies for rescission, revisions of the price or damages are exercised by the purchaser within the time limit prescribed by the securities legislation of the purchaser's province or territory. The purchaser should refer to any applicable provisions of the securities legislation of the purchaser's province or territory for the particulars of these rights or consult with a legal adviser.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: CERTIFICATE OF THE BANK ⭐
# =============================================================================
# ⚖️ CERTIFICATE OF THE BANK
# ⭐ This is the formal certification by the Bank, signed by its senior officers and directors, attesting to the accuracy and completeness of the prospectus.

Certificate_of_the_Bank = """
Certificate of the Bank

Dated: [Date of Prospectus]
This short form prospectus, together with the documents incorporated in this prospectus by reference, will, as of the date of the last supplement to this prospectus relating to the securities offered by this prospectus and the supplement(s), constitute full, true and plain disclosure of all material facts relating to the securities offered by this prospectus and the supplement(s) as required by the Bank Act (Canada) and the regulations thereunder and the securities legislation of all provinces and territories of Canada.

(signed) [Signatory CEO]
President and Chief Executive Officer

(signed) [Signatory CFO]
Group Head and Chief Financial Officer

On behalf of the Board of Directors

(signed) [Signatory Director 1]
Director

(signed) [Signatory Director 2]
Director
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: CERTIFICATE OF THE DEALERS ⭐
# =============================================================================
# ⚖️ CERTIFICATE OF THE DEALERS
# ⭐ This is the formal certification by the Investment Dealers, attesting to their belief in the accuracy and completeness of the prospectus.

Certificate_of_the_Dealers = """
Certificate of the Dealers

Dated: [Date of Prospectus]
To the best of our knowledge, information and belief, this short form prospectus, together with the documents incorporated in this prospectus by reference, will, as of the date of the last supplement to this prospectus relating to the securities offered by this prospectus and the supplement(s), constitute full, true and plain disclosure of all material facts relating to the securities offered by this prospectus and the supplement(s) as required by the Bank Act (Canada) and the regulations thereunder and the securities legislation of all provinces and territories of Canada.

[List of Investment Dealers with Signatories]
"""

# =============================================================================
# ⭐ TEMPLATE MANAGEMENT FUNCTIONS ⭐
# =============================================================================

def get_template(template_name: str, audience: str = "institutional") -> str:
    """
    Retrieve a BSP large text template by canonical section key.

    Supported template_name values (canonical keys):
    - cover_page_disclosures
    - forward_looking_statements
    - documents_incorporated_by_reference
    - description_of_the_notes
    - plan_of_distribution
    - risk_factors
    - use_of_proceeds
    - purchasers_statutory_rights
    - certificate_of_the_bank
    - certificate_of_the_dealers

    The audience parameter is accepted for API compatibility but currently
    does not vary content for BSP templates.
    """
    templates = {
        "cover_page_disclosures": {
            "institutional": Cover_Page_Disclosures,
            "retail": Cover_Page_Disclosures,
        },
        "forward_looking_statements": {
            "institutional": FORWARD_LOOKING_STATEMENTS,
            "retail": FORWARD_LOOKING_STATEMENTS,
        },
        "documents_incorporated_by_reference": {
            "institutional": DOCUMENTS_INCORPORATED_BY_REFERENCE,
            "retail": DOCUMENTS_INCORPORATED_BY_REFERENCE,
        },
        "description_of_the_notes": {
            "institutional": DESCRIPTION_OF_THE_NOTES,
            "retail": DESCRIPTION_OF_THE_NOTES,
        },
        "plan_of_distribution": {
            "institutional": PLAN_OF_DISTRIBUTION,
            "retail": PLAN_OF_DISTRIBUTION,
        },
        "risk_factors": {
            "institutional": RISK_FACTORS,
            "retail": RISK_FACTORS,
        },
        "use_of_proceeds": {
            "institutional": Use_of_Proceeds,
            "retail": Use_of_Proceeds,
        },
        "purchasers_statutory_rights": {
            "institutional": Purchaser_s_Statutory_Rights,
            "retail": Purchaser_s_Statutory_Rights,
        },
        "certificate_of_the_bank": {
            "institutional": Certificate_of_the_Bank,
            "retail": Certificate_of_the_Bank,
        },
        "certificate_of_the_dealers": {
            "institutional": Certificate_of_the_Dealers,
            "retail": Certificate_of_the_Dealers,
        },
    }

    section = templates.get(template_name)
    if not section:
        return "Template not found."

    return section.get(audience, section.get("institutional", "Template not found."))


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


def create_complete_document_from_templates(product_data: dict, audience: str = "institutional") -> dict:
    """
    Create a complete document using large text templates.
    
    Args:
        product_data: Dictionary with product information and variables
        audience: Target audience for template selection
    
    Returns:
        Dictionary with all BSP document sections
    """

    # Fetch canonical BSP templates
    cover_page = get_template("cover_page_disclosures", audience)
    fls = get_template("forward_looking_statements", audience)
    dir_docs = get_template("documents_incorporated_by_reference", audience)
    notes_desc = get_template("description_of_the_notes", audience)
    pod = get_template("plan_of_distribution", audience)
    risks = get_template("risk_factors", audience)
    uop = get_template("use_of_proceeds", audience)
    statutory = get_template("purchasers_statutory_rights", audience)
    cert_bank = get_template("certificate_of_the_bank", audience)
    cert_dealers = get_template("certificate_of_the_dealers", audience)

    # Customize with product data
    document = {
        "cover_page_disclosures": customize_template(cover_page, product_data),
        "forward_looking_statements": customize_template(fls, product_data),
        "documents_incorporated_by_reference": customize_template(dir_docs, product_data),
        "description_of_the_notes": customize_template(notes_desc, product_data),
        "plan_of_distribution": customize_template(pod, product_data),
        "risk_factors": customize_template(risks, product_data),
        "use_of_proceeds": customize_template(uop, product_data),
        "purchasers_statutory_rights": customize_template(statutory, product_data),
        "certificate_of_the_bank": customize_template(cert_bank, product_data),
        "certificate_of_the_dealers": customize_template(cert_dealers, product_data),
    }

    return document


# =============================================================================
# ⭐ TESTING YOUR CUSTOMIZATIONS ⭐
# =============================================================================

def test_your_templates():
    """
    Test your customized templates with sample data.
    
    ⭐ MODIFY THE SAMPLE DATA BELOW to match your actual program information ⭐
    """
    # Sample BSP test data
    your_sample_data = {
        "Program Name": "Structured Notes Program 2025",
        "Issuer": "Your Financial Institution Ltd",
        "Shelf Amount": "1,000,000,000",
        "Currency": "USD",
        "Regulatory Jurisdiction": "SEC",
        "Business Description": "Financial services including structured products and investment banking",
        "Document Date": "January 15, 2025",
        "Generation Date": "2025-01-15",
        # New BSP placeholders with sensible defaults for testing
        "Date of Prospectus": "January 15, 2025",
        "Dealer Agreement Date": "January 15, 2025",
        "List of Investment Dealers": "TBD – see pricing supplement",
        "Directors Resident Outside of Canada": "None",
        "Bank Legal Counsel": "TBD",
        "Dealers Legal Counsel": "TBD",
        "Specific Designation of Notes": "Structured Notes Program 2025 Notes",
        "Aggregate Principal Amount": "TBD – see pricing supplement",
        "Maturity Date": "TBD – see pricing supplement",
        "Offering Price": "TBD – see pricing supplement",
        "Variable Return Formula": "As described in the applicable pricing supplement",
        "Underlying Interests": "As described in the applicable pricing supplement",
        "Minimum Principal Repayment": "0% unless otherwise specified",
    }
    
    print("🧪 Testing BSP Large Text Templates")
    print("=" * 50)
    
    # Test template generation
    document = create_complete_document_from_templates(your_sample_data, "institutional")
    
    print("✅ Templates generated successfully!")
    print(f"📄 Cover Page: {len(document['cover_page_disclosures'])} characters")
    print(f"🗂️ Incorporated Docs: {len(document['documents_incorporated_by_reference'])} characters")
    print(f"📘 Notes Description: {len(document['description_of_the_notes'])} characters")
    print(f"🧭 Distribution Plan: {len(document['plan_of_distribution'])} characters")
    print(f"⚠️ Risk Factors: {len(document['risk_factors'])} characters")
    
    return document


if __name__ == "__main__":
    test_your_templates() 