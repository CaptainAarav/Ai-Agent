import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from config import SYSTEM_PROMPT
from agent import run_agent

def main():
    # loads and sets our api key
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if api_key is None:
        raise RuntimeError("api key could not be loaded")

    # sets up argparse parser so we can get the run commands arguments 
    parser = argparse.ArgumentParser(description="ai coding agent")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--allow_commands", action="store_true", help="Enables the use of destructive commands without permission. USE WITH CAUTION!")
    args = parser.parse_args()
    
    # gets working dir from where user ran command
    working_directory: str = os.getcwd()

    # initialised the ai client and creates the messages list
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": args.user_prompt},
    ]

    # runs the agent loop
    run_agent(client, messages, args.user_prompt, working_directory, verbose=args.verbose, allow_commands=args.allow_commands)

# makes sure that this file is only run not imported
if __name__ == "__main__":
    main()