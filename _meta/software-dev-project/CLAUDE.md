# Claude Code Instructions - Software Development Project

## Project Overview
This is a software development project. Focus on code quality, maintainability, and best practices.

## Development Standards

### Code Quality
- Write clean, readable code with meaningful variable names
- Follow DRY (Don't Repeat Yourself) principle
- Keep functions small and focused on single responsibility
- Add comments only when necessary to explain "why", not "what"

### Project Structure
- Source code goes in `/src`
- Tests go in `/tests` (mirror the src structure)
- Configuration files in `/config`
- Utility scripts in `/scripts`
- Documentation in `/docs`

### Testing
- Write tests for new features and bug fixes
- Maintain test coverage above 80%
- Run tests before committing
- Include both unit and integration tests

### Version Control
- Write clear, descriptive commit messages
- Keep commits atomic and focused
- Branch for new features: `feature/feature-name`
- Branch for bug fixes: `fix/issue-description`

## Tasks Guidelines

### When Adding New Features
- Create tests first (TDD approach when appropriate)
- Update relevant documentation
- Follow existing code patterns and conventions
- Consider backwards compatibility

### When Fixing Bugs
- Reproduce the issue first
- Write a test that fails
- Fix the bug
- Verify the test passes
- Check for similar issues elsewhere

### When Refactoring
- Ensure tests pass before and after
- Refactor in small, incremental steps
- Don't change behavior, only structure
- Update documentation if needed

### Before Committing
- Run linter and fix issues
- Run full test suite
- Update CHANGELOG if applicable
- Review your own changes

## Environment Setup
- Copy `.env.example` to `.env` and configure
- Never commit `.env` or secrets
- Document all required environment variables
- Use development values in `.env.example`

## Important Reminders
- NEVER create files unless explicitly requested
- ALWAYS prefer editing existing files
- Run tests after making changes
- Keep dependencies up to date
- Follow the principle of least surprise
