# Email Assistant

Email Assistant is a Streamlit application that helps you draft professional emails and replies using AI. The app offers a simple, intuitive interface for generating well-crafted emails with customizable tones.

## Features

- **Two Modes**:
  - **Draft New Email**: Generate a complete email from scratch based on your content description
  - **Generate Reply**: Create appropriate responses to existing emails
- **Customizable Tone**: Choose from various tones including Professional, Friendly, Formal, Persuasive, and Concise
- **Flexible Backend Options**: 
  - **Local Ollama**: Run completely on your local machine with Ollama models
  - **Hugging Face API**: Connect to Hugging Face's hosted models
- **Interactive Setup**: Easy-to-use installer script that guides you through configuration
- **Copy-to-Use Format**: Generated emails include subject lines and properly formatted content

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Basic Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/email-assistant.git
   cd email-assistant
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the installer script:
   ```
   ./launch
   ```

## Usage

The application can now be launched using the interactive installer script:

1. Make the script executable (if needed):
   ```
   chmod +x launch
   ```

2. Run the installer script:
   ```
   ./launch
   ```

3. Follow the on-screen prompts to choose and configure your preferred backend:

### Option 1: Using Hugging Face API

The installer will:
- Ask for your Hugging Face API key
- Allow you to specify a custom model (or use the default)
- Launch the application automatically

### Option 2: Using Local Ollama (Recommended for local development)

The installer will:
- Check if Ollama is installed on your system
- Offer to install it if needed
- Allow you to specify which Ollama model to use
- Configure the Ollama URL (useful for remote Ollama instances)
- Launch the application automatically

## Configuration

The installer script handles all configuration for you, so there's no need to manually edit files. During setup, you can customize:

### For Hugging Face:
- API key
- Model selection (default: "mistralai/Mistral-7B-Instruct-v0.3")

### For Ollama:
- Model selection (default: "llama2")
- API URL (default: "http://127.0.0.1:11434")

## Troubleshooting

- **Ollama Connection Issues**: 
  - Ensure Ollama is running and accessible at the configured URL
  - Verify you have pulled the model you specified
  - Check Ollama logs for any errors: `ollama logs`

- **Hugging Face API Errors**: 
  - Verify your API key is correct and not expired
  - Confirm the selected model is available and you have access to it
  - Check for any rate limiting issues

- **Installer Script Issues**:
  - Make sure the script has execution permissions (`chmod +x launch`)
  - If installation fails, you can try installing Ollama manually from [ollama.ai](https://ollama.ai/download)

- **Slow Performance**: 
  - Local models may be resource-intensive; consider using a smaller model
  - For Ollama, try models optimized for your hardware (e.g., quantized models)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Uses [LangChain](https://github.com/hwchase17/langchain) for LLM integration
- Powered by [Ollama](https://ollama.ai/) and [Hugging Face](https://huggingface.co/)