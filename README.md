# Pneuma OpenWebUI Integration

A conversational data discovery interface combining Pneuma's LLM-powered table search with OpenWebUI's chat interface.

## Quick Start

1. **Setup Environment**

    ```bash copy
    cp .env.example .env
    # Edit .env with your configuration
    ```

2. **Install Dependencies**

    ```bash copy
    pip install -r requirements.txt
    ```

3. **Setup Ollama & OpenWebUI**

    ```bash copy
    # Install Ollama
    curl -fsSL https://ollama.com/install.sh | sh

    # Pull a model
    ollama pull llama3.1:8b

    # Install OpenWebUI
    pip install open-webui
    ```

4. **Start Services**

    ```bash copy
    # Start all services
    ./scripts/start_services.sh

    # Or manually:
    # Terminal 1: ollama serve
    # Terminal 2: uvicorn api.main:app --reload
    # Terminal 3: open-webui serve --backend ollama
    ```

5. **Access Interface**
    - OpenWebUI: http://localhost:8080
    - API Docs: http://localhost:8000/docs

## Architecture

```
User Query → OpenWebUI → Ollama (LLM) → Python Tools → FastAPI → Pneuma Core
```

## Development

-   **API Development**: See `docs/api_reference.md`
-   **Tool Development**: See `docs/tool_development.md`
-   **Testing**: `pytest tests/`
-   **Format Code**: `black . && isort .`

## Deployment

See `docs/deployment.md` for production deployment instructions.

# ===================================

# setup.py

```python copy
from setuptools import setup, find_packages

setup(
    name="pneuma-openwebui",
    version="0.1.0",
    description="OpenWebUI integration for Pneuma data discovery",
    author="Archit Rathod",
    author_email="arath21@uic.edu",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "requests>=2.31.0",
        "redis>=5.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.12.0",
            "isort>=5.13.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "pneuma-api=api.main:main",
        ],
    },
)
```
