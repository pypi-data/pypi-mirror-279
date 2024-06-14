import datetime
from enum import Enum
from functools import cached_property
from pathlib import PurePath
from typing import ClassVar, Generic, Literal, TypeGuard, TypeVar

from pydantic import BaseModel, Field


class UseToolsMode(str, Enum):
    read_only = "read_only"
    read_write = "read_write"
    disabled = "disabled"


class UseToolsConfig(BaseModel):
    mode: UseToolsMode = UseToolsMode.read_only

    @property
    def read_only(self) -> bool:
        return self.mode == UseToolsMode.read_only

    @property
    def read_write(self) -> bool:
        return self.mode == UseToolsMode.read_write

    def disable(self) -> None:
        self.mode = UseToolsMode.disabled


class CreateChatResponse(BaseModel):
    chat_uuid: str


class StartChatRequest(BaseModel):
    chat_uuid: str
    prompt: str
    use_tools_config: UseToolsConfig


class StartChatResponse(BaseModel):
    chat_uuid: str


class ExecutionEndResponse(BaseModel):
    execution_ended: bool


class SignalType(str, Enum):
    disconnect = "disconnect"


class SignalStatus(str, Enum):
    sent = "sent"
    acknowledged = "acknowledged"
    none = "none"


class SignalResponse(BaseModel):
    signal_type: SignalType
    status: SignalStatus


class GitInfo(BaseModel):
    branch: str
    remote: str | None


class PythonEnvInfo(BaseModel):
    interpreter_path: str | None
    interpreter_version: str | None
    name: str | None = "exponent"
    provider: Literal["venv", "pyenv", "pipenv", "conda"] | None = "pyenv"


class SystemInfo(BaseModel):
    name: str
    cwd: str
    os: str
    shell: str
    git: GitInfo | None
    python_env: PythonEnvInfo | None


class HeartbeatInfo(BaseModel):
    system_info: SystemInfo | None
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )


class RemoteFile(BaseModel):
    file_path: str
    working_directory: str

    @cached_property
    def _path(self) -> PurePath:
        return PurePath(self.working_directory, self.file_path)

    @cached_property
    def name(self) -> str:
        return self._path.name

    @cached_property
    def absolute_path(self) -> str:
        return self._path.as_posix()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RemoteFile):
            return False
        return self.absolute_path == other.absolute_path

    def __lt__(self, other: "RemoteFile") -> bool:
        return self.absolute_path < other.absolute_path


Direction = Literal[
    "request",
    "response",
]

Namespace = Literal[
    "code_execution",
    "list_files",
    "get_file_attachment",
    "get_matching_files",
    "system_context",
    "get_all_tracked_files",
]

SupportedLanguage = Literal[
    "python",
    "shell",
    "diff",
]


class RemoteExecutionMessageData(BaseModel):
    namespace: Namespace
    direction: Direction
    message_data: str

    def message_type(self) -> str:
        return f"{self.namespace}.{self.direction}"


class RemoteExecutionResponseData(RemoteExecutionMessageData):
    pass


class RemoteExecutionRequestData(RemoteExecutionMessageData):
    pass


class RemoteExecutionMessage(BaseModel):
    direction: ClassVar[Direction]
    namespace: ClassVar[Namespace]
    correlation_id: str

    @classmethod
    def message_type(cls) -> str:
        return f"{cls.namespace}.{cls.direction}"

    @property
    def result_key(self) -> str:
        return f"{self.namespace}:{self.correlation_id}"


class RemoteExecutionResponse(RemoteExecutionMessage):
    direction: ClassVar[Direction] = "response"


ResponseT = TypeVar("ResponseT", bound=RemoteExecutionResponse)


class RemoteExecutionRequest(RemoteExecutionMessage, Generic[ResponseT]):
    direction: ClassVar[Direction] = "request"

    def validate_response_type(
        self, response: RemoteExecutionMessage
    ) -> TypeGuard[ResponseT]:
        if self.namespace != response.namespace or response.direction != "response":
            raise ValueError(
                f"Expected {self.namespace}.response, but got {response.namespace}.{response.direction}"
            )
        return True


class CodeExecutionResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "code_execution"

    content: str


class CodeExecutionRequest(RemoteExecutionRequest[CodeExecutionResponse]):
    namespace: ClassVar[Namespace] = "code_execution"

    language: SupportedLanguage
    content: str


class ListFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "list_files"

    files: list[RemoteFile]


class ListFilesRequest(RemoteExecutionRequest[ListFilesResponse]):
    namespace: ClassVar[Namespace] = "list_files"

    directory: str


class GetFileAttachmentResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_file_attachment"

    file: RemoteFile
    content: str


class GetFileAttachmentRequest(RemoteExecutionRequest[GetFileAttachmentResponse]):
    namespace: ClassVar[Namespace] = "get_file_attachment"

    file: RemoteFile


class GetMatchingFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_matching_files"

    files: list[RemoteFile]


class GetMatchingFilesRequest(RemoteExecutionRequest[GetMatchingFilesResponse]):
    namespace: ClassVar[Namespace] = "get_matching_files"

    search_term: str


class GetAllTrackedFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_all_tracked_files"

    files: list[RemoteFile]


class GetAllTrackedFilesRequest(RemoteExecutionRequest[GetAllTrackedFilesResponse]):
    namespace: ClassVar[Namespace] = "get_all_tracked_files"


class SystemContextResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "system_context"

    exponent_txt: str | None
    system_info: SystemInfo | None


class SystemContextRequest(RemoteExecutionRequest[SystemContextResponse]):
    namespace: ClassVar[Namespace] = "system_context"


RemoteExecutionRequestType = (
    CodeExecutionRequest
    | ListFilesRequest
    | GetFileAttachmentRequest
    | GetMatchingFilesRequest
    | GetAllTrackedFilesRequest
    | SystemContextRequest
)

RemoteExecutionResponseType = (
    CodeExecutionResponse
    | ListFilesResponse
    | GetFileAttachmentResponse
    | GetMatchingFilesResponse
    | GetAllTrackedFilesResponse
    | SystemContextResponse
)


class CLIConnectedState(BaseModel):
    chat_uuid: str
    connected: bool
    last_connected_at: datetime.datetime | None
    system_info: SystemInfo | None
