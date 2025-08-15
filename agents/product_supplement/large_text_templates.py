"""
Large Text Templates for PDS Agent

🎯 THIS IS WHERE YOU CUSTOMIZE YOUR PDS LARGE TEXT CHUNKS

INSTRUCTIONS:
1. Find the template sections below (marked with ⭐ CUSTOMIZE THIS ⭐)
2. Replace the example text with your exact content
3. Keep the [PLACEHOLDER] variables - they'll be replaced automatically
4. Test your changes using the functions at the bottom

AVAILABLE PLACEHOLDERS:
[Prospectus Supplement Date] - The date the prospectus supplement is issued, in "Month Day, Year" format.
[Base Shelf Prospectus Date] - The date of the short form base shelf prospectus to which the supplement relates, in "Month Day, Year" format.
[New Issue Date] - The date the new issue is released, in "Month Day, Year" format.
[Note Type] - The specific type of notes being offered (e.g., Index Linked Notes, Equity and Unit Linked Notes).
[Underlying Asset Name] - The specific name of the index, equity, unit, or other underlying interest to which the notes are linked. This could be a single asset or a basket of assets.
[Specific Pricing Supplement] - A reference to the relevant pricing supplement document that contains specific terms for a particular series of notes.
[Maturity Date] - The date on which the notes are scheduled to mature.
[Website for Note Information] - The specific URL where investors can find information about the notes (e.g., www.scotianotes.com).
[Principal Amount] - The principal amount of a note, as specified in the applicable pricing supplement.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Initial Declarations and Disclaimers ⭐
# =============================================================================

# 🔧 Initial Declarations and Disclaimers
# ⭐ This section appears at the very beginning of the document. It includes mandatory legal disclaimers required by securities regulators and specifies the scope and limitations of the offering. ⭐
Initial_Declarations_and_Disclaimers = """
Initial Declarations and Disclaimers

No securities regulatory authority has expressed an opinion about these securities and it is an offence to claim otherwise. This prospectus supplement together with the short form base shelf prospectus dated [Base Shelf Prospectus Date] to which it relates, as amended or supplemented, and each document incorporated by reference into such prospectus, constitutes a public offering of these securities only in those jurisdictions where they may be lawfully offered for sale and therein only by persons permitted to sell such securities. The securities to be issued hereunder have not been and will not be registered under the United States Securities Act of 1933, as amended (the "U.S. Securities Act") and, subject to certain exceptions, may not be offered, sold or delivered, directly or indirectly, in the United States or to or for the account or benefit of U.S. Persons (as defined in Regulation S under the U.S. Securities Act). See "Plan of Distribution" in the short form base shelf prospectus.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Offering Details    ⭐
# =============================================================================
# 💼 Offering Details
# ⭐ This section provides a high-level overview of the offering, identifying the issuer, the type of security, and the general nature of the investment. ⭐

Offering_Details = """
Offering Details

New Issue [New Issue Date]
The Bank of Nova Scotia
Senior Notes (Principal at Risk Notes)
[Note Type]

The Bank of Nova Scotia (the "Bank") may, from time to time, offer and issue unsecured and unsubordinated debt securities (principal at risk notes) (the "Notes") in one or more tranches or series as described in its short form base shelf prospectus dated [Base Shelf Prospectus Date] (the "Prospectus") establishing the Bank's senior (principal at risk) note program.
"""

# 📋 Nature of the Notes and Investment Profile
# ⭐ This is a crucial section that describes the fundamental characteristics of the notes. It clarifies that they are not standard debt instruments, carry significant risk, and are intended for a specific type of investor. ⭐
Nature_of_the_Notes_and_Investment_Profile = """
Nature of the Notes and Investment Profile

The Notes will not constitute deposits under the Canada Deposit Insurance Corporation Act or under any other deposit insurance regime. The return on the Notes will be based on the performance of [Underlying Asset Name] during the term of such Notes. The Notes are designed for investors seeking exposure to the specified [Underlying Asset Name], and who are prepared to assume the risks associated with an investment linked to the specified [Underlying Asset Name]. An investment in the Notes involves risks. The Notes are not designed to be alternatives to fixed income or money market instruments. The Notes are only appropriate investments for persons who understand the risks associated with structured products and derivatives. The Notes are considered to be "specified derivatives" under applicable Canadian securities laws. An investment in the Notes does not represent a direct or indirect investment in the [Underlying Asset Name] to which it is linked or its underlying interests, and investors do not have an ownership or any other interest (including voting rights or the right to receive any dividends, distributions or other income or amounts accruing or paid thereon) in respect of such [Underlying Asset Name] or its or their underlying interests. A purchaser of Notes will be exposed to fluctuations and changes in the levels of the [Underlying Asset Name] to which the Notes are linked. [Underlying Asset Name] levels may be volatile and an investment linked to [Underlying Asset Name] levels may also be volatile. The Notes do not guarantee the repayment of any amount of the principal (subject to the minimum principal repayment as may be specified in the applicable pricing supplement), or the payment of any return and may be subject to a cap or other limitation on return and may be fully exposed to any decline in the value of the securities or other interests that comprise the specified [Underlying Asset Name]. The amount received at maturity will depend on the performance of the [Underlying Asset Name]. A purchaser of Notes could lose substantially all of his or her investment in the Notes. See "Risk Factors" in the Prospectus, this product supplement and/or the applicable pricing supplement.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Prospectus Structure and Document Incorporation ⭐
# =============================================================================
# 📊 Prospectus Structure and Document Incorporation
# ⭐ This part explains how different documents (the base shelf prospectus, this product supplement, and the specific pricing supplement) work together to form the complete prospectus for the notes. It also covers legal statements about how information is incorporated by reference. ⭐

PROSPECTUS_STRUCTURE_AND_DOCUMENT_INCORPORATION = """
Prospectus Structure and Document Incorporation

Prospectus for Notes
Notes that may be issued under the Bank's senior (principal at risk) note program are direct senior unsecured and unsubordinated debt securities. The [Note Type] will be described in separate documents, including: (1) the Prospectus, and (2) (i) this product supplement, which generally describes a particular type of Note the Bank may issue under its senior (principal at risk) note program, as described in the Prospectus, and/or (ii) a pricing supplement that contains the specific terms (including pricing information) about the Notes being offered. In respect of any particular [Note Type] the Bank may offer under its senior (principal at risk) note program, the Prospectus together with this product supplement and/or the applicable pricing supplement will collectively constitute the "prospectus" in respect of such Notes. Each of these documents should be read and considered carefully before a prospective purchaser makes an investment decision in respect of the Notes. See "About this Prospectus for Notes" in the Prospectus. A copy of the Prospectus for the Notes will be available at [Website for Note Information].

Documents Incorporated by Reference
This product supplement is deemed to be incorporated by reference into the Prospectus solely for the purpose of the Notes issued pursuant hereto. Other documents are also incorporated or deemed to be incorporated by reference into the Prospectus and reference should be made to the Prospectus for full particulars.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Principal at Risk Notes ⭐
# =============================================================================
# 📊 Principal at Risk Notes
# ⭐ This section explains that the notes are principal at risk, meaning that investors could lose their entire investment. ⭐

Principal_at_Risk_Notes = """
Principal at Risk Notes

The Notes do not guarantee the repayment of any amount of the principal, subject to the minimum principal repayment as may be specified in the applicable pricing supplement. The applicable pricing supplement for the Notes will specify the amount of the principal of the Notes that is "protected", which amount may be as little as 1% of the principal amount of such Notes. Notes in respect of which the minimum principal repayment by the Bank will be an amount in excess of 1% of the principal are referred to as "partially principal protected notes". All other Notes are "non-protected notes", which means that all but 1% of the principal amount of such Notes will be fully exposed and investors could lose substantially all of their investment subject to the minimum principal repayment of 1% of the principal amount of such Notes, or $1.00 per Note. See "Description of the Notes Principal at Risk" in the Prospectus.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Determinations of the Calculation Agent ⭐
# =============================================================================
# 📊 Determinations of the Calculation Agent
# ⭐ This clause establishes the authority and discretion of the Calculation Agent, which is responsible for all calculations related to the notes' performance and payouts. It limits the agent's liability when acting in good faith. ⭐

Determinations_of_the_Calculation_Agent = """
Principal at Risk Notes

All calculations and determinations in respect of the Notes made by the Calculation Agent will, absent manifest error, be final and binding on the holders of Notes and will be made in the Calculation Agent's sole and absolute discretion. In certain circumstances, the Bank will appoint one or more independent calculation experts. The Calculation Agent will not be responsible for its errors or omissions if made in good faith. See "Description of the Notes Calculation Agent" and "Description of the Notes Independent Calculation Experts" in the Prospectus.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Risk Factor Introduction ⭐
# =============================================================================
# 📊 Risk Factor Introduction
# ⭐ This serves as the preamble to the detailed risk factors. It reiterates the high-risk nature of the investment and advises prospective investors to read all related documents thoroughly. ⭐

Risk_Factor_Introduction = """
Risk Factors

An investment in the Notes is subject to the risks described below, as well as the risks described under "Risk Factors" in the Prospectus and the applicable pricing supplement. The Notes are not secured debt and involve greater risks than ordinary unsecured debt securities. Investing in the Notes is not equivalent to investing directly or indirectly in the [Underlying Asset Name]. These risk factors shall be read with the necessary modifications to also apply to a Target Index and the underlying interests comprising a Target Index. The Notes are not appropriate investments for persons who do not understand the risks associated with structured products or derivatives. Prospective purchasers should carefully consider whether the Notes are suited to their respective particular circumstances. This section describes certain risks relating to an investment in the Notes. Prospective purchasers should read the following information about these risks, together with the other information in the Prospectus, this product supplement and/or the applicable pricing supplement, before investing in the Notes.
"""

# =============================================================================
# ⭐ CUSTOMIZE THIS: Potential for Loss ⭐
# =============================================================================
# 📊 Potential for Loss
# ⭐ This is a standard and critical risk factor that explicitly warns investors that they could lose a substantial portion or all of their investment ⭐

Potential_for_Loss = """
An investment in the Notes may result in a loss
The Notes do not guarantee the return of the entire amount of the principal of the Notes and, unless otherwise specified in the applicable pricing supplement for the Notes, the Bank will not repay a fixed amount of principal on the Notes on their maturity date. The return on the Notes may be zero, positive or negative and will depend on the ... direction of and percentage change in the ... [Underlying Asset Name] over the applicable measurement period and the specified correlation between the direction of such change and the return on the Notes. ... a purchaser of the Notes may receive at maturity less, and possibly significantly less, than the principal amount of such Notes. Subject to any minimum principal repayment as specified in the applicable pricing supplement, purchasers of Notes could lose their entire investment.
"""

# =============================================================================
# ⭐ TEMPLATE MANAGEMENT FUNCTIONS ⭐
# =============================================================================

def list_canonical_section_keys() -> list[str]:
    """
    Return the canonical section keys exposed by this module.
    """
    return [
        "initial_disclaimers",
        "offering_details",
        "nature_and_profile",
        "prospectus_structure",
        "principal_at_risk_notes",
        "calculation_agent_determinations",
        "risk_factor_introduction",
        "potential_for_loss",
    ]


def get_template(template_name: str, audience: str = "retail") -> str:
    """
    Get a canonical template by name.

    Supported canonical names are provided by list_canonical_section_keys().
    The audience parameter is accepted for API compatibility but is not used
    to vary content for PDS at this time.
    """
    canonical_templates = {
        "initial_disclaimers": Initial_Declarations_and_Disclaimers,
        "offering_details": Offering_Details,
        "nature_and_profile": Nature_of_the_Notes_and_Investment_Profile,
        "prospectus_structure": PROSPECTUS_STRUCTURE_AND_DOCUMENT_INCORPORATION,
        "principal_at_risk_notes": Principal_at_Risk_Notes,
        "calculation_agent_determinations": Determinations_of_the_Calculation_Agent,
        "risk_factor_introduction": Risk_Factor_Introduction,
        "potential_for_loss": Potential_for_Loss,
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
                      placeholders exactly, e.g., "Base Shelf Prospectus Date",
                      "New Issue Date", "Note Type", "Underlying Asset Name",
                      "Specific Pricing Supplement", "Maturity Date",
                      "Website for Note Information", "Principal Amount",
                      etc.
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
    
    ⭐ MODIFY THE SAMPLE DATA BELOW to match your actual note information ⭐
    """
    # Sample PDS test data
    your_sample_data = {
        # Canonical placeholders expected by the templates above
        "Prospectus Supplement Date": "January 15, 2025",
        "Base Shelf Prospectus Date": "March 04, 2024",
        "New Issue Date": "January 29, 2025",
        "Note Type": "Autocallable Notes",
        "Underlying Asset Name": "S&P 500 Index",
        "Specific Pricing Supplement": "Pricing Supplement for Series 2025-1 dated January 29, 2025",
        "Maturity Date": "January 29, 2032",
        "Website for Note Information": "www.scotianotes.com",
        "Principal Amount": "100,000,000",
    }
    
    print("🧪 Testing PDS Large Text Templates")
    print("=" * 50)
    
    # Test template generation
    document = create_complete_document_from_templates(your_sample_data, "retail")
    
    print("✅ Templates generated successfully!")
    for key in list_canonical_section_keys():
        print(f"📄 {key}: {len(document[key])} characters")
    
    return document


if __name__ == "__main__":
    test_your_templates() 