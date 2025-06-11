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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons."""

# Ensure a prompt is provided
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command-line argument.")
    sys.exit(1)

# Define the Function Schema
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

# Define the available functions for the AI to call
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
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