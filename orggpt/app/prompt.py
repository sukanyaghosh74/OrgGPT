from typing import Dict

MEMO_SECTIONS = [
    "Company Overview",
    "Financial Highlights",
    "Risk Factors",
    "Opportunities",
    "Valuation Notes"
]

def get_section_prompt(section: str) -> str:
    """
    Returns a prompt template for a given memo section.
    """
    templates = {
        "Company Overview": "Summarize the company's core business, products, and market position.",
        "Financial Highlights": "Extract and summarize key financial metrics: revenue, EBITDA, margins, and trends.",
        "Risk Factors": "List and explain the main risk factors, challenges, and market threats.",
        "Opportunities": "Identify growth areas, market tailwinds, and strategic opportunities.",
        "Valuation Notes": "Provide commentary on valuation, multiples, and any relevant financial context."
    }
    return templates.get(section, f"Summarize the section: {section}")

def build_memo_prompt(context: str, section: str) -> str:
    """
    Builds a full prompt for a given section using retrieved context.
    """
    section_prompt = get_section_prompt(section)
    return f"""You are an expert investment analyst. Using ONLY the context below, write the '{section}' section of an investment memo.\n\nContext:\n{context}\n\nInstructions: {section_prompt}\nBe concise, use bullet points where appropriate, and avoid speculation.""" 