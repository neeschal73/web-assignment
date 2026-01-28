# Contributing Guide - Online Bookstore

## Welcome Contributors!

Thank you for your interest in contributing to the Online Bookstore project. This guide provides instructions and guidelines for contributing.

## Code of Conduct

Be respectful and professional in all interactions. We maintain a welcoming community for developers of all experience levels.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/yourusername/online-bookstore.git
cd online-bookstore
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

### 3. Create Feature Branch

```bash
# Always create a new branch for your work
git checkout -b feature/your-feature-name

# Branch naming conventions:
# feature/description - for new features
# bugfix/description - for bug fixes
# docs/description - for documentation
# refactor/description - for code refactoring
```

## Making Changes

### Code Style Guidelines

#### Python (PEP 8)

```python
# ✓ Good
def calculate_total_price(items):
    """Calculate total price of items in cart."""
    return sum(item.price * item.quantity for item in items)

# ✗ Bad
def calc_total(i):
    return sum(x.price*x.qty for x in i)
```

#### Naming Conventions

- **Classes**: `PascalCase` → `UserModel`, `BookManager`
- **Functions**: `snake_case` → `get_user_by_id()`, `validate_email()`
- **Constants**: `UPPER_SNAKE_CASE` → `MAX_LOGIN_ATTEMPTS`, `DEFAULT_PAGE_SIZE`
- **Private methods**: `_snake_case` → `_validate_input()`, `_format_date()`

#### Line Length

- Maximum 79 characters for code
- Maximum 72 characters for docstrings
- Maximum 99 characters for comments

#### Imports

```python
# Organize imports by type
# 1. Standard library imports
import os
import sys
from datetime import datetime
from functools import wraps

# 2. Third-party imports
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# 3. Local application imports
from app.models import User, Book
from app.forms import LoginForm
```

#### Comments and Docstrings

```python
# Use docstrings for functions and classes
def register_user(username, email, password):
    """
    Register a new user account.
    
    Args:
        username (str): Unique username (3-50 chars)
        email (str): Valid email address
        password (str): Password (min 6 chars)
    
    Returns:
        User: Created user object
    
    Raises:
        ValueError: If username/email already exists
        ValidationError: If inputs are invalid
    """
    pass

# Use comments for complex logic
# Calculate discount based on order total
if total > 100:
    discount = total * 0.1
```

### HTML/Jinja2 Templates

```html
<!-- ✓ Good: Proper indentation and structure -->
<div class="container">
    <div class="row">
        {% for book in books %}
            <div class="col-md-4">
                <h3>{{ book.title }}</h3>
                <p>{{ book.author }}</p>
            </div>
        {% endfor %}
    </div>
</div>

<!-- ✗ Bad: Poor formatting -->
<div class="container">
<div class="row">
{% for book in books %}
<div class="col-md-4">
<h3>{{ book.title }}</h3>
</div>
{% endfor %}
</div>
</div>
```

### CSS

```css
/* ✓ Good: Organized with comments */
/* Header Styles */
.header {
    background-color: #333;
    padding: 1rem;
}

.header-title {
    font-size: 2rem;
    color: #fff;
}

/* ✗ Bad: No organization */
.header { background-color: #333; padding: 1rem; }
.header-title { font-size: 2rem; color: #fff; }
```

### JavaScript

```javascript
// ✓ Good: Clear variable names and functions
const MAX_LOGIN_ATTEMPTS = 5;

function validateUserEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// ✗ Bad: Unclear names and no comments
const x = 5;
function v(e) { return /.*@.*/.test(e); }
```

## Testing Requirements

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Writing Tests

```python
import unittest
from app import create_app, db
from app.models import User, Book

class UserModelTest(unittest.TestCase):
    """Test cases for User model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_creation(self):
        """Test creating a new user."""
        user = User(
            username='testuser',
            email='test@example.com',
            full_name='Test User'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        self.assertEqual(User.query.count(), 1)
        self.assertTrue(user.check_password('password123'))
    
    def test_duplicate_username(self):
        """Test that duplicate usernames are rejected."""
        user1 = User(username='duplicate', email='first@example.com')
        user2 = User(username='duplicate', email='second@example.com')
        
        db.session.add(user1)
        db.session.commit()
        
        with self.assertRaises(Exception):
            db.session.add(user2)
            db.session.commit()
```

### Test Coverage Targets

- **Minimum**: 80% code coverage
- **Recommended**: 90%+ code coverage
- **Critical paths**: 100% coverage

## Documentation

### Commit Messages

Follow these guidelines for clear commit history:

```bash
# Format: <type>(<scope>): <subject>

# Type: feat, fix, docs, style, refactor, test, chore
# Scope: area of code affected (optional)
# Subject: clear, concise description (imperative mood)

git commit -m "feat(models): add product rating system
- Create Rating model with 1-5 star scale
- Add rating aggregation methods to Product model
- Implement rating validation in forms"

git commit -m "fix(auth): correct password reset email token expiry"

git commit -m "docs(readme): update installation instructions"

git commit -m "refactor(routes): simplify book listing logic"
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests passing
- [ ] No new warnings
```

## Submitting Changes

### Step-by-Step Process

1. **Make Your Changes**
   ```bash
   # Make changes to files
   # Test thoroughly
   pytest --cov=app
   ```

2. **Commit Your Work**
   ```bash
   # Stage changes
   git add .
   
   # Commit with clear message
   git commit -m "feat(books): add advanced search filters"
   ```

3. **Push to Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out PR template
   - Submit for review

5. **Address Feedback**
   ```bash
   # Make requested changes
   git add .
   git commit -m "Address review feedback: improve error handling"
   git push origin feature/your-feature-name
   ```

## Project Structure

When adding new features, follow this structure:

```
app/
├── models.py          # Add new model here
├── forms.py           # Add form validation here
├── routes_main.py     # Add new routes here
├── static/
│   ├── css/          # Add CSS files here
│   └── js/           # Add JavaScript files here
└── templates/        # Add HTML templates here
    └── new_page.html

tests/
└── test_new_feature.py # Add tests here

documentation/
└── FEATURE.md        # Document your feature
```

## Feature Development Checklist

When adding a new feature:

- [ ] Create new branch
- [ ] Implement feature following code standards
- [ ] Write comprehensive tests (80%+ coverage)
- [ ] Update documentation
- [ ] Test in development environment
- [ ] Create pull request with clear description
- [ ] Address review feedback
- [ ] Feature merged and deployed

## Common Contribution Types

### Adding a New Route

1. Add route to appropriate `routes_*.py` file
2. Create corresponding template
3. Add form if needed
4. Write tests for new route
5. Update documentation

### Adding a New Model

1. Create model in `models.py`
2. Add relationships with existing models
3. Create migration (if using Alembic)
4. Write model tests
5. Update database documentation

### Fixing a Bug

1. Create `bugfix/` branch
2. Write failing test demonstrating bug
3. Fix the bug
4. Verify test passes
5. Create pull request with test included

### Adding Tests

1. Follow existing test structure
2. Use descriptive test names
3. Include docstrings
4. Ensure 80%+ coverage
5. Test both success and failure cases

## Review Process

### What Reviewers Look For

- Code follows project standards
- Adequate test coverage
- Clear commit messages
- Documentation updated
- No breaking changes
- Performance implications considered
- Security best practices followed

### How to Request Review

1. Create pull request
2. Assign reviewers
3. Request review from team members
4. Allow 24-48 hours for feedback
5. Address comments promptly

## Reporting Issues

### Bug Report Template

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Bug occurs

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows/Mac/Linux
- Python Version: 3.11
- Browser: Chrome/Firefox

## Additional Context
Any other relevant information
```

### Feature Request Template

```markdown
## Description
Clear description of requested feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches?

## Additional Context
Mockups, examples, etc.
```

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Issues**: Report bugs in Issues tab
- **Documentation**: Check docs/ folder
- **Contact**: Reach out to project maintainers

## Contributors List

Contributors are recognized in [CONTRIBUTORS.md](CONTRIBUTORS.md)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

## Development Workflow Example

```bash
# 1. Create feature branch
git checkout -b feature/add-wishlist

# 2. Make changes
# - Create models/models.py additions
# - Create routes/wishlist.py
# - Add templates/wishlist.html
# - Add tests/test_wishlist.py

# 3. Run tests
pytest --cov=app tests/test_wishlist.py

# 4. Format code
black app/
flake8 app/

# 5. Commit
git add .
git commit -m "feat(wishlist): implement user wishlist functionality
- Add Wishlist and WishlistItem models
- Create wishlist routes for CRUD operations
- Add wishlist UI templates
- Implement wishlist tests with 90% coverage"

# 6. Push
git push origin feature/add-wishlist

# 7. Create PR on GitHub
# 8. Address feedback
# 9. Merge when approved
```

---

Thank you for contributing to make Online Bookstore better!

**Last Updated**: December 2024
**Version**: 1.0
