# VersaCoreLLMChatAPI

A Python library for interacting with VersaCore LLM Chat API.

## Installation

```bash
pip install versacorellmchatapi
```

## Usage

```bash
from versacorellmchatapi.api import VersaCoreLLMChatAPI

llm_api = VersaCoreLLMChatAPI("ollama")
messages = [
    {"role": "user", "content": "why is the sky blue?"}
]
response = llm_api.chat_completions(messages, temperature=0.7, max_tokens=50, stream=False)
print(response)
```