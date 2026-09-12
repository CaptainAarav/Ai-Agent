import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "overwrites all the content in a selected file",
        "parameters": {
            "type": "object",
            "properties": {
				"file_path": {
					"type": "string",
					"description": "a relative file path to the file you want to write to"
				},
				"content": {
					"type": "string",
					"description": "the content you want to overwrite the file with"
				}
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    # setup a try except block to catch any exceptions from external library
	try:
		# building the target path by getting absolute path first then joining the file path arg
		working_dir_absolute_path: str = os.path.abspath(working_directory)
		target_file: str = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
		
		# checks if the target file is in the working dir abs path
		if not os.path.commonpath([working_dir_absolute_path, target_file]) == working_dir_absolute_path:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
		
		# makes sure target file is a file and not a dir
		if os.path.isdir(target_file):
			return f'Error: Cannot write to "{file_path}" as it is a directory'

		# checks if the target files parent directorys exist, if not it will create them for us
		os.makedirs(os.path.dirname(target_file), exist_ok=True)

		# opening the target file in write mode
		with open(target_file, "w") as file:
			# writing content to file
			file.write(content)
			return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f"Error: {e}"