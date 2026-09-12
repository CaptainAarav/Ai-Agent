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
    args = parser.parse_args()

    # initialised the ai client and creates the messages list
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": args.user_prompt},
    ]

    # runs the agent loop
    run_agent(client, messages, args.user_prompt, verbose=args.verbose)

# makes sure that this file is only run not imported
if __name__ == "__main__":
    main()