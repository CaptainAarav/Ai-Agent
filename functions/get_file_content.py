import os

def get_file_content(working_directory: str, file_path: str) -> str:
	# setup a try except block to catch any exceptions from external library
	try:
		if not os.path.commonpath([working_directory, file_path]) == working_directory:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
		
		if not os.path.isdir(file_path):
			return f'Error: File not found or is not a regular file: "{file_path}"'
 