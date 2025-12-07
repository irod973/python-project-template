# Irving's Python Project Cookiecutter Template

A python project template to simplify project setup. Adapted from https://github.com/fmind/cookiecutter-mlops-package

The template provides a robust foundation for building, testing, packaging, and deploying Python packages and Docker Images. Adapt it to your project's needs; the source material is MLOps-focused but is suitable for a wide array of Python projects.

**Original resources**:
- **[MLOps Coding Course (Learning)](https://mlops-coding-course.fmind.dev/)**: Learn how to create, develop, and maintain a state-of-the-art MLOps code base.
- **[MLOps Python Package (Example)](https://github.com/fmind/mlops-python-package)**: Kickstart your MLOps initiative with a flexible, robust, and productive Python package.

## Philosophy

This [Cookiecutter](https://cookiecutter.readthedocs.io/) is designed to be a common ground for diverse python environments. Whether you're working with [Kubernetes](https://www.kubeflow.org/), [Vertex AI](https://cloud.google.com/vertex-ai), [Databricks](https://www.databricks.com/), [Azure ML](https://azure.microsoft.com/en-us/products/machine-learning), or [AWS SageMaker](https://aws.amazon.com/sagemaker/), the core principles of using Python packages and Docker images remain consistent.

This template equips you with the essentials for creating, testing, and packaging your code, providing a solid base for integration into your chosen platform.

You have the freedom to structure your `src/` and `tests/` directories according to your preferences. Alternatively, you can draw inspiration from the structure used in the [MLOps Python Package](https://github.com/fmind/mlops-python-package) project for a ready-made implementation.

## Applications

This template includes a few optional application skeletons. See the nested README for details.

## Key Features

This section was copied into the created project's README so tool info is available.

* **Streamlined Project Structure:** A well-defined directory layout for source code, tests, documentation, tasks, and Docker configurations.
Uv Integration: Effortless dependency management and packaging with [uv](https://docs.astral.sh/uv/).
* **Automated Testing and Checks:** Pre-configured workflows using [Pytest](https://docs.pytest.org/), [Ruff](https://docs.astral.sh/ruff/), [Mypy](https://mypy.readthedocs.io/), [Bandit](https://bandit.readthedocs.io/), and [Coverage](https://coverage.readthedocs.io/) to ensure code quality, style, security, and type safety.
* **Pre-commit Hooks:** Automatic code formatting and linting with [Ruff](https://docs.astral.sh/ruff/) and other pre-commit hooks to maintain consistency.
* **Dockerized Deployment:** Dockerfile and docker-compose.yml for building and running the package within a containerized environment ([Docker](https://www.docker.com/)).
* **uv+just Task Automation:** [just](https://github.com/casey/just) commands to simplify development workflows such as cleaning, installing, formatting, checking, building, documenting and running the project.
* **Comprehensive Documentation:** [pdoc](https://pdoc.dev/) generates API documentation, and Markdown files provide clear usage instructions.
* **GitHub Workflow Integration:** Continuous integration and deployment workflows are set up using [GitHub Actions](https://github.com/features/actions), automating testing, checks, and publishing.

## Quick Start

1. **Generate your project:**

```bash
# With uv:
uv tool install cookiecutter
# With pip:
# pip install cookiecutter
cookiecutter gh:irod973/python-project-template
```

You'll be prompted for the following variables.

- `user`: Your GitHub username.
- `name`: The name of your project.
- `repository`: The name of your GitHub repository.
- `package`: The name of your Python package.
- `license`: The license for your project (Note: use "NA" until we define a standard licence or omit entirely)
- `version`: The initial version of your project.
- `description`: A brief description of your project.
- `python_version`: The Python version to use (e.g., 3.12).
- `include_fastapi`: Whether to include a sample FastAPI application.
- `include_metaflow`: Whether to include a sample Metaflow application.
- `include_torchvision`: Whether to include a sample Torchvision application.
- `include_package`: Whether to include a sample application for publishing a Python package.

2. **Initialize a git repository:**

```bash
cd {{ cookiecutter.repository }}
git init
# Should also create remote repo, e.g. via Github web console
# Then make first push e.g.
# git add .
# git commit -m "Initial commit"
# git remote add origin https://github.com/irod973/{{myproject}}.git
# git push -u origin main 
```

3. **Explore the generated project:**

- `src/{{cookiecutter.package}}`: Your Python package source code.
- `tests/`: Unit tests for your package.
- `tasks/`: `just` commands for automation.
- `docker/Dockerfile.python`: Configuration for building your Docker image.
- `docker-compose.yml`: Orchestration file for running your project.

4. **Start developing!**

Use the provided `just` commands to manage your development workflow:

- `uv run just check`: Run code quality, type, security, and test checks.
- `uv run just clean`: Clean up generated files.
- `uv run just commit`: Commit changes to your repository.
- `uv run just doc`: Generate API documentation.
- `uv run just docker`: Build and run your Docker image.
- `uv run just format`: Format your code with Ruff.
- `uv run just install`: Install dependencies, pre-commit hooks, and GitHub rulesets.
- `uv run just package`: Build your Python package.
- `uv run just project`: Run the project in the CLI.

## License

The source material this is adapted from is licensed under the [MIT License](https://opensource.org/license/mit). See the [`LICENSE.txt`](https://github.com/fmind/cookiecutter-mlops-package/blob/main/LICENSE.txt) file for details.
