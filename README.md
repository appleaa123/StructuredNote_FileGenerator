# Multi-Agent Financial Document Generation Framework

Enterprise-grade framework for generating structured note documentation (Investor Summary, Base Shelf Prospectus, Product Supplement, Pricing Supplement) using specialized AI agents with LightRAG knowledge retrieval and Pydantic-typed IO models. Outputs DOCX/JSON/TXT with consistent naming.

## 🎯 What you can build
- **Investor Summary**: Investor-friendly summaries (production-ready)
- **Base Shelf Prospectus**: Base Shelf Prospectus (large-text templates + DOCX ready; LLM path available)
- **Product Supplement**: Product Supplement (large-text templates + DOCX ready; LLM path available)
- **Pricing Supplement**: Pricing Supplement (large-text templates + DOCX ready; LLM path available)

## ✅ Status at a glance
- **Core framework** (routing, conversation, RAG): ready
- **Investor Summary**: fully implemented with tests
- **Base Shelf Prospectus**: implemented with large-text/DOCX and knowledge hooks
- **Product Supplement/Pricing Supplement**: implemented large-text/DOCX paths and baseline LLM paths; document generators are minimal but functional for template rendering
- **Open Source Ready**: All sensitive data removed, comprehensive documentation provided

## 🧩 Architecture
- `core/global_agent.py`: Orchestrates multi-agent workflows via `process_request(...)`
- `core/router.py`: Analyzes NL requests → extracts fields → chooses agents
- `core/conversation_manager.py`: Sessions, feedback, audit
- `agents/*`: Specialized agents with models, tools, instructions, and template integrations
- `knowledge_bases/*_kb/`: LightRAG stores per agent (empty by default for security)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key (or other supported LLM provider)
- macOS/Linux/WSL recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AutocollableSNAgt
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env_template.txt .env  # if available, or create manually
   # Edit .env with your API keys and settings
   ```

### Basic Usage

⚠️ **Important**: The framework comes with empty knowledge bases for security. You must populate them with your own financial documents before use.

1. **Set up knowledge bases** (Required first step)
   ```bash
   # See SETUP_GUIDE.md for detailed instructions
   python -c "from agents.factory import create_agent_with_factory; agent = create_agent_with_factory('investor_summary'); print('Agent created successfully!')"
   ```

2. **Run the example**
   ```bash
   python main_example.py
   ```

3. **Generate full document suite**
   ```bash
   python scripts/generate_all_docx.py
   ```

**📚 For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

## 🔧 Step-by-Step Implementation Guide

### **Phase 1: Environment Setup**

#### Step 1: System Requirements
```bash
# Check Python version
python --version  # Should be 3.11+

# Check pip
pip --version

# Install git if not available
# macOS: brew install git
# Ubuntu: sudo apt-get install git
# Windows: Download from https://git-scm.com/
```

#### Step 2: Repository Setup
```bash
# Clone the repository
git clone <your-repository-url>
cd AutocollableSNAgt

# Verify structure
ls -la
# Should see: agents/, core/, knowledge_bases/, scripts/, etc.
```

#### Step 3: Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (choose your OS)
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Verify activation
which python  # Should point to .venv/bin/python
pip list      # Should show minimal packages
```

#### Step 4: Dependencies
```bash
# Install requirements
pip install -r requirements.txt

# Verify key packages
python -c "import pydantic, lightrag, openai; print('Dependencies installed successfully!')"
```

#### Step 5: Environment Configuration
```bash
# Create .env file
cat > .env << EOF
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL=gpt-4o-mini
MAX_TOKENS=4000
TEMPERATURE=0.1

# Project paths
KNOWLEDGE_BASES_ROOT=knowledge_bases
GENERATED_DOCUMENTS_ROOT=generated_documents

# Custom variables file
CUSTOM_VARS_JSON=inputs/custom_vars_series5.json
EOF

# Verify .env
cat .env
```

### **Phase 2: Knowledge Base Setup**

#### Step 1: Understand the Current State
```bash
# Check knowledge base structure
ls -la knowledge_bases/
# Should see empty directories with README files

# View setup instructions
cat knowledge_bases/README.md
```

#### Step 2: Prepare Your Documents
```bash
# Create a directory for your source documents
mkdir -p my_documents

# Add your financial documents (ensure they're generic/non-sensitive)
# Example: my_documents/generic_autocallable_note.txt
cat > my_documents/generic_autocallable_note.txt << EOF
GENERIC AUTOCALLABLE NOTES - SERIES X
Principal at Risk Notes – Due [DATE]

[COMPANY NAME] short form base shelf prospectus dated [DATE], 
a prospectus supplement thereto dated [DATE] and pricing supplement 
No. [NUMBER] (the "pricing supplement") thereto dated [DATE] 
(collectively, the "Prospectus") have been filed with the securities 
regulatory authorities in [JURISDICTION].

KEY TERMS
Issuer: [COMPANY NAME]
Reference Portfolio: [GENERIC PORTFOLIO DESCRIPTION]
Principal Amount: $100.00 per Note
Term to Maturity: [X] years
Autocall Trigger: [X]% of Initial Portfolio Price
Barrier Level: [X]% of Initial Portfolio Price
Fixed Return: [X]% annually
Additional Return Leverage: [X]% of excess performance
EOF
```

#### Step 3: Build Knowledge Bases
```bash
# Create a script to build knowledge bases
cat > build_knowledge_bases.py << 'EOF'
#!/usr/bin/env python3
"""
Script to build knowledge bases from your documents.
"""

import os
from pathlib import Path

def build_knowledge_base(documents, output_path):
    """Build a knowledge base from documents."""
    
    try:
        from lightrag import LightRAG
        
        # Initialize LightRAG
        rag = LightRAG()
        
        # Add documents
        for doc in documents:
            rag.add_document(doc)
        
        # Save knowledge base
        rag.save(output_path)
        print(f"✅ Knowledge base saved to {output_path}")
        
    except ImportError:
        print(f"⚠️  LightRAG not available, creating placeholder structure for {output_path}")
        # Create placeholder structure
        os.makedirs(output_path, exist_ok=True)
        
        # Create placeholder files
        placeholder_content = {
            "documents": documents,
            "note": "This is a placeholder knowledge base. Install LightRAG to build the full knowledge base."
        }
        
        import json
        with open(os.path.join(output_path, "placeholder_kb.json"), "w") as f:
            json.dump(placeholder_content, f, indent=2)

def main():
    """Build knowledge bases for all agent types."""
    
    # Read your documents
    docs_dir = Path("my_documents")
    documents = []
    
    if docs_dir.exists():
        for doc_file in docs_dir.glob("*.txt"):
            with open(doc_file, "r") as f:
                documents.append(f.read())
        print(f"📚 Found {len(documents)} documents")
    else:
        # Create sample document if none exist
        sample_doc = """
        SAMPLE FINANCIAL DOCUMENT
        
        This is a generic financial document template.
        Replace with your own financial documents.
        
        Key Terms:
        - Issuer: [COMPANY NAME]
        - Product: [PRODUCT DESCRIPTION]
        - Principal: $100.00
        - Term: [X] years
        """
        documents = [sample_doc]
        print("📝 Using sample document")
    
    # Build knowledge bases for each agent type
    agent_types = [
        "investor_summary",
        "base_shelf_prospectus", 
        "product_supplement",
        "pricing_supplement"
    ]
    
    for agent_type in agent_types:
        kb_path = f"knowledge_bases/{agent_type}_kb"
        print(f"\n🔨 Building {agent_type} knowledge base...")
        build_knowledge_base(documents, kb_path)
    
    print("\n🎉 Knowledge base setup complete!")
    print("Next: Test agent creation and document generation")

if __name__ == "__main__":
    main()
EOF

# Make executable and run
chmod +x build_knowledge_bases.py
python build_knowledge_bases.py
```

#### Step 4: Verify Knowledge Base Structure
```bash
# Check the structure
ls -la knowledge_bases/investor_summary_kb/
ls -la knowledge_bases/base_shelf_prospectus_kb/

# Should see either LightRAG files or placeholder files
```

### **Phase 3: Agent Testing and Validation**

#### Step 1: Test Agent Creation
```bash
# Test creating all agents
python -c "
from agents.factory import create_agent_with_factory

agents = {}
for agent_type in ['investor_summary', 'base_shelf_prospectus', 'product_supplement', 'pricing_supplement']:
    try:
        agents[agent_type] = create_agent_with_factory(agent_type)
        print(f'✅ {agent_type}: Created successfully')
    except Exception as e:
        print(f'❌ {agent_type}: Failed - {e}')

print(f'\n🎯 Total agents created: {len([a for a in agents.values() if a])}/4')
"
```

#### Step 2: Test Basic Functionality
```bash
# Test the main example
python main_example.py

# Expected output: Either successful generation or clear error messages
# If successful, check for generated documents
ls -la generated_documents/
```

#### Step 3: Test Individual Agents
```bash
# Test investor summary agent specifically
python -c "
import asyncio
from agents.factory import create_agent_with_factory
from agents.investor_summary.models import ISMInput

async def test_agent():
    try:
        # Create agent
        agent = create_agent_with_factory('investor_summary')
        print('✅ Agent created')
        
        # Test input
        input_data = ISMInput(
            company_name='Example Financial Services Inc.',
            product_name='Example Autocallable Notes Series 1',
            principal_amount=10000,
            term_years=5,
            reference_portfolio='Example US Market Basket',
            autocall_trigger=0.95,
            barrier_level=0.80,
            fixed_return=0.08,
            additional_return_leverage=0.05
        )
        print('✅ Input data created')
        
        # Test document generation (this may take time and API calls)
        print('🔄 Testing document generation...')
        result = await agent.generate_document(input_data)
        print(f'✅ Document generated: {result.document_title}')
        
    except Exception as e:
        print(f'❌ Error: {e}')

# Run test
asyncio.run(test_agent())
"
```

### **Phase 4: Document Generation**

#### Step 1: Generate Individual Documents
```bash
# Generate investor summary
python -c "
import asyncio
from agents.factory import create_agent_with_factory
from agents.investor_summary.models import ISMInput

async def generate_ism():
    agent = create_agent_with_factory('investor_summary')
    
    input_data = ISMInput(
        company_name='Your Company Name',
        product_name='Your Product Name',
        principal_amount=50000,
        term_years=7,
        reference_portfolio='Your Reference Portfolio',
        autocall_trigger=0.97,
        barrier_level=0.75,
        fixed_return=0.12,
        additional_return_leverage=0.06
    )
    
    result = await agent.generate_document(input_data)
    print(f'Document generated: {result.document_title}')
    return result

asyncio.run(generate_ism())
"
```

#### Step 2: Generate Full Document Suite
```bash
# Generate all documents
python scripts/generate_all_docx.py

# Check outputs
ls -la generated_documents/
ls -la generated_documents/investor_summary/
ls -la generated_documents/base_shelf_prospectus/
```

#### Step 3: Customize Outputs
```bash
# Edit custom variables
cat inputs/custom_vars_series5.json

# Modify with your company information
# Then regenerate
python scripts/generate_all_docx.py
```

### **Phase 5: Feedback and Iteration**

#### Step 1: Review Generated Documents
```bash
# Open generated documents
# macOS:
open generated_documents/investor_summary/*.docx
# Linux:
xdg-open generated_documents/investor_summary/*.docx
# Windows:
# start generated_documents\investor_summary\*.docx
```

#### Step 2: Provide Feedback
```bash
# Create feedback file
cat > feedback.md << EOF
# Document Generation Feedback

## Generated Documents Review
- [ ] Investor Summary: [Feedback here]
- [ ] Base Shelf Prospectus: [Feedback here]
- [ ] Product Supplement: [Feedback here]
- [ ] Pricing Supplement: [Feedback here]

## Quality Assessment
- [ ] Content accuracy
- [ ] Formatting quality
- [ ] Compliance requirements
- [ ] Readability

## Suggested Improvements
1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

## Next Steps
- [ ] Refine templates
- [ ] Update knowledge base
- [ ] Adjust agent configurations
- [ ] Test with different inputs
EOF
```

#### Step 3: Iterate and Improve
```bash
# Based on feedback, update your knowledge base
python build_knowledge_bases.py

# Test changes
python main_example.py

# Generate updated documents
python scripts/generate_all_docx.py
```

## 🔒 Security & Compliance
- **Empty knowledge bases by default** - no sensitive data included
- **Secrets via `.env`** - never commit sensitive information
- **Deterministic placeholder validation** for templated outputs
- **Audit trail** under `conversation_data/`
- **Comprehensive .gitignore** to prevent accidental data exposure

## 🧪 Testing
```bash
# Run all tests
python tests/run_all_tests.py all --verbose --save-results

# Run specific test suites
python tests/run_all_tests.py unit --verbose
python tests/run_all_tests.py integration --verbose

# See `tests/README.md` for structure and targeted test runners
```

## 🧱 Customization
- **Edit large-text templates**:
  - `agents/investor_summary/large_text_templates.py`
  - `agents/base_shelf_prospectus/large_text_templates.py`
  - `agents/product_supplement/large_text_templates.py`
  - `agents/pricing_supplement/large_text_templates.py`
- **Enforce placeholder validation** to catch missing data in DOCX export
- **Tune agent configs** for tone, structure, and compliance targets
- **Add/ingest documents** into `knowledge_bases/*_kb/` and initialize via RAG components

## 🧠 Key modules
```text
core/
  global_agent.py         # Orchestration entrypoint
  router.py               # NL → agent & field extraction
  conversation_manager.py # sessions, feedback, audit trail
agents/
  investor_summary/       # Investor summary generation
  base_shelf_prospectus/  # Base shelf prospectus generation
  product_supplement/     # Product supplement generation
  pricing_supplement/     # Pricing supplement generation
scripts/
  generate_all_docx.py    # suite generation with DOCX
  generate_all_from_custom_vars.py
```

## 🆘 Troubleshooting

### Common Issues

#### **Issue: "Knowledge base not found"**
**Solution**: Ensure knowledge base directories exist and contain required files
```bash
ls -la knowledge_bases/
python build_knowledge_bases.py
```

#### **Issue: "Agent creation failed"**
**Solution**: Check that all dependencies are installed and environment variables are set
```bash
pip list | grep -E "(pydantic|lightrag|openai)"
cat .env
```

#### **Issue: "Document generation error"**
**Solution**: Verify your input data matches the expected Pydantic model structure
```bash
python -c "from agents.investor_summary.models import ISMInput; print(ISMInput.__annotations__)"
```

#### **Issue: "API rate limit exceeded"**
**Solution**: Check your OpenAI API usage and adjust rate limits
```bash
# Check API key
echo $OPENAI_API_KEY
# Reduce concurrent requests or upgrade plan
```

### Getting Help
1. **Check Logs**: Review console output for detailed error messages
2. **Verify Setup**: Ensure all prerequisites and configuration steps are completed
3. **Test Incrementally**: Test each component individually before full integration
4. **Community Support**: Check project issues and discussions for similar problems

## 📚 Additional Resources

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[KNOWLEDGE_BASE_SOLUTION.md](KNOWLEDGE_BASE_SOLUTION.md)** - Security implementation details
- **[CHANGELOG.md](CHANGELOG.md)** - Project change history
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project

## 🎯 Success Metrics

- ✅ **All agents can be created** without errors
- ✅ **Knowledge bases are populated** with your documents
- ✅ **Document generation works** with your inputs
- ✅ **No sensitive data appears** in generated outputs
- ✅ **Framework is ready** for production use

## Roadmap
- **Web UI** (FastAPI/Streamlit)
- **Cross-document consistency checks**
- **Expanded knowledge base templates**
- **Enhanced compliance features**
- **Multi-language support**

---

**🎉 Congratulations! You've successfully set up the Multi-Agent Financial Document Generation Framework.**

The framework is now ready to generate financial documents using your own knowledge bases while maintaining security and compliance standards.

**If you run into issues, check your `.env`, ensure Python 3.11+, review the troubleshooting section above, and consult the additional resources.**