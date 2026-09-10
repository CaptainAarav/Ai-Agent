import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown  

# loading the api key from .env
load_dotenv()
api_key: str = os.environ.get("OPENROUTER_API_KEY")

# checks if the api key was found
if api_key is None:
    raise RuntimeError("api key could not be loaded")

# sets up console object for printing markdown
console = Console()

# initialise a new argparse parser so we can use the run commands arguments
parser = argparse.ArgumentParser(description="ai coding agent")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# set the user prompt using argument parser
user_prompt = args.user_prompt

# a new messages list that will store the entire conversations messages
messages = [
    {"role": "user", "content": user_prompt},
]

# create a new client that talks to openrouter api
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# creates a new chat completions request with our user prompt
response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)

formatted_response = Markdown(response.choices[0].message.content)

# checks whether --verbose arg was added
if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Model used: {response.model}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}") 
    
# prints the formatted md using rich library
console.print(formatted_response)