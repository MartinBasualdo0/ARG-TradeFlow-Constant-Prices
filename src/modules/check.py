import os

# Function to check and create directories if needed
def check_and_create_directories():
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
        print("Created 'downloads' folder.")
    if not os.path.exists("output"):
        os.mkdir("output")
        print("Created 'output' folder.")

# Function to check if api_key.py exists
def check_api_key_file():
    if not os.path.exists("api_key.py"):
        print("WARNING: 'api_key.py' file is missing. Please create it with your API key.\Feel free to read the README.md if you need help")
        exit(1)  # Exit the program with an error code
    else: 
        print("All checks passed")
    
