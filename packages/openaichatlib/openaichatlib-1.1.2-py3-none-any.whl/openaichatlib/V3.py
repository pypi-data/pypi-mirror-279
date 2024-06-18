"""
A simple wrapper for the official ChatGPT API
"""
import json
import os

import requests
from requests.adapters import HTTPAdapter, Retry

from . import typings as t


class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
            self,
            api_key: str,
            api_url: str = os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions",
            engine: str = os.environ.get("GPT_ENGINE") or "gpt-3.5-turbo",
            proxy: str = None,
            timeout: float = None,
            max_tokens: int = None,
            customize_header: dict = None,
            temperature: float = 0.5,
            reply_count: int = 1,
            system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
            retry_count: int = 5,
    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        self.api_url: str = api_url
        self.engine: str = engine
        self.api_key: str = api_key
        self.customize_header = customize_header
        self.system_prompt: str = system_prompt
        self.max_tokens: int = max_tokens
        self.temperature: float = temperature
        self.reply_count: int = reply_count
        self.timeout: float = timeout
        self.proxy = proxy
        self.session = requests.Session()
        retries = Retry(total=retry_count, backoff_factor=1,
                        allowed_methods=["HEAD", "GET", "PUT", "OPTIONS", "POST"],
                        status_forcelist=[429, 502, 503, 504, 529])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.proxies.update(
            {
                "http": proxy,
                "https": proxy,
            },
        )

        self.conversation: dict[str, list[dict]] = {
            "default": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
            ],
        }

    def add_to_conversation(
            self,
            message,
            role: str,
            convo_id: str = "default",
    ) -> None:
        """
        Add a message to the conversation
        """
        self.conversation[convo_id].append({"role": role, "content": message})

    def ask_stream(
            self,
            prompt,
            role: str = "user",
            convo_id: str = "default",
            model: str = None,
            pass_history: bool = True,
            json_format: bool = False,
            stream_include_usage: bool = False,
            stream: bool = True,
            ignore_convo: bool = False,
            **kwargs,
    ):
        """
        Ask a question
        """
        # Make conversation if it doesn't exist
        if not ignore_convo:
            if convo_id not in self.conversation:
                self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
            self.add_to_conversation(prompt, role, convo_id=convo_id)
            messages = self.conversation[convo_id] if pass_history else [prompt]
        else:
            messages = prompt
        # Get response
        url = (
            self.api_url
        )
        headers = {"Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"}
        payload = {
            "model": os.environ.get("MODEL_NAME") or model or self.engine,
            "messages": messages,
            "stream": stream,
            # kwargs
            "temperature": kwargs.get("temperature", self.temperature),
            "n": kwargs.get("n", self.reply_count),
        }
        top_p = kwargs.get("top_p", None)
        if top_p:
            payload["top_p"] = top_p
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if json_format:
            payload["response_format"] = {
                "type": "json_object"
            }
        if stream and stream_include_usage:
            payload["stream_options"] = {
                "include_usage": True
            }

        presence_penalty = kwargs.get("presence_penalty", None)
        if presence_penalty:
            payload["presence_penalty"] = presence_penalty
        frequency_penalty = kwargs.get("frequency_penalty", None)
        if frequency_penalty:
            payload["frequency_penalty"] = frequency_penalty
        user = kwargs.get("user", None)
        if user:
            payload["user"] = user
        if self.customize_header:
            headers.update(self.customize_header)
        response = self.session.post(
            url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
            stream=stream,
        )
        if response.status_code != 200:
            raise t.APIConnectionError(
                f"{response.status_code} {response.reason} {response.text}",
            )
        response_role: str = "assistant"
        full_response: str = ""
        if stream:
            prompt_tokens = 0
            completion_tokens = 0
            for line in response.iter_lines():
                if not line:
                    continue
                # Remove "data: "
                line = line.decode("utf-8")[6:]
                if line == "[DONE]":
                    break
                resp: dict = json.loads(line)
                usage = resp.get("usage", None)
                if usage:
                    if prompt_tokens == 0:
                        prompt_tokens = usage.get("prompt_tokens", 0)
                    if completion_tokens == 0:
                        completion_tokens = usage.get("completion_tokens", 0)
                choices = resp.get("choices")
                if not choices:
                    continue
                delta = choices[0].get("delta")
                if not delta:
                    continue
                if "role" in delta:
                    response_role = delta["role"]
                if "content" in delta:
                    content = delta["content"]
                    full_response += content
                    yield content
            yield prompt_tokens, completion_tokens
        else:
            resp: dict = response.json()
            choices = resp.get("choices")
            delta = choices[0].get("message")
            response_role = delta["role"]
            content = delta["content"]
            usage = resp.get("usage", None)
            prompt_tokens = 0
            completion_tokens = 0
            if usage:
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)
            full_response = content
            yield content
            yield prompt_tokens, completion_tokens
        if not ignore_convo:
            self.add_to_conversation(full_response, response_role, convo_id=convo_id)

    def ask(
            self,
            prompt,
            role: str = "user",
            convo_id: str = "default",
            model: str = None,
            pass_history: bool = True,
            json_format: bool = False,
            ignore_convo: bool = False,
            **kwargs,
    ) -> tuple:
        """
        Non-streaming ask
        """
        response = self.ask_stream(
            prompt=prompt,
            role=role,
            convo_id=convo_id,
            model=model,
            pass_history=pass_history,
            json_format=json_format,
            stream_include_usage=False,
            stream=False,
            ignore_convo=ignore_convo,
            **kwargs,
        )
        full_response = ""
        prompt_tokens = 0
        completion_tokens = 0
        for content in response:
            if isinstance(content, str):
                full_response += content
            if isinstance(content, tuple):
                prompt_tokens, completion_tokens = content
        return full_response, prompt_tokens, completion_tokens

    def rollback(self, n: int = 1, convo_id: str = "default") -> None:
        """
        Rollback the conversation
        """
        for _ in range(n):
            self.conversation[convo_id].pop()

    def reset(self, convo_id: str = "default", system_prompt: str = None) -> None:
        """
        Reset the conversation
        """
        self.conversation[convo_id] = [
            {"role": "system", "content": system_prompt or self.system_prompt},
        ]
