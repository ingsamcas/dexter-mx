FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY interactive_compare_fixed.py ./
COPY interactive_compare_with_memory.py ./

RUN uv sync --frozen && uv add python-dotenv

# Por defecto: versión con memoria
CMD ["uv", "run", "python", "interactive_compare_with_memory.py"]
