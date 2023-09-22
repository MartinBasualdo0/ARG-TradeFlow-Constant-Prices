import os
from rich import print

# Function to check and create directories if needed
def check_and_create_directories():
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
        print("[bold green]Created 'downloads' folder.[/bold green]")
    if not os.path.exists("output"):
        os.mkdir("output")
        print("[bold green]Created 'output' folder.[/bold green]")

# Function to check if api_key.py exists
def check_api_key_file():
    if not os.path.exists("api_key.py"):
        print("[bold red]WARNING: 'api_key.py' file is missing. Please create it with your API key.[/bold red]")
        print("Feel free to read the README.md if you need help")
        exit(1)  # Exit the program with an error code
    else:
        print("[bold green]All checks passed[/bold green]")



