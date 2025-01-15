import os 
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s')

from pathlib import Path
import os
import logging

# List of files to create
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "App.py",
    "research/trials.iypnb",
    "test.py"
]

# Iterate through the file paths
for filepath in list_of_files:
    filepath = Path(filepath)  
    filedir = filepath.parent  
    filename = filepath.name   

    if filedir != "":
        filedir.mkdir(parents=True, exist_ok=True)  
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    # Check if the file exists or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()  # Create an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
