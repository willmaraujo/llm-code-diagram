#!/bin/sh

# Use MODEL_NAME from environment
MODEL_NAME=${MODEL_NAME:-llama3:8b}

# Start Ollama in background
ollama serve > /dev/null 2>&1 &

# Wait for the API to be ready
echo "Waiting for Ollama to be ready..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done

# Pull the model only if not already downloaded
if ! ollama list | grep -q "$MODEL_NAME"; then
  echo "Pulling model $MODEL_NAME. This may take a while..."
  ollama pull "$MODEL_NAME"
else
  echo "Model $MODEL_NAME already pulled."
fi

# Wait a few seconds to ensure model is fully initialized
sleep 5

# Start your main Python app
echo "Starting application..."
python3 main.py