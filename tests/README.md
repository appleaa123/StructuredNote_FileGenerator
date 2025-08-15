# AutocollableSNAgt Framework - Test Suite

This directory contains all tests for the AutocollableSNAgt framework, organized by type and functionality.

## Directory Structure

```
tests/
├── README.md                           # This file
├── run_all_tests.py                    # Main test runner
├── unit/                               # Unit tests
│   ├── test_ism_agent.py              # Unified ISM agent tests
│   ├── test_global_agent.py           # Unified global agent tests
│   └── phase1_test_plan.py            # Comprehensive test plan
├── integration/                        # Integration tests
│   ├── run_integration_tests.py       # Integration test runner
│   ├── test_end_to_end_workflow.py    # End-to-end workflow tests
│   ├── test_global_agent_integration.py
│   ├── test_ism_agent_integration.py
│   └── test_router_integration.py
├── agents/                            # Agent-specific tests
│   ├── base_large_text_test.py       # Base test framework
│   ├── ism/                          # ISM agent tests
│   ├── bsp/                          # BSP agent tests
│   ├── pds/                          # PDS agent tests
│   └── prs/                          # PRS agent tests
├── core/                              # Core component tests
│   ├── test_global_agent.py          # Global agent tests
│   └── test_router.py                # Router tests
├── conversation_management/           # Conversation management tests
│   ├── test_conversation_management.py
│   ├── test_conversation_minimal.py
│   ├── test_conversation_simple.py
│   └── test_conversation_standalone.py
└── results/                          # Test results and outputs
    ├── *.json                        # Test result files
    └── *.txt                         # Test output files
```

## Test Types

### 1. Unit Tests (`tests/unit/`)
- **test_ism_agent.py**: Comprehensive ISM agent testing
  - Basic functionality testing
  - Model validation
  - Agent creation
  - Large text agent testing
  - Document generation
  - Error handling

- **test_global_agent.py**: Global agent testing
  - Constructor testing
  - Core functions
  - Agent coordination
  - Session management
  - Error handling

### 2. Integration Tests (`tests/integration/`)
- **run_integration_tests.py**: Integration test runner
- **test_end_to_end_workflow.py**: End-to-end workflow testing
- **test_global_agent_integration.py**: Global agent integration
- **test_ism_agent_integration.py**: ISM agent integration
- **test_router_integration.py**: Router integration

### 3. Agent-Specific Tests (`tests/agents/`)
- **base_large_text_test.py**: Base framework for large text agents
- **ism/**: ISM agent specific tests
- **bsp/**: BSP agent specific tests
- **pds/**: PDS agent specific tests
- **prs/**: PRS agent specific tests

### 4. Core Component Tests (`tests/core/`)
- **test_global_agent.py**: Global agent core functionality
- **test_router.py**: Router functionality

### 5. Conversation Management Tests (`tests/conversation_management/`)
- **test_conversation_management.py**: Full conversation management
- **test_conversation_minimal.py**: Minimal conversation tests
- **test_conversation_simple.py**: Simple conversation tests
- **test_conversation_standalone.py**: Standalone conversation tests

## Running Tests

### Main Test Runner
```bash
# Run all tests
python tests/run_all_tests.py all

# Run specific test types
python tests/run_all_tests.py unit
python tests/run_all_tests.py integration
python tests/run_all_tests.py e2e

# Run specific agent tests
python tests/run_all_tests.py ism
python tests/run_all_tests.py global

# With options
python tests/run_all_tests.py all --verbose --save-results
```

### Individual Test Files
```bash
# Run ISM agent tests
python tests/unit/test_ism_agent.py

# Run global agent tests
python tests/unit/test_global_agent.py

# Run integration tests
python tests/integration/run_integration_tests.py

# Run end-to-end tests
python tests/integration/test_end_to_end_workflow.py
```

### Agent-Specific Tests
```bash
# Run ISM agent tests
python tests/agents/ism/test_ism_agent_comprehensive.py

# Run conversation management tests
python tests/conversation_management/test_conversation_management.py
```

## Test Results

All test results are saved to `tests/results/` with timestamps:
- `ism_test_results_YYYYMMDD_HHMMSS.json`
- `global_agent_test_results_YYYYMMDD_HHMMSS.json`
- `comprehensive_test_results_YYYYMMDD_HHMMSS.json`

## Test Configuration

### Environment Setup
1. Ensure virtual environment is activated
2. Install all dependencies: `pip install -r requirements.txt`
3. Set up API keys for LLM services
4. Configure knowledge bases if needed

### Test Data
- Sample ISM inputs are provided in test files
- Test configurations are in `tests/agents/ism/ism_test_config.json`
- Generated documents are saved to `tests/results/`

## Test Categories

### Unit Tests
- **Purpose**: Test individual components in isolation
- **Coverage**: Models, agents, core functions
- **Speed**: Fast execution
- **Dependencies**: Minimal external dependencies

### Integration Tests
- **Purpose**: Test component interactions
- **Coverage**: Agent coordination, workflow
- **Speed**: Medium execution time
- **Dependencies**: Multiple components

### End-to-End Tests
- **Purpose**: Test complete workflows
- **Coverage**: Full user scenarios
- **Speed**: Slower execution
- **Dependencies**: Full system

## Test Scoring

Tests are scored on a scale of 0-10:
- **8-10**: Excellent - Ready for production
- **6-7**: Good - Some improvements needed
- **4-5**: Fair - Significant improvements needed
- **0-3**: Poor - Major issues to address

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure project root is in Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **API Key Issues**
   ```bash
   # Set OpenAI API key
   export OPENAI_API_KEY="your-api-key"
   ```

3. **Missing Dependencies**
   ```bash
   # Install requirements
   pip install -r requirements.txt
   ```

4. **Test Failures**
   - Check test logs in `tests/results/`
   - Verify API keys are set
   - Ensure all dependencies are installed

### Debug Mode
```bash
# Run tests with verbose output
python tests/run_all_tests.py all --verbose
```

## Contributing

When adding new tests:

1. **Unit Tests**: Add to appropriate `tests/unit/` file
2. **Integration Tests**: Add to `tests/integration/`
3. **Agent Tests**: Add to `tests/agents/[agent_type]/`
4. **Update Documentation**: Update this README if needed

### Test Naming Convention
- `test_[component]_[functionality].py`
- Use descriptive names
- Include test type in filename

### Test Structure
```python
class ComponentTester:
    def __init__(self):
        self.test_results = {}
    
    async def run_all_tests(self):
        # Test methods here
        pass
    
    def _print_summary(self):
        # Summary output
        pass
```

## Performance

- **Unit Tests**: < 30 seconds
- **Integration Tests**: < 2 minutes
- **End-to-End Tests**: < 5 minutes
- **Full Test Suite**: < 10 minutes

## Continuous Integration

Tests can be integrated into CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Run Tests
  run: python tests/run_all_tests.py all
```

## Support

For test-related issues:
1. Check test logs in `tests/results/`
2. Review this README
3. Check individual test file documentation
4. Verify environment setup 