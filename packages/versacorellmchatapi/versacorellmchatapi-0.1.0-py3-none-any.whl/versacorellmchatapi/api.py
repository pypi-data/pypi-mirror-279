import requests
import json
import logging
from requests.exceptions import RequestException, HTTPError

class VersaCoreLLMChatAPI:
    def __init__(self, api_identifier, retry_attempts=3):
        self.base_url = self._get_base_url(api_identifier)
        self.retry_attempts = retry_attempts
        self.default_model = "llama3"
        logging.basicConfig(level=logging.INFO)

    def _get_base_url(self, api_identifier):
        base_url_mapping = {
            "lmstudio": "http://localhost:1234",
            "ollama": "http://localhost:11434/api/chat"
            # Add more mappings as needed
        }
        return base_url_mapping.get(api_identifier, "http://localhost:1234")

    def _make_request(self, url, headers, payload):
        attempt = 0
        while attempt < self.retry_attempts:
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
                response.raise_for_status()  # Raises HTTPError for bad responses
                return response
            except (RequestException, HTTPError) as e:
                attempt += 1
                logging.warning(f"Attempt {attempt} failed: {e}. Retrying...")
        raise RequestException("All retry attempts failed.")

    def chat_completions(self, messages, model=None, temperature=0.7, max_tokens=-1, stream=True, **kwargs):
        if model is None:
            model = self.default_model
        
        url = self.base_url
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        payload.update(kwargs)  # Add any additional parameters to the payload

        try:
            response = self._make_request(url, headers, payload)
            if stream:
                for line in response.iter_lines():
                    if line:
                        print(json.loads(line))
            else:
                return response.json()
        except RequestException as e:
            logging.error(f"Failed to get a response: {e}")
