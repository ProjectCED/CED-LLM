# WARNING, this file needs to be in UNIX format for end-of-line characters

#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve Mistral model..."
ollama run mistral
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid