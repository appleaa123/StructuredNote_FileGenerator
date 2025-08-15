# Contributing to Multi-Agent Financial Document Generation Framework

Thank you for your interest in contributing to our project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Report issues you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with code changes
- **Documentation**: Improve or add documentation
- **Testing**: Help test the framework and report issues
- **Examples**: Create example configurations or use cases

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request** with a clear description

## 🏗️ Development Setup

### Prerequisites

- Python 3.11+
- Git
- Virtual environment tool (venv, conda, etc.)

### Local Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test categories
python tests/run_all_tests.py unit
python tests/run_all_tests.py integration
python tests/run_all_tests.py agents

# Run with coverage
pytest --cov=agents --cov=core tests/
```

### Code Quality Tools

```bash
# Format code
black .
isort .

# Lint code
flake8 .

# Type checking
mypy .

# Security checks
bandit -r .
```

## 📝 Coding Standards

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

### Code Structure

- Place new agents in `agents/` directory
- Follow existing agent structure (agent.py, models.py, config.py, etc.)
- Update router capabilities when adding new agents
- Add tests for new functionality
- Update documentation for new features

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(router): add support for new agent type`
- `fix(ism): resolve template rendering issue`
- `docs(readme): update installation instructions`

## 🧪 Testing Guidelines

### Test Requirements

- All new code must have corresponding tests
- Maintain test coverage above 80%
- Tests should be independent and repeatable
- Use descriptive test names that explain the scenario

### Test Structure

```python
def test_agent_generates_document_successfully():
    """Test that agent successfully generates a document with valid input."""
    # Arrange
    agent = TestAgent()
    input_data = ValidInputData()
    
    # Act
    result = agent.generate_document(input_data)
    
    # Assert
    assert result.success is True
    assert result.document is not None
```

### Running Tests Locally

```bash
# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v

# Run tests and generate coverage report
pytest --cov=agents --cov=core --cov-report=html tests/
```

## 📚 Documentation

### Documentation Standards

- Write clear, concise documentation
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Use proper markdown formatting

### Required Documentation

- README.md with setup and usage instructions
- API documentation for public interfaces
- Configuration guides for each agent
- Example configurations and use cases

## 🔒 Security

### Security Guidelines

- Never commit API keys or sensitive credentials
- Use environment variables for configuration
- Validate all user inputs
- Follow secure coding practices
- Report security vulnerabilities privately

### Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public issue
2. Email security@example.com with details
3. Include steps to reproduce the issue
4. Allow time for response before public disclosure

## 🚀 Pull Request Process

### Before Submitting

1. **Test thoroughly** - Ensure all tests pass
2. **Update documentation** - Include any new features or changes
3. **Check code quality** - Run linting and formatting tools
4. **Review changes** - Self-review your code before submitting

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test addition/update

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Address feedback** and make requested changes
4. **Maintainer approval** required for merge

## 🏷️ Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes prepared

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions and reviews

### Questions and Support

- Check existing documentation first
- Search existing issues and discussions
- Create a new issue for bugs or feature requests
- Use discussions for questions and help

## 🙏 Recognition

Contributors will be recognized in:

- Project README
- Release notes
- Contributor statistics
- Special acknowledgments for significant contributions

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to our project! Your contributions help make this framework better for everyone.
