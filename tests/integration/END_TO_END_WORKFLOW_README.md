# End-to-End Workflow Tests

This directory contains comprehensive end-to-end workflow tests for the AutocollableSNAgt framework. These tests validate the complete workflow from user request to final document generation, including feedback loops and error recovery mechanisms.

## 🎯 Test Scenarios

### 1. Simple ISM Document Generation
**Objective**: Test basic ISM document generation with minimal input
- **Input**: Basic product information (name, issuer, underlying, term, currency)
- **Expected**: Complete ISM document with proper structure and content
- **Validation**: Content quality, structure, compliance, processing time

**Test Flow**:
1. User provides basic product information
2. GlobalAgent routes request to ISM agent
3. ISM agent generates document
4. System validates content quality and structure
5. Results are aggregated and returned

### 2. Complex Multi-Agent Workflow
**Objective**: Test coordination between multiple agents (with expected import errors)
- **Input**: Complex financial product request involving multiple document types
- **Expected**: ISM document generated successfully, other agents handled gracefully
- **Validation**: System stability, error handling, appropriate error messages

**Test Flow**:
1. User requests comprehensive document suite (ISM, BSP, PDS, PRS)
2. GlobalAgent attempts to route to all agents
3. ISM agent succeeds (implemented)
4. BSP, PDS, PRS agents fail gracefully (not implemented yet)
5. System provides appropriate error messages
6. Overall workflow completes successfully

### 3. User Feedback Loop
**Objective**: Test the complete feedback loop with document updates
- **Input**: Initial document + sequence of user feedback
- **Expected**: Document updated based on feedback, final approval recorded
- **Validation**: Feedback processing, content updates, state transitions

**Test Flow**:
1. Generate initial ISM document
2. User provides content update feedback
3. System updates document with requested changes
4. User provides rejection feedback
5. System regenerates document with improvements
6. User provides final approval
7. System marks document as complete

### 4. Error Recovery Workflow
**Objective**: Test graceful handling of invalid or incomplete data
- **Input**: Various invalid input scenarios
- **Expected**: Graceful error handling with helpful messages
- **Validation**: Error messages, system stability, recovery suggestions

**Test Scenarios**:
- Missing required fields
- Invalid data types
- Malformed requests
- Incomplete information

## 🚀 Running the Tests

### Prerequisites

1. **Virtual Environment**: Ensure you're in the correct virtual environment
```bash
source ism_test_env/bin/activate
```

2. **Dependencies**: Install all required packages
```bash
pip install -r requirements.txt
```

3. **Knowledge Bases**: Ensure ISM knowledge base is available
```bash
ls knowledge_bases/ism_kb/
```

### Running Tests

#### Option 1: Using the Test Runner (Recommended)
```bash
# Run all end-to-end tests
python run_end_to_end_tests.py

# Run with verbose logging
python run_end_to_end_tests.py --verbose

# Run and save detailed results
python run_end_to_end_tests.py --save-results

# Run with both verbose logging and save results
python run_end_to_end_tests.py --verbose --save-results
```

#### Option 2: Direct Test Execution
```bash
# Run the test file directly
python tests/integration/test_end_to_end_workflow.py

# Run with pytest
pytest tests/integration/test_end_to_end_workflow.py -v
```

#### Option 3: Using the Integration Test Runner
```bash
# Run all integration tests including end-to-end
python tests/integration/run_integration_tests.py
```

## 📊 Expected Results

### Success Criteria

#### Simple ISM Document Generation
- ✅ Response received within 30 seconds
- ✅ Document generated successfully
- ✅ Content quality score ≥ 0.7
- ✅ All required sections present
- ✅ Professional tone and compliance language

#### Complex Multi-Agent Workflow
- ✅ System remains stable despite import errors
- ✅ ISM agent executes successfully
- ✅ Other agents fail gracefully with import errors
- ✅ Appropriate error messages provided
- ✅ Overall workflow completes

#### User Feedback Loop
- ✅ Initial document generated
- ✅ All feedback processed successfully
- ✅ Document updated based on feedback
- ✅ State transitions are logical
- ✅ Final approval recorded

#### Error Recovery Workflow
- ✅ All error scenarios handled gracefully
- ✅ System remains stable
- ✅ Helpful error messages provided (≥80%)
- ✅ Recovery suggestions offered (≥60%)

### Performance Expectations

- **Total Execution Time**: < 60 seconds for all tests
- **Success Rate**: > 90% of individual test scenarios
- **Error Handling**: All error conditions handled gracefully
- **System Stability**: No crashes or unhandled exceptions

## 🔧 Test Configuration

### Expected Import Errors

The tests are designed to handle expected import errors for BSP, PDS, and PRS agents since they haven't been built yet:

```python
# Expected behavior for unimplemented agents
try:
    from agents.bsp import BSPAgent
except ImportError:
    # This is expected - agent not implemented yet
    pass
```

### Test Data

Sample test data includes:
- Realistic ISM input scenarios
- Multi-agent request examples
- Complex document generation requests
- Edge cases and error conditions
- Feedback sequences

### Mocking Strategy

The tests use minimal mocking to:
- Avoid actual LLM API calls where possible
- Provide predictable test scenarios
- Handle expected import errors gracefully
- Maintain realistic workflow testing

## 📈 Test Results

### Output Format

Test results are provided in multiple formats:

1. **Console Output**: Real-time progress and summary
2. **JSON Results**: Detailed results saved to file
3. **Log File**: Comprehensive logging for debugging

### Sample Output

```
🚀 Starting End-to-End Workflow Tests for AutocollableSNAgt Framework
================================================================================
📋 Running Test Scenario: Simple ISM Document Generation
✅ Simple ISM Document Generation completed: SUCCESS

📋 Running Test Scenario: Complex Multi-Agent Workflow
✅ Complex Multi-Agent Workflow completed: SUCCESS

📋 Running Test Scenario: User Feedback Loop
✅ User Feedback Loop completed: SUCCESS

📋 Running Test Scenario: Error Recovery Workflow
✅ Error Recovery Workflow completed: SUCCESS

🎯 End-to-End Workflow Tests Complete
📊 Results: 4/4 tests passed
⏱️  Total execution time: 45.23 seconds

================================================================================
📊 END-TO-END WORKFLOW TEST RESULTS
================================================================================
🎯 Overall Success Rate: 100.0%
✅ Tests Passed: 4
❌ Tests Failed: 0
⏱️  Total Execution Time: 45.23 seconds

📋 Individual Test Results:
  ✅ PASS Simple ISM Document Generation
  ✅ PASS Complex Multi-Agent Workflow
  ✅ PASS User Feedback Loop
  ✅ PASS Error Recovery Workflow

💡 Recommendations:
  🎉 All end-to-end workflow tests passed! The system is ready for production use.
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors for BSP/PDS/PRS Agents**
   - **Expected**: These agents haven't been built yet
   - **Solution**: Tests are designed to handle these gracefully
   - **Action**: Implement these agents when ready

2. **ISM Agent Import Errors**
   - **Check**: Ensure ISM agent is properly installed
   - **Solution**: Verify `agents/ism/agent.py` exists
   - **Action**: Run ISM agent tests separately

3. **Knowledge Base Issues**
   - **Check**: Verify knowledge base files exist
   - **Solution**: Ensure `knowledge_bases/ism_kb/` is populated
   - **Action**: Run knowledge base setup if needed

4. **Performance Issues**
   - **Check**: Test execution time > 60 seconds
   - **Solution**: Optimize agent execution or reduce test complexity
   - **Action**: Review agent performance

### Debug Mode

To debug specific issues:

```bash
# Run with verbose logging
python run_end_to_end_tests.py --verbose

# Check log file
tail -f end_to_end_tests.log

# Run individual test scenarios
python -c "
import asyncio
from tests.integration.test_end_to_end_workflow import EndToEndWorkflowTester
tester = EndToEndWorkflowTester()
result = asyncio.run(tester._test_simple_ism_generation(tester.test_scenarios['simple_ism_generation']))
print(result)
"
```

## 🔄 Integration with CI/CD

### GitHub Actions

Add to your workflow:
```yaml
- name: Run End-to-End Tests
  run: |
    source ism_test_env/bin/activate
    python run_end_to_end_tests.py --save-results
```

### Exit Codes

- **0**: All tests passed
- **1**: Some tests failed
- **2**: Test runner error

## 📝 Adding New Test Scenarios

### Creating New Test Scenarios

1. **Add to Test Scenarios Dictionary**:
```python
"new_scenario": {
    "name": "New Test Scenario",
    "description": "Description of the test scenario",
    "input": {
        # Test input data
    },
    "expected_outcomes": [
        # Expected outcomes
    ]
}
```

2. **Add Test Method**:
```python
async def _test_new_scenario(self, scenario_config: Dict[str, Any]) -> Dict[str, Any]:
    # Test implementation
    pass
```

3. **Update Test Runner**:
```python
if scenario_key == "new_scenario":
    result = await self._test_new_scenario(scenario_config)
```

### Test Guidelines

- **Descriptive Names**: Use clear, descriptive test names
- **Comprehensive Validation**: Test multiple aspects of functionality
- **Error Handling**: Include error scenarios and edge cases
- **Performance**: Consider execution time and resource usage
- **Documentation**: Update this README with new scenarios

## 🎯 Next Steps

### After Test Implementation

1. **Review Results**: Analyze test results and identify areas for improvement
2. **Implement Missing Agents**: Build BSP, PDS, and PRS agents
3. **Enhance Error Handling**: Improve error messages and recovery mechanisms
4. **Optimize Performance**: Reduce execution time and improve efficiency
5. **Add More Scenarios**: Expand test coverage with additional scenarios

### Production Readiness

- **Success Rate**: Aim for 100% test success rate
- **Performance**: Ensure tests complete within acceptable time limits
- **Reliability**: Verify consistent results across multiple runs
- **Documentation**: Keep test documentation up to date

---

**Status**: ✅ **END-TO-END WORKFLOW TESTS IMPLEMENTED** - Comprehensive testing framework ready for validation of complete workflows. 