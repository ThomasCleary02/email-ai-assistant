# Email Assistant

Email Assistant is a Streamlit application that helps you draft professional emails and replies using AI. The app offers a simple, intuitive interface for generating well-crafted emails with customizable tones.

## Features

- **Two Modes**:
  - **Draft New Email**: Generate a complete email from scratch based on your content description
  - **Generate Reply**: Create appropriate responses to existing emails
- **Customizable Tone**: Choose from various tones including Professional, Friendly, Formal, Persuasive, and Concise
- **Flexible Backend**: Works with either local Ollama models or Hugging Face models
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

## Usage

The application can be run in two different modes:

### Option 1: Using Local Ollama (Recommended for local development)

1. Install [Ollama](https://ollama.ai/download) on your machine
2. Make sure you have a model available in Ollama (the default is "mistral")
   ```
   ollama pull mistral
   ```
   - You can use any model by changing the `OLLAMA_MODEL` variable in `app.py`
3. Start the Ollama service:
   ```
   ollama serve
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

### Option 2: Using Hugging Face API

1. Get a [Hugging Face API key](https://huggingface.co/settings/tokens)
2. Set the API key as an environment variable:
   ```
   export HUGGINGFACE_API_KEY=your_api_key_here
   ```
3. (Optional) Modify the `HF_MODEL` variable in `app.py` to use a different model:
   ```python
   HF_MODEL = "your-preferred-model"
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

When deploying to Streamlit Cloud, add your Hugging Face API key to the Streamlit secrets:

1. Create a `.streamlit/secrets.toml` file with:
   ```toml
   [huggingface]
   api_key = "your_api_key_here"
   ```
2. Add this file to your Streamlit Cloud secrets when deploying.

## Configuration

You can easily customize the models used by the application by modifying these variables at the top of the `app.py` file:

```python
# Hugging Face model setup
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"  # Change to your preferred Hugging Face model

# Ollama model setup
OLLAMA_MODEL = "mistral"  # Change to any model you have pulled in Ollama
```

Other configurable parameters:
- Generation parameters: Modify temperature, max tokens, etc. in the `text_generation` function call
- Email tones: Add or modify the `tone_options` list in the UI section

## Troubleshooting

- **Ollama Connection Issues**: 
  - Ensure Ollama is running and accessible at http://127.0.0.1:11434
  - Verify you have pulled the model specified in `OLLAMA_MODEL`
  - Check Ollama logs for any errors: `ollama logs`

- **Hugging Face API Errors**: 
  - Verify your API key is correct and not expired
  - Confirm the selected model is available and you have access to it
  - Check for any rate limiting issues

- **Slow Performance**: 
  - Local models may be resource-intensive; consider using a smaller model
  - For Ollama, try models optimized for your hardware (e.g., quantized models)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Uses [LangChain](https://github.com/hwchase17/langchain) for LLM integration
- Powered by [Ollama](https://ollama.ai/) and [Hugging Face](https://huggingface.co/)