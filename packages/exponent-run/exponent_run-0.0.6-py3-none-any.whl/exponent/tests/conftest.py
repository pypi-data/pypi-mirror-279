import asyncio
import os
import tempfile
from collections.abc import Generator
from unittest.mock import patch

import pygit2
import pytest
from click.testing import CliRunner

from exponent.core.remote_execution.languages import python
from exponent.core.remote_execution.types import PythonEnvInfo
from exponent.tests.utils import create_commit, stage_file


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope="session", autouse=True)
async def fixture_setup_env() -> None:
    session_mpatch = pytest.MonkeyPatch()
    session_mpatch.setenv("EXPONENT_API_KEY", "123456")
    session_mpatch.setenv("EXPONENT_BASE_URL", "https://exponent.run")
    session_mpatch.setenv("EXPONENT_API_BASE_URL", "https://api.exponent.run")


@pytest.fixture(scope="function")
def temporary_directory() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as test_directory:
        yield test_directory


@pytest.fixture(scope="function")
def default_temporary_directory(temporary_directory: str) -> Generator[str, None, None]:
    with open(os.path.join(temporary_directory, "test1.py"), "w") as f:
        f.write("print('Hello, world!')")

    with open(os.path.join(temporary_directory, "test2.py"), "w") as f:
        f.write("print('Hello, world!')")

    with open(os.path.join(temporary_directory, "exponent.txt"), "w") as f:
        f.write("Hello, world!")

    repo = pygit2.init_repository(temporary_directory, bare=False)

    stage_file(repo, "test1.py")
    stage_file(repo, "test2.py")
    stage_file(repo, "exponent.txt")
    create_commit(repo, "Initial commit", "Tester McTesterface", "test@example.com")

    yield temporary_directory


@pytest.fixture(scope="function", autouse=True)
def mock_cli_heartbeat() -> Generator[None, None, None]:
    patcher = patch(
        "exponent.core.remote_execution.client.RemoteExecutionClient.send_heartbeat"
    )
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture(name="python_env_info", scope="function", autouse=True)
def fixture_python_env_info(
    monkeypatch: pytest.MonkeyPatch,
) -> PythonEnvInfo:
    env_info = PythonEnvInfo(
        interpreter_path="python",
        interpreter_version="3.11.0",
    )

    def get_python_env_info() -> PythonEnvInfo:
        return env_info

    monkeypatch.setattr(
        python,
        "get_python_env_info",
        get_python_env_info,
    )

    return env_info
