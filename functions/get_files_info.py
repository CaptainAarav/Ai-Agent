import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
	try:
		working_dir_absolute_path: str = os.path.abspath(working_directory)
		target_dir: str = os.path.normpath(os.path.join(working_dir_absolute_path, directory))
		
		if not os.path.commonpath([working_dir_absolute_path, target_dir]) == working_dir_absolute_path:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		
		if not os.path.isdir(target_dir):
			return f'Error: "{directory}" is not a directory'

		files: list[dict] = list(map(lambda f: get_file_info(f, target_dir), os.listdir(target_dir)))

		return_string: str = ""
		for file in files:
			return_string += f"- {file["name"]}: file_size={file["size"]}, is_dir={file["is_dir"]}\n"
   
		return return_string
	except Exception as e:
		return f"Error: {e}"
    
def get_file_info(file: str, base_path: str) -> dict[str: str | bool] | str:
	target_path: str = os.path.join(base_path, file)
	try:  
		return {
			"name": file,
			"size": f"{os.path.getsize(target_path)} bytes",
			"is_dir": os.path.isdir(target_path)
		}
	except Exception as e:
		return f"Error: {e}"