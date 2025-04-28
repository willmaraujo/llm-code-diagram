import os
import requests
import json

# Settings
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3:8b"
PROJECT_PATH = "./toy-project/src/app"  # Adjust this if needed


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
    prompt = f"""
You are a system that analyzes Angular projects.

Your task is to read the following TypeScript files and extract a logical representation of the project dependencies between modules, components, and services.

Please output the dependency graph using **Mermaid syntax**.

---
{code_content}
---

Please generate the Mermaid diagram showing how modules, components, and services are connected.
"""
    return prompt.strip()


def send_prompt_to_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
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


if __name__ == "__main__":
    print("Reading project files...")
    code_content = read_all_ts_files(PROJECT_PATH)

    print("Building the prompt...")
    prompt = build_prompt(code_content)

    print("Sending prompt to Llama 3...")
    result = send_prompt_to_ollama(prompt)

    print("\n--- Mermaid Diagram Output ---\n")
    print(result)