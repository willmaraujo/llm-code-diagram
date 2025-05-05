# LLM Code Diagram Generator

This project uses a locally running Large Language Model (LLM) with [Ollama](https://ollama.com/) to analyze an Angular project and automatically generate dependency diagrams in [Mermaid](https://mermaid.js.org/) syntax.

## 🚀 Getting Started

### Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Run the Application

To build and start the application, simply run:

```bash
docker-compose up --build
```

This will:

1. Start the Ollama server in the container.
2. Pull the model defined in the `MODEL_NAME` environment variable.
3. Execute the Python application to analyze the Angular code and generate the Mermaid diagram.

## ⚙️ Configuration

You can change the LLM model by editing the `MODEL_NAME` value inside `docker-compose.yml`:

```yaml
environment:
  - MODEL_NAME=qwen3:8b
```

Make sure the model is supported by Ollama and has been pulled or will be pulled automatically at startup.

## 📁 Project Structure

- `toy-project/`: Add any Angular project here. The tool will analyze all `.ts` files recursively from this folder.
- `diagrams/`: The Mermaid diagram output is saved here (as a `.mmd` file).

## 📋 Output

The diagram will be saved in the `diagrams/` folder as a `.mmd` file that can be visualized using any Mermaid-compatible viewer like [MermaidLive](https://mermaid.live/)

## 📌 Notes

- This project runs the LLM using CPU by default. You can enable GPU support if your system supports it.
- Logs from Ollama are currently disabled to make the output cleaner. You can enable them by modifying the `entrypoint.sh`.

## 🧠 Example

You can test the tool by placing any small or medium Angular project inside the `toy-project/` folder and rerunning:

```bash
docker-compose up --build
```

The system will regenerate the diagram for the new codebase.

### Sample Output

```bash
diagram-generator-1  | Waiting for Ollama to be ready...
diagram-generator-1  | Model qwen3:8b already pulled.
diagram-generator-1  | Starting application...
diagram-generator-1  | Generating diagram. This may take a moment depending on your system resources...
diagram-generator-1  | Diagram generated
diagram-generator-1  | Checking syntax...
diagram-generator-1  | Diagram is valid! Saving...
diagram-generator-1  | Mermaid diagram saved to diagrams/diagram-20250505-110919.mmd
```

---

Enjoy analyzing your Angular code with AI! ✨
