import os
import sys
import json
import asyncio

from pathlib import Path

from core.global_agent import GlobalAgent


async def generate_all(custom_vars_path: str) -> int:
    # Load custom variables
    if not Path(custom_vars_path).exists():
        print(f"ERROR: custom vars file not found: {custom_vars_path}")
        return 1
    with open(custom_vars_path, "r", encoding="utf-8") as f:
        custom_variables = json.load(f)

    # Prepare filenames per agent for clarity
    filenames = {
        "ism": "ISM_Series5.docx",
        "bsp": "BSP_Series5.docx",
        "pds": "PDS_Series5.docx",
        "prs": "PRS_Series5.docx",
    }

    agent = GlobalAgent()

    results = {}
    for agent_type in ["ism", "bsp", "pds", "prs"]:
        resp = await agent.process_request(
            user_request="Generate Series 5 documents from templates",
            agents=[agent_type],
            use_large_text_templates=True,
            render_docx=True,
            audience="retail",
            enforce_placeholder_validation=False,
            filename=filenames[agent_type],
            custom_variables=custom_variables,
        )

        if not resp.primary_result or not resp.primary_result.success:
            err = resp.primary_result.error_message if resp.primary_result else resp.message
            print(f"❌ {agent_type.upper()} generation failed: {err}")
            return 2

        out = resp.primary_result.output or {}
        results[agent_type] = {
            "docx": out.get("docx_path"),
        }

    print("\n✅ Generation complete. Paths:")
    for k, v in results.items():
        print(f"  {k.upper()}: {v['docx']}")

    return 0


def main() -> int:
    # Default path
    custom_vars_path = os.environ.get(
        "CUSTOM_VARS_JSON",
        str(Path("inputs") / "custom_vars_series5.json"),
    )
    return asyncio.run(generate_all(custom_vars_path))


if __name__ == "__main__":
    sys.exit(main())


