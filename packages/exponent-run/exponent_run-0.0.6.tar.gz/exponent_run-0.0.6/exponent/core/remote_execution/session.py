from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from exponent.core.remote_execution.languages.python import Kernel


class RemoteExecutionClientSession:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel


@asynccontextmanager
async def get_session() -> AsyncGenerator[RemoteExecutionClientSession, None]:
    session = RemoteExecutionClientSession(Kernel())
    try:
        yield session
    except Exception as e:
        session.kernel.close()
        raise e
