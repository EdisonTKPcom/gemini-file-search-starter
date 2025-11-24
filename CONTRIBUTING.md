# Contributing to Gemini File Search Starter

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🎯 Ways to Contribute

- **Bug Reports**: Found a bug? Open an issue with detailed steps to reproduce
- **Feature Requests**: Have an idea? Open an issue describing the feature
- **Code Contributions**: Submit pull requests with improvements or fixes
- **Documentation**: Help improve or translate documentation
- **Testing**: Write tests or test the application and report findings

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Git
- Google AI API Key

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/gemini-file-search-starter.git
cd gemini-file-search-starter
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/EdisonTKPcom/gemini-file-search-starter.git
```

### Set Up Development Environment

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

#### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local if needed
```

## 🔨 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

**Code Style:**
- Python: Follow PEP 8
- TypeScript/JavaScript: Use ESLint rules
- Add comments for complex logic
- Keep functions small and focused

**Commit Messages:**
Use conventional commit format:
```
feat: add new feature
fix: resolve bug
docs: update documentation
test: add tests
refactor: refactor code
style: format code
chore: update dependencies
```

### 3. Test Your Changes

#### Backend Tests
```bash
cd backend
pytest -v
pytest --cov=. --cov-report=html  # With coverage
```

#### Frontend Build
```bash
cd frontend
npm run build
npm run lint
```

#### Manual Testing
1. Start backend: `cd backend && python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Test all affected functionality
4. Check browser console for errors

### 4. Update Documentation

If you changed:
- **API endpoints**: Update README.md and ARCHITECTURE.md
- **Configuration**: Update .env.example and README.md
- **Dependencies**: Update requirements.txt or package.json
- **Features**: Update README.md with usage examples

### 5. Commit and Push
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

1. Go to GitHub and create a pull request
2. Fill in the PR template:
   - Describe changes
   - Link related issues
   - Add screenshots if UI changes
   - List testing done
3. Wait for review

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Tests pass (`pytest` for backend)
- [ ] Code builds (`npm run build` for frontend)
- [ ] Code follows style guidelines
- [ ] Documentation updated if needed
- [ ] Commit messages follow convention
- [ ] No unnecessary files committed (.env, node_modules, etc.)

### PR Description Should Include
- What: What changes were made
- Why: Why the changes were necessary
- How: How you implemented the changes
- Testing: How you tested the changes
- Screenshots: If UI changes

## 🐛 Bug Reports

### Good Bug Report Includes
1. **Clear title**: Describe the issue briefly
2. **Environment**: OS, Python/Node version, browser
3. **Steps to reproduce**: Detailed steps
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Screenshots**: If applicable
7. **Logs**: Relevant error messages

### Example
```markdown
**Title**: File upload fails for PDF files larger than 10MB

**Environment**:
- OS: macOS 13.0
- Python: 3.11
- Node: 18.17.0
- Browser: Chrome 120

**Steps to Reproduce**:
1. Start backend and frontend
2. Click "Upload File"
3. Select a PDF file > 10MB
4. Click upload

**Expected**: File uploads successfully
**Actual**: Error "Request entity too large"

**Error Log**:
```
413 Request Entity Too Large
```
```

## 💡 Feature Requests

### Good Feature Request Includes
1. **Clear description**: What feature you want
2. **Use case**: Why this feature is needed
3. **Proposed solution**: How it might work
4. **Alternatives**: Other ways to solve the problem
5. **Additional context**: Screenshots, mockups, etc.

## 🧪 Testing Guidelines

### Writing Tests

**Backend (pytest):**
```python
def test_feature_name():
    """Test description"""
    # Arrange
    input_data = {...}
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_output
```

**Test Coverage:**
- Unit tests for new functions
- Integration tests for API endpoints
- Edge cases and error handling
- Mock external API calls

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Max line length: 100
- Docstrings for all public functions
```python
def function_name(param: str) -> Dict[str, Any]:
    """
    Brief description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass
```

### TypeScript/JavaScript
- Use TypeScript for type safety
- Follow ESLint rules
- Functional components for React
- Use hooks for state management
```typescript
interface Props {
  name: string;
}

export function Component({ name }: Props) {
  // Component code
}
```

## 🔒 Security

### Reporting Security Issues
**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email: [your-email@example.com] (Update this)
2. Include detailed description
3. Include steps to reproduce
4. We'll respond within 48 hours

### Security Best Practices
- Never commit API keys or secrets
- Use environment variables
- Validate all inputs
- Sanitize user data
- Keep dependencies updated

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discriminatory language
- Personal attacks
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## 🎓 Resources

### Learning
- [Python Best Practices](https://docs.python-guide.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React Documentation](https://react.dev/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Tools
- [VS Code](https://code.visualstudio.com/) - Recommended editor
- [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [ESLint Extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)

## ❓ Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Security issues**: Email privately
- **Chat**: Join our community (if applicable)

## 🙏 Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
