import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_files(paths):
    all_files = []
    for path in paths:
        if os.path.isdir(path):
            all_files += _collect_files(path)
        elif os.path.isfile(path):
            if path.endswith('.py') or path.endswith('.ipynb'):
                all_files.append(path)
    
    if not all_files:
        print("No applicable files found.")
    return all_files

def _collect_files(directory):
    applicable_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') or file.endswith('.ipynb'):
                applicable_files.append(os.path.join(root, file))
        for dir in dirs:
            applicable_files += _collect_files(dir)
    return applicable_files

def _run_subprocess(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logging.error(f"Error running command {' '.join(command)}: {result.stderr}")
            return []
        return result.stdout.splitlines()
    except Exception as e:
        logging.exception(f"Exception running command {' '.join(command)}: {e}")
        return []