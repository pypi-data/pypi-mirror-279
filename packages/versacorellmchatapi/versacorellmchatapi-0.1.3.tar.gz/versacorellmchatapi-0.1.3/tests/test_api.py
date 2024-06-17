import unittest
from versacorellmchatapi.api import VersaCoreLLMChatAPI

class TestVersaCoreLLMChatAPI(unittest.TestCase):
    def test_initialization(self):
        api = VersaCoreLLMChatAPI("ollama")
        self.assertEqual(api.base_url, "http://localhost:11434/api/chat")

    def test_chat_completions(self):
        api = VersaCoreLLMChatAPI("ollama")
        messages = [
            {"role": "user", "content": "why is the sky blue?"}
        ]
        response = api.chat_completions(messages, model="mistral", stream=False)
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()