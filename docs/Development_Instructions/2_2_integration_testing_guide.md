# Component Integration Tests

This directory contains comprehensive integration tests for the AutocollableSNAgt framework's core components. These tests validate the interaction between different components and ensure the system works correctly as a whole.

## Test Structure

### 1. Router Integration Tests (`test_router_integration.py`)

Tests the SmartAgentRouter's ability to analyze requests and route them to appropriate agents.

**Test Scenarios:**
- **Single Agent Routing**: Tests routing to ISM agent only
- **Multi-Agent Routing**: Tests routing to multiple agents (ISM + BSP)
- **Confidence Scoring**: Validates confidence scoring accuracy for different request types
- **Information Extraction**: Tests extraction of key information from natural language requests
- **Task Decomposition**: Validates complex task breakdown into sub-tasks
- **Error Handling**: Tests handling of invalid or malformed requests
- **Routing Decision Validation**: Tests decision validation and missing information suggestions
- **Agent Capabilities**: Tests retrieval of agent capabilities and supported tasks
- **Route Request Method**: Tests the route_request method functionality
- **Edge Cases**: Tests boundary conditions and special characters

### 2. GlobalAgent Integration Tests (`test_global_agent_integration.py`)

Tests the GlobalAgent's orchestration capabilities and session management.

**Test Scenarios:**
- **Session Management**: Tests session creation, retrieval, and cleanup
- **Agent Coordination**: Tests coordination between multiple agents
- **Result Aggregation**: Tests aggregation of results from multiple agents
- **Feedback Processing**: Tests processing of different types of user feedback
- **Conversation State Transitions**: Tests state transitions based on feedback
- **Error Recovery**: Tests error recovery mechanisms for invalid inputs
- **Conversation History**: Tests conversation history management
- **Agent Status**: Tests agent status retrieval functionality
- **Audit Trail**: Tests audit trail functionality
- **Conversation Statistics**: Tests statistics generation
- **Edge Cases**: Tests concurrent sessions and special inputs

### 3. ISM Agent Integration Tests (`test_ism_agent_integration.py`)

Tests the ISM Agent's document generation and knowledge base integration capabilities.

**Test Scenarios:**
- **Document Generation Workflow**: Tests complete document generation process
- **Template Retrieval and Customization**: Tests template retrieval and customization
- **Knowledge Base Integration**: Tests integration with knowledge base
- **Large Text Template Handling**: Tests handling of large templates with many placeholders
- **Custom Placeholder Processing**: Tests processing of custom placeholders
- **Output Validation and Formatting**: Tests output validation and formatting requirements
- **Customized Document Generation**: Tests generation with audience overrides
- **Knowledge Update Integration**: Tests knowledge update proposal and application
- **Edge Cases**: Tests minimal inputs and error handling

## Running the Tests

### Prerequisites

1. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Make sure the knowledge bases are properly set up:
```bash
# Knowledge bases should be in the knowledge_bases/ directory
ls knowledge_bases/ism_kb/
```

### Running Individual Test Files

```bash
# Run Router integration tests
python tests/integration/test_router_integration.py

# Run GlobalAgent integration tests
python tests/integration/test_global_agent_integration.py

# Run ISM Agent integration tests
python tests/integration/test_ism_agent_integration.py
```

### Running All Integration Tests

Use the comprehensive test runner:

```bash
python tests/integration/run_integration_tests.py
```

This will:
- Run all integration tests
- Provide detailed progress reporting
- Generate a comprehensive summary report
- Save results to JSON file
- Return appropriate exit codes

### Running with pytest

```bash
# Run all integration tests with pytest
pytest tests/integration/ -v

# Run specific test file
pytest tests/integration/test_router_integration.py -v

# Run specific test method
pytest tests/integration/test_router_integration.py::TestRouterIntegration::test_single_agent_routing_ism_only -v
```

## Test Output

### Console Output

The tests provide detailed console output showing:
- Test progress with ✓/✗ indicators
- Detailed error messages for failed tests
- Component-specific test results
- Overall summary statistics

### JSON Results

Test results are automatically saved to:
```
tests/integration/results/integration_test_results_YYYYMMDD_HHMMSS.json
```

The JSON file contains:
- Overall test statistics
- Component-specific results
- Detailed test outcomes
- Error messages and stack traces
- Performance metrics

## Test Configuration

### Mocking Strategy

The tests use extensive mocking to:
- Avoid actual LLM API calls
- Mock LightRAG knowledge base queries
- Mock agent execution for faster testing
- Provide predictable test scenarios

### Test Data

Sample test data includes:
- Realistic ISM input scenarios
- Multi-agent request examples
- Complex document generation requests
- Edge cases and error conditions

## Expected Results

### Success Criteria

- **Router Tests**: Should correctly identify agent types and extract information
- **GlobalAgent Tests**: Should manage sessions and coordinate agents properly
- **ISM Agent Tests**: Should generate valid documents and handle templates

### Performance Expectations

- **Test Duration**: Complete suite should run in < 30 seconds
- **Success Rate**: > 90% of tests should pass
- **Error Handling**: All error conditions should be handled gracefully

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the project root is in Python path
2. **Missing Dependencies**: Install all required packages
3. **Knowledge Base Issues**: Verify knowledge base files exist
4. **Mock Failures**: Check mock configurations

### Debug Mode

Run tests with verbose output:
```bash
python tests/integration/run_integration_tests.py --verbose
```

### Individual Test Debugging

To debug a specific test:
```bash
# Add debug prints to test method
# Run with -s flag to see print statements
pytest tests/integration/test_router_integration.py::TestRouterIntegration::test_single_agent_routing_ism_only -v -s
```

## Integration with CI/CD

### GitHub Actions

Add to your workflow:
```yaml
- name: Run Integration Tests
  run: python tests/integration/run_integration_tests.py
```

### Exit Codes

- **0**: All tests passed
- **1**: Some tests failed
- **2**: Test runner error

## Contributing

### Adding New Tests

1. Follow the existing test structure
2. Use descriptive test names
3. Include comprehensive assertions
4. Add proper error handling
5. Update this README

### Test Guidelines

- Use fixtures for common setup
- Mock external dependencies
- Test both success and failure scenarios
- Include edge cases and boundary conditions
- Provide clear error messages

## Test Coverage

The integration tests cover:

- **Component Interactions**: How components work together
- **Data Flow**: Information flow between components
- **Error Propagation**: How errors are handled across components
- **State Management**: Session and conversation state handling
- **Resource Management**: Memory and resource cleanup
- **Performance**: Response times and throughput
- **Reliability**: Error recovery and fault tolerance

This comprehensive test suite ensures the AutocollableSNAgt framework is robust, reliable, and ready for production use. 