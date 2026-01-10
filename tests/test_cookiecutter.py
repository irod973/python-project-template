"""Test the project generation."""

# %% IMPORTS

from pytest_cookies.plugin import Cookies
from pytestshellutils.shell import Subprocess

# %% COMMANDS

COMMANDS = [
    "git init",
    "uv run just clean",
    "uv run just install",
    "uv run just format",
    "uv run just check",
    "uv run just doc",
    "uv run just project",
    "uv run just package",
    "uv run just docker",
]

# %% TESTS


def test_project_generation(cookies: Cookies) -> None:
    """Test the generation of the project."""
    # given
    context = {
        "user": "tester",
        "name": "MLOps 123",
        "license": "Apache-2.0",  # Note: needs to be a "valid SPDX identifier"
        "version": "1.0.0",
        "description": "A test project.",
        "python_version": "3.12",
        "include_fastapi": "y",
        "include_metaflow": "y",
        "include_package": "y",
        "include_torchvision": "y",
        "coverage_threshold": "1",
    }
    repository = context['name'].lower().replace(' ', '-')
    package = repository.replace('-', '_')
    # when
    result = cookies.bake(extra_context=context)
    # then
    # - cookies
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert result.project_path.name == repository
    assert result.context == {
        "user": context["user"],
        "name": context["name"],
        "package": package,
        "repository": repository,
        "license": context["license"],
        "version": context["version"],
        "description": context["description"],
        "python_version": context["python_version"],
        "include_fastapi": context["include_fastapi"],
        "include_metaflow": context["include_metaflow"],
        "include_torchvision": context["include_torchvision"],
        "include_package": context["include_package"],
        "coverage_threshold": context["coverage_threshold"],
    }
    # - commands
    shell = Subprocess(cwd=result.project_path)
    for command in COMMANDS:
        result = shell.run(*command.split())
        assert result.returncode == 0, f"Command failed: {command}"
