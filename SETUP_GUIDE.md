# 🚀 Setup Guide for Multi-Agent Financial Document Generation Framework

## 📋 **Prerequisites**

Before you begin, ensure you have:
- **Python 3.8+** installed
- **Git** for cloning the repository
- **Access to OpenAI API** (or other supported LLM providers)
- **Financial documents** ready for processing (with sensitive data removed)

## 🔧 **Installation**

### **Step 1: Clone the Repository**
```bash
git clone <your-repository-url>
cd AutocollableSNAgt
```

### **Step 2: Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Set Up Environment Variables**
Create a `.env` file in the project root:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional: for custom endpoints

# LightRAG Configuration
LIGHTRAG_MODEL_NAME=openai:gpt-4o-mini  # Default model
LIGHTRAG_MAX_TOKENS=4000
LIGHTRAG_TEMPERATURE=0.7

# Project Paths
KNOWLEDGE_BASES_ROOT=knowledge_bases
GENERATED_DOCUMENTS_ROOT=generated_documents
```

## 📚 **Knowledge Base Setup**

### **Important: Knowledge Bases Are Empty by Default**

The framework comes with **empty knowledge bases** for security reasons. You must populate them with your own financial documents.

### **Step 1: Prepare Your Documents**

1. **Convert to Text Format**: Ensure your financial documents are in text format
2. **Remove Sensitive Data**: Replace company names, CUSIP numbers, and proprietary information with generic placeholders
3. **Use Generic Examples**: Create templates that others can customize

**Example Generic Document:**
```
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
```

### **Step 2: Build Knowledge Bases with LightRAG**

```python
from lightrag import LightRAG
import json

def build_knowledge_base(documents, output_path):
    """Build a knowledge base from documents."""
    
    # Initialize LightRAG
    rag = LightRAG()
    
    # Add documents
    for doc in documents:
        rag.add_document(doc)
    
    # Save knowledge base
    rag.save(output_path)
    print(f"Knowledge base saved to {output_path}")

# Example usage
documents = [
    "Your generic financial document 1 content here...",
    "Your generic financial document 2 content here...",
    # Add more documents
]

# Build knowledge base for each agent type
build_knowledge_base(documents, "knowledge_bases/investor_summary_kb")
build_knowledge_base(documents, "knowledge_bases/base_shelf_prospectus_kb")
build_knowledge_base(documents, "knowledge_bases/product_supplement_kb")
build_knowledge_base(documents, "knowledge_bases/pricing_supplement_kb")
```

### **Step 3: Verify Knowledge Base Structure**

Each knowledge base should contain these files:
```
knowledge_bases/investor_summary_kb/
├── kv_store_full_docs.json          # Full document content
├── kv_store_text_chunks.json        # Document chunks for retrieval
├── vdb_chunks.json                  # Vector database chunks
├── vdb_entities.json                # Entity information
├── vdb_relationships.json           # Relationship data
└── graph_chunk_entity_relation.graphml  # Knowledge graph
```

## 🧪 **Testing Your Setup**

### **Test 1: Agent Creation**
```python
from agents.factory import create_agent_with_factory

# Test creating agents
agents = {}
for agent_type in ['investor_summary', 'base_shelf_prospectus', 'product_supplement', 'pricing_supplement']:
    try:
        agents[agent_type] = create_agent_with_factory(agent_type)
        print(f"✅ {agent_type}: Created successfully")
    except Exception as e:
        print(f"❌ {agent_type}: Failed - {e}")
```

### **Test 2: Document Generation**
```python
from agents.investor_summary.models import ISMInput

# Test input data
input_data = ISMInput(
    company_name="Example Financial Services Inc.",
    product_name="Example Autocallable Notes Series 1",
    principal_amount=10000,
    term_years=5,
    reference_portfolio="Example US Market Basket",
    autocall_trigger=0.95,
    barrier_level=0.80,
    fixed_return=0.08,
    additional_return_leverage=0.05
)

# Generate document
agent = create_agent_with_factory('investor_summary')
result = await agent.generate_document(input_data)
print(f"Document generated: {result.document_title}")
```

## 🔒 **Security Best Practices**

### **Never Commit Sensitive Data**
1. **Use .gitignore**: The project includes a `.gitignore` file that excludes knowledge bases
2. **Generic Examples**: Always use generic, non-proprietary examples
3. **Test Outputs**: Verify generated documents don't contain sensitive information
4. **Regular Audits**: Periodically review your knowledge bases for sensitive data

### **Data Sanitization Checklist**
- [ ] Company names replaced with generic placeholders
- [ ] CUSIP numbers and fund codes removed
- [ ] Specific product details generalized
- [ ] Contact information replaced with examples
- [ ] Financial figures converted to generic examples
- [ ] Regulatory jurisdiction made generic

## 🚀 **Production Deployment**

### **Environment Configuration**
```bash
# Production environment variables
OPENAI_API_KEY=your_production_key
LIGHTRAG_MODEL_NAME=openai:gpt-4o  # Use production model
KNOWLEDGE_BASES_ROOT=/secure/path/to/knowledge_bases
GENERATED_DOCUMENTS_ROOT=/secure/path/to/generated_documents
```

### **Knowledge Base Management**
1. **Regular Updates**: Keep knowledge bases current with latest regulations
2. **Backup Strategy**: Implement regular backups of your knowledge bases
3. **Access Control**: Restrict access to knowledge base directories
4. **Monitoring**: Monitor usage and performance metrics

## 🆘 **Troubleshooting**

### **Common Issues**

#### **Issue: "Knowledge base not found"**
**Solution**: Ensure knowledge base directories exist and contain required files

#### **Issue: "No documents found"**
**Solution**: Verify your knowledge base contains `kv_store_full_docs.json`

#### **Issue: "Agent creation failed"**
**Solution**: Check that all dependencies are installed and environment variables are set

#### **Issue: "Document generation error"**
**Solution**: Verify your input data matches the expected Pydantic model structure

### **Getting Help**
1. **Check Logs**: Review console output for detailed error messages
2. **Verify Setup**: Ensure all prerequisites and configuration steps are completed
3. **Test Incrementally**: Test each component individually before full integration
4. **Community Support**: Check project issues and discussions for similar problems

## 📚 **Next Steps**

1. **Customize Templates**: Modify document templates to match your needs
2. **Add More Agents**: Extend the framework with additional document types
3. **Integrate Systems**: Connect with your existing financial systems
4. **Scale Up**: Deploy to production environments with proper monitoring

## 🎯 **Success Metrics**

- ✅ **Agents can be created** without errors
- ✅ **Knowledge bases are populated** with generic examples
- ✅ **Document generation works** with test inputs
- ✅ **No sensitive data appears** in generated outputs
- ✅ **Framework is ready** for production use

---

**🎉 Congratulations! You've successfully set up the Multi-Agent Financial Document Generation Framework.**

The framework is now ready to generate financial documents using your own knowledge bases while maintaining security and compliance standards.
