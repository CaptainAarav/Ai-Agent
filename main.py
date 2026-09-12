import os
import argparse
import json
from dotenv import load_dotenv
from config import MODEL, BASE_URL, SYSTEM_PROMPT
from openai import OpenAI
from available_functions import available_functions
from functions.call_function import call_function
from rich.console import Console
from rich.markdown import Markdown  
from rich.panel import Panel
from rich.table import Table

# loading the api key from .env
load_dotenv()
api_key: str = os.environ.get("API_KEY")

# checks if the api key was found
if api_key is None:
    raise RuntimeError("api key could not be loaded")

# sets up console object for printing markdown and add a title bar to top of terminal
console = Console()
console.rule("[bold]AI Coding Agent")

# initialise a new argparse parser so we can use the run commands arguments
parser = argparse.ArgumentParser(description="ai coding agent")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# set the user prompt using argument parser
user_prompt = args.user_prompt

# a new messages list that will store the entire conversations messages
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_prompt},
]

# create a new client that talks to openrouter api
client = OpenAI(
    api_key=api_key
)

# creates a new chat completions request with our user prompt and using rich console to show a loading spinning circle
with console.status("Thinking..."):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        tool_call_result = call_function(tool_call, args.verbose)

        if not tool_call_result["content"]:
            raise Exception("tool call returned no content")
        
        if args.verbose:
            print(f"-> {tool_call_result["content"]}")

else:
    # formats response content to md
    formatted_response = Markdown(response.choices[0].message.content)
    
    # checks whether --verbose arg was added
    if args.verbose:
        # prints all the extra details with formatting using rich
        console.print(f"User Prompt: [bold white]{user_prompt}[/bold white]", justify="center")
        table = Table(title="Stats", expand=False)
        table.add_column("Model")
        table.add_column("Prompt Tokens", justify="right")
        table.add_column("Response Tokens", justify="right")
        table.add_column("Total Tokens", justify="right")
        table.add_row(
            response.model,
            str(response.usage.prompt_tokens),
            str(response.usage.completion_tokens),
            str(response.usage.total_tokens),
        )
        console.print(table, justify="center")

    # prints response content even if --verbose is not set
    console.print(Panel(formatted_response, title="[bold white]Response[/bold white]", border_style="cyan"))