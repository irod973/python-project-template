# https://docs.docker.com/engine/reference/builder/

FROM ghcr.io/astral-sh/uv:python{{cookiecutter.python_version}}-bookworm
COPY dist/*.whl .
RUN uv pip install --system *.whl
CMD ["{{cookiecutter.repository}}", "--help"]

COPY ./src /app
ENV PYTHONPATH="${PYTHONPATH}:/app"
WORKDIR /app

CMD ["{{cookiecutter.repository}}", "--help"]
# Example command
# CMD ["uvicorn", "example_app.main:app", "--host", "0.0.0.0"]
