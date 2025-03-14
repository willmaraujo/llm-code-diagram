import requests
import os

def load_prompt_template(filepath="../prompts/agent_project_analyst.txt"):
    """
    Reads the LLM prompt template from a file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def call_llm(prompt, model="llama3.1:8b"):
    """
    Sends the prompt to an LLM server and returns the response.
    """
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0,   # Makes output deterministic
        "top_p": 1,         # Uses full probability distribution
        "seed": 42          # Ensures repeatability (if supported)
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"] if response.status_code == 200 else None

def read_project_code(directory):
    """
    Reads all Python files in the given directory and returns a dictionary 
    with filenames as keys and file contents as values.
    """
    code_files = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Read only Python files
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code_files[file] = f.read()
    
    return code_files

def run():
    project_dir = "../toy-project"
    code_files = read_project_code(project_dir)

    # Combine all code files into a single string
    full_code = "\n\n".join([f"### {name} ###\n{content}" for name, content in code_files.items()])
    
    # Load the prompt template
    prompt_template = load_prompt_template()

    # Inject the code into the prompt template
    prompt = prompt_template.replace("{CODE_HERE}", full_code)

    print(prompt)

    output = call_llm(prompt)

    return output