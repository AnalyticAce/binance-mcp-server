# Copilot Instructions - Best Development Practices

This guide establishes development standards and best practices for our tech stack: Python, FastAPI, FastMCP. Following these practices ensures maintainable, sustainable, and high-quality systems.
when building the mcp server follow the guidelines available at https://modelcontextprotocol.io/quickstart/server using the #fetch tool

## General Instructions
- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- If possible use available tools to search libary documentation to write and suggestion updated code.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

## Python Development

### Code Style & Structure
- Structure projects using a clear module hierarchy
- Use the typing module for type annotations (e.g., List[str], Dict[str, int]).
- Create meaningful docstrings (Google style recommended)
- Break down complex functions into smaller, more manageable functions.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Place function and class docstrings immediately after the `def` or `class` keyword.
- Use blank lines to separate functions, classes, and code blocks where appropriate.

### Python Best Practices
- Prefer explicit code over implicit
- Use virtual environments `venv`
- Use `uv` as a package manager for Python projects
- Implement comprehensive error handling with specific exception types
- Follow SOLID principles for OOP code
- Leverage dataclasses for data containers
- Use enums for related constants

### Testing and Edge Cases
- Write unit tests with pytest (aim for >80% coverage)
- Implement integration and end-to-end tests
- Use test fixtures for reusable test components
- Mock external dependencies and services
- Practice TDD where applicable
- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.


## Version Control & Commit Practices

### Commit Message Structure
- Use a structured format: `<type>(<scope>): <subject>`
- Keep first line under 72 characters
- Add detailed description after subject when needed
- Reference issue numbers where applicable

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvements
- `test`: Adding or modifying tests
- `chore`: Build process or tooling changes
- `ci`: CI configuration changes
- `revert`: Reverting previous changes

### Scope Guidelines
- Use module/component name when applicable (`auth`, `users`, `ui`, etc.)
- Use `*` for changes spanning multiple modules
- Optional but recommended for clarity

### Commit Message Examples
- `feat(auth): implement OAuth2 login flow`
- `fix(api): correct status code for validation errors`
- `docs(readme): update deployment instructions`
- `refactor(models): simplify user schema`
- `test(endpoints): add tests for profile update`

### Commit Content Best Practices
- Make atomic commits (one logical change per commit)
- Separate refactoring commits from feature commits
- Never commit secrets or sensitive data
- Verify changes before committing (run tests)
- Keep commits small and focused

### Smart Commit Messages
- Include details that reflect code modifications:
  - `feat(database): add migration for user preferences table`
  - `fix(validation): handle null values in email validator`
  - `refactor(services): extract authentication logic to dedicated module`
- Reference performance impacts if applicable:
  - `perf(queries): optimize user search by adding index (50% faster)`

### Code Change Analysis for Commits
- For API changes: `feat(api): add endpoint for user preferences [POST /users/{id}/preferences]`
- For UI changes: `feat(ui): implement responsive navigation menu`
- For dependency updates: `chore(deps): update FastAPI to 0.95.0`
- For schema changes: `feat(models): add email verification fields to User model`
- For bug fixes: `fix(auth): prevent token refresh after password change [CVE-2023-1234]`

### Security
- Store secrets in environment variables or secure vaults
- Implement proper authentication and authorization
- Regularly update dependencies
- Scan for vulnerabilities
- Follow OWASP security guidelines

## Project Management

### Documentation
- Maintain comprehensive README.md files
- Document system architecture and data flows
- Create API documentation (auto-generated + manual)
- Implement change logs
- Use diagrams for complex systems (C4 model recommended)

### Code Review Process
- Establish code review checklist
- Use pull requests for all changes
- Enforce style guidelines through automation
- Focus reviews on logic and architecture
- Provide constructive feedback

### Knowledge Sharing
- Schedule regular knowledge sharing sessions
- Document architectural decisions (ADRs)
- Create onboarding guides for new team members
- Maintain a technical wiki or knowledge base
- Encourage pair programming for complex features

## Conclusion

These practices provide a foundation for building maintainable, sustainable systems using our tech stack. Adapt these guidelines to your specific project needs while maintaining the core principles of clean code, good documentation, and responsible development practices.