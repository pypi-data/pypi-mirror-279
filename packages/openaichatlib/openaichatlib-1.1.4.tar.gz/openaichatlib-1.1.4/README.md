# OpenAI Chat Python Lib

## Requirements
```
python: >=3.9
```

## Installation

```
pip install openaichatlib
```

## Usage

```python
from openaichatlib.V3 import Chatbot

bot = Chatbot(
    api_key="YOUR_API_KEY", 
    api_url="YOUR_API_HOST", # default is https://api.openai.com/v1/chat/completions
    engine='gpt-3.5-turbo-16k',
    timeout=120, 
    max_tokens=15_000, 
    proxy="YOUR_PROXY_URL", # like http://127.0.0.1:7890
    system_prompt="You are ChatGPT, a large language model trained by OpenAI"
)

reply = bot.ask("Hello")
print(reply)
```
