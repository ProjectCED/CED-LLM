#!/bin/bash

ENV_FILE=".env"

# Ensure the .env file exists
if [ ! -f "$ENV_FILE" ]; then
  touch "$ENV_FILE"
fi

# Function to update or append a key-value pair in the .env file
update_env_file() {
  local key=$1
  local value=$2

  # Sanitize the value to remove unwanted characters
  value=$(echo "$value" | tr -d '\r' | tr -d '\t' | sed 's/[[:space:]]*$//') # Removes \r, \t, and trailing spaces

  if grep -q "^$key=" "$ENV_FILE"; then
    # If the key exists, update its value
    sed -i "s/^$key=.*/$key=$value/" "$ENV_FILE"
  else
    # If the key doesn't exist, append it
    echo "$key=$value" >> "$ENV_FILE"
  fi
}

# Function to prompt for input with a default value
echo "Please enter the following environment variables. Press Enter to use the default value in square brackets."
prompt_with_default() {
  local prompt=$1
  local default=$2
  local input
  read -p "$prompt [$default]: " input
  # If the input is empty, use the default value
  if [ -z "$input" ]; then
    input="$default"
  fi
  # Return sanitized input
  echo "$(echo "$input" | tr -d '\r' | tr -d '\t' | sed 's/[[:space:]]*$//')"
}

# Prompt for general environment variables with defaults
DB_USERNAME=$(prompt_with_default "Enter the database username (DB_USERNAME)" "neo4j")
DB_PASSWORD=$(prompt_with_default "Enter the database password (DB_PASSWORD)" "password")
DB_NAME=$(prompt_with_default "Enter the database name (DB_NAME)" "neo4j")
OPENAI_KEY=$(prompt_with_default "Enter the OpenAI key (OPENAI_KEY)" "default_openai_key")

# Update the general environment variables
update_env_file "DB_USERNAME" "$DB_USERNAME"
update_env_file "DB_PASSWORD" "$DB_PASSWORD"
update_env_file "DB_NAME" "$DB_NAME"
update_env_file "OPENAI_KEY" "$OPENAI_KEY"
update_env_file "VITE_PORT" "5173"

# GPU configuration with retry loop
while true; do
  echo "Select GPU type:"
  echo "1. NVIDIA"
  echo "2. AMD"
  read -p "Enter your choice (1 or 2): " GPU_CHOICE

  if [ "$GPU_CHOICE" -eq 1 ]; then
    update_env_file "GPU_TYPE" "NVIDIA"
    update_env_file "GPU_RUNTIME" "nvidia"
    update_env_file "GPU_DRIVER" "nvidia"
    update_env_file "GPU_VISIBLE_DEVICES" "NVIDIA_VISIBLE_DEVICES"
    update_env_file "GPU_DRIVER_CAPABILITIES" "NVIDIA_DRIVER_CAPABILITIES"
    echo "Configuration updated in $ENV_FILE for NVIDIA GPU."
    break
  elif [ "$GPU_CHOICE" -eq 2 ]; then
    update_env_file "GPU_TYPE" "AMD"
    update_env_file "GPU_RUNTIME" "rocm"
    update_env_file "GPU_DRIVER" "amd"
    update_env_file "GPU_VISIBLE_DEVICES" "ROCR_VISIBLE_DEVICES"
    update_env_file "GPU_DRIVER_CAPABILITIES" "ROCR_DRIVER_CAPABILITIES"
    echo "Configuration updated in $ENV_FILE for AMD GPU."
    break
  else
    echo "Invalid choice. Please enter 1 for NVIDIA or 2 for AMD."
  fi
done

echo "Environment variables have been successfully configured and written to $ENV_FILE."

# Wait for user input before exiting
read -p "Press any key to exit..." -n1 -s
echo