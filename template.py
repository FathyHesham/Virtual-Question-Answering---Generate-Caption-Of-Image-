# import libraries
import os # interacting with the operation system file
from pathlib import Path # import the class path from the pathlib medule for working file paths

# Building the structure
structure = [
    "main.py",
    "DockerFile",
    "config.yaml",
    "custom_logger/__init__.py",
    "custom_logger/custom_logging.py",
    "utils/__init__.py",
    "utils/config_loader.py",
    "model/__init__.py",
    "model/vqa_experiment.ipynb",
    "model/vqr_model.py",
    "application/__init__.py",
    "application/streamlit.py",
]

# Loop through each file path in the structure
for filepath in map(Path, structure):
    # Check if the file has a parent directory
    if filepath.parent:
        # Ensure the parent directory exists, create if it doesn't
        filepath.parent.mkdir(parents = True, exist_ok = True)
        print(f"Ensured directory exists: {filepath.parent}")
    # Check if the file does not exist
    if not filepath.exists():
        # Create the file
        filepath.touch()
        print(f"Created file: {filepath}")
    else:
        # Notify that the file already exists
        print(f"File already exists: {filepath}")
