# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory to /app
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the dependency file first (for caching)
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN uv sync --no-install-project

# Copy the rest of the code
COPY . /app

# Tell it how to run the server
ENTRYPOINT ["uv", "run", "main.py"]