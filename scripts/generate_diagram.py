import requests
import os
from read_code import read_project_code

def load_prompt_template(filepath="../prompts/llm-prompt.txt"):
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
        "stream": False
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"] if response.status_code == 200 else None

def main():
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

    # Define the output directory and file
    output_dir = "../diagrams"
    output_file = os.path.join(output_dir, "generated_diagram.mmd")

    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save Mermaid diagram
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Diagram saved as {output_file}")

if __name__ == "__main__":
    main()
