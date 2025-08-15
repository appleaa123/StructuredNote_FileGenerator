# Knowledge Bases

This directory contains LightRAG knowledge bases for each agent type. **IMPORTANT: The current knowledge bases contain sensitive financial data and should NOT be shared publicly.**

## 🔒 **Security Notice**

The existing knowledge bases contain:
- **Proprietary financial documents** with specific company information
- **CUSIP numbers** and fund codes
- **Specific product details** and pricing information
- **Company-specific templates** and examples

## 🚀 **For Open Source Distribution**

### **Option 1: Empty Knowledge Bases (Recommended)**
- Users will need to populate their own knowledge bases
- Provides maximum security and flexibility
- Users can add their own company-specific documents

### **Option 2: Generic Template Knowledge Bases**
- Contains generic, non-sensitive financial document examples
- Demonstrates the structure and format
- Users can customize with their own content

## 📁 **Directory Structure**

```
knowledge_bases/
├── investor_summary_kb/          # Formerly 'ism_kb'
├── base_shelf_prospectus_kb/     # Formerly 'bsp_kb'
├── product_supplement_kb/        # Formerly 'pds_kb'
├── pricing_supplement_kb/        # Formerly 'prs_kb'
└── README.md                     # This file
```

## 🔧 **How to Populate Knowledge Bases**

### **Step 1: Prepare Your Documents**
- Convert your financial documents to text format
- Ensure no sensitive information is included
- Use generic company names and examples

### **Step 2: Use LightRAG to Build Knowledge Base**
```python
from lightrag import LightRAG

# Initialize LightRAG
rag = LightRAG()

# Add your documents
rag.add_documents(your_documents)

# Save the knowledge base
rag.save("knowledge_bases/your_agent_kb/")
```

### **Step 3: Test Your Knowledge Base**
- Run the agent with your populated knowledge base
- Verify document generation works correctly
- Ensure no sensitive data appears in outputs

## 📋 **Required Knowledge Base Files**

Each knowledge base should contain:
- `kv_store_full_docs.json` - Full document content
- `kv_store_text_chunks.json` - Document chunks for retrieval
- `vdb_chunks.json` - Vector database chunks
- `vdb_entities.json` - Entity information
- `vdb_relationships.json` - Relationship data
- `graph_chunk_entity_relation.graphml` - Knowledge graph

## ⚠️ **Important Notes**

1. **Never commit sensitive financial data** to version control
2. **Use .gitignore** to exclude knowledge base files
3. **Provide clear instructions** for users to populate their own data
4. **Test thoroughly** with generic examples before distribution

## 🎯 **Next Steps**

1. **Remove sensitive knowledge bases** from the repository
2. **Create generic template examples** (optional)
3. **Update documentation** to explain the setup process
4. **Test with empty knowledge bases** to ensure functionality
