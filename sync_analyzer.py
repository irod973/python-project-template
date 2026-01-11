"""
Analyze a project and compare it with the template.

This script generates a detailed report of what's missing or out of sync
before running the sync tool.

Usage:
    uv run python sync_analyzer.py ~/path/to/project
"""

import sys
from pathlib import Path
from typing import Dict, Tuple

from loguru import logger


class ProjectAnalyzer:
    """Analyzes a project against the template structure."""

    # Items to check in the project
    CHECKS = {
        'git_repo': {
            'description': 'Git repository',
            'check': lambda p: (p / '.git').exists(),
        },
        'pyproject': {
            'description': 'pyproject.toml',
            'check': lambda p: (p / 'pyproject.toml').exists(),
        },
        'uv_config': {
            'description': 'UV configuration (in pyproject.toml)',
            'check': lambda p: 'tool.uv' in (p / 'pyproject.toml').read_text()
            if (p / 'pyproject.toml').exists()
            else False,
        },
        'justfile': {
            'description': 'justfile',
            'check': lambda p: (p / 'justfile').exists(),
        },
        'tasks': {
            'description': 'tasks/ directory',
            'check': lambda p: (p / 'tasks').is_dir(),
        },
        'gitignore': {
            'description': '.gitignore',
            'check': lambda p: (p / '.gitignore').exists(),
        },
        'python_version': {
            'description': '.python-version',
            'check': lambda p: (p / '.python-version').exists(),
        },
        'precommit': {
            'description': '.pre-commit-config.yaml',
            'check': lambda p: (p / '.pre-commit-config.yaml').exists(),
        },
        'github_workflows': {
            'description': '.github/workflows/',
            'check': lambda p: (p / '.github' / 'workflows').is_dir(),
        },
        'dockerfile': {
            'description': 'Dockerfile',
            'check': lambda p: (p / 'docker' / 'Dockerfile.python').exists()
            or (p / 'Dockerfile').exists(),
        },
        'docker_compose': {
            'description': 'docker-compose.yml',
            'check': lambda p: (p / 'docker-compose.yml').exists(),
        },
    }

    def __init__(self, target_path: Path, template_path: Path):
        """Initialize the analyzer.

        Args:
            target_path: Path to the target project
            template_path: Path to the template source
        """
        self.target = Path(target_path).resolve()
        self.template = Path(template_path).resolve()
        self.results: Dict[str, bool] = {}

    def analyze(self) -> Tuple[Dict[str, bool], list]:
        """Analyze the target project against the template.

        Returns:
            Tuple of (results dict, recommendations list)
        """
        logger.info(f"Analyzing project: {self.target}")
        logger.debug(f"Template: {self.template}")

        # Run all checks
        for check_key, check_info in self.CHECKS.items():
            try:
                result = check_info['check'](self.target)
                self.results[check_key] = result
                status = "✓" if result else "✗"
                logger.debug(f"{status} {check_info['description']}")
            except Exception as e:
                self.results[check_key] = False
                logger.warning(f"Check '{check_key}' failed: {e}")

        # Generate recommendations
        recommendations = self._generate_recommendations()
        return self.results, recommendations

    def _generate_recommendations(self) -> list:
        """Generate migration recommendations based on analysis."""
        recs = []

        # Check for critical items
        if not self.results.get('git_repo'):
            recs.append("Initialize git repository: `git init` and `git add . && git commit`")

        if not self.results.get('uv_config'):
            recs.append(
                "Add UV configuration to pyproject.toml: `[tool.uv]` section with dependency groups"
            )

        if not self.results.get('justfile'):
            recs.append("Copy justfile from template for task automation")

        if not self.results.get('tasks'):
            recs.append("Add tasks/ directory with just command definitions")

        if not self.results.get('precommit'):
            recs.append("Add .pre-commit-config.yaml for automated code quality checks")

        if not self.results.get('github_workflows'):
            recs.append("Add GitHub Actions workflows (.github/workflows/) for CI/CD")

        if not self.results.get('dockerfile'):
            recs.append("Add Dockerfile for containerization")

        return recs

    def print_report(self) -> None:
        """Print a formatted analysis report."""
        logger.info("=" * 70)
        logger.info("PROJECT SYNC ANALYSIS")
        logger.info("=" * 70)
        logger.info(f"Target:   {self.target}")
        logger.info(f"Template: {self.template}")
        logger.info("")

        logger.info("INFRASTRUCTURE STATUS")
        logger.info("-" * 70)
        for check_key, check_info in self.CHECKS.items():
            status = "✓" if self.results.get(check_key) else "✗"
            logger.info(f"  {status} {check_info['description']}")

        logger.info("")
        logger.info("MIGRATION RECOMMENDATIONS")
        logger.info("-" * 70)
        recommendations = self._generate_recommendations()
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                logger.info(f"  {i}. {rec}")
        else:
            logger.success("  Project appears to be in sync with template!")

        logger.info("")
        logger.info("FILES READY TO SYNC")
        logger.info("-" * 70)
        files_to_sync = [
            ("tasks/", "Task definitions and automation"),
            ("justfile", "Just task runner configuration"),
            (".gitignore", "Git ignore patterns"),
            (".python-version", "Python version specification"),
        ]
        for filename, description in files_to_sync:
            logger.info(f"  • {filename:<20} {description}")

        logger.info("")
        logger.info("=" * 70)

    def get_summary(self) -> str:
        """Get a brief summary of the analysis."""
        missing = sum(1 for v in self.results.values() if not v)
        total = len(self.results)
        return f"{total - missing}/{total} infrastructure components present"


def main(argv=None):
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze a project against the template"
    )
    parser.add_argument("target", help="Path to the target project")
    # Get the template path from environment or use default
    default_template = str(Path.home() / "Documents" / "workspace" / "python-project-template" / "{{cookiecutter.repository}}")

    parser.add_argument(
        "--template",
        default=default_template,
        help="Path to the template directory (default: ~/Documents/workspace/python-project-template/{{cookiecutter.repository}})",
    )

    args = parser.parse_args(argv)

    target_path = Path(args.target).resolve()
    template_path = Path(args.template).resolve()

    if not target_path.exists():
        logger.error(f"Target path does not exist: {target_path}")
        return 1

    if not template_path.exists():
        logger.error(f"Template path does not exist: {template_path}")
        return 1

    analyzer = ProjectAnalyzer(target_path, template_path)
    results, recommendations = analyzer.analyze()
    analyzer.print_report()

    return 0


if __name__ == "__main__":
    sys.exit(main())