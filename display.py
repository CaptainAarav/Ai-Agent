import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

# initialised rich console
console = Console()
# adds the top title bar when using agent
console.rule("[bold]AI Coding Agent")

# shows spinning loading bar in console
def show_thinking():
    return console.status("Thinking...")

# shows different calling function print statements depending on verbose arg
def show_calling_function(name, args=None, verbose=False):
    if verbose:
        print(f" - Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

# displays result of tool if verbose arg True
def show_tool_result(content, verbose=False):
    if verbose:
        print(f"-> {content}")

# shows full formatted response from agent
def show_response(response, user_prompt, verbose=False):
	# formats original md from agent into a renderable md in terminal
    formatted_response = Markdown(response.choices[0].message.content)

	# when verbose also adds table with extra details
    if verbose:
		# displays user prompt
        console.print(f"User Prompt: [bold white]{user_prompt}[/bold white]", justify="center")

		# creates a rich table that has all stats about tokens
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
		# displays the table
        console.print(table, justify="center")

	# displays the agent response with box and title
    console.print(Panel(formatted_response, title="[bold white]Response[/bold white]", border_style="cyan"))

# exits program when agent loop is exceeded
def show_loop_exceeded():
    print("agent loop iterations exceeded")
    sys.exit(1)