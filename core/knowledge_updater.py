"""
Knowledge Updater for LightRAG
"""
import logging
from typing import Dict, Any, Optional
import asyncio

from .rag_manager import rag_manager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KnowledgeUpdater:
    """
    Handles the process of updating LightRAG knowledge bases.

    This class provides a high-level interface to parse update requests,
    plan the update, and apply it using the RAGManager. It abstracts the
    complexities of direct interaction with the knowledge base.
    """

    def __init__(self, rag_manager_instance):
        """
        Initializes the KnowledgeUpdater with a RAGManager instance.

        Args:
            rag_manager_instance: An instance of RAGManager to handle KB operations.
        """
        self.rag_manager = rag_manager_instance

    def parse_update_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses and validates the incoming update request.

        For now, this is a simple validation, but it can be expanded to
        include more complex parsing, such as identifying entities or topics.

        Args:
            request_data: A dictionary containing the update information.
                          Expected keys: 'action', 'domain', 'content'.

        Returns:
            The validated and parsed update information.

        Raises:
            ValueError: If the request data is invalid.
        """
        action = request_data.get("action")
        domain = request_data.get("domain")
        content = request_data.get("content")

        if not all([action, domain, content]):
            raise ValueError("Invalid request format. Must include 'action', 'domain', and 'content'.")
        
        if action.lower() != 'insert':
            raise ValueError(f"Action '{action}' is not supported. Only 'insert' is allowed.")

        return {"action": action, "domain": domain, "content": content}

    def create_update_plan(self, parsed_request: Dict[str, Any]) -> str:
        """
        Creates a human-readable plan for the knowledge base update.

        Args:
            parsed_request: The parsed request dictionary.

        Returns:
            A string describing the planned action.
        """
        return (f"Plan: The '{parsed_request['domain']}' knowledge base will be "
                f"updated with new content.")

    async def apply_update(self, update_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies the update to the specified LightRAG knowledge base.

        This method orchestrates the update process:
        1. It parses the request.
        2. It creates a plan (for logging and potential confirmation).
        3. It calls the RAGManager to perform the document insertion.

        Args:
            update_request: The raw update request data.

        Returns:
            A dictionary containing the result of the update operation.
        """
        try:
            parsed_request = self.parse_update_request(update_request)
            plan = self.create_update_plan(parsed_request)
            logger.info(f"Executing update plan: {plan}")

            result = await self.rag_manager.insert_document(
                domain=parsed_request['domain'],
                document_content=parsed_request['content']
            )
            
            if result.get("success"):
                logger.info("Update applied successfully.")
            else:
                logger.error(f"Failed to apply update: {result.get('message')}")

            return result

        except ValueError as e:
            logger.error(f"Update request failed validation: {e}")
            return {"success": False, "message": str(e)}
        except Exception as e:
            logger.error(f"An unexpected error occurred during the update: {e}", exc_info=True)
            return {"success": False, "message": "An unexpected error occurred."}


# Example usage:
async def main():
    """
    Example of how to use the KnowledgeUpdater to add a new document.
    """
    # Initialize the updater with the global rag_manager
    updater = KnowledgeUpdater(rag_manager)

    # Define a new document to be added to the 'ism' knowledge base
    update_data = {
        "action": "insert",
        "domain": "ism",
        "content": "Generative AI is a class of artificial intelligence that can create new and original content."
    }

    # Apply the update
    result = await updater.apply_update(update_data)
    print(result)

    # Clean up resources
    await rag_manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
