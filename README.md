# Python Web Service Template

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/github/actions/workflow/status/SchwartzKamel/helloworld_python/ci.yml)

A production-ready Python web service template with built-in security and DevOps best practices.

## 🚀 Features

- **Secure Flask API** with CSP headers & rate limiting
- **Dockerized** deployment (multi-stage builds)
- CI/CD pipeline with **vulnerability scanning**
- Automated testing (**pytest** + coverage)
- **Sphinx documentation** generation
- Health check endpoints & monitoring
- Environment variable validation
- **Poetry** dependency management

## 📦 Quick Start

```bash
# Clone & enter project
git clone https://github.com/SchwartzKamel/helloworld_python.git
cd helloworld_python

# Install dependencies
poetry install

# Configure environment
cp .env.example .env
nano .env  # Add your API_KEY

# Start development server
poetry run make docker-up
```

Access endpoints:
- `http://localhost:8000` - Hello World
- `http://localhost:8000/health` - Health check
- `http://localhost:8000/random-name` - Example API call

## 🛠️ Project Structure

```
helloworld_python/
├── app/                   # Application code
│   ├── modules/          # Business logic components
│   └── main.py           # Entry point
├── tests/                # Pytest test suite
├── docs/                 # Sphinx documentation
├── Dockerfile            # Production container
├── docker-compose.yml    # Local development
├── Makefile              # Development tasks
└── pyproject.toml        # Poetry dependencies
```

## 🔒 Security Features

- Non-root Docker containers
- Automatic Trivy vulnerability scans
- 5 reqs/minute rate limiting
- Input sanitization & validation
- Environment secret validation
- Security headers (CSP, HSTS)
- [Security Policy](SECURITY.md)

## 📚 Documentation

Generate and view documentation:

1. **Build HTML docs**:
```bash
cd helloworld_python
make -C docs html
```

2. **Open in browser**:
```bash
open docs/_build/html/index.html  # macOS
# Or:
xdg-open docs/_build/html/index.html  # Linux
```

3. **Live development** (auto-rebuild):
```bash
sphinx-autobuild docs docs/_build/html
```

## 🤖 CI/CD Pipeline

Includes:
- Automated testing
- Docker image builds
- Vulnerability scanning (Trivy)
- Dependency auditing (pip-audit)
- Documentation deployment

## 📜 License
MIT - See [LICENSE](LICENSE) for details