#!/bin/bash

# Email AI Assistant Launcher
# Simplified version for the unified app

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
    
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Downloading Ollama..."
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

# Function to set up Ollama environment
setup_ollama() {
    # Check if Ollama is installed
    if ! check_ollama; then
        echo -e "${YELLOW}Ollama is not installed on your system.${NC}"
        read -p "Would you like to install it now? (y/n): " install_choice
        if [[ $install_choice == "y" || $install_choice == "Y" ]]; then
            if ! install_ollama; then
                echo -e "${RED}Please install Ollama manually to use the local LLM option.${NC}"
                return 1
            fi
        else
            echo -e "${YELLOW}Note: You can still use HuggingFace API without Ollama.${NC}"
            return 0
        fi
    fi
    
    # Check if Ollama is running
    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${YELLOW}Starting Ollama service...${NC}"
        ollama serve > /dev/null 2>&1 &
        sleep 2
    fi
    
    return 0
}

# Function to set up HuggingFace API key
setup_huggingface() {
    echo -e "${BLUE}Setting up HuggingFace API...${NC}"
    
    # Get API key if not already set
    if [ -z "$HUGGINGFACE_API_KEY" ]; then
        read -p "Enter your HuggingFace API key (or press Enter to skip): " api_key
        if [ ! -z "$api_key" ]; then
            export HUGGINGFACE_API_KEY="$api_key"
            echo -e "${GREEN}HuggingFace API key set!${NC}"
        else
            echo -e "${YELLOW}No API key provided. You can still enter it in the app.${NC}"
        fi
    else
        echo -e "${GREEN}Using existing HuggingFace API key.${NC}"
    fi
}

# Function to launch the unified app
launch_app() {
    echo -e "${GREEN}Launching Email AI Assistant...${NC}"
    streamlit run app/main.py
}

# Main script
clear
echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}      Email AI Assistant Setup      ${NC}"
echo -e "${BLUE}====================================${NC}"
echo
echo -e "This script will help you set up and run the Email AI Assistant."
echo -e "The app supports both HuggingFace API and local Ollama."
echo

# Setup both options
setup_huggingface
setup_ollama

# Launch the unified app
launch_app