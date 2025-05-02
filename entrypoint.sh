#!/bin/sh

# Start Ollama in background
ollama serve &

# Wait for the API to be ready
echo "⏳ Waiting for Ollama to be ready..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done

# Pull the model
echo "⬇️ Pulling model llama3:8b..."
ollama pull llama3:8b

# Keep the container alive
tail -f /dev/null