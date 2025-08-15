# LightRAG Implementations

**LightRAG**: An advanced, lightweight RAG implementation with enhanced knowledge graph capabilities


- **Simplified API**: LightRAG provides a more streamlined API with fewer configuration parameters
- **Automatic Document Processing**: LightRAG handles document chunking and embedding automatically
- **Knowledge Graph Integration**: LightRAG leverages knowledge graph capabilities for improved context understanding
- **More Efficient Retrieval**: LightRAG's query mechanism provides more relevant results with less configuration

## Installation

### Prerequisites
- Python 3.11+
- OpenAI API key

### Setup

1. Clone this repository

2. Create a `.env` file in both the `BasicRAG` and `LightRAG` directories (or whichever you want to use) with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Set up a virtual environment and install dependencies:

   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   # Install dependencies for LightRAG
   cd LightRAG
   pip install -r requirements.txt
   
   # In a new terminal with activated venv, install BasicRAG dependencies
   cd BasicRAG
   pip install -r requirements.txt
   ```

## Running the Implementations

### LightRAG (Most Powerful)

1. **Insert Documentation** (this will take a while - using full Pydantic AI docs as an example!):
   ```bash
   cd LightRAG
   python insert_pydantic_docs.py
   ```
   This will fetch the Pydantic AI documentation and process it using LightRAG's advanced document processing.

2. **Run the Agent**:
   ```bash
   python rag_agent.py --question "How do I create a Pydantic AI agent?"
   ```

3. **Run the Interactive Streamlit App**:
   ```bash
   streamlit run streamlit_app.py
   ```
   This provides a chat interface where you can ask questions about Pydantic AI.


## Key Implementations

### Document Processing
- **LightRAG**: Automatically handles document processing with intelligent chunking

### Vector Storage
- **LightRAG**: Abstracts storage details behind a clean API with optimized defaults

### Query Mechanism
- **LightRAG**: Uses a more sophisticated query mechanism with different modes (e.g., "naive" or "hybrid")

### Code Complexity
- **LightRAG**: Offers a more concise API with fewer lines of code needed

## Project Structure

### LightRAG
- `LightRAG/rag_agent.py`: Pydantic AI agent using LightRAG
- `LightRAG/insert_pydantic_docs.py`: Script to fetch and process documentation
- `LightRAG/streamlit_app.py`: Interactive web interface