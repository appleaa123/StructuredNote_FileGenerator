# Structured Notes Agent

This project contains an AI agent specialized in generating legal documents for structured notes. It is designed as a sub-agent within a larger multi-agent system for a bank. The agent leverages LightRAG for its powerful knowledge retrieval capabilities and Pydantic for ensuring data consistency and structure.

# Philosophy and High-Level Plan

My core philosophy here is to create a system that is modular, testable, and scalable. We will separate the AI's "thinking" (content generation) from the final document formatting. This allows us to evolve the agent's intelligence and the document's presentation independently.

The workflow for our first agent will be as follows:
1.Structured Input: The process begins with a clearly defined set of parameters for the structured note (e.g., issuer, maturity date, underlying asset). We will define this as a Pydantic model to ensure data validity from the start.
2.Agent-led Retrieval: The agent will receive this input and formulate targeted queries to the LightRAG knowledge base located in rag_storage/. This ensures we retrieve only the most relevant legal clauses, templates, and risk factors.
3.LLM-powered Synthesis: An LLM will then synthesize the retrieved context with the specific input parameters. This step generates the actual text for the various sections of the legal document.
4.Structured Output: The agent's final output will not be a raw document, but another Pydantic model containing the generated content, neatly organized into sections (e.g., Summary, Risk Factors, Terms). This makes the agent's output predictable and easy to work with.
5.Final Document Generation: A separate, dedicated module will take this structured output and render it into a final, user-facing document, such as a .docx file.

## Features

- **Structured Data Handling**: Utilizes Pydantic models for both input parameters and generated output, ensuring data integrity and a clear, predictable data flow.
- **Retrieval-Augmented Generation (RAG)**: Integrates with a LightRAG knowledge base (`rag_storage/`) to retrieve relevant legal clauses, templates, and risk factors, ensuring the generated documents are accurate and context-aware.
- **Modular Architecture**: The project is organized into distinct modules for configuration, data models, agent logic, and document generation, making it easy to maintain, test, and extend.
- **Automated Document Generation**: Produces a final, formatted `.docx` file from the agent's structured output.

## Project Structure

The agent's code is located in the `structured_notes_agent/` directory:

- `__init__.py`: Makes the directory a Python package.
- `config.py`: Manages configuration, including API keys and file paths.
- `models.py`: Defines the Pydantic models for structured input (`StructuredNoteInput`) and output (`StructuredNoteOutput`).
- `agent.py`: Contains the core `StructuredNotesAgent` class, which orchestrates the RAG retrieval and content synthesis.
- `document_generator.py`: A utility module to convert the agent's structured output into a `.docx` file.
- `main.py`: The main script to run the agent and generate a document.
- `requirements.txt`: Lists the Python dependencies for the project.
- `venv_structured_notes/`: A dedicated virtual environment for this agent.

## Setup and Installation

### 1. Environment Variables

Before running the agent, you need to set up your environment variables. Create a `.env` file in the root directory of this project (`AutocollableSNAgt/.env`) with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Virtual Environment and Dependencies

The project uses a dedicated virtual environment to manage its dependencies.

To set it up and install the necessary packages, run the following commands from the project's root directory:

```bash
# Create the virtual environment
python3 -m venv structured_notes_agent/venv_structured_notes

# Activate the virtual environment
# On macOS/Linux:
source structured_notes_agent/venv_structured_notes/bin/activate
# On Windows:
# .\\structured_notes_agent\\venv_structured_notes\\Scripts\\activate

# Install the required packages
pip install -r structured_notes_agent/requirements.txt
```

## How to Run the Agent

To generate a structured note document, you can run the `main.py` script. Make sure your virtual environment is activated first.

1.  **Activate the virtual environment** (if not already active):
    ```bash
    source structured_notes_agent/venv_structured_notes/bin/activate
    ```

2.  **Run the agent**:
    The `main.py` script is designed to be run as a module from the project's root directory.

    ```bash
    python -m structured_notes_agent.main
    ```

3.  **Check the Output**:
    After the script finishes, a new `.docx` file will be created in the `generated_documents/` directory. The filename will be based on the issuer and issue date (e.g., `Global_Finance_Inc._2024-07-21.docx`).
