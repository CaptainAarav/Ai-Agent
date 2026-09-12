import os

# defines function schema
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
	# setup a try except block to catch any exceptions from external library
	try:
		# building the target path by getting absolute path first then joining the directory arg
		working_dir_absolute_path: str = os.path.abspath(working_directory)
		target_dir: str = os.path.normpath(os.path.join(working_dir_absolute_path, directory))
		
		# checks if the target dir is in the working dir abs path to stop the agent from accessing dirs we don't want it to
		if not os.path.commonpath([working_dir_absolute_path, target_dir]) == working_dir_absolute_path:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		
		# simply checks whether our target dir is a valid directory
		if not os.path.isdir(target_dir):
			return f'Error: "{directory}" is not a directory'

		# builds a files list by mapping through all the files in our target dir and using another func to make dicts of each file with relevant data
		files: list[dict] = list(map(lambda f: get_file_info(f, target_dir), os.listdir(target_dir)))

		# generator expression that builds the return string
		return "\n".join(
			f"- {file["name"]}: file_size={file["size"]}, is_dir={file["is_dir"]}"
			for file in files
		)
	except Exception as e:
		return f"Error: {e}"
    
def get_file_info(file: str, base_path: str) -> dict[str: str | bool] | str:
	# building the file target path, required for the os library functions
	target_path: str = os.path.join(base_path, file)
	# try except block to catch external library exceptions
	try:  
		return {
			"name": file,
			"size": f"{os.path.getsize(target_path)} bytes",
			"is_dir": os.path.isdir(target_path)
		}
	except Exception as e:
		return f"Error: {e}"