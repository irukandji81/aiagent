import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  # Needed for message formatting and system prompt config

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Define system prompt
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

# Ensure a prompt is provided
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command-line argument.")
    sys.exit(1)

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
    config=types.GenerateContentConfig(system_instruction=system_prompt)
)

# Print verbose output first if enabled
if verbose:
    print(f"User prompt: {user_prompt}")

# Print model response
print(response.text)

# Print token usage if verbose
if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")