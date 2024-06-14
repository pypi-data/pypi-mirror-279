import json
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from httpx import (
    AsyncClient,
    Response,
    codes as http_status,
)

from exponent.core.remote_execution import files, git, system_context
from exponent.core.remote_execution.code_execution import execute_code
from exponent.core.remote_execution.session import (
    RemoteExecutionClientSession,
    get_session,
)
from exponent.core.remote_execution.types import (
    CLIConnectedState,
    CodeExecutionRequest,
    CreateChatResponse,
    ExecutionEndResponse,
    GetAllTrackedFilesRequest,
    GetFileAttachmentRequest,
    GetMatchingFilesRequest,
    HeartbeatInfo,
    ListFilesRequest,
    RemoteExecutionRequestType,
    RemoteExecutionResponse,
    RemoteExecutionResponseType,
    SignalResponse,
    SignalStatus,
    StartChatRequest,
    StartChatResponse,
    SystemContextRequest,
    UseToolsConfig,
)
from exponent.core.remote_execution.utils import (
    deserialize_request_data,
    serialize_message,
)

logger = logging.getLogger(__name__)


class RemoteExecutionClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        working_directory: str,
        session: RemoteExecutionClientSession,
    ):
        self.headers = {"API-KEY": api_key}
        self.base_url = base_url
        self.working_directory = working_directory
        self.current_session = session

        self.file_cache: files.FileCache = files.FileCache(working_directory)

    async def get_execution_requests(
        self, chat_uuid: str
    ) -> list[RemoteExecutionRequestType]:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/requests",
                headers=self.headers,
            )

        response_json = self._response_json(response)
        return [deserialize_request_data(result) for result in response_json]

    async def post_execution_result(
        self, chat_uuid: str, response: RemoteExecutionResponse
    ) -> None:
        async with AsyncClient() as client:
            await client.post(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/result",
                headers=self.headers,
                content=serialize_message(response),
            )

    async def check_cli_execution_end_event(self, chat_uuid: str) -> bool:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/execution_end",
                headers=self.headers,
            )
        response_json = self._response_json(response)
        execution_end_response = ExecutionEndResponse(**response_json)
        return execution_end_response.execution_ended

    async def create_chat(self) -> CreateChatResponse:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/create_chat",
                headers=self.headers,
            )
        return CreateChatResponse(**response.json())

    async def start_chat(
        self, chat_uuid: str, prompt: str, use_tools_config: UseToolsConfig
    ) -> StartChatResponse:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/start_chat",
                headers=self.headers,
                json=StartChatRequest(
                    chat_uuid=chat_uuid,
                    prompt=prompt,
                    use_tools_config=use_tools_config,
                ).model_dump(),
                timeout=60,
            )
        response_json = self._response_json(response)
        return StartChatResponse(**response_json)

    def get_heartbeat_info(self) -> HeartbeatInfo:
        return HeartbeatInfo(
            system_info=system_context.get_system_info(self.working_directory),
        )

    async def send_heartbeat(self, chat_uuid: str) -> CLIConnectedState:
        logger.info(f"Sending heartbeat for chat_uuid {chat_uuid}")
        heartbeat_info = self.get_heartbeat_info()
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/heartbeat",
                headers=self.headers,
                content=heartbeat_info.model_dump_json(),
                timeout=60,
            )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Heartbeat failed with status code {response.status_code} and response {response.text}"
            )
        response_json = self._response_json(response)
        connected_state = CLIConnectedState(**response_json)
        logger.info(f"Heartbeat response: {connected_state}")
        return connected_state

    async def handle_request(
        self, request: RemoteExecutionRequestType
    ) -> RemoteExecutionResponseType:
        if isinstance(request, CodeExecutionRequest):
            return await execute_code(
                request, self.current_session, working_directory=self.working_directory
            )
        elif isinstance(request, ListFilesRequest):
            return files.list_files(request)
        elif isinstance(request, GetFileAttachmentRequest):
            return files.get_file_attachment(request)
        elif isinstance(request, GetMatchingFilesRequest):
            return files.get_matching_files(request, self.file_cache)
        elif isinstance(request, SystemContextRequest):
            return system_context.get_system_context(request, self.working_directory)
        elif isinstance(request, GetAllTrackedFilesRequest):
            return git.get_all_tracked_files(request, self.working_directory)

    async def disconnect_signal_received(self, chat_uuid: str) -> bool:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/signal/disconnect/check",
                headers=self.headers,
                timeout=60,
            )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Failed to fetch disconnect status {response.status_code} and response {response.text}"
            )
        response_json = self._response_json(response)
        signal = SignalResponse.model_validate(response_json)
        return signal.status == SignalStatus.sent

    async def acknowledge_disconnect_signal(self, chat_uuid: str) -> None:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/signal/disconnect/acknowledge",
                headers=self.headers,
                timeout=60,
            )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Failed to fetch disconnect status {response.status_code} and response {response.text}"
            )

    def _response_json(self, response: Response) -> Any:
        try:
            response_json = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing response: {e}")
            logger.error(
                f"Raw response: [status-{response.status_code}] {response.text}"
            )
            raise e
        return response_json

    @staticmethod
    @asynccontextmanager
    async def session(
        api_key: str, base_url: str, working_directory: str
    ) -> AsyncGenerator["RemoteExecutionClient", None]:
        async with get_session() as session:
            yield RemoteExecutionClient(api_key, base_url, working_directory, session)
