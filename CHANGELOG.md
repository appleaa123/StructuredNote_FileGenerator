# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-08-14 - Open Source Preparation

### 🏗️ Major Changes

#### Agent Naming Standardization
- **Renamed agent directories** to use official names:
  - `agents/ism/` → `agents/investor_summary/`
  - `agents/bsp/` → `agents/base_shelf_prospectus/`
  - `agents/pds/` → `agents/product_supplement/`
  - `agents/prs/` → `agents/pricing_supplement/`

- **Renamed knowledge base directories**:
  - `knowledge_bases/ism_kb/` → `knowledge_bases/investor_summary_kb/`
  - `knowledge_bases/bsp_kb/` → `knowledge_bases/base_shelf_prospectus_kb/`
  - `knowledge_bases/pds_kb/` → `knowledge_bases/product_supplement_kb/`
  - `knowledge_bases/prs_kb/` → `knowledge_bases/pricing_supplement_kb/`

- **Renamed generated documents directories**:
  - `generated_documents/ism/` → `generated_documents/investor_summary/`
  - `generated_documents/bsp/` → `generated_documents/base_shelf_prospectus/`
  - `generated_documents/pds/` → `generated_documents/product_supplement/`
  - `generated_documents/prs/` → `generated_documents/pricing_supplement/`

#### Code Updates
- **Updated core configuration** (`core/config.py`) to map old agent names to new names
- **Updated router** (`core/router.py`) to use new agent enum values and names
- **Updated agent factory** (`agents/factory.py`) to support both old and new names
- **Updated agent registry** (`agents/__init__.py`) to register agents with new names
- **Updated all import statements** throughout the codebase to use new directory names
- **Maintained backward compatibility** - old agent names (`ism`, `bsp`, `pds`, `prs`) still work

### 🔒 Security & Privacy

#### Sensitive Data Removal
- **Removed specific company information** from example configurations
- **Replaced Scotia Bank details** with generic "Example Financial Services Inc."
- **Updated contact information** to use placeholder values
- **Generalized product examples** to remove proprietary information
- **Updated test configurations** to use generic examples

#### Configuration Generalization
- **Updated `inputs/custom_vars_series5.json`** with generic examples
- **Updated `ism_test_config.json`** with generic company information
- **Maintained functionality** while removing sensitive data

### 📚 Documentation

#### New Files Created
- **`README_OPENSOURCE.md`** - Comprehensive open source documentation
- **`LICENSE`** - MIT License for open source distribution
- **`CONTRIBUTING.md`** - Contribution guidelines for contributors
- **`CHANGELOG.md`** - This changelog documenting all changes

#### Documentation Updates
- **Updated main `README.md`** to reflect new agent names
- **Updated code comments** to use new naming conventions
- **Added clear examples** for open source users
- **Included setup instructions** for new users

### 🔧 Technical Improvements

#### Backward Compatibility
- **Maintained support** for old agent names (`ism`, `bsp`, `pds`, `prs`)
- **Automatic mapping** from old names to new names
- **No breaking changes** for existing code
- **Seamless migration** path for users

#### Code Quality
- **Consistent naming** throughout the codebase
- **Updated import paths** to use new directory structure
- **Maintained test coverage** and functionality
- **Improved code organization** with logical naming

### 🧪 Testing

#### Test Updates
- **Updated all test files** to use new import paths
- **Maintained test functionality** with new naming
- **Verified backward compatibility** works correctly
- **Confirmed all agents** can be created and used

### 🚀 Deployment

#### Open Source Ready
- **Project structure** optimized for open source distribution
- **Clear documentation** for new users
- **Generic examples** that can be customized
- **No sensitive data** in the repository
- **MIT License** for maximum adoption

### 📋 Migration Guide

#### For Existing Users
1. **No immediate changes required** - old agent names still work
2. **Update imports gradually** to use new names for better clarity
3. **Update configuration files** to use new directory paths
4. **Test functionality** with new naming conventions

#### For New Users
1. **Use new agent names** for clarity and consistency
2. **Follow setup instructions** in `README_OPENSOURCE.md`
3. **Customize examples** with your own company information
4. **Refer to contributing guidelines** if you want to contribute

### 🔮 Future Considerations

#### Potential Improvements
- **Web UI development** for easier document generation
- **Additional document types** beyond the current four
- **Enhanced template system** with more customization options
- **Cloud deployment guides** for production use
- **Multi-language support** for international users

---

## [1.0.0] - 2025-08-14 - Initial Release

### ✨ Features
- Multi-agent financial document generation framework
- Support for ISM, BSP, PDS, and PRS document types
- LightRAG integration for knowledge management
- Template-based document generation
- Multiple output formats (DOCX, JSON, TXT)
- Intelligent routing and agent selection
- Comprehensive testing suite
- Production-ready ISM agent implementation

### 🏗️ Architecture
- Modular agent-based architecture
- Pydantic models for type safety
- Async/await support for scalability
- LightRAG for knowledge retrieval
- Factory pattern for agent creation
- Registry system for agent management
