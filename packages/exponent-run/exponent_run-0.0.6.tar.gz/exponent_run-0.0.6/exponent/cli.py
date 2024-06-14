import _thread
import asyncio
import logging
import os
import sys
from collections.abc import Callable
from functools import wraps
from typing import Any

import click
import httpx
from dotenv import load_dotenv

from exponent.cli_utils import print_editable_install_warning, print_exponent_message
from exponent.core.config import Settings, get_settings, is_editable_install
from exponent.core.remote_execution.client import RemoteExecutionClient
from exponent.core.remote_execution.types import UseToolsConfig

load_dotenv()


def use_settings(f: Callable[..., Any]) -> Callable[..., Any]:
    @click.option(
        "--prod",
        is_flag=True,
        hidden=True,
        help="Use production URLs even if in editable mode",
    )
    @click.option(
        "--staging",
        is_flag=True,
        hidden=True,
        help="Use staging URLs even if in editable mode",
    )
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        prod = kwargs.pop("prod", False)
        staging = kwargs.pop("staging", False)
        settings = get_settings(use_prod=prod, use_staging=staging)

        if is_editable_install() and not (prod or staging):
            print_editable_install_warning(settings)

        return f(*args, settings=settings, **kwargs)

    return decorated_function


@click.group()
def cli() -> None:
    """Exponent CLI group."""
    set_log_level()


@cli.command()
@click.option("--key", help="Your Exponent API Key")
@use_settings
def login(settings: Settings, key: str) -> None:
    if not key:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/")
        return
    click.echo("Saving API Key to ~/.exponent...")
    if settings.api_key and settings.api_key != key:
        click.confirm("Detected existing API Key, continue? ", default=True, abort=True)
    with open(os.path.expanduser("~/.exponent"), "a") as f:
        f.write(f"\nEXPONENT_API_KEY={key}\n")
    click.echo("API Key saved.")


@cli.command()
@click.option(
    "--chat-id",
    help="ID of an existing chat session to reconnect",
    required=False,
)
@click.option(
    "--prompt",
    help="Start a chat with a given prompt.",
)
@click.option(
    "--benchmark",
    is_flag=True,
    help="Enable benchmarking mode",
)
@use_settings
def run(
    settings: Settings,
    chat_id: str | None = None,
    prompt: str | None = None,
    benchmark: bool = False,
) -> None:
    chat_uuid = chat_id

    if not settings.api_key:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/")
        return
    else:
        api_key = settings.api_key

    loop = asyncio.get_event_loop()
    task = loop.create_task(
        start_client(
            api_key,
            settings.base_url,
            settings.base_api_url,
            chat_uuid=chat_uuid,
            prompt=prompt,
            benchmark=benchmark,
        )
    )
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass


@cli.command()
@click.option(
    "--prompt",
    help="Start a chat with a given prompt.",
)
@use_settings
def cloud(
    settings: Settings,
    prompt: str | None = None,
) -> None:
    if not settings.api_key:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/")
        return
    else:
        api_key = settings.api_key

    loop = asyncio.get_event_loop()
    task = loop.create_task(
        start_cloud(
            api_key,
            settings.base_url,
            settings.base_api_url,
            prompt=prompt,
        )
    )
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass


async def start_cloud(
    api_key: str,
    base_url: str,
    base_api_url: str,
    prompt: str | None = None,
) -> None:
    current_working_directory = os.getcwd()

    # Step 0. Load config
    _repository = "helloworld/exponent"
    _image = "..."

    # Step 1. Create a chat
    try:
        async with RemoteExecutionClient.session(
            api_key, base_api_url, current_working_directory
        ) as client:
            chat = await client.create_chat()
            chat_uuid = chat.chat_uuid
    except httpx.ConnectError as e:
        click.secho(f"Error: {e}", fg="red")
        return

    click.secho("Chat created. Waiting for devbox to spin up...", fg="green", bold=True)

    # Step 2. Launch Runloop with
    # if prompt: exponent run --chat-id {chat_uuid} --prompt {prompt}
    # else: exponent run --chat-id {chat_uuid}
    pass

    # Step 3. Poll Runloop for container spinup and log status
    # Example output:
    # Waiting for devbox to spin up...
    # Waiting for devbox to spin up...
    # Waiting for devbox to spin up...
    # Waiting for devbox to spin up...
    # Devbox ready
    pass

    # Step 4. Open the chat in the browser
    # Sucess criteria:
    # - Chat shows CLI is connected
    print_exponent_message(base_url, chat_uuid)
    click.launch(f"{base_url}/chats/{chat_uuid}")

    # Step 5. Wait for user input with the message "Stop Runloop?"
    input("Stop Runloop?: [press enter to continue]")

    # Step 6. Stop Runloop
    pass

    click.secho("Runloop stopped", fg="green", bold=True)

    # Final state success criteria:
    # - Chat shows CLI is disconnected


async def start_client(  # noqa: PLR0913
    api_key: str,
    base_url: str,
    base_api_url: str,
    chat_uuid: str | None = None,
    prompt: str | None = None,
    benchmark: bool = False,
) -> None:
    if benchmark is True and prompt is None:
        click.secho("Error: Benchmark mode requires a prompt.", fg="red")
        return

    current_working_directory = os.getcwd()

    if not chat_uuid:
        try:
            async with RemoteExecutionClient.session(
                api_key, base_api_url, current_working_directory
            ) as client:
                chat = await client.create_chat()
                chat_uuid = chat.chat_uuid
        except httpx.ConnectError as e:
            click.secho(f"Error: {e}", fg="red")
            return

    print_exponent_message(base_url, chat_uuid)

    # Open the chat in the browser
    if not benchmark and not prompt and not chat_uuid:
        click.launch(f"{base_url}/chats/{chat_uuid}")

    use_tools_config = UseToolsConfig()
    async with RemoteExecutionClient.session(
        api_key, base_api_url, current_working_directory
    ) as client:
        if benchmark:
            assert prompt is not None
            await asyncio.gather(
                start_chat(
                    client, chat_uuid, prompt, use_tools_config=use_tools_config
                ),
                run_execution_client(client, chat_uuid),
                benchmark_mode_exit(client, chat_uuid),
                heartbeat_thread(client, chat_uuid),
                signal_listener_thread(client, chat_uuid),
            )
        elif prompt:
            await asyncio.gather(
                start_chat(
                    client, chat_uuid, prompt, use_tools_config=use_tools_config
                ),
                run_execution_client(client, chat_uuid),
                heartbeat_thread(client, chat_uuid),
                signal_listener_thread(client, chat_uuid),
            )
        else:
            await asyncio.gather(
                run_execution_client(client, chat_uuid),
                heartbeat_thread(client, chat_uuid),
                signal_listener_thread(client, chat_uuid),
            )


async def run_execution_client(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        execution_requests = await client.get_execution_requests(chat_uuid)
        for execution_request in execution_requests:
            click.echo(f"Handling {execution_request.namespace} request:")
            click.echo(f"  - {execution_request}")
            execution_response = await client.handle_request(execution_request)
            click.echo(f"Posting {execution_request.namespace} response.")
            await client.post_execution_result(chat_uuid, execution_response)
        await asyncio.sleep(0.2)


async def start_chat(
    client: RemoteExecutionClient,
    chat_uuid: str,
    prompt: str,
    use_tools_config: UseToolsConfig,
) -> None:
    click.secho("Starting chat...")
    await client.start_chat(chat_uuid, prompt, use_tools_config=use_tools_config)
    click.secho("Chat started. Open the link to join the chat.")


async def benchmark_mode_exit(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        await asyncio.sleep(5)
        if await client.check_cli_execution_end_event(chat_uuid):
            sys.exit(0)


async def heartbeat_thread(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        await client.send_heartbeat(chat_uuid)
        await asyncio.sleep(1)


async def signal_listener_thread(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        disconnect_signaled = await client.disconnect_signal_received(chat_uuid)
        if disconnect_signaled:
            await client.acknowledge_disconnect_signal(chat_uuid)
            click.secho("Disconnect signaled. Exiting.")
            _thread.interrupt_main()
        await asyncio.sleep(1)


def set_log_level() -> None:
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level), stream=sys.stdout)


if __name__ == "__main__":
    cli()
