#!/bin/bash

# Install dependencies
sudo apt update
sudo apt install -y python3-pip
pip3 install gpt4all requests beautifulsoup4 duckduckgo-search pyyaml

# Create directories
mkdir -p models web_cache interaction_history

# Download model
wget https://gpt4all.io/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf -P models/

# Initialize personality.yaml
echo "base_personality:
  mood: \"neutral\"
  safeword: \"epsilon\"" > personality.yaml

echo "Installation complete! Run: python3 adaptive_ai.py"
