import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  # Import types for message formatting

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Ensure a prompt is provided
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command-line argument.")
    sys.exit(1)

# Extract command-line arguments
user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv  # Check if verbose flag is present

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Create a list of messages with roles
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Generate response from Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

# Print the model's response
print(response.text)

# Print verbose output if the flag is enabled
if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")