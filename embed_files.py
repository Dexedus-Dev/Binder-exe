import os
import sys

def get_embedded_file_data(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    return file_data

def generate_embedded_files_dict(file_paths):
    embedded_files = {}
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        file_data = get_embedded_file_data(file_path)
        embedded_files[file_name] = file_data
    return embedded_files

def generate_loader_file(embedded_files):
    loader_code = "embedded_files = {\n"
    for file_name, file_data in embedded_files.items():
        loader_code += f"    '{file_name}': b'{file_data}',\n"
    loader_code += "}\n"
    
    with open("loader.py", "w") as loader_file:
        loader_file.write(loader_code)
    print("loader.py has been generated successfully.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <path_to_first_exe> <path_to_second_exe>")
        sys.exit(1)

    file = sys.argv[1].strip('"')
    file2 = sys.argv[2].strip('"')

    file_paths = [
        file,
        file2
    ]

    embedded_files = generate_embedded_files_dict(file_paths)
    generate_loader_file(embedded_files)
