"""
CLI tool to add feedback from a generated document into a domain knowledge base
and record the action in the conversation/audit trail.

Usage examples:

  - Ingest a TXT file into the ISM KB and verify with a query:
    python scripts/add_feedback_to_kb.py \
      --domain ism \
      --file /Users/allenliu/Desktop/ML-Project/AutocollableSNAgt/generated_documents/ism/my_doc.txt \
      --verify-query "barrier level"

  - Ingest a JSON output file into PRS KB, with explicit feedback text and session id:
    python scripts/add_feedback_to_kb.py \
      --domain prs \
      --file /Users/allenliu/Desktop/ML-Project/AutocollableSNAgt/generated_documents/prs/product_sheet.json \
      --feedback-text "Add this version as a reference template for PRS" \
      --session-id my-local-session

This script performs the following steps:
  1) Creates (or uses) a conversation session and posts a knowledge_update feedback entry.
  2) Inserts the provided document content into the target domain's LightRAG knowledge base.
  3) Approves and marks the knowledge update as implemented in the conversation manager for traceability.
  4) Optionally runs a verification query against the domain KB and prints the result.
"""

import argparse
import asyncio
from pathlib import Path
from typing import Optional

import sys

# Ensure project root is on sys.path so `core` and `agents` imports work when run as a script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.conversation_manager import (
    get_conversation_manager,
    KnowledgeUpdateType,
)
from core.global_agent import global_agent, FeedbackType
from core.rag_manager import rag_manager


async def ingest_feedback(
    domain: str,
    file_path: str,
    session_id: Optional[str],
    user_id: Optional[str],
    feedback_text: Optional[str],
    priority: str,
    verify_query: Optional[str],
):
    cm = get_conversation_manager()

    # Ensure file exists and load content
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    document_content = path.read_text(encoding="utf-8", errors="ignore")

    # Create or attach to a conversation session
    conversation = cm.create_conversation(
        user_id=user_id or "cli-user",
        title=f"KB update for {domain.upper()} from {path.name}",
        description=f"Ingesting generated document '{path.name}' into {domain.upper()} KB via CLI",
        session_id=session_id,
    )

    # Post feedback (knowledge_update) into the conversation
    feedback_text = feedback_text or (
        f"Knowledge update: add '{path.name}' content into {domain.upper()} knowledge base."
    )

    await global_agent.handle_feedback(
        session_id=conversation.session_id,
        feedback=feedback_text,
        feedback_type=FeedbackType.KNOWLEDGE_UPDATE,
        target_agent=domain,
        priority=priority,
    )

    # Insert the document into the domain KB
    insert_result = await rag_manager.insert_document(
        domain=domain,
        document_content=document_content,
    )

    # Best-effort: approve and mark the last knowledge update as implemented for audit trail
    # (Only if a knowledge update was created by handle_feedback)
    updates = cm.get_conversation(conversation.session_id).knowledge_updates
    if updates:
        last_update = updates[-1]
        cm.approve_knowledge_update(
            update_id=last_update.update_id,
            approver=user_id or "cli-user",
            comments="Auto-approved via CLI after successful insertion",
        )
        cm.implement_knowledge_update(
            update_id=last_update.update_id,
            implementer=user_id or "cli-user",
            implementation_details={"file": str(path), "insert_success": insert_result.get("success", False)},
        )

    # Optional verification query
    verification_output = None
    if verify_query:
        verification_output = await rag_manager.query_domain(
            domain=domain,
            query=verify_query,
            mode="mix",
            top_k=3,
        )

    return {
        "session_id": conversation.session_id,
        "insert_result": insert_result,
        "verification_output": verification_output,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add feedback from a generated document to a domain KB and record it in the conversation/audit trail.",
    )
    parser.add_argument(
        "--domain",
        required=True,
        choices=["ism", "bsp", "prs", "pds"],
        help="Target domain/agent knowledge base to update.",
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Absolute path to the generated document to ingest (TXT/JSON/etc).",
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help="Optional existing session id to attach this feedback to (otherwise a new one is created).",
    )
    parser.add_argument(
        "--user-id",
        default=None,
        help="Optional user id for audit trail metadata (defaults to 'cli-user').",
    )
    parser.add_argument(
        "--feedback-text",
        default=None,
        help="Optional feedback text to store in the conversation (defaults to a sensible message).",
    )
    parser.add_argument(
        "--priority",
        default="normal",
        choices=["low", "normal", "high", "urgent"],
        help="Feedback priority.",
    )
    parser.add_argument(
        "--verify-query",
        default=None,
        help="Optional query to run against the domain KB after insertion for a quick verification.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    result = asyncio.run(
        ingest_feedback(
            domain=args.domain,
            file_path=args.file,
            session_id=args.session_id,
            user_id=args.user_id,
            feedback_text=args.feedback_text,
            priority=args.priority,
            verify_query=args.verify_query,
        )
    )

    print("=== Feedback + KB Update Complete ===")
    print(f"Session ID: {result['session_id']}")
    print(f"Insert Result: {result['insert_result']}")
    if result.get("verification_output") is not None:
        print("--- Verification Output (truncated) ---")
        # LightRAG may return long text; keep it readable
        out = str(result["verification_output"]).strip()
        print(out[:2000])


if __name__ == "__main__":
    main()


