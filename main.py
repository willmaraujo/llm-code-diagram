import os
import requests
import json
from datetime import datetime

# Settings
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "deepseek-r1:14b"
PROJECT_PATH = "./toy-project/src/app"
MERMAID_DOC_PATH = "mermaid_flowchart_doc.md"
DIAGRAM_OUTPUT_DIR = "diagrams"
MAX_ATTEMPTS = 5

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
- Use only the syntax: NodeA --> NodeB or NodeA -->|Label|NodeB
- DO NOT use |>, |>B[Node], or any invalid combinations.
- Only use |Label| syntax between nodes.
- If you use invalid syntax like |>, it will be considered wrong.
- Keep the graph strictly compliant with Mermaid Flowchart syntax.

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

Your ONLY possible outputs are:

- If the diagram is fully syntactically correct, reply with exactly this word: VALID
- If the diagram has syntax errors, list the errors clearly.

IMPORTANT:
- Do not explain anything.
- Do not compliment the diagram.
- Do not say anything else except either VALID or a list of syntax errors.
- Any extra text will be considered an invalid response.

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


        # Additional manual syntax check for forbidden patterns
        if '|>' in self.diagram_text:
            return "ERROR: Forbidden syntax '|>' detected."
        return full_response.strip()

class CorrectionAgent:
    def __init__(self, invalid_diagram: str, validation_errors: str, original_prompt: str = None):
        self.invalid_diagram = invalid_diagram
        self.validation_errors = validation_errors
        self.original_prompt = original_prompt

    def build_correction_prompt(self) -> str:
        prompt = f"""
You are a Mermaid diagram correction agent.

Your task is to fix the syntax errors in a Mermaid diagram.

You will receive:
- A Mermaid diagram that contains errors
- A list of those errors
- The original prompt that generated the diagram (for context)
- Do NOT use reserved Mermaid keywords like `end` as node IDs. Replace them with safe alternatives like `endNode`.

Please fix the diagram to make it syntactically valid.
Do not explain anything. Output only the corrected Mermaid diagram between ```mermaid and ```.

Errors:
{self.validation_errors}

Invalid Diagram:
{self.invalid_diagram}

Original Prompt:
{self.original_prompt or 'N/A'}
"""
        return prompt.strip()

    def correct_diagram(self) -> str:
        prompt = self.build_correction_prompt()

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
                json_line = line.decode("utf-8")
                try:
                    parsed = json.loads(json_line)
                    if "message" in parsed and "content" in parsed["message"]:
                        full_response += parsed["message"]["content"]
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
    # Step 1: Generate the diagram
    print("Generating diagram...")
    generator = DiagramGeneratorAgent(PROJECT_PATH, MERMAID_DOC_PATH)
    prompt = generator.build_prompt(generator.read_all_ts_files())
    diagram = generator.generate_diagram()
    print("Diagram generated.\n")

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        print(f"\nAttempt {attempt} of {MAX_ATTEMPTS}")
        print("Checking syntax...\n")
        checker = SyntaxCheckerAgent(diagram)
        syntax_result = checker.check_syntax()

        if "VALID" in syntax_result:
            print("Diagram is valid! Saving...\n")
            save_mermaid_diagram(diagram)
            break
        else:
            print("Diagram is invalid:")
            print(syntax_result)

            if attempt == MAX_ATTEMPTS:
                print("Max attempts reached. Diagram could not be validated.")
                break

            print("Attempting correction...")
            corrector = CorrectionAgent(diagram, syntax_result, prompt)
            diagram = corrector.correct_diagram()

        attempt += 1
