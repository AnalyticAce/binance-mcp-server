# Contributing to Binance MCP Server

Thank you for your interest in contributing to the Binance MCP Server! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

When contributing to this repository, please first discuss the changes you wish to make via issue, email, or any other method with the project maintainers before making significant changes.

### Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up development environment** (see [Development Guide](development.md))
4. **Create a feature branch** from `main`
5. **Make your changes** following our coding standards
6. **Test thoroughly** on testnet
7. **Submit a pull request** with clear description

## 🛠️ Development Setup

See our comprehensive [Development Guide](development.md) for detailed setup instructions, including:

- Prerequisites and installation
- Local development environment setup
- Code formatting and linting
- Testing guidelines
- Adding new tools

## 📋 Pull Request Process

### Before Submitting

- [ ] **Test your changes** thoroughly on Binance testnet
- [ ] **Run the full test suite** and ensure all tests pass
- [ ] **Update documentation** if you've changed APIs or added features
- [ ] **Follow code style guidelines** (Black formatting, type hints)
- [ ] **Add tests** for new functionality
- [ ] **Check that build succeeds** with your changes

### Pull Request Requirements

1. **Clear description** of what the PR does and why
2. **Link to related issues** if applicable
3. **Screenshots** for UI changes (if any)
4. **Testing evidence** that changes work on testnet
5. **Documentation updates** for new features or API changes
6. **Version update** if this is a breaking change

### Review Process

1. **Automated checks** must pass (CI/CD, tests, linting)
2. **Code review** by project maintainers
3. **Security review** for changes affecting API interactions
4. **Documentation review** for completeness
5. **Final approval** and merge

## 🧪 Testing Guidelines

### Testing Requirements

- **Unit tests** for all new functions and methods
- **Integration tests** for tool interactions with Binance API
- **Error handling tests** for various failure scenarios
- **Mock tests** to avoid real API calls during development

### Testing on Testnet

Always test new features on Binance testnet:

```bash
export BINANCE_TESTNET="true"
export BINANCE_API_KEY="your_testnet_key"
export BINANCE_API_SECRET="your_testnet_secret"
```

### Test Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=binance_mcp_server

# Run specific tests
pytest tests/test_tools/test_new_feature.py
```

## 📝 Documentation Guidelines

### Documentation Requirements

- **API documentation** for any new tools
- **Code comments** for complex logic
- **Type hints** for all function parameters and returns
- **Docstrings** following Google style
- **Usage examples** for new features

### Documentation Style

Follow our established patterns:

- Use **clear, concise language**
- Include **practical examples**
- Provide **error handling guidance**
- Add **security considerations** where relevant

## 🎯 Types of Contributions

### 🐛 Bug Reports

When reporting bugs, please include:

- **Environment details** (Python version, OS, package version)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and stack traces
- **Minimal code example** if possible

### ✨ Feature Requests

For new features:

- **Describe the use case** and business value
- **Provide examples** of how it would be used
- **Consider backward compatibility**
- **Check existing issues** to avoid duplicates

### 📚 Documentation Improvements

Documentation contributions are always welcome:

- **Fix typos** and grammatical errors
- **Improve clarity** of existing content
- **Add missing examples**
- **Update outdated information**

### 🔧 Code Contributions

#### New Tools

When adding new Binance API tools:

1. **Create tool module** in `binance_mcp_server/tools/`
2. **Follow existing patterns** for error handling and response format
3. **Add comprehensive tests**
4. **Document the tool** in API reference
5. **Register tool** in main server

#### Bug Fixes

- **Include tests** that reproduce the bug
- **Fix only the specific issue**
- **Maintain backward compatibility**
- **Update documentation** if behavior changes

## 📏 Code Standards

### Python Code Style

- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking
- **pytest** for testing
- **Google-style docstrings**

### Code Quality

- **Type hints** for all function signatures
- **Error handling** for all external API calls
- **Rate limiting** consideration for new API endpoints
- **Logging** for debugging and monitoring
- **Security** best practices for credential handling

### Commit Messages

Use conventional commit format:

```
feat(tools): add get_margin_info tool
fix(config): handle missing environment variables
docs(api): update examples for get_balance
test(orders): add integration tests for create_order
```

## 🚀 Release Process

### Version Management

We follow [Semantic Versioning (SemVer)](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

- [ ] All tests pass on multiple Python versions
- [ ] Documentation is up to date
- [ ] Version number updated in `pyproject.toml`
- [ ] Changelog updated with release notes
- [ ] Security review completed
- [ ] Performance testing on testnet

## 🔒 Security Guidelines

### API Key Security

- **Never commit** API keys or secrets
- **Use environment variables** for all credentials
- **Test with testnet** credentials only
- **Document security requirements** for new features

### Code Security

- **Validate all inputs** from external sources
- **Sanitize user data** before API calls
- **Handle rate limiting** properly
- **Implement proper error handling** without exposing sensitive information

## 📞 Getting Help

### Community Support

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community support
- **Documentation**: Comprehensive guides and API reference

### Maintainer Contact

For security issues or private discussions:
- Email: [dossehdosseh14@gmail.com](mailto:dossehdosseh14@gmail.com)

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of unacceptable behavior may be reported by contacting the project team at [dossehdosseh14@gmail.com](mailto:dossehdosseh14@gmail.com). All complaints will be reviewed and investigated promptly and fairly.

---

Thank you for contributing to the Binance MCP Server! Your efforts help make cryptocurrency trading more accessible through AI agents and the Model Context Protocol.