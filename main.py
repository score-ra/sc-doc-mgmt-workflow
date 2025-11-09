"""
Main entry point for Symphony Core Document Management Workflow.

Run this file to access the CLI:
    python main.py --help
    python main.py validate
    python main.py validate --help
"""

from src.cli import cli


if __name__ == '__main__':
    cli(obj={})
