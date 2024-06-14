import os


def execute_diff(contents: str, working_directory: str) -> str:
    try:
        # Split contents into lines and extract the filename
        lines = contents.split("\n")
        filename_line = lines[0]

        if not filename_line.startswith("filepath="):
            return "Invalid input format. The first line should start with 'filepath='."

        # Extract the relative filename and the new file content
        relative_filepath = filename_line[len("filepath=") :]
        new_content = "\n".join(lines[1:])

        # Construct the absolute path
        file_path = os.path.join(working_directory, relative_filepath)

        # Check if the directory exists, if not, create it
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Determine if the file exists and write the new content
        if os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write(new_content)
            return f"Modified file {relative_filepath}"
        else:
            with open(file_path, "w") as file:
                file.write(new_content)
            return f"Created file {relative_filepath}"

    except Exception as e:  # noqa: BLE001
        return f"An error occurred: {e!s}"
