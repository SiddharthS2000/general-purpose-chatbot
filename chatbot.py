from google import genai
from logging import getLogger
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
logger = getLogger(__name__)

DEFAULT_MODEL = "gemini-3.6-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_TOKENS = 512
DEFAULT_TOKEN_BUDGET = 4096

# Try Streamlit secrets first (production)
if "API_KEY" in st.secrets:
    DEFAULT_API_KEY = st.secrets["API_KEY"]
else:
    # Fallback to .env (local dev)
    load_dotenv()
    DEFAULT_API_KEY = os.environ.get("API_KEY")



class Chatbot:
    def __init__(
        self,
        model=None,
        api_key=None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
        token_budget: int = DEFAULT_TOKEN_BUDGET,
    ):
        self._model = model if model else DEFAULT_MODEL
        self._api_key = api_key if api_key else DEFAULT_API_KEY
        self._temperature = temperature
        self._max_output_tokens = max_output_tokens
        self._token_budget = token_budget

        self.client = genai.Client(api_key=self._api_key)
        self.chat = self.client.chats.create(model=self._model)

        # ✅ dict for per-model usage
        self.token_usage = {}
        self.request_count = 0
        self.history = []
        self.token_log = []  # per-turn log for current model

        if self._model not in self.token_usage:
            self.token_usage[self._model] = [{"prompt": 0, "output": 0, "total": 0}]

    # --- Model Switching ---
    def switch_model(self, new_model: str):
        logger.info(f"Switching model from {self._model} to {new_model}")
        self._model = new_model
        self.chat = self.client.chats.create(model=self._model, history=self.history)
        self.request_count = 0
        self.token_log = []
        if new_model not in self.token_usage:
            self.token_usage[new_model] = [{"prompt": 0, "output": 0, "total": 0}]
        logger.info(f"Model switched successfully to {self._model}")

    # --- Send Message + Token Tracking ---
    def send_message(self, user_input: str) -> str:
        try:
            response = self.chat.send_message(user_input)
            self.request_count += 1

            # Log history
            self.history = self.chat.get_history()

            # Track usage per model
            usage = {
                "prompt": response.usage_metadata.prompt_token_count,
                "output": response.usage_metadata.candidates_token_count,
                "total": response.usage_metadata.total_token_count,
            }
            self.token_usage[self._model].append(usage)

            # Also keep per-turn log for current model
            self.token_log.append(usage)

            return response.text
        except genai.errors.APIError as api_error:
            logger.error(f"API error: {api_error.message}")
            return api_error.message

    # --- Token Summary ---
    def get_token_summary(self, model=None) -> int:
        model = model or self._model
        logs = self.token_usage.get(model, [])
        return sum(log["total"] for log in logs)

    def get_all_token_summaries(self) -> dict:
        return {
            m: sum(log["total"] for log in logs) for m, logs in self.token_usage.items()
        }

    # --- Properties ---
    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        if not (0 <= value <= 2):
            raise ValueError("Temperature should be between 0 and 2")
        self._temperature = value

    @property
    def max_output_tokens(self):
        return self._max_output_tokens

    @max_output_tokens.setter
    def max_output_tokens(self, value: int):
        if value <= 0:
            raise ValueError("Max output tokens should be greater than 0")
        self._max_output_tokens = value

    @property
    def token_budget(self):
        return self._token_budget

    @token_budget.setter
    def token_budget(self, value: int):
        if value <= 0:
            raise ValueError("Token budget should be greater than 0")
        self._token_budget = value
