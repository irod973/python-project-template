# Sync Project Template

## Description
Analyze a target project against the Python project template, identify what's missing or out of sync, and guide the user through syncing with the latest template.

## Usage

```bash
/sync-project-template /path/to/target-project
```

### Example

```bash
/sync-project-template ~/Documents/workspace/nba-persistence
```

## What It Does

This command performs these steps:

1. **Analyzes** the target project structure
2. **Compares** against the template at `~/Documents/workspace/python-project-template/{{cookiecutter.repository}}/`
3. **Reports** what's present, missing, or out of sync
4. **Recommends** migration steps needed
5. **Confirms** with user before syncing
6. **Syncs** files if approved, creating a git commit

## Infrastructure Checklist

### Core Components (Usually Present)
- ✓ Git repository (.git)
- ✓ Project metadata (pyproject.toml)
- ✓ UV configuration ([tool.uv] in pyproject.toml)
- ✓ Task automation (justfile)
- ✓ Task definitions (tasks/ directory)
- ✓ Build configuration (.gitignore, .python-version)

### Advanced Components (Optional)
- ? Pre-commit hooks (.pre-commit-config.yaml)
- ? CI/CD (.github/workflows/)
- ? Containerization (Dockerfile, docker-compose.yml)

## Sample Analysis Report

```
PROJECT SYNC ANALYSIS
======================================================================
Target:   /Users/you/nba-persistence
Template: ~/Documents/workspace/python-project-template/{{cookiecutter.repository}}/

INFRASTRUCTURE STATUS
----------------------------------------------------------------------
  ✓ Git repository
  ✓ pyproject.toml
  ✓ UV configuration (in pyproject.toml)
  ✓ justfile
  ✓ tasks/ directory
  ✓ .gitignore
  ✓ .python-version
  ✗ .pre-commit-config.yaml
  ✗ .github/workflows/
  ✗ Dockerfile
  ✗ docker-compose.yml

MIGRATION RECOMMENDATIONS
----------------------------------------------------------------------
  1. Add .pre-commit-config.yaml for automated code quality checks
  2. Add GitHub Actions workflows (.github/workflows/) for CI/CD
  3. Add Dockerfile for containerization

FILES READY TO SYNC
----------------------------------------------------------------------
  • tasks/               Task definitions and automation
  • justfile             Just task runner configuration
  • .gitignore           Git ignore patterns
  • .python-version      Python version specification
```

## Sync Confirmation

After analysis, you'll be asked to confirm:

```
Ready to sync? This will:
- Sync tasks/ directory (all task definitions)
- Update justfile, .gitignore, .python-version
- Create a git commit with all changes

Would you like to proceed? (yes/no)
```

Answering "yes" will:
- Run the sync tool on your project
- Stage and commit all changes to git
- Show summary of what was synced

Answering "no" will:
- Show what would have been synced
- Exit without making changes

## Behind the Scenes

This command uses two tools:
- **~/Documents/workspace/python-project-template/sync_analyzer.py** - Analyzes project structure and generates report
- **~/Documents/workspace/python-project-template/template_sync_cli.py** - Performs the actual file sync

Both tools use loguru for clean, structured logging.

## Requirements

- Target project must be a git repository
- Template must exist at `~/Documents/workspace/python-project-template/`

## Notes

- Changes are always previewed before syncing
- All synced changes go into a single commit
- Files that haven't changed are automatically skipped