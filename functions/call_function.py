import json
from collections.abc import Callable
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.web_search import web_search

# maps each function str to the callable function
function_map: dict[str: Callable[..., str]] = {
	"get_files_info": get_files_info,
	"get_file_content": get_file_content,
	"write_file": write_file,
	"run_python_file": run_python_file,
    "web_search": web_search,
}

DESTRUCTIVE_FUNCTIONS = {"write_file", "run_python_file"}

def call_function(tool_call, working_directory: str, allow_commands: bool = False) -> dict:
	# grabs function name and args from tool call
    function_name: str = tool_call.function.name
	# uses short circuiting to use empty dict if tool call args are not there 
    function_args = json.loads(tool_call.function.arguments or "{}")
    
	# checks that tool call function is in the defined function map
    if tool_call.function.name not in function_map:
        return {
			"role": "tool",
			"tool_call_id": tool_call.id,
			"content": f"Error: Unknown function: {function_name}",
		} 
	
    if tool_call.function.name in DESTRUCTIVE_FUNCTIONS and not allow_commands:
        confirm = input(f"WARNING: Agent wants to run '{function_name}' with args {function_args} in '{working_directory}'. Allow? [y/N] ")
        if confirm.strip().lower() != "y":
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"User declined to run {function_name}.",
            }
    
    function_args["working_directory"] = working_directory 
    
	# result from calling function
    result = function_map[tool_call.function.name](**function_args)
    
	# returns the tool call details
    return {
		"role": "tool",
		"tool_call_id": tool_call.id,
		"content": result
	}