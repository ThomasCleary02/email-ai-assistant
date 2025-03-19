#!/bin/bash

# Email AI Assistant Launcher
# This script helps users set up and run the appropriate version of the Email AI Assistant

# Color definitions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if Ollama is installed
check_ollama() {
    if command -v ollama >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to install Ollama if needed
install_ollama() {
    echo -e "${BLUE}Installing Ollama...${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Downloading Ollama for macOS..."
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Downloading Ollama for Linux..."
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo -e "${RED}Unsupported operating system. Please install Ollama manually from https://ollama.com${NC}"
        return 1
    fi
    
    # Check if installation was successful
    if check_ollama; then
        echo -e "${GREEN}Ollama installed successfully!${NC}"
        return 0
    else
        echo -e "${RED}Ollama installation failed. Please install manually from https://ollama.com${NC}"
        return 1
    fi
}

# Function to start Ollama and pull the default model
setup_ollama() {
    echo -e "${BLUE}Starting Ollama service...${NC}"
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    
    # Give it a moment to start
    sleep 2
    
    echo -e "${BLUE}Pulling default model ($OLLAMA_MODEL)...${NC}"
    ollama pull $OLLAMA_MODEL
    
    echo -e "${GREEN}Ollama setup complete!${NC}"
}

# Function to configure HuggingFace environment
configure_huggingface() {
    echo -e "${BLUE}Configuring HuggingFace API settings...${NC}"
    
    # Get API key
    read -p "Enter your HuggingFace API key: " api_key
    if [ -z "$api_key" ]; then
        echo -e "${RED}API key cannot be empty.${NC}"
        exit 1
    fi
    export HUGGINGFACE_API_KEY="$api_key"
    
    # Ask for optional model name
    read -p "Enter HuggingFace model name (press Enter for default 'mistralai/Mistral-7B-Instruct-v0.3'): " hf_model
    if [ ! -z "$hf_model" ]; then
        export HUGGINGFACE_MODEL="$hf_model"
    else
        export HUGGINGFACE_MODEL="mistralai/Mistral-7B-Instruct-v0.3"
    fi
    
    echo -e "${GREEN}HuggingFace configuration complete!${NC}"
    echo -e "Using model: ${YELLOW}$HUGGINGFACE_MODEL${NC}"
}

# Function to configure Ollama environment
configure_ollama() {
    echo -e "${BLUE}Configuring Ollama settings...${NC}"
    
    # Ask for model name
    read -p "Enter Ollama model name (press Enter for default 'llama2'): " model_name
    if [ ! -z "$model_name" ]; then
        export OLLAMA_MODEL="$model_name"
    else
        export OLLAMA_MODEL="llama2"
    fi
    
    # Ask for custom Ollama URL 
    read -p "Enter custom Ollama URL (press Enter for default 'http://127.0.0.1:11434'): " ollama_url
    if [ ! -z "$ollama_url" ]; then
        export OLLAMA_BASE_URL="$ollama_url"
    else
        export OLLAMA_BASE_URL="http://127.0.0.1:11434"
    fi
    
    echo -e "${GREEN}Ollama configuration complete!${NC}"
    echo -e "Using model: ${YELLOW}$OLLAMA_MODEL${NC}"
    echo -e "Using URL: ${YELLOW}$OLLAMA_BASE_URL${NC}"
}

# Function to launch the HuggingFace app
launch_huggingface() {
    echo -e "${GREEN}Launching Email AI Assistant with HuggingFace backend...${NC}"
    streamlit run app/huggingface_app.py
}

# Function to launch the Ollama app
launch_ollama() {
    echo -e "${GREEN}Launching Email AI Assistant with Ollama backend...${NC}"
    streamlit run app/ollama_app.py
}

# Main menu
clear
echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}      Email AI Assistant Setup      ${NC}"
echo -e "${BLUE}====================================${NC}"
echo
echo -e "This script will help you set up and run the Email AI Assistant."
echo -e "Please choose an option:"
echo 
echo -e "1) ${YELLOW}Use HuggingFace API${NC} (requires API key)"
echo -e "2) ${YELLOW}Use local Ollama${NC} (runs locally on your machine)"
echo -e "3) ${YELLOW}Exit${NC}"
echo

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo
        # Configure HuggingFace settings
        configure_huggingface
        # Launch the app
        launch_huggingface
        ;;
    2)
        echo
        # Default Ollama model
        export OLLAMA_MODEL="llama2"
        
        if ! check_ollama; then
            echo -e "${YELLOW}Ollama is not installed on your system.${NC}"
            read -p "Would you like to install it now? (y/n): " install_choice
            if [[ $install_choice == "y" || $install_choice == "Y" ]]; then
                if ! install_ollama; then
                    exit 1
                fi
                configure_ollama
                setup_ollama
            else
                echo -e "${RED}Ollama is required to run the local version.${NC}"
                exit 1
            fi
        else
            echo -e "${GREEN}Ollama is already installed!${NC}"
            # Configure Ollama settings
            configure_ollama
            # Check if Ollama is running
            if ! pgrep -x "ollama" > /dev/null; then
                echo -e "${YELLOW}Ollama is not running.${NC}"
                setup_ollama
            fi
        fi
        # Launch the app
        launch_ollama
        ;;
    3)
        echo -e "${BLUE}Exiting...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac