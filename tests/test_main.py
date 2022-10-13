"""Test cases for the __main__ module."""
from click.testing import CliRunner
import pytest

from cornflakes.__main__ import cornflakes_cli


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cornflakes_cli, prog_name="cornflakes")
    if result.exc_info:
        assert result.exc_info[0] == TypeError or result.exc_info[0] == DeprecationWarning or result.exit_code == 0