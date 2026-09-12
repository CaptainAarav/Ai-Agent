import json
from collections.abc import Callable
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# maps each function str to the callable function
function_map: dict[str: Callable[..., str]] = {
	"get_files_info": get_files_info,
	"get_file_content": get_file_content,
	"write_file": write_file,
	"run_python_file": run_python_file,
}

def call_function(tool_call, working_directory: str) -> dict:
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
    
    function_args["working_directory"] = working_directory 
    
	# result from calling function
    result = function_map[tool_call.function.name](**function_args)
    
	# returns the tool call details
    return {
		"role": "tool",
		"tool_call_id": tool_call.id,
		"content": result
	}