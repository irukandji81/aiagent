import os

def write_file(working_directory, file_path, content):
    # Resolve absolute paths
    base_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Ensure the target file is within the working directory
    if not target_path.startswith(base_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        # Write content to the file
        with open(target_path, "w", encoding="utf-8") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"