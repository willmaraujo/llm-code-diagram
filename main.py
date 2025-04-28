import os
import requests
import json
from datetime import datetime

# Settings
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3:8b"
PROJECT_PATH = "./toy-project/src/app"
MERMAID_DOC_PATH = "mermaid_flowchart_doc.md"
DIAGRAM_OUTPUT_DIR = "diagrams"

class DiagramGeneratorAgent:
    def __init__(self, project_path, mermaid_doc_path):
        self.project_path = project_path
        self.mermaid_doc_path = mermaid_doc_path

    def read_all_ts_files(self):
        code_blocks = []
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".ts"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        code_blocks.append(f"// FILE: {file_path}\n{content}")
        return "\n\n".join(code_blocks)

    def build_prompt(self, code_content):
        with open(self.mermaid_doc_path, 'r', encoding='utf-8') as f:
            mermaid_doc = f.read()

        prompt = f"""
You have access to the following documentation about Mermaid Flowchart syntax (DO NOT summarize or modify it):

---
{mermaid_doc}
---

IMPORTANT EXAMPLES:

GOOD EXAMPLE:
```mermaid
graph LR
subgraph AppModule
  AppComponent
  NavbarComponent
end

AppComponent --> NavbarComponent
NavbarComponent --> RouterModule
```

BAD EXAMPLE:
```mermaid
graph LR
subgraph AppModule
  AppModule --> BrowserModule
  AppRoutingModule --> AppRoutingModule
end
TasksModule --> TaskItemComponent
TasksModule --> TasksModule
```

Your task:
You are a system that analyzes Angular projects.

Your job is to read the TypeScript files below and extract a correct dependency graph, using valid Mermaid syntax.

STRICT RULES:
- Follow the style of the GOOD EXAMPLE.
- Avoid mistakes seen in the BAD EXAMPLE.
- Use exact names from the TypeScript code.
- Inside each subgraph, list only node names (no arrows).
- Declare all dependencies (--> connections) outside subgraphs.
- The diagram must start with ```mermaid and end cleanly.
- Do NOT explain anything outside the diagram.

Here are the TypeScript files:
---
{code_content}
---
"""
        return prompt.strip()

    def generate_diagram(self):
        code_content = self.read_all_ts_files()
        prompt = self.build_prompt(code_content)

        payload = {
            "model": MODEL_NAME,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}]
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
                    pass

        return full_response


class SyntaxCheckerAgent:
    def __init__(self, diagram_text):
        self.diagram_text = diagram_text

    def build_syntax_check_prompt(self):
        prompt = f"""
You are a Mermaid syntax validator.

Your task:
- Carefully read the following Mermaid diagram.
- If the syntax is fully valid, simply reply exactly: VALID
- If the syntax is invalid, list the syntax errors you detect.
- Do not modify or correct the diagram.

Diagram to validate:
```mermaid
{self.diagram_text}
```
"""
        return prompt.strip()

    def check_syntax(self):
        prompt = self.build_syntax_check_prompt()

        payload = {
            "model": MODEL_NAME,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}]
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
                    pass

        return full_response.strip()


def save_mermaid_diagram(content, output_dir=DIAGRAM_OUTPUT_DIR):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"diagram-{timestamp}.mmd"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Mermaid diagram saved to {output_path}")


if __name__ == "__main__":
    generator = DiagramGeneratorAgent(PROJECT_PATH, MERMAID_DOC_PATH)
    diagram = generator.generate_diagram()

    checker = SyntaxCheckerAgent(diagram)
    syntax_result = checker.check_syntax()

    if syntax_result == "VALID":
        save_mermaid_diagram(diagram)
    else:
        print("\nSyntax Errors Found:")
        print(syntax_result)
