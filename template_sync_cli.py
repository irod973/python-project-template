#!/usr/bin/env python3
"""
CLI wrapper for the sync_project_template utility.

This script provides a command-line interface to sync projects with the latest
Python project template. It can be used directly or as a Claude Code skill.
"""

import argparse
import sys

from sync_project_template.sync import main


def run() -> int:
    """Run the template sync CLI."""
    parser = argparse.ArgumentParser(
        description="Sync your project with the latest Python project template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync current project with the template
  python template_sync_cli.py --source ~/path/to/template --target .

  # Preview changes without committing
  python template_sync_cli.py --source ~/path/to/template --target . --dry-run

  # Sync another project
  python template_sync_cli.py --source ~/path/to/template --target ~/another-project
        """,
    )

    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to the template source directory",
        metavar="PATH",
    )

    parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to the target project (default: current directory)",
        metavar="PATH",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without committing them",
    )

    args = parser.parse_args()

    # Call the main sync function with the parsed arguments
    return main([
        "--source", args.source,
        "--target", args.target,
        *(["--dry-run"] if args.dry_run else []),
    ])


if __name__ == "__main__":
    sys.exit(run())