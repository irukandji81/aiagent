import os

def get_files_info(working_directory, directory=None):
    # Resolve absolute paths
    base_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, directory or ""))

    # Ensure the target directory is within the working directory
    if not target_path.startswith(base_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Check if the target path is a valid directory
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'

    try:
        # List directory contents
        files_info = []
        for entry in os.scandir(target_path):
            files_info.append(
                f'- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}'
            )

        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {str(e)}"