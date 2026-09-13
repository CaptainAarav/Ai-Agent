# CLI AI Agent

A very simple CLI AI Agent, If you have used Claude Code, Codex or Opencode you'll understand what it is, written in python3. I have left it for now because of how big and time consuming it was getting but, I hope to come back and add some more features I had planned or, even rebuild it in C, Go or typescript. I also used rich, os, sys, json, argparse, dotenv, openai, requests libraries.

### Usefull Documentation
- [rich Documentation](https://rich.readthedocs.io/en/stable/introduction.html)
- [argparse Documentation](https://docs.python.org/3/library/argparse.html)
- [OpenAi SKD Documentation](https://developers.openai.com/api/reference/python)
- [requests Documentation](https://requests.readthedocs.io/en/latest/user/quickstart/)
- [os Documentation](https://docs.python.org/3/library/os.html)
- [subprocess Documentation](https://docs.python.org/3/library/subprocess.html#subprocess.run)


**WARNING: WHILE THE AGENT HAS BASIC PROTECTION IN IT I CAN NOT PROMISE YOU ANYTHING, USE AT YOUR OWN RISK**

## Current Features
- List and read directories
- Read files
- Write files
- Execute **python** files
- Web search

## Future Maybe Features
- A persistant conversation loop instead of seperate command runs
- Global install into your PATH so it can be callable like ls, git, cd
- Persistant memory using JSON that any different chat can access and write to
- Streaming response so you can get live updating text in terminal

## Contribution
If you want to contribute to the project and add any of those future features for me or even some of your own, I am totally happy for you to. Just create a pull request with your changes, I will take a peak at them and make sure they don't break anything and merge them if they're fine and add you as a contributer

## Example Usage
```
aaravsahni@Aaravs-Macintosh Ai Agent % uv run main.py "My bugs.py file is not working correctly, can you fix it?" --allow_commands
───────────────────────────────────────────────────────────────────────── AI Coding Agent ─────────────────────────────────────────────────────────────────────────
 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: write_file
 - Calling function: run_python_file
╭─────────────────────────────────────────────────────────────────────────── Response ────────────────────────────────────────────────────────────────────────────╮
│ I have fixed the issues in your bugs.py file. Here are the changes made:                                                                                        │
│                                                                                                                                                                 │
│  1 Corrected the median calculation to properly return the average of the two middle numbers when the list has an even number of elements.                      │
│  2 Updated the add method in the RunningTotal class to correctly accumulate the total instead of resetting it.                                                  │
│  3 Ensured that the vowel counting is case-insensitive.                                                                                                         │
│                                                                                                                                                                 │
│ After making these changes, I ran the file, and it executed successfully with the following output:                                                             │
│                                                                                                                                                                 │
│                                                                                                                                                                 │
│  Median of [1, 2, 3, 4]: 2.5                                                                                                                                    │
│  Median of [5, 3, 1]: 3                                                                                                                                         │
│  Vowels in 'HELLO': 2                                                                                                                                           │
│  Running total after adding 5, 3, 2: 10                                                                                                                         │
│  Deduplicate [1, 2, 2, 3, 1]: [1, 2, 3]                                                                                                                         │
│                                                                                                                                                                 │
│                                                                                                                                                                 │
│ Your bugs.py file is now working correctly! If you need any further assistance, feel free to ask.                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
aaravsahni@Aaravs-Macintosh Ai Agent %
```

## How to setup for yourself and usage

First clone the repo onto your system, you can do this with a simple `git clone https://github.com/CaptainAarav/Ai-Agent.git` 

After it is cloned in your Ai Agent folder run the `uv sync` command **this is requried**, it will initialise the project.

Once you have it you'll need to **create a .env file** this is cruical, the agent will not work without it. Heres an example file:
```
API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

API_KEY is your ai api key, this project uses the openai python SDK so any provider compatible with that can be easily added e.g openai, openrouter, gemini openai compatible layer.

If you are going to use open ai  you simply just have to provide your api key in the .env **if you are using another provider that again is compatible** you will have to set a base url variable in `config.py` like below:

`BASE_URL={your providers url}`

If you want to use providers like anthropic who have their own distinct API are not compatible with openai SDK therefore if you want to use them you will have to adjust the file to use their SDK and api usage syntax.

If you want web search capabilities you will have to add a tavily api key, their free tier includes 1000 queries a month which should last for a while. Create a tavily account at [tavily.com](https://www.tavily.com). **This is optional**

Keep in mind i have not added protection and so if you dont provide a key and the agent trys to use web search it will keep running into exceptions so you will have to specifically tell it not to use web search.

Now you simple run `uv run main.py {your prompt goes here}` 

**keep in mind** this requires the files that you want it to edit to be in the Ai Agents directory, I do plan to add features to stop needing this in the future.

When you run the main.py file there are two extra params you can pass in:
- `--verbose` This provides more details when the agent is running like token usage and more details about function calling
- `--allow_commands` This will stop the allow function messages when the agent tries to run a destructive function e.g writing to file

## Editing config

There is a `config.py` file that contains the config you can play around with, heres what it looks like:
```
BASE_URL=""
MODEL="gpt-4o-mini"
FILE_READ_CHAR_LIMIT=10000
WEB_SEARCH_MAX_RESULTS=5
FILE_RUN_TIMEOUT=30
AGENT_LOOP_LIMIT=20
SYSTEM_PROMPT="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, create a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Search the web for current information

When a user asks about the codebase, a specific file, or how something works,
ALWAYS investigate by calling get_files_info and/or get_file_content BEFORE
answering never answer from assumption or general knowledge alone.

After fixing a bug in a file, always verify the fix by running the file
(using run_python_file) before reporting success to the user. If the file
has no obvious entry point to run, explain what you were unable to verify.

NEVER ask a follow up question execute functions directly instead.

All paths you provide should be relative to the working directory. You do not
need to specify the working directory in your function calls as it is
automatically injected for security reasons.

When calling any function, use the EXACT parameter names shown below, with no
extra characters (such as = or quotes) appended to the name itself. For example:

Correct call to write_file:
  write_file(file_path="main.py", content="print('hello')")

Incorrect call (never do this):
  write_file(file_path="main.py", content_="print('hello')")

Correct call to get_file_content:
  get_file_content(file_path="main.py")

Correct call to run_python_file:
  run_python_file(file_path="main.py", args=["3", "5"])
"""
```

Heres what each value is:
- `BASE_URL` A base url for your api provider only required if you're using any provider other than openai that is compatible with the SDK

- `MODEL` The Ai model you want to use by default I have it on gpt 4o mini but you can change this to anything else

- `FILE_READ_CHAR_LIMIT` In the function where the agent can read a certain file, this const sets the max amount of characters the agent can read from a single file this is to make sure it doenst read a MASSIVE file and use lots of tokens.

- `WEB_SEARCH_MAX_RESULTS` This sets the maximum web results there will be in the response from the tavily API

- `FILE_RUN_TIMEOUT` A const that puts a cap on how long a file can take to run in the `run_python_file.py` file

- `AGENT_LOOP_LIMIT` This max amount of iterations the agent loop can have this is to stop the agent from looping for hundreds or thousands of times and eating through usage

- `SYSTEM_PROMPT` The system prompt provided to the agent before the users prompt, I have already fine tuned this to work most of the time although you can change it to change your resulsts

## How It works

For my dev people out there, heres a overview on each file and what it's doing. I have added comments to all files with more specific wording on what each line is doing.

### Project Structure
```
Ai-Agent/
├── main.py                    # entry point(argument parsing, agent loop calling)
├── agent.py                   # the core agent loop
├── display.py                 # all rich terminal output
├── config.py                  # constants and system prompt
├── available_functions.py     # collects all tool schemas into one list
├── functions/
│   ├── call_function.py       # maps function names to real functions and calls using run python file
│   ├── get_files_info.py      # lists a directory's contents
│   ├── get_file_content.py    # reads a file's contents (with a char limit from config)
│   ├── write_file.py          # writes/overwrites a file
│   ├── run_python_file.py     # runs a Python file as a subprocess (with a timeout from config)
│   └── web_search.py          # searches the web and returns results via the Tavily API
├── .env.example                # template environment variables
├── .gitignore
├── .python-version             # pins the python version for uv
├── pyproject.toml
├── uv.lock
└── README.md                 # what you're reading
```

### Security

To make the agent secure I have implemented:
- path sandboxing
- working_directory is never set by agent it is externally injected by us
- confirmation prompts before any destructive commands are run
- timeout on subproccess execution

### Error Handling and redunency

Every tool returns a string rather than raising exceptions so that malformed tools are caught and fed back to the model instead of crashing the entire program, every tool is wrapped in try except blocks to catch and gracefully handle Exceptions.

## Limitations

There are a few limitations I have found, some fixiable in future updates and some not:
- Latex is not rendered
- One shot answer its not persistant
- Occasional incorrect function calls from agent
- Requires files to be in the Agent folder
- No persistant memory
- Not production level hardened(no rate limiting, no protection against malicious actors)