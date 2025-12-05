# {{cookiecutter.name}}

[![check.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/check.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/check.yml)
[![publish.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/publish.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/publish.yml)
[![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://{{cookiecutter.user}}.github.io/{{cookiecutter.repository}}/)
[![License](https://img.shields.io/github/license/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/blob/main/LICENCE.txt)
[![Release](https://img.shields.io/github/v/release/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/releases)

# Description	

{{cookiecutter.description}}.

(This README is generated from a cookiecutter template. Delete this comment and modify your README!)

# Installation

Initialize your project with the provided `just` command.
```bash	
# Install dependencies and pre-commit hooks	
uv run just install	
```
# Usage

(The source comes with an example python package and an example FastAPI app. Delete this comment and add details for your application.)

Test the example package
```bash
uv run {{cookiecutter.repository}}
```

Test the example API with Docker:
```bash	
uv add fastapi uvicorn	
uv run just package	

# Invoke docker compose	
uv run just docker-compose

# Or run with docker compose	
docker compose up --build	

# Or run with docker	
# Note: specify platform if running on Apple M chip 	
docker build --platform linux/amd64 -t {{cookiecutter.repository}}-image -f Dockerfile .	
docker run -it --platform linux/amd64 --name {{cookiecutter.repository}}-ctr -p 8000:8000 {{cookiecutter.repository}}-image	
```

Test the API using the local environment:
```bash
cd src	
uv run uvicorn example_app.main:app --reload
```

## Development Features

(This section was copied into the created project's README so tool info is available to users.)

* **Streamlined Project Structure:** A well-defined directory layout for source code, tests, documentation, tasks, and Docker configurations.
Uv Integration: Effortless dependency management and packaging with [uv](https://docs.astral.sh/uv/).
* **Automated Testing and Checks:** Pre-configured workflows using [Pytest](https://docs.pytest.org/), [Ruff](https://docs.astral.sh/ruff/), [Mypy](https://mypy.readthedocs.io/), [Bandit](https://bandit.readthedocs.io/), and [Coverage](https://coverage.readthedocs.io/) to ensure code quality, style, security, and type safety.
* **Pre-commit Hooks:** Automatic code formatting and linting with [Ruff](https://docs.astral.sh/ruff/) and other pre-commit hooks to maintain consistency.
* **Dockerized Deployment:** Dockerfile and docker-compose.yml for building and running the package within a containerized environment ([Docker](https://www.docker.com/)).
* **uv+just Task Automation:** [just](https://github.com/casey/just) commands to simplify development workflows such as cleaning, installing, formatting, checking, building, documenting and running the project.
* **Comprehensive Documentation:** [pdoc](https://pdoc.dev/) generates API documentation, and Markdown files provide clear usage instructions.
* **GitHub Workflow Integration:** Continuous integration and deployment workflows are set up using [GitHub Actions](https://github.com/features/actions), automating testing, checks, and publishing.

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

# Template Update Management

This project template recommends using [Cruft](https://cruft.github.io/cruft/) to keep downstream projects up to date with template changes. Cruft tracks the template source and allows you to apply updates to your project, with the option to review and approve changes (e.g., via Pull Requests).

## Keeping Your Project Up to Date

1. **Initialize with Cruft**
   - When creating a new project, use:
     ```bash
     cruft create https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}.git
     ```
   - This will create your project and add a `.cruft.json` file to track the template source.

2. **Update Your Project**
   - When the template is updated, run:
     ```bash
     cruft update
     ```
   - Review the changes and resolve any conflicts. Commit the changes to your repository.

3. **Automate Updates with Pull Requests**
   - You can automate the update process and open a Pull Request for review using GitHub Actions. Add a workflow like the following to your downstream project:
     ```yaml
     # .github/workflows/template-update.yml
     name: Update from Template
     on:
       schedule:
         - cron: '0 0 * * 0'  # Weekly
       workflow_dispatch:
     jobs:
       update-template:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           - name: Set up Python
             uses: actions/setup-python@v5
             with:
               python-version: '3.11'
           - name: Install Cruft
             run: pip install cruft
           - name: Update from template
             run: |
               cruft update --skip-apply || true
               git config user.name github-actions
               git config user.email github-actions@github.com
               git add .
               git commit -m "Update from template" || echo "No changes to commit"
               git push origin HEAD:template-update || true
           - name: Create Pull Request
             uses: peter-evans/create-pull-request@v6
             with:
               branch: template-update
               title: "Update from template"
               body: "Automated update from the project template. Please review and merge."
     ```
   - This workflow will check for template updates weekly and open a PR for review.

