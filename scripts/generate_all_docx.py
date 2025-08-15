import os
import asyncio
from datetime import date

from dotenv import load_dotenv

from core.global_agent import GlobalAgent


async def main() -> int:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set. Add it to your .env before running.")
        return 1

    # Use the global orchestrator to generate BSP, PDS, and PRS via large-text templates and render DOCX
    agent = GlobalAgent()

    user_request = (
        "Create BSP, PDS, and PRS documents for an autocallable note. "
        "Issuer The Bank of Nova Scotia, program Senior Notes (Principal at Risk Notes), underlying Canadian Financials Basket."
    )

    print("\n🚀 Generating full document suite (BSP, PDS, PRS) with DOCX rendering...")
    # Optional: load custom variables from JSON file if CUSTOM_VARS_JSON is set
    custom_vars_path = os.getenv("CUSTOM_VARS_JSON", "").strip()
    custom_variables = None
    if custom_vars_path:
        try:
            import json
            with open(custom_vars_path, "r", encoding="utf-8") as f:
                custom_variables = json.load(f)
            print(f"Loaded custom variables from {custom_vars_path} ({len(custom_variables)} keys)")
        except Exception as e:
            print(f"WARNING: Failed to load CUSTOM_VARS_JSON '{custom_vars_path}': {e}")

    resp = await agent.process_request(
        user_request=user_request,
        agents=["bsp", "pds", "prs"],
        use_large_text_templates=True,
        render_docx=True,
        audience="retail",
        enforce_placeholder_validation=False,
        title="Autocallable Note Document Suite",
        custom_variables=custom_variables,
    )

    print(f"\nSession: {resp.session_id}")
    print(f"Status: {'SUCCESS' if resp.success else 'FAIL'}")
    print(f"Message: {resp.message}")

    def _extract_docx_path(result_output):
        if isinstance(result_output, dict):
            return result_output.get("docx_path")
        return None

    # Print primary
    if resp.primary_result:
        p = resp.primary_result
        print(f"\nPrimary: {p.agent_type} -> {'OK' if p.success else 'ERROR'} ({p.processing_time:.2f}s)")
        if p.success:
            print(f"  docx: {_extract_docx_path(p.output)}")
        else:
            print(f"  error: {p.error_message}")

    # Print secondary
    for s in resp.secondary_results:
        print(f"Secondary: {s.agent_type} -> {'OK' if s.success else 'ERROR'} ({s.processing_time:.2f}s)")
        if s.success:
            print(f"  docx: {_extract_docx_path(s.output)}")
        else:
            print(f"  error: {s.error_message}")

    # Summarize placeholder guidance if we see validation errors
    def _emit_placeholder_hint(err: str):
        if not err:
            return
        if "Unresolved placeholders detected" in err:
            print("\n⚠️ Placeholder validation failed. Provide values for the listed placeholders or update templates.")
            print("   You can resolve them by either:")
            print("   - Supplying missing fields in the input model for the target agent, or")
            print("   - Passing custom_variables to the large-text generation, or")
            print("   - Editing templates under agents/<agent>/large_text_templates.py to remove or replace placeholders.")

    if resp.primary_result and resp.primary_result.error_message:
        _emit_placeholder_hint(resp.primary_result.error_message)
    for s in resp.secondary_results:
        _emit_placeholder_hint(s.error_message)

    return 0 if resp.success else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))


