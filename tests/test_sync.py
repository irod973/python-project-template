"""Tests for the sync module."""

import subprocess
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Import the sync module from the project root
from sync_project_template.sync import SyncError, TemplateSyncer, main


@pytest.fixture
def temp_dirs() -> Generator[tuple[Path, Path], None, None]:
    """Create temporary directories for source and target."""
    with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
        source = Path(source_dir)
        target = Path(target_dir)
        yield source, target


@pytest.fixture
def source_template(temp_dirs: tuple[Path, Path]) -> Path:
    """Create a minimal valid template source."""
    source, _ = temp_dirs
    # Create required template files
    (source / "justfile").write_text("# justfile")
    (source / "tasks").mkdir()
    (source / "tasks" / "test.just").write_text('test: echo "test"')
    (source / ".gitignore").write_text("*.pyc\n__pycache__/\n")
    (source / ".python-version").write_text("3.12\n")
    return source


@pytest.fixture
def target_project(temp_dirs: tuple[Path, Path]) -> Path:
    """Create a minimal valid target project with git."""
    _, target = temp_dirs
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=target, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=target,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"], cwd=target, capture_output=True, check=True
    )
    # Create initial commit
    (target / "README.md").write_text("# Project")
    subprocess.run(["git", "add", "README.md"], cwd=target, capture_output=True, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"], cwd=target, capture_output=True, check=True
    )
    return target


class TestTemplateSyncerValidation:
    """Test path validation logic."""

    def test_validate_source_path_not_exists(self, temp_dirs: tuple[Path, Path]) -> None:
        """Test validation fails when source doesn't exist."""
        _, target = temp_dirs
        nonexistent = Path("/nonexistent/path")
        syncer = TemplateSyncer(nonexistent, target)
        with pytest.raises(SyncError, match="Source path does not exist"):
            syncer.validate_paths()

    def test_validate_source_not_directory(self, temp_dirs: tuple[Path, Path]) -> None:
        """Test validation fails when source is not a directory."""
        source, target = temp_dirs
        file_path = source / "file.txt"
        file_path.write_text("test")
        syncer = TemplateSyncer(file_path, target)
        with pytest.raises(SyncError, match="Source path is not a directory"):
            syncer.validate_paths()

    def test_validate_source_not_valid_template(self, temp_dirs: tuple[Path, Path]) -> None:
        """Test validation fails when source doesn't have justfile."""
        source, target = temp_dirs
        syncer = TemplateSyncer(source, target)
        with pytest.raises(SyncError, match="Source doesn't appear to be a valid template"):
            syncer.validate_paths()

    def test_validate_target_path_not_exists(self, source_template: Path) -> None:
        """Test validation fails when target doesn't exist."""
        nonexistent = Path("/nonexistent/target")
        syncer = TemplateSyncer(source_template, nonexistent)
        with pytest.raises(SyncError, match="Target path does not exist"):
            syncer.validate_paths()

    def test_validate_target_not_git_repo(
        self, source_template: Path, temp_dirs: tuple[Path, Path]
    ) -> None:
        """Test validation fails when target is not a git repo."""
        _, target = temp_dirs
        syncer = TemplateSyncer(source_template, target)
        with pytest.raises(SyncError, match="Target is not a git repository"):
            syncer.validate_paths()

    def test_validate_paths_success(self, source_template: Path, target_project: Path) -> None:
        """Test validation succeeds with valid paths."""
        syncer = TemplateSyncer(source_template, target_project)
        # Should not raise
        syncer.validate_paths()


class TestTemplateSyncerOperations:
    """Test sync operations."""

    def test_sync_file_creates_new_file(self, source_template: Path, target_project: Path) -> None:
        """Test syncing a new file to target."""
        syncer = TemplateSyncer(source_template, target_project)
        syncer.sync_file(".gitignore")
        assert (target_project / ".gitignore").exists()
        assert (target_project / ".gitignore").read_text() == (
            source_template / ".gitignore"
        ).read_text()
        assert ".gitignore" in syncer.changes

    def test_sync_file_updates_existing_file(
        self, source_template: Path, target_project: Path
    ) -> None:
        """Test syncing an existing file with changes."""
        # Create old version of file in target
        (target_project / ".python-version").write_text("3.11\n")
        syncer = TemplateSyncer(source_template, target_project)
        syncer.sync_file(".python-version")
        # File should be updated
        assert (target_project / ".python-version").read_text() == "3.12\n"
        assert ".python-version" in syncer.changes

    def test_sync_file_skips_unchanged(self, source_template: Path, target_project: Path) -> None:
        """Test syncing skips unchanged files."""
        # Create matching file in target
        (target_project / ".python-version").write_text("3.12\n")
        syncer = TemplateSyncer(source_template, target_project)
        initial_changes = len(syncer.changes)
        syncer.sync_file(".python-version")
        # Changes list should not grow
        assert len(syncer.changes) == initial_changes

    def test_sync_directory_creates_new(self, source_template: Path, target_project: Path) -> None:
        """Test syncing a new directory to target."""
        syncer = TemplateSyncer(source_template, target_project)
        syncer.sync_directory("tasks")
        assert (target_project / "tasks").exists()
        assert (target_project / "tasks" / "test.just").exists()
        assert (target_project / "tasks" / "test.just").read_text() == 'test: echo "test"'

    def test_sync_directory_replaces_existing(
        self, source_template: Path, target_project: Path
    ) -> None:
        """Test syncing replaces existing directory."""
        # Create old version in target
        (target_project / "tasks").mkdir()
        (target_project / "tasks" / "old.just").write_text("# old")
        syncer = TemplateSyncer(source_template, target_project)
        syncer.sync_directory("tasks")
        # Old file should be gone
        assert not (target_project / "tasks" / "old.just").exists()
        # New file should exist
        assert (target_project / "tasks" / "test.just").exists()

    def test_sync_all_operations(self, source_template: Path, target_project: Path) -> None:
        """Test syncing all configured targets."""
        syncer = TemplateSyncer(source_template, target_project)
        syncer.sync_all()
        # Check all files were synced
        assert (target_project / "justfile").exists()
        assert (target_project / ".gitignore").exists()
        assert (target_project / ".python-version").exists()
        assert (target_project / "tasks").exists()
        assert len(syncer.changes) > 0


class TestTemplateSyncerGit:
    """Test git operations."""

    def test_git_commit_creates_commit(self, source_template: Path, target_project: Path) -> None:
        """Test git commit creates a commit with changes."""
        syncer = TemplateSyncer(source_template, target_project)
        syncer.sync_all()
        syncer.git_add_changes()
        result = syncer.git_commit()
        assert result is True
        # Check commit was created
        log_result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=target_project,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "Sync with latest project template" in log_result.stdout

    def test_git_commit_dry_run(self, source_template: Path, target_project: Path) -> None:
        """Test dry run doesn't create commit."""
        syncer = TemplateSyncer(source_template, target_project, dry_run=True)
        syncer.sync_all()
        result = syncer.git_commit()
        assert result is True
        # Check no commit was created
        log_result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=target_project,
            capture_output=True,
            text=True,
            check=True,
        )
        # Should only have initial commit
        assert log_result.stdout.count("\n") <= 2

    def test_git_add_changes(self, source_template: Path, target_project: Path) -> None:
        """Test git add stages changes."""
        syncer = TemplateSyncer(source_template, target_project)
        syncer.sync_all()
        syncer.git_add_changes()
        # Check files are staged
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=target_project,
            capture_output=True,
            text=True,
            check=True,
        )
        # Files should be staged (A = added)
        assert "A" in status_result.stdout or "M" in status_result.stdout


class TestTemplateSyncerCLI:
    """Test CLI interface."""

    def test_main_with_valid_args(self, source_template: Path, target_project: Path) -> None:
        """Test main function with valid arguments."""
        result = main(
            [
                "--source",
                str(source_template),
                "--target",
                str(target_project),
            ]
        )
        assert result == 0

    def test_main_with_dry_run(self, source_template: Path, target_project: Path) -> None:
        """Test main function with dry-run flag."""
        result = main(
            [
                "--source",
                str(source_template),
                "--target",
                str(target_project),
                "--dry-run",
            ]
        )
        assert result == 0

    def test_main_invalid_source(self, target_project: Path) -> None:
        """Test main function fails with invalid source."""
        result = main(
            [
                "--source",
                "/nonexistent/path",
                "--target",
                str(target_project),
            ]
        )
        assert result != 0

    def test_main_invalid_target(self, source_template: Path) -> None:
        """Test main function fails with invalid target."""
        result = main(
            [
                "--source",
                str(source_template),
                "--target",
                "/nonexistent/target",
            ]
        )
        assert result != 0
