#!/usr/bin/env python
"""Command-line interface."""
import click
from rich import traceback


@click.command()
@click.version_option(version="1.4.4", message=click.style("cornflakes Version: 1.4.4"))
def main() -> None:
    """cornflakes."""


if __name__ == "__main__":
    traceback.install()
    main(prog_name="cornflakes")  # pragma: no cover
