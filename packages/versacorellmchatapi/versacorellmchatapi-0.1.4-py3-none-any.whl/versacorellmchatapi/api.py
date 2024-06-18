import requests
import json
import logging
from requests.exceptions import RequestException, HTTPError

class VersaCoreLLMChatAPI:
    def __init__(self, api_identifier, retry_attempts=3, default_model=None):
        self.api_identifier = api_identifier
        self.base_url = self._get_base_url(api_identifier)
        self.retry_attempts = retry_attempts
        if default_model:
            self.default_model = default_model
        else:
            self.default_model = self._get_default_model(api_identifier)
        logging.basicConfig(level=logging.INFO)

    def _get_base_url(self, api_identifier):
        base_url_mapping = {
            "lmstudio": "http://localhost:1234/v1/chat/completions",
            "ollama": "http://localhost:11434/api/chat"
            # Add more mappings as needed
        }
        return base_url_mapping.get(api_identifier, "http://localhost:1234/v1/chat/completions")

    def _get_default_model(self, api_identifier):
        default_model_mapping = {
            "lmstudio": "MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf",
            "ollama": "mistral"
        }
        return default_model_mapping.get(api_identifier, "MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf")

    def _make_request(self, url, headers, payload, stream):
        attempt = 0
        while attempt < self.retry_attempts:
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10, stream=stream)
                response.raise_for_status()  # Raises HTTPError for bad responses
                return response
            except (RequestException, HTTPError) as e:
                attempt += 1
                logging.warning(f"Attempt {attempt} failed: {e}. Retrying...")
        raise RequestException("All retry attempts failed.")

    def chat_completions(self, messages, model=None, temperature=0.7, max_tokens=-1, stream=True, callback=None, **kwargs):
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
            response = self._make_request(url, headers, payload, stream)
            if stream:
                return self._handle_streaming_response(response, callback)
            else:
                response_json = response.json()
                if 'choices' in response_json:
                    # lmstudio response format
                    content = response_json['choices'][0]['message']['content']
                elif 'message' in response_json:
                    # ollama response format
                    content = response_json['message']['content']
                else:
                    logging.error(f"Unexpected response format: {response_json}")
                    raise ValueError("Unexpected response format")
                return content
        except RequestException as e:
            logging.error(f"Failed to get a response: {e}")
        except ValueError as e:
            logging.error(f"Failed to parse response: {e}")

    def _handle_streaming_response(self, response, callback=None):
        content = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_line = json.loads(decoded_line)
                    if 'message' in json_line and 'content' in json_line['message']:
                        chunk = json_line['message']['content']
                        if callback:
                            callback(chunk)
                        content += chunk
                except json.JSONDecodeError as e:
                    logging.warning(f"Failed to decode line: {decoded_line} - Error: {e}")
        return content


# Usage example
if __name__ == "__main__":

    def handle_chunk(chunk):
        # Custom handling of each chunk
        print(chunk, end='', flush=True)


    lm_studio_llm_api = VersaCoreLLMChatAPI("lmstudio")
    ollama_llm_api = VersaCoreLLMChatAPI("ollama")
    
    messages = [
        { "role": "system", "content": "You are a useful chatbot." },
        { "role": "user", "content": "write a short story of 2000 words about a funny corgi." }
    ]
    
    # lm_studio_response = lm_studio_llm_api.chat_completions(
    #     messages, 
    #     model="lmstudio-community/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf", 
    #     temperature=0.7, 
    #     max_tokens=-1, 
    #     stream=False
    # )
    

    ollama_response = ollama_llm_api.chat_completions(
        messages,
        model="mistral", 
        stream=True,
        callback=handle_chunk  # Use the custom callback to handle streaming chunks
    )



    # if lm_studio_response:
    #     print("lm_studio_response:", lm_studio_response)

    # if ollama_response:
    #     print("ollama_response:", ollama_response)
