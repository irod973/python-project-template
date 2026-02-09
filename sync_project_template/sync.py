#!/usr/bin/env python3
"""
Sync this project with the latest Python project template.

This script syncs high-priority files from the template repository to your project,
including tasks, justfile, and configuration files. It tracks changes and automatically
commits them to git.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from loguru import logger


class SyncError(Exception):
    """Base exception for sync operations."""
    pass


class TemplateSyncer:
    """Syncs a project with the latest template files."""

    # Files/directories to sync (relative to template root)
    SYNC_TARGETS = {
        'tasks': {'type': 'directory', 'description': 'Task definitions'},
        'justfile': {'type': 'file', 'description': 'Just task runner config'},
        '.gitignore': {'type': 'file', 'description': 'Git ignore patterns'},
        '.python-version': {'type': 'file', 'description': 'Python version'},
    }

    def __init__(self, source_path: Path, target_path: Path, dry_run: bool = False):
        """Initialize the syncer.

        Args:
            source_path: Path to the template source directory
            target_path: Path to the target project directory
            dry_run: If True, don't commit changes
        """
        self.source_path = Path(source_path).resolve()
        self.target_path = Path(target_path).resolve()
        self.dry_run = dry_run
        self.changes = []

    def validate_paths(self) -> None:
        """Validate that both source and target paths exist and are valid."""
        if not self.source_path.exists():
            raise SyncError(f"Source path does not exist: {self.source_path}")

        if not self.source_path.is_dir():
            raise SyncError(f"Source path is not a directory: {self.source_path}")

        # Check if source has expected template structure
        if not (self.source_path / 'justfile').exists():
            raise SyncError(
                f"Source doesn't appear to be a valid template "
                f"(missing justfile): {self.source_path}"
            )

        if not self.target_path.exists():
            raise SyncError(f"Target path does not exist: {self.target_path}")

        if not self.target_path.is_dir():
            raise SyncError(f"Target path is not a directory: {self.target_path}")

        # Check if target is a git repository
        if not (self.target_path / '.git').exists():
            raise SyncError(f"Target is not a git repository: {self.target_path}")

    def check_git_clean(self) -> None:
        """Warn if git working directory is dirty."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.target_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                logger.warning("Git working directory has uncommitted changes")
                logger.info("Consider committing them before syncing")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # git not available or timed out, skip check
            pass

    def sync_directory(self, relative_path: str) -> None:
        """Sync a directory from source to target, recursively.

        Args:
            relative_path: Path relative to source/target roots
        """
        source_dir = self.source_path / relative_path
        target_dir = self.target_path / relative_path

        if not source_dir.exists():
            logger.warning(f"Source directory not found: {source_dir}")
            return

        # Remove target directory if it exists
        if target_dir.exists():
            shutil.rmtree(target_dir)

        # Copy directory
        shutil.copytree(source_dir, target_dir)
        file_count = len(list(target_dir.rglob('*')))
        self.changes.append(f"{relative_path}/ (directory, {file_count} items)")
        logger.debug(f"Synced directory: {relative_path}")

    def sync_file(self, relative_path: str) -> None:
        """Sync a single file from source to target.

        Args:
            relative_path: Path relative to source/target roots
        """
        source_file = self.source_path / relative_path
        target_file = self.target_path / relative_path

        if not source_file.exists():
            logger.warning(f"Source file not found: {source_file}")
            return

        # Check if file has changed
        if target_file.exists():
            with open(source_file, 'rb') as sf, open(target_file, 'rb') as tf:
                if sf.read() == tf.read():
                    logger.debug(f"File unchanged: {relative_path}")
                    return

        # Copy file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        self.changes.append(relative_path)
        logger.debug(f"Synced file: {relative_path}")

    def sync_all(self) -> None:
        """Sync all configured targets."""
        logger.info("Syncing files from template")
        logger.debug(f"Source: {self.source_path}")
        logger.debug(f"Target: {self.target_path}")

        for target_name, target_info in self.SYNC_TARGETS.items():
            target_type = target_info['type']
            description = target_info['description']

            logger.info(f"Syncing {description}...")

            if target_type == 'directory':
                self.sync_directory(target_name)
            elif target_type == 'file':
                self.sync_file(target_name)

    def git_add_changes(self) -> None:
        """Stage all changes for commit."""
        if not self.changes:
            logger.info("No changes to sync")
            return

        for target_name in self.SYNC_TARGETS.keys():
            try:
                subprocess.run(
                    ['git', 'add', target_name],
                    cwd=self.target_path,
                    capture_output=True,
                    timeout=5,
                )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

    def git_commit(self) -> bool:
        """Create a commit with the synced changes.

        Returns:
            True if commit was successful, False otherwise
        """
        if not self.changes:
            return False

        if self.dry_run:
            logger.info("DRY RUN: Would create commit with the following changes:")
            for change in self.changes:
                logger.info(f"  • {change}")
            return True

        # Generate commit message
        synced_items = "\n".join(f"  • {change}" for change in self.changes)
        commit_message = f"""Sync with latest project template

Synced the following files and directories:
{synced_items}

This commit updates the project infrastructure to match the latest
template version, including task definitions, configuration files,
and development tools."""

        try:
            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.target_path,
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )
            logger.debug(f"Git commit output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Git commit failed: {e.stderr}")
            return False
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.error(f"Git operation failed: {e}")
            return False

    def print_summary(self) -> None:
        """Print a summary of what was synced."""
        if not self.changes:
            logger.success("No changes needed - project is already up to date!")
            return

        logger.success("Successfully synced the following:")
        for change in self.changes:
            logger.success(f"  • {change}")

        if not self.dry_run:
            logger.success("Changes committed to git")
        else:
            logger.info("DRY RUN: No changes were actually made")

    def run(self) -> bool:
        """Run the sync operation.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.validate_paths()
            self.check_git_clean()
            self.sync_all()
            self.git_add_changes()
            success = self.git_commit()
            self.print_summary()
            return success
        except SyncError as e:
            logger.error(f"{e}")
            return False


def main(argv: Optional[list] = None) -> int:
    """Main entry point for the sync CLI.

    Args:
        argv: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(
        description="Sync this project with the latest Python project template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync with a local template directory
  python sync.py --source ~/python-project-template/{{{{cookiecutter.repository}}}} --target .

  # Dry run to preview changes
  python sync.py --source ~/templates/pytemplate --target . --dry-run
        """,
    )

    parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='Path to the template source directory',
    )

    parser.add_argument(
        '--target',
        type=str,
        default='.',
        help='Path to the target project (default: current directory)',
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without committing',
    )

    args = parser.parse_args(argv)

    syncer = TemplateSyncer(
        source_path=args.source,
        target_path=args.target,
        dry_run=args.dry_run,
    )

    success = syncer.run()
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
