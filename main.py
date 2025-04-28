import os
import requests
import json
from datetime import datetime

# Settings
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3:8b"
PROJECT_PATH = "./toy-project/src/app"


def read_all_ts_files(base_path):
    code_blocks = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".ts"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    code_blocks.append(f"// FILE: {file_path}\n{content}")
    return "\n\n".join(code_blocks)


def build_prompt(code_content):
    with open('mermaid_flowchart_doc.md', 'r', encoding='utf-8') as f:
        mermaid_doc = f.read()

    prompt = f"""
You have access to the following documentation about Mermaid Flowchart syntax (DO NOT repeat, summarize, or modify it):

{mermaid_doc}

IMPORTANT EXAMPLES:

GOOD EXAMPLE (Correct Mermaid Diagram):
```mermaid
graph LR
subgraph AppModule
  AppComponent
  NavbarComponent
end

AppComponent --> NavbarComponent
NavbarComponent --> RouterModule

graph LR
subgraph AppModule
  AppModule --> BrowserModule
  AppRoutingModule --> AppRoutingModule
end
TasksModule --> TaskItemComponent
TasksModule --> TasksModule

Your task:

You are a system that analyzes Angular projects.

Your task is to read the following TypeScript files and extract a logical representation of the project dependencies between modules, components, and services.

You must **use the Mermaid syntax rules silently** (without explaining them again) and **directly generate** a valid Mermaid diagram.

IMPORTANT:
- Only use elements found exactly in the code.
- No invention, no modification, no assumptions.
- Inside subgraphs, list node names only (no arrows).
- All arrows (--> connections) must be outside subgraphs.
- The diagram must start with ```mermaid and end cleanly.
- Do not explain anything outside the code block.

Here are the TypeScript files:
---
{code_content}
---
"""
    return prompt.strip()


def send_prompt_to_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "temperature": 0, # makes the model more consistent and less creative
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
    response.raise_for_status()

    full_response = ""
    for line in response.iter_lines():
        if line:
            json_line = line.decode('utf-8')
            try:
                parsed = json.loads(json_line)
                if 'message' in parsed and 'content' in parsed['message']:
                    full_response += parsed['message']['content']
            except json.JSONDecodeError:
                pass  # Ignore any broken lines

    return full_response

def save_mermaid_diagram(content, output_dir="diagrams"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"diagram-{timestamp}.mmd"
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Mermaid diagram saved to {output_path}")


if __name__ == "__main__":
    print("Reading project files...")
    code_content = read_all_ts_files(PROJECT_PATH)

    print("Building the prompt...")
    prompt = build_prompt(code_content)

    print("Sending prompt to Llama 3...")
    result = send_prompt_to_ollama(prompt)

    save_mermaid_diagram(result)