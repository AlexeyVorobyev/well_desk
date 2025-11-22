# Well Desk Backend

A lightweight FastAPI backend structured with routers, services, repositories, models, DTOs, and shared components. Configuration is powered by Pydantic Settings and dependencies are managed with `uv` via `pyproject.toml`.

## Running locally

1. Create a virtual environment and install dependencies using `uv` (or `pip`):
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```
2. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

Add routers, models, and business logic within the corresponding directories to build out your API.
