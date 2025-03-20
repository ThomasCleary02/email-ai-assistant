# Email AI Assistant

A Streamlit application that helps you draft professional emails and replies using AI. This tool supports both local LLMs via Ollama and cloud-based models via HuggingFace's API.

## Features

- Create new email drafts with custom content and tone
- Generate thoughtful replies to existing emails
- Switch between HuggingFace and Ollama LLM backends
- Customize tone: Professional, Friendly, Formal, Persuasive, or Concise
- Simple and intuitive user interface

## Installation

### Prerequisites

- Python 3.8+
- pip
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- Optional: [Ollama](https://ollama.com/) for local LLM support

### Setup

1. Clone this repository:

```bash
git clone https://github.com/yourusername/email-ai-assistant.git
cd email-ai-assistant
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. For Ollama support (local LLMs):
   - Install Ollama from [ollama.com](https://ollama.com/)
   - Pull your preferred model: `ollama pull llama2` (or another model)

4. For HuggingFace support:
   - [Create a HuggingFace account](https://huggingface.co/join)
   - Generate an API key from your [HuggingFace settings](https://huggingface.co/settings/tokens)

## Usage

### Quick Start with Launch Script

The easiest way to run the application is using the launch script:

```bash
./launch.sh
```

This script will help set up both HuggingFace API and Ollama if needed.

### Manual Start

Alternatively, you can run the app directly:

```bash
streamlit run app/main.py
```

### Environment Variables

You can configure the app using these environment variables:

- `HUGGINGFACE_API_KEY`: Your HuggingFace API key
- `HUGGINGFACE_MODEL`: Model to use on HuggingFace (default: "mistralai/Mistral-7B-Instruct-v0.3")
- `OLLAMA_MODEL`: Model to use with Ollama (default: "llama2")
- `OLLAMA_BASE_URL`: Ollama server URL (default: "http://127.0.0.1:11434")

## Using the App

1. Select your preferred AI provider (HuggingFace or Ollama) from the sidebar
2. Configure your selected provider if needed
3. Choose either "Draft New Email" or "Generate Reply" tab
4. Fill in the required fields:
   - For new emails: content/purpose and tone
   - For replies: original email, your response message, and tone
5. Click "Generate Email" or "Generate Reply"
6. Copy the generated content for use in your email client

## Project Structure

```
├── app
│   ├── src
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   └── llm_client.py
│   │   ├── __init__.py
│   │   ├── huggingface_client.py
│   │   └── ollama_client.py
│   └── main.py
├── launch.sh
├── requirements.txt
├── LICENSE
└── README.md
```

## Troubleshooting

### HuggingFace Issues

- Ensure your API key is valid and has proper permissions
- Check your internet connection
- Verify that the model you selected is available on HuggingFace

### Ollama Issues

- Make sure Ollama is installed and running (`ollama serve`)
- Verify that you've pulled the model you want to use (`ollama pull modelname`)
- Check that the Ollama server is accessible at the configured URL

## License

[MIT License](LICENSE)

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web interface
- [LangChain](https://python.langchain.com/) for the language model integration
- [Ollama](https://ollama.com/) for local LLM support
- [HuggingFace](https://huggingface.co/) for cloud LLM support