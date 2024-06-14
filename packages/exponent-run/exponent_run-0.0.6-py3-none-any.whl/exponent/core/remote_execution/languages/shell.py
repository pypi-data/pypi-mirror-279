import asyncio


async def execute_shell(code: str, working_directory: str) -> str:
    process = await asyncio.create_subprocess_shell(
        code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=working_directory,
    )
    stdout_data, stderr_data = await process.communicate()
    decoded_stdout = stdout_data.decode()
    decoded_stderr = stderr_data.decode()
    output = []
    if decoded_stdout:
        output.append(decoded_stdout)
    if decoded_stderr:
        output.append(decoded_stderr)
    shell_output = "\n".join(output)
    return shell_output
