# https://docs.docker.com/engine/reference/builder/
# https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers

# Install uv
FROM python:{{cookiecutter.python_version}}-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Default command (overridden by docker-compose)
CMD ["python", "--version"]
