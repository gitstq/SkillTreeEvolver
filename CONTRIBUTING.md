# Contributing to SkillTreeEvolver

We welcome contributions! Please follow these guidelines.

## Development Setup

\\\ash
git clone https://github.com/gitstq/SkillTreeEvolver.git
cd SkillTreeEvolver
pip install -e ".[all]"
\\\

## Running Tests

\\\ash
pytest tests/ -v
pytest tests/ -v --cov=core --cov=adapters --cov=cli
\\\

## Code Style

- Follow PEP 8
- Add type hints where possible
- Write docstrings for public functions
- Keep functions small and focused

## Commit Messages

Use Angular Commit Convention:

- eat: New feature
- ix: Bug fix
- docs: Documentation changes
- style: Formatting, no code change
- efactor: Code restructuring
- 	est: Adding/updating tests
- chore: Maintenance tasks

Example: \eat(cli): add token tracking report command\

## Pull Request Process

1. Fork the repository
2. Create a feature branch: \git checkout -b feature/my-feature\
3. Make your changes with tests
4. Ensure all tests pass: \pytest tests/\
5. Commit with clear messages
6. Push and open a PR

## Reporting Issues

Please include:
- Python version
- Operating system
- Minimal reproducible example
- Full error traceback
