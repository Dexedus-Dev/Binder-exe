import sys
import os
import subprocess
import threading

def extract_and_run():
    embedded_files = {
        'test.exe': b'... (byte data of test.exe) ...',
        'test2.exe': b'... (byte data of test2.exe) ...'
    }

    for filename, data in embedded_files.items():
        with open(filename, 'wb') as f:
            f.write(data)

    def run_program(exe_name):
        subprocess.Popen([exe_name])

    thread1 = threading.Thread(target=run_program, args=('test.exe',))
    thread2 = threading.Thread(target=run_program, args=('test2.exe',))

    thread1.start()
    thread2.start()

if __name__ == '__main__':
    extract_and_run()

