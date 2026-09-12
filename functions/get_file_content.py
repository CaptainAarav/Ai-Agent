import os
from config import FILE_READ_CHAR_LIMIT

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets a files content and returns a string of it",
        "parameters": {
				"type": "object",
				"properties": {
					"file_path": {
						"type": "string",
						"description": "Relative file path to the file you need to access"
					},
				},
            },
        },
},

def get_file_content(working_directory: str, file_path: str) -> str:
	# setup a try except block to catch any exceptions from external library
	try:
		# building the target path by getting absolute path first then joining the file path arg
		working_dir_absolute_path: str = os.path.abspath(working_directory)
		target_file: str = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
		
		# checks if the target file is in the working dir abs path
		if not os.path.commonpath([working_dir_absolute_path, target_file]) == working_dir_absolute_path:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
		
		# simply checks whether our target file is a valid file
		if not os.path.isfile(target_file):
			return f'Error: File not found or is not a regular file: "{file_path}"'

		# opens the target file with read
		with open(target_file, "r") as file:
			file_content: str = file.read(FILE_READ_CHAR_LIMIT)
			# runs a check to see if we had to truncate the file
			if file.read(1):
				file_content += f'[...File "{file_path}" truncated at {FILE_READ_CHAR_LIMIT} characters]'

			return file_content		
	except Exception as e:
		return f"Error: {e}"
 