# Template Sync Tool - Complete Setup

This document describes the complete setup for syncing Python projects with the template.

## 📁 File Structure

```
python-project-template/
├── sync_project_template/          # Core sync engine package
│   ├── __init__.py
│   └── sync.py                      # Main sync logic with loguru
├── sync_analyzer.py                 # Project analysis tool
├── template_sync_cli.py             # CLI wrapper for sync
└── SYNC_TOOL_README.md             # This file

~/.claude/commands/
└── sync-project-template.md         # Claude Code command spec
```

## 🚀 Quick Start

### Using the CLI Directly

```bash
# Analyze a project without syncing
uv run python sync_analyzer.py ~/target-project \
  --template /path/to/template/{{cookiecutter.repository}}

# Sync a project (preview first with --dry-run)
uv run python template_sync_cli.py \
  --source /path/to/template/{{cookiecutter.repository}} \
  --target ~/target-project \
  --dry-run

# Sync for real
uv run python template_sync_cli.py \
  --source /path/to/template/{{cookiecutter.repository}} \
  --target ~/target-project
```

### Using Claude Code Command

A Claude Code command is set up to allow running inside Claude Code sessions. See `.claude/commands/sync-project-template.md` for details.

```bash
/sync-project-template ~/target-project
```

## 🔧 Components

### 1. sync_project_template Package
**Location**: `sync_project_template/sync.py`

Core sync engine with the `TemplateSyncer` class.

**Features**:
- Validates source template and target project
- Syncs files/directories: `tasks/`, `justfile`, `.gitignore`, `.python-version`
- Smart file comparison (skips unchanged files)
- Git integration (auto-staging and committing)
- Dry-run mode for previewing changes
- Loguru logging for clean output

**Usage**:
```python
from sync_project_template.sync import TemplateSyncer

syncer = TemplateSyncer(
    source_path="~/python-project-template/{{cookiecutter.repository}}",
    target_path="~/my-project",
    dry_run=True  # Preview only
)
syncer.run()
```

### 2. sync_analyzer.py
**Location**: `sync_analyzer.py`

Project analysis and reporting tool.

**What it checks**:
- Git repository presence
- pyproject.toml presence
- UV configuration
- Build automation (justfile)
- Task definitions (tasks/)
- Configuration files (.gitignore, .python-version)
- Pre-commit hooks
- GitHub Actions CI/CD
- Docker configuration

**Usage**:
```bash
uv run python sync_analyzer.py ~/target-project
```

**Output**:
- ✓ Checklist of what's present
- ✗ Checklist of what's missing
- Numbered recommendations for migration

### 3. template_sync_cli.py
**Location**: `template_sync_cli.py`

Standalone CLI wrapper for the sync engine.

**Usage**:
```bash
uv run python template_sync_cli.py --source SOURCE --target TARGET [--dry-run]
```

**Arguments**:
- `--source` (required): Path to template directory
- `--target` (required): Path to target project
- `--dry-run` (optional): Preview changes without committing

### 4. Claude Code Command
**Location**: `~/.claude/commands/sync-project-template.md`

Integration with Claude Code for guided sync workflow.

**Invocation**:
```bash
/sync-project-template ~/target-project
```

**Workflow**:
1. Analyzes target project
2. Shows infrastructure report
3. Lists migration recommendations
4. Asks for confirmation
5. Syncs files if approved
6. Creates descriptive git commit

## 📊 Files Synced

When you run the sync tool, these files are synced:

| File/Directory | Purpose |
|---|---|
| `tasks/` | Just command definitions (all task files) |
| `justfile` | Task runner configuration |
| `.gitignore` | Git ignore patterns |
| `.python-version` | Python version specification |

## 🔄 Workflow Example

### Scenario: Sync nba-persistence project

1. **Analyze first**:
   ```bash
   uv run python sync_analyzer.py ~/nba-persistence \
     --template ~/python-project-template/{{cookiecutter.repository}}
   ```

   Output:
   ```
   ✓ 7 items present and in sync
   ✗ 4 items missing:
     - .pre-commit-config.yaml
     - .github/workflows/
     - Dockerfile
     - docker-compose.yml

   RECOMMENDATIONS:
   1. Add .pre-commit-config.yaml for code quality
   2. Add GitHub Actions workflows for CI/CD
   3. Add Dockerfile for containerization

   FILES READY TO SYNC:
   • tasks/ (directory, 9 items)
   • justfile
   • .gitignore
   • .python-version
   ```

2. **Preview the sync**:
   ```bash
   uv run python template_sync_cli.py \
     --source ~/python-project-template/{{cookiecutter.repository}} \
     --target ~/nba-persistence \
     --dry-run
   ```

3. **Run the actual sync**:
   ```bash
   uv run python template_sync_cli.py \
     --source ~/python-project-template/{{cookiecutter.repository}} \
     --target ~/nba-persistence
   ```

4. **Verify**:
   ```bash
   cd ~/nba-persistence
   git log --oneline -1  # See the sync commit
   ```

## 📝 Testing

All components are tested:

```bash
# Run the full test suite
uv run pytest tests/test_sync.py -v

# Run specific test class
uv run pytest tests/test_sync.py::TestTemplateSyncerOperations -v
```

## 🛠️ Dependencies

All tools use:
- **loguru**: Structured logging (already in template dependencies)
- **pathlib**: File operations
- **subprocess**: Git operations
- **argparse**: CLI argument parsing

No additional dependencies are needed.

## 🔐 Safety Features

- ✓ Validates source and target paths before syncing
- ✓ Checks if target is a git repository
- ✓ Warns if git working directory is dirty
- ✓ Skips files that haven't changed
- ✓ Provides dry-run mode to preview changes
- ✓ Creates descriptive git commits with all changes
- ✓ All operations are reversible (git history)

## 🚧 Future Enhancements

Planned improvements:

- [ ] Smart merge for `pyproject.toml` (preserve custom deps, update tools)
- [ ] Smart merge for `.pre-commit-config.yaml`
- [ ] Sync GitHub Actions workflows
- [ ] Configuration file for custom sync targets
- [ ] Rollback capability (git revert)
- [ ] Support for syncing newer/older versions of template

## 📞 Troubleshooting

### "Template path does not exist"
- Verify the template directory path is correct
- Use the full path or ensure the `~` expands correctly

### "Target is not a git repository"
- Initialize git in the target project: `git init`
- Create an initial commit: `git add . && git commit -m "Initial commit"`

### "No changes to sync"
- Run `sync_analyzer.py` to see what's missing
- The tool skips files that are already in sync
- Use `--dry-run` to preview what would be synced

### Git commit failed
- Check that `git config user.name` and `user.email` are set
- Ensure you have write permissions to the repository
- Check if the working directory has uncommitted changes

## 📚 Additional Resources

- [Template Documentation](README.md)
- [Sync Tool Tests](tests/test_sync.py)
- [Just Task Definitions]({{cookiecutter.repository}}/tasks/)
