FROM ollama/ollama

# Install required tools
RUN apt-get update && apt-get install -y curl python3 python3-pip

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy custom entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Entry point that will start Ollama, wait for it to be ready, pull model, then run Python app
ENTRYPOINT ["/entrypoint.sh"]