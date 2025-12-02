# Contributing to Tiny Injection

Thank you for considering contributing to Tiny Injection! Here are some guidelines to help you get started.

## Code of Conduct
Be respectful and inclusive. We welcome contributors from all backgrounds.

## How to Contribute

### 1. Report Bugs
- Use the GitHub issue tracker
- Include: description, steps to reproduce, expected vs actual behavior
- Add labels if possible (bug, enhancement, etc.)

### 2. Suggest Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Include use cases if possible

### 3. Submit Code Changes
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### 4. Add New Attack Payloads
Add new payloads to `data/payloads/` directory:
- `basic.txt`: Simple, direct injections
- `advanced.txt`: Sophisticated techniques
- `obfuscated.txt`: Encoded/hidden attacks

### 5. Improve Documentation
- Fix typos or clarify explanations
- Add examples or tutorials
- Translate to other languages

## Development Setup

1. Clone the repo
2. Run `./install.sh`
3. Activate virtual environment: `source venv/bin/activate`
4. Make changes
5. Test: `pytest tests/`
6. Format: `black .`
7. Lint: `flake8`

## Code Style
- Follow PEP 8
- Use type hints
- Add docstrings for functions
- Keep functions focused and small
- Write tests for new features

## Pull Request Process
1. Update README.md if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. PR will be reviewed within 48 hours

## Questions?
Open an issue or reach out to the maintainers.

Happy hacking! 🚀
