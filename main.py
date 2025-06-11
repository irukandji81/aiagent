import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  # Needed for message formatting and system prompt config

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Define system prompt
system_prompt = """You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons."""

# Ensure a prompt is provided
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command-line argument.")
    sys.exit(1)

# Define the Function Schemas
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

# Define the available functions for the AI to call
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Extract command-line arguments
user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Build the conversation history (for now, it's just one user message)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Generate response using system prompt
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    )
)

if response.function_calls:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)

# Print verbose output first if enabled
if verbose:
    print(f"User prompt: {user_prompt}")

# Print model response
print(response.text)

# Print token usage if verbose
if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")