import os
import subprocess
from config import FILE_RUN_TIMEOUT

# defines function schema
schema_run_python_file = {
	"type": "function",
	"function": {
		"name": "run_python_file",
		"description": "runs a selected python file and returns the stdout or stderr",
		"parameters": {
			"type": "object",
			"properties" : {
				"file_path": {
					"type": "string",
					"description": "relative file path to the function you want to run"
				},
				"args": {
					"type": "array",
					"items": {"type": "string"},
					"description": "a list of strings in order of every parameter you want to add to the run command after the pre added python and target file"
     
				}
			}
		}
	}
}

def run_python_file(
	working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    # setup a try except block to catch any exceptions from external library
	try:
		# building the target path by getting absolute path first then joining the file path arg
		working_dir_absolute_path: str = os.path.abspath(working_directory)
		target_file: str = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
		
		# checks if the target file is in the working dir abs path
		if not os.path.commonpath([working_dir_absolute_path, target_file]) == working_dir_absolute_path:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		
		# simply checks whether our target file is a valid file and if it exists
		if not os.path.isfile(target_file):
			return f'Error: "{file_path}" does not exist or is not a regular file'

		# checks if file extensions is valid python file
		if not file_path.endswith(".py"):
			return f'Error: "{file_path}" is not a Python file'
		
		# builds the command to run
		command: list[str] = ["python", target_file]
		# adds any extra args provided
		if args:
			command.extend(args)

		# creates and runs the subprocess with all necassary args	
		file_process = subprocess.run(
			command,
			cwd=working_dir_absolute_path,
			capture_output=True,
			text=True,
			timeout=FILE_RUN_TIMEOUT	
		)

		output_string: str = ""
			
		# if return code is not 0 adds a new line to output string
		if file_process.returncode != 0:
			output_string += f"Process exited with code {file_process.returncode}\n"

		# if the stdout and stderr dont have any content adds new line to output string
		if file_process.stdout == "" and file_process.stderr == "":
			output_string += "No output produced\n"
		else:
			# adds the stdout and stderr content to output string	
			output_string += f"STDOUT:\n{file_process.stdout}\n"
			output_string += f"STDERR:\n{file_process.stderr}\n"
  
		return output_string
	except Exception as e:
		return f"Error: executing Python file: {e}"