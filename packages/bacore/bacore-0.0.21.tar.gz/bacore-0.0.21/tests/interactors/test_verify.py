"""Tests for interactors.verify module."""
import pytest
from bacore.domain import system
from bacore.interactors import retrieve, verify

pytestmark = pytest.mark.interactors


@pytest.fixture
def fixture_test_command_on_path():
    """Fixture for command_on_path."""
    if retrieve.system_information_os().os in ["Darwin", "Linux"]:
        return "ls"
    else:
        return "dir"


def test_command_on_path(fixture_test_command_on_path):
    """Test command_on_path."""
    command = system.CommandLineProgram(name=fixture_test_command_on_path)
    assert verify.command_on_path(command=command) is True
    bogus_command = system.CommandLineProgram(name="bogus_does_not_exist")
    assert verify.command_on_path(command=bogus_command) is False
