import os

def get_file_content(working_directory, file_path):
    # Resolve absolute paths
    base_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Ensure the target file is within the working directory
    if not target_path.startswith(base_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the target path is a valid file
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Read file contents
        with open(target_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Truncate if longer than 10,000 characters
        if len(content) > 10000:
            content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"